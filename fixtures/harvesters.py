# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Users fixtures module."""

import secrets
import string

from flask import current_app
from flask_security.confirmable import confirm_user
from flask_security.utils import hash_password
from invenio_access.models import ActionUsers
from invenio_access.proxies import current_access
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_rdm_records.fixtures.fixture import FixtureMixin
from invenio_users_resources.services.users.tasks import reindex_users
from sqlalchemy.exc import IntegrityError

"""
invenio oai harvesters create --id zenodo-upol --name "Zenodo UPOL harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "upol" --model datasets \
    --loader zenodo --transformer "zenodo"             \
    --setspec 'creators.affiliation:("upol" OR "Univerzita Palackého v Olomouci" OR "Palacký University Olomouc" OR "Palacky University Olomouc") AND resource_type.type:dataset'
"""

"""
@harvesters_cli.command("create")
@click.option("--id", required=True, help="Harvester ID")
@click.option("--name", required=True, help="Harvester name")
@click.option("--base-url", required=True, help="OAI-PMH base URL")
@click.option("--metadata-prefix", required=True, help="Metadata prefix (e.g., oai_dc)")
@click.option("--setspec", default="", help="Set specification")
@click.option("--loader", default="oai-pmh", help="Loader definition (default: oai-pmh)")
@click.option("--model", help="Model name (automatically sets transformers and writers)")
@click.option(
    "--transformer",
    multiple=True,
    help="Transformer (can be specified multiple times, overrides --model)",
)
@click.option(
    "--writer",
    multiple=True,
    help="Writer (can be specified multiple times, overrides --model)",
)
@click.option(
    "--harvest-manager",
    multiple=True,
    help="Harvest manager user email (can be specified multiple times)",
)
@click.option("--comment", default="", help="Comment")
@with_appcontext
"""

"""
def create(self, entry):
    email = entry.pop("email")
    password = self._get_password(email, entry)
    username = entry.get("username")
    full_name = entry.get("full_name", "")
    affiliations = entry.get("affiliations", "")
    active = entry.get("active", False)
    confirmed = entry.get("confirmed", False)
    hashed_password = hash_password(password)
"""

class HarvestersFixture(FixtureMixin):
    """Users fixture."""

    def create(self, entry) -> None:
        """Create a new OAI-PMH harvester."""
        # Handle model option to auto-generate transformers and writers

        transformers = list(entry.pop("transformer"))
        writers = list(entry.pop("writer"))
        model = entry.pop("model", None)

        if model:
            if not transformers:
                transformers = [f'oai-import{{model:"{model}"}}']
            if not writers:
                writers = [f'oai-service{{model:"{model}",update:true}}']

        harvester_data = {
            "id": entry.pop("id"),
            "name": entry.pop("name"),
            "base_url": entry.pop("base_url"),
            "metadata_prefix": entry.pop("metadata_prefix"),
            "setspec": entry.pop("setspec", ""),
            "loader": entry.pop("loader", "oai-pmh"),
            "transformers": transformers,
            "writers": writers,
            # "harvest_managers": [{"user": lookup_user(email)} for email in harvest_manager],
            # "comment": comment,
        }

        harvest_managers = entry.pop("harvest_manager", [])



        try:
            current_oai_harvester_service.create(system_identity, harvester_data)
            db.session.commit()
            current_oai_harvester_service.indexer.refresh()

            console = Console()
            console.print(f"[green]✓[/green] Harvester '{name}' created successfully with ID: {id}")
        except Exception as e:
            db.session.rollback()
            click.echo(f"Error creating harvester: {e}", err=True)
            raise