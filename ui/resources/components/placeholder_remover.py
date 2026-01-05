#
# Copyright (c) 2025 CESNET z.s.p.o.
#
"""UI Resource component."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from riv.resolvers.base import TITLE_PLACEHOLDER, CREATORS_PLACEHOLDER
from oarepo_ui.resources.components import UIResourceComponent

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_records_resources.services.records.results import RecordItem


class PlaceholderRemoverComponent(UIResourceComponent):

    def before_ui_edit(  # noqa: PLR0913  too many arguments
            self,
            *,
            api_record: RecordItem,
            record: dict,
            data: dict,
            identity: Identity,
            form_config: dict,
            ui_links: dict,
            extra_context: dict,
            **kwargs: Any,
    ) -> None:
        """
        Removes placeholder values from record metadata before the record
        is passed to the UI edit form.
        """
        if record["metadata"]["title"] == TITLE_PLACEHOLDER:
            record["metadata"]["title"] = ""
            record["metadata"]["publication_date"] = ""

        creators = record["metadata"].get("creators", [])
        record["metadata"]["creators"] = [
            creator for creator in creators
            if creator != CREATORS_PLACEHOLDER[0]
        ]
