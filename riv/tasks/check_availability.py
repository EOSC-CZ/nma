from __future__ import annotations

import traceback
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_jobs.jobs import JobType
from invenio_records_resources.proxies import current_service_registry
from opensearch_dsl import Q

from ..config import LAST_CHECKED_THRESHOLD_DAYS
from ..utils import check_url_availability, create_session_with_retries

if TYPE_CHECKING:
    from datetime import datetime


@shared_task(ignore_result=True)
def check_availability_task():
    # Calculate expired threshold
    expiry_threshold = (
        (datetime.now(timezone.utc) - timedelta(days=LAST_CHECKED_THRESHOLD_DAYS))
        .isoformat()
        .replace("+00:00", "Z")
    )

    # Build Q filter for expired or missing last_checked
    extra_filter = Q(
        "bool",
        should=[
            Q(
                "range", **{"metadata.last_checked": {"lt": expiry_threshold}}
            ),  # expired
            ~Q("exists", field="metadata.last_checked"),  # missing last_checked
        ],
    )

    # Get datasets service
    datasets_service = current_service_registry.get("datasets")

    # Search datasets
    results = datasets_service.search(
        system_identity, params={"size": 100}, extra_filter=extra_filter
    )

    # be very polite here
    session = create_session_with_retries(throttle_sleep=5.0)

    # Iterate over results
    for hit in results.to_dict()["hits"]["hits"]:
        # re-read from the database - the search result may have reduced fields
        hit = datasets_service.read(
            identity=system_identity,
            id_=hit["id"],
        ).to_dict()

        record_id = hit["id"]
        metadata = hit["metadata"]

        current_app.logger.info(
            "Processing record: %s (ID: %s)",
            metadata.get("title", "N/A"),
            record_id,
        )

        persistent_url = metadata.get("persistent_url")
        if not persistent_url:
            current_app.logger.warning(
                "Skipping record %s: no persistent_url", record_id
            )
            continue

        # Check URL availability with retry logic
        _, status, message = check_url_availability(
            persistent_url,
            title=metadata.get("title", ""),
            session=session,
        )

        # Get current status to compare
        current_status = metadata.get("check_status")

        # Always update last_checked since we performed a check
        update_metadata = hit["metadata"]
        update_metadata["last_checked"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        # Only update status and message if status has changed
        if current_status != status:
            update_metadata["check_status"] = status
            update_metadata["check_message"] = message

            current_app.logger.info(
                "Record %s: %s -> %s (changed from %s)",
                record_id,
                persistent_url,
                status,
                current_status,
            )
        else:
            current_app.logger.info(
                "Record %s: %s -> %s (unchanged, updated last_checked)",
                record_id,
                persistent_url,
                status,
            )

        try:
            datasets_service.update(
                identity=system_identity,
                id_=record_id,
                data=hit,
            )
        except Exception:
            current_app.logger.exception(
                "Failed to update record %s: %s", record_id, traceback.format_exc()
            )


class CheckAvailabilityJob(JobType):
    """A job type to check if record is still available in the source repository."""

    id = "check_record_availability"
    title = "Check record persistent URLs availability"
    description = "Check availability of dataset persistent URLs."
    task = check_availability_task
