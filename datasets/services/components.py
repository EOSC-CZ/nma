from typing import Any

from flask import current_app
from flask_login import current_user
from flask_principal import Identity
from invenio_accounts.models import User
from invenio_drafts_resources.records import Record
from invenio_records_resources.services.records.components import ServiceComponent

from .idutils import resolve_identifiers


class ExternalPIDComponent(ServiceComponent):
    """PID registration component."""

    def create(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        """Create PID when record is created.."""
        # We create the PID after all the data has been initialized. so that
        # we can rely on having the 'id' and type set.
        record["id"] = data["id"]
        self.service.draft_cls.pid.create(record)


ANONYMOUS_IDENTIFIER = "Anonymous"


class UpdateMetadataComponent(ServiceComponent):
    """Service component for metadata update action.

    As we modify published record in place, we need to add this component
    as standard rdm component always modifies draft metadata.
    """

    field = "metadata"

    def update(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        """Inject parsed metadata to the record."""
        setattr(record, self.field, data.get(self.field, {}))


def _get_editor_dict_for_user(user: User | None = None):
    if user is None:
        user = current_user
    if not user:
        return {
            "id": ANONYMOUS_IDENTIFIER,
            "full_name": ANONYMOUS_IDENTIFIER,
            "affiliations": "",
        }
    user_profile = getattr(user, "user_profile", {})
    user_name = user_profile.get("full_name", "")
    if not user_name:
        user_email = getattr(user, "email", "")
        user_name = user_email.split("@")[0][:-3] + "***"
    return {
        "id": str(user.id),
        "full_name": user_name,
        "affiliations": user_profile.get("affiliations", ""),
    }


def _update_editors_field_for_user(record: Record, editor: dict) -> dict:
    editors = record.setdefault("editors", [])
    for obj in editors:
        if obj["id"] == editor["id"]:
            obj["full_name"] = editor["full_name"]
            obj["affiliations"] = editor["affiliations"]
            return obj
    else:
        editors.append(editor)
    return editor


def register_editor(record: Record, user: User | None = None) -> dict:
    editor = _get_editor_dict_for_user(user)
    if editor["id"] == ANONYMOUS_IDENTIFIER:
        return editor
    return _update_editors_field_for_user(record, editor)


class UpdateEditorsComponent(ServiceComponent):
    """Modified by component."""

    field = "editors"

    def create(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        register_editor(record)

    def update(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        register_editor(record)

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        register_editor(record)

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        register_editor(record)

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        register_editor(record)


class FetchIdentifiersComponent(ServiceComponent):
    """Service component for fetching external identifiers."""

    affects = "*"

    def fetch_identifiers(self, data: dict[str, Any]) -> None:
        """Fetch and populate identifiers from external sources."""
        try:
            resolve_identifiers(data, uow=self.uow)
        except Exception as e:
            current_app.logger.exception(
                "Error resolving identifiers in record",
                exc_info=e,
            )

    def create(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        self.fetch_identifiers(data)

    def update(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        self.fetch_identifiers(data)

    def update_draft(
        self,
        identity: Identity,
        data: dict[str, Any] = None,
        record: Record = None,
        **kwargs: Any,
    ) -> None:
        self.fetch_identifiers(data)
