from datetime import datetime, timedelta, timezone

import click
from celery import shared_task
from invenio_access.permissions import system_identity
from invenio_records_resources.proxies import current_service_registry
from opensearch_dsl import Q

from .config import LAST_CHECKED_THRESHOLD_DAYS
from .utils import check_url_availability


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
        system_identity, params={}, extra_filter=extra_filter
    )

    # Iterate over results
    for hit in results.to_dict()["hits"]["hits"]:
        # re-read from the database - the search result may have reduced fields
        hit = datasets_service.read(
            identity=system_identity,
            id_=hit["id"],
        ).to_dict()

        record_id = hit["id"]
        metadata = hit["metadata"]

        click.secho(
            f"Processing record: {metadata.get('title', 'N/A')} (ID: {record_id})",
            fg="cyan",
        )

        persistent_url = metadata.get("persistent_url")
        if not persistent_url:
            click.secho(f"Skipping record {record_id}: no persistent_url", fg="yellow")
            continue

        # Check URL availability with retry logic
        _, status, message = check_url_availability(
            persistent_url, title=metadata.get("title", "")
        )

        # Get current status to compare
        current_status = metadata.get("check_status")

        # Always update last_checked since we performed a check
        hit["metadata"]["last_checked"] = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )

        # Determine color based on status
        if status == "success":
            status_color = "green"
        elif status == "warning":
            status_color = "magenta"  # Warning: needs manual check
        elif status in ["not_accessible", "not_found"]:
            status_color = "yellow"
        else:  # error statuses
            status_color = "red"

        # Only update status and message if status has changed
        if current_status != status:
            hit["metadata"]["check_status"] = status
            hit["metadata"]["check_message"] = message

            click.secho(
                f"Record {record_id}: {persistent_url} -> {status} (changed from {current_status})",
                fg=status_color,
            )
        else:
            click.secho(
                f"Record {record_id}: {persistent_url} -> {status} (unchanged, updated last_checked)",
                fg="blue",
            )

        try:
            datasets_service.update(
                identity=system_identity,
                id_=record_id,
                data=hit,
            )
        except Exception as e:
            click.secho(
                f"Failed to update record {record_id}: {e}",
                fg="red",
            )
