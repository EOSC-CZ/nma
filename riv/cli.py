#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""CLI for RIV availability checker."""

import click
from flask.cli import with_appcontext

from .tasks import check_availability_task


@click.group()
def riv():
    """RIV management commands."""


@riv.command("check-availability")
@click.option(
    "--eager",
    "-e",
    is_flag=True,
    help="Run task synchronously instead of sending to Celery queue.",
)
@with_appcontext
def check_availability(eager=False):
    """Check availability of persistent URLs in datasets."""
    if eager:
        click.secho("Checking availability synchronously...", fg="green")
        check_availability_task()
        click.secho("Availability check completed successfully.", fg="green")
    else:
        check_availability_task.delay()
        click.secho("Availability check task sent to Celery queue...", fg="yellow")


@riv.command("harvest")
@click.argument("harvester")
@with_appcontext
def temporary_harvest_catch_all(harvester):

    """Temporary command to harvest catch-all OAI-PMH repository before jobs have cli."""
    from oarepo_oaipmh_harvester.tasks import harvest_oaipmh_records

    # not using .delay here as we want to run it synchronously
    # for testing purposes
    harvest_oaipmh_records(harvester_id=harvester, batch_size=1)
