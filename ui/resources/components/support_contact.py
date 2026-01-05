#
# Copyright (c) 2025 CESNET z.s.p.o.
#
"""UI Resource component for form config."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any


from oarepo_ui.resources.components import UIResourceComponent

from flask import current_app

if TYPE_CHECKING:
    from flask_principal import Identity
    from invenio_records_resources.services.records.results import RecordItem


class RDMSupportContactComponent(UIResourceComponent):
    """Pass support contact to form config."""

    def form_config(  # noqa: PLR0913  too many arguments
        self,
        *,
        api_record: RecordItem,  # noqa: ARG002
        record: dict,  # noqa: ARG002
        identity: Identity,  # noqa: ARG002
        form_config: dict,
        ui_links: dict,  # noqa: ARG002
        extra_context: dict,  # noqa: ARG002
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Add smaller RDM vocabularies to form config."""
        form_config["supportContact"] = current_app.config.get("REPOSITORY_SUPPORT_CONTACT", "")