from __future__ import annotations

import shlex
import subprocess
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING

import click
from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_jobs.jobs import JobType, PredefinedArgsSchema
from invenio_records_resources.proxies import current_service_registry
from invenio_search import current_search
from marshmallow import fields
from opensearch_dsl import Q

from .config import LAST_CHECKED_THRESHOLD_DAYS
from .utils import check_url_availability

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


@shared_task(ignore_result=True)
def invenio_command(cmdline: str, timeout=600):
    """Run an invenio CLI command in a Celery task."""

    # split the cmdline into parts separated by &&
    commands = [cmd.strip() for cmd in cmdline.split("&&")]

    failed_subcommands = []
    for command in commands:
        current_app.logger.info("Running command: invenio %s", command)
        resultcode, stdout, stderr = _run_invenio_command(command, timeout=timeout)
        for line in stdout:
            current_app.logger.info("%s", line)
        for line in stderr:
            current_app.logger.error("%s", line)
        if resultcode:
            failed_subcommands.append(command)
            current_app.logger.error(
                f"Command 'invenio {command}' failed with return code {resultcode}"
            )
        else:
            current_app.logger.info(
                f"Command 'invenio {command}' completed successfully"
            )
    if failed_subcommands:
        raise Exception(
            f"Invenio command failed for subcommands: {', '.join(failed_subcommands)}"
        )


def _run_invenio_command(cmdline: str, timeout=600) -> tuple[int, list[str], list[str]]:
    # get the current python executable
    current_python = sys.executable
    invenio_cmd = Path(current_python).parent / "invenio"
    if not invenio_cmd.exists():
        raise FileNotFoundError(f"Invenio command not found at {invenio_cmd}")

    try:
        current_app.logger.info(
            "Executing command: %s %s with timeout %s",
            str(invenio_cmd),
            cmdline,
            timeout,
        )
        result = subprocess.run(
            [str(invenio_cmd)] + shlex.split(cmdline),
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            timeout=timeout,  # 10 minutes by default
        )
        current_app.logger.info(
            "Command executed with return code %s",
            result.returncode,
        )
        return result.returncode, result.stdout.splitlines(), result.stderr.splitlines()
    except subprocess.CalledProcessError as e:
        current_app.logger.error(
            f"Command failed with return code {e.returncode}:\n{e.stderr}"
        )

        return -1, [], traceback.format_exc().splitlines()


class InvenioTaskJobSchema(PredefinedArgsSchema):
    job_arg_schema = fields.String(
        metadata={"type": "hidden"},
        dump_default="InvenioTaskJobSchema",
        load_default="InvenioTaskJobSchema",
    )

    cmdline = fields.String(
        required=True,
        metadata={"description": "The Invenio CLI command to run."},
    )
    timeout = fields.Integer(
        required=False,
        dump_default=600,
        load_default=600,
        metadata={"description": "Timeout for each command in seconds."},
    )


class InvenioTaskJob(JobType):
    """A job type to run invenio CLI commands as Celery tasks."""

    id = "invenio_command"
    title = "Invenio Command"
    description = "Run an arbitrary Invenio CLI command or a sequence of commands separated by &&."

    task = invenio_command

    arguments_schema = InvenioTaskJobSchema

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, cmdline=None, **kwargs):
        """Override to define extra arguments to be injected on task execution.

        :param job_obj (Job): the Job object.
        :param since (datetime): last time the job was executed, or None if never
            executed.
        :return: a dict of arguments to be injected on task execution.
        """
        return {"cmdline": cmdline, "timeout": kwargs.get("timeout", 600)}


@shared_task(ignore_result=True)
def create_missing_indices():
    from invenio_search.proxies import current_search

    current_app.logger.info("Creating missing indices...")
    current_search.create(ignore_existing=True)


class CreateMissingIndicesJob(JobType):
    """A job type to run invenio CLI commands as Celery tasks."""

    id = "create_missing_indices"
    title = "Create missing indices"
    description = "Create any missing search indices in the search engine."
    task = create_missing_indices


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


class RebuildAllIndicesJob(JobType):
    """A job type to run invenio CLI commands as Celery tasks."""

    id = "rebuild_all_indices"
    title = "Rebuild all indices (drop them and recreate and reindex everything)"
    description = "Rebuild all search indices from scratch."
    task = rebuild_all_indices
