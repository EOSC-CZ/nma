# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 TU Wien.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Users fixtures module."""

from flask import current_app
from invenio_access.permissions import system_identity
from invenio_db import db
from invenio_rdm_records.fixtures.fixture import FixtureMixin
from oarepo_oaipmh_harvester.proxies import current_oai_harvester_service


class HarvestersFixture(FixtureMixin):
    """Users fixture."""

    def transform_data(self, entry):
        transformers = list(entry.pop("transformer", []))
        writers = list(entry.pop("writer", []))
        model = entry.pop("model", None)

        if model:
            if not transformers:
                transformers = [f'oai-import{{model:"{model}"}}']
            if not writers:
                writers = [f'collision-aware{{model:"{model}"}}']

        harvester_data = {
            "id": entry.pop("id"),
            "name": entry.pop("name"),
            "base_url": entry.pop("base-url"),
            "metadata_prefix": entry.pop("metadata-prefix"),
            "setspec": entry.pop("setspec", ""),
            "loader": entry.pop("loader", "oai-pmh"),
            "transformers": transformers,
            "writers": writers,
            "comment": entry.pop("comment", ""),
        }

        harvest_managers = list(entry.pop("harvest-manager", []))
        if harvest_managers:
            harvester_data["harvest_managers"] = harvest_managers

        return harvester_data

    # move to oaipmh harvesters
    def create(self, entry) -> None:
        """Create a new OAI-PMH harvester."""
        # Handle model option to auto-generate transformers and writers
        harvester_data = self.transform_data(entry)
        try:
            current_oai_harvester_service.create(system_identity, harvester_data)
            db.session.commit()
            current_oai_harvester_service.indexer.refresh()

            current_app.logger.info(
                "Harvester '%s' created successfully with ID: %s",
                harvester_data["name"],
                harvester_data["id"],
            )
        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Error creating harvester: %s", e)
            raise