from __future__ import annotations

import shlex
import subprocess
import sys
import traceback
from pathlib import Path
from typing import TYPE_CHECKING

from celery import shared_task
from flask import current_app
from invenio_jobs.jobs import JobType, PredefinedArgsSchema
from marshmallow import fields

if TYPE_CHECKING:
    pass


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
