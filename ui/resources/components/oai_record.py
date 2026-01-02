#
# Copyright (c) 2025 CESNET z.s.p.o.
#
"""UI Resource component for form config."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING
from invenio_db import db
from oarepo_oaipmh_harvester.oai_record.models import OAIHarvestedRecord
from oarepo_ui.resources.components import UIResourceComponent
if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_records_resources.services.records.results import RecordItem


class OaiRecordComponent(UIResourceComponent):
    """Pass RDM vocabulary fixtures to form config."""

    def before_ui_detail(
            self,
            *,
            api_record: RecordItem,
            record: dict,
            identity: Identity,
            ui_links: dict,
            extra_context: dict,
            **kwargs: Any,
    ) -> None:
        """
        Extends the UI detail context with OAI-PMH information.
        If the record was harvested via OAI-PMH, the corresponding
        OAIHarvestedRecord is loaded. Otherwise, the value is set to None.
        """
        harvested_record = db.session.query(OAIHarvestedRecord).filter_by(record_pid=record["id"]).first()
        extra_context["oai_record"] = harvested_record

