from __future__ import annotations

from typing import TYPE_CHECKING

from celery import shared_task
from flask import current_app
from invenio_jobs.jobs import JobType
from invenio_search import current_search

from .invenio_command import invenio_command

if TYPE_CHECKING:
    pass


@shared_task(ignore_result=True)
def create_missing_indices():
    from invenio_search.proxies import current_search

    current_app.logger.info("Creating missing indices...")
    current_search.create(ignore_existing=True)


@shared_task(ignore_result=True)
def rebuild_all_indices():

    for name, response in current_search.delete(ignore=[400, 404]):
        current_app.logger.info("Deleted index: %s, response: %s", name, response)
    current_app.logger.info("Recreating all indices...")
    for name, response in current_search.create(ignore_existing=True):
        current_app.logger.info("Created index: %s, response: %s", name, response)
    # oarepo patches
    from importlib.metadata import entry_points

    current_app.logger.info("Running Oarepo CLI search init entry points...")
    for ep in entry_points(group="oarepo.cli.search.init"):
        current_app.logger.info("Running entry point: %s", ep.name)
        ep.load()()
    current_app.logger.info("Oarepo CLI search init entry points completed.")

    invenio_command("rdm-records custom-fields init")
    invenio_command("communities custom-fields init")
    invenio_command("rdm rebuild-all-indices")


class CreateMissingIndicesJob(JobType):
    """A job type to create any missing search indices."""

    id = "create_missing_indices"
    title = "Create missing indices"
    description = "Create any missing search indices in the search engine."
    task = create_missing_indices


class RebuildAllIndicesJob(JobType):
    """A job type to rebuild all indices."""

    id = "rebuild_all_indices"
    title = "Rebuild all indices (drop them and recreate and reindex everything)"
    description = "Rebuild all search indices from scratch."
    task = rebuild_all_indices
