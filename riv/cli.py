#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""CLI for RIV availability checker."""

import traceback

import click
import tqdm
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier
from oarepo_oaipmh_harvester.oai_record.models import OAIHarvestedRecord
from sqlalchemy import select
from invenio_access.permissions import system_identity
from fixtures import FixturesEngine

from fixtures import FixturesEngine

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


@riv.command("remove-records", hidden=True)
@click.option(
    "--harvested-only/--all-records",
    is_flag=True,
    default=True,
    help="Remove only harvested records or all records. Default is harvested only.",
)
@click.option(
    "--yes-i-know",
    is_flag=True,
    help="Confirm that you really want to remove the records.",
)
@with_appcontext
def remove_records(harvested_only, yes_i_know):
    """Remove records from RIV dataset."""
    from sqlalchemy_continuum import version_class

    from datasets.model import datasets_model

    RecordVersion = version_class(datasets_model.RecordMetadata)

    if not yes_i_know:
        records_to_remove_text = (
            "harvested records" if harvested_only else "all records"
        )
        click.secho(
            "This operation is destructive. "
            f"It will remove {records_to_remove_text} records permanently."
            " If you are sure, type 'yes' or use the --yes-i-know flag.",
            fg="red",
        )
        confirmation = input("Type 'yes' to confirm: ")
        if confirmation.lower() != "yes":
            click.secho("Operation cancelled.", fg="yellow")
            return

    if harvested_only:
        record_ids = set(
            db.session.scalars(select(OAIHarvestedRecord.record_pid)).all()
        )
    else:
        record_ids = db.session.scalars(
            select(PersistentIdentifier.pid_value).where(
                PersistentIdentifier.pid_type == "datsts"
            )
        ).all()
    total = len(record_ids)
    click.secho(f"Removing {total} records...", fg="green")

    for record_id in tqdm.tqdm(record_ids):
        if record_id is None:
            continue
        # remove oai harvested record entry if exists
        try:
            with db.session.begin_nested() as nested:
                pid = (
                    db.session.query(PersistentIdentifier)
                    .filter_by(pid_type="datsts", pid_value=record_id)
                    .one()
                )
                recid = (
                    db.session.query(PersistentIdentifier)
                    .filter_by(pid_type="recid", pid_value=record_id)
                    .one_or_none()
                )
                draft_record = (
                    db.session.query(datasets_model.DraftMetadata)
                    .filter_by(id=pid.object_uuid)
                    .one_or_none()
                )
                published_record = (
                    db.session.query(datasets_model.RecordMetadata)
                    .filter_by(id=pid.object_uuid)
                    .one_or_none()
                )
                parent_record = (
                    db.session.query(datasets_model.ParentRecordMetadata)
                    .filter_by(id=pid.object_uuid)
                    .one_or_none()
                )
                if parent_record:
                    draft_record = (
                        db.session.query(datasets_model.DraftMetadata)
                        .filter_by(parent_id=parent_record.id)
                        .one_or_none()
                    )
                    published_record = (
                        db.session.query(datasets_model.RecordMetadata)
                        .filter_by(parent_id=parent_record.id)
                        .one_or_none()
                    )
                elif draft_record:
                    parent_record = (
                        db.session.query(datasets_model.ParentRecordMetadata)
                        .filter_by(id=draft_record.parent_id)
                        .one_or_none()
                    )
                elif published_record:
                    parent_record = (
                        db.session.query(datasets_model.ParentRecordMetadata)
                        .filter_by(id=published_record.parent_id)
                        .one_or_none()
                    )
                if published_record:
                    metadata_versions = db.session.query(RecordVersion).filter_by(
                        id=published_record.id
                    )
                else:
                    metadata_versions = None
                if parent_record:
                    parent_record_state = (
                        db.session.query(datasets_model.ParentRecordState)
                        .filter_by(parent_id=parent_record.id)
                        .one_or_none()
                    )
                else:
                    parent_record_state = None
                if parent_record_state:
                    db.session.delete(parent_record_state)
                if metadata_versions:
                    metadata_versions.delete()
                if published_record:
                    db.session.delete(published_record)
                if draft_record:
                    db.session.delete(draft_record)
                if parent_record:
                    db.session.delete(parent_record)
                db.session.delete(pid)
                if recid:
                    db.session.delete(recid)
                nested.commit()
        except:
            traceback.print_exc()
            continue

    # remove the remaining OAI harvested records without associated records
    db.session.query(OAIHarvestedRecord).delete()
    db.session.commit()

    if not harvested_only:
        # remove everything in versions table, for sure
        db.session.query(RecordVersion).delete()
        db.session.query(PersistentIdentifier).filter_by(pid_type="recid").delete()
        db.session.query(PersistentIdentifier).filter_by(pid_type="oai").delete()
        db.session.commit()

    from invenio_app_rdm.cli import rebuild_all_indices

    rebuild_all_indices.callback("")

    click.secho(
        "Records removed successfully. Please wait, the search index is being rebuilt.",
        fg="green",
    )

@riv.command("fixtures")
@with_appcontext
def create_fixtures():
    """Create the fixtures required for record creation."""
    click.secho("Creating required fixtures...", fg="green")

    FixturesEngine(system_identity).run()

    click.secho("Created required fixtures!", fg="green")

@riv.command("fixtures")
@with_appcontext
def create_fixtures():
    """Create the fixtures required for record creation."""
    click.secho("Creating required fixtures...", fg="green")

    FixturesEngine(system_identity).run()

    click.secho("Created required fixtures!", fg="green")
