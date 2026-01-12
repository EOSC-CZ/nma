from __future__ import annotations

from typing import TYPE_CHECKING

from celery import shared_task
from invenio_access.permissions import system_identity
from invenio_jobs.jobs import JobType
from invenio_records_resources.proxies import current_service_registry
from opensearch_dsl import Q

if TYPE_CHECKING:
    pass


@shared_task(ignore_result=True)
def cleanup_unknown_titles():
    datasets_service = current_service_registry.get("datasets")

    extra_filter = Q(
        "bool",
        filter=[
            Q("term", **{"metadata.title.keyword": "Unknown title"}),
            Q("range", created={"lt": "now/d"}),
        ],
    )
    hits = datasets_service.scan(
        identity=system_identity,
        extra_filter=extra_filter,
    )
    for hit in hits:
        datasets_service.delete(identity=system_identity, id_=hit["id"])


class CleanupUnknownTitlesJob(JobType):
    """A job type that cleans up datasets with an unknown title."""

    id = "cleanup_unknown_titles"
    title = "Cleanup datasets with unknown title"
    description = (
        "Deletes datasets older than one day that still have the title 'Unknown title'."
    )
    task = cleanup_unknown_titles
