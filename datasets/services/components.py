from typing import Any

from flask_login import current_user
from flask_principal import Identity
from invenio_accounts.models import User
from invenio_drafts_resources.records import Record
from invenio_records_resources.services.records.components import ServiceComponent


class ExternalPIDComponent(ServiceComponent):
    """PID registration component."""

    def create(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
        """Create PID when record is created.."""
        # We create the PID after all the data has been initialized. so that
        # we can rely on having the 'id' and type set.
        record["id"] = data["id"]
        self.service.draft_cls.pid.create(record)


class UpdateMetadataComponent(ServiceComponent):
    """Service component for metadata update action."""

    field = "metadata"

    def update(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
        """Inject parsed metadata to the record."""
        setattr(record, self.field, data.get(self.field, {}))


def _get_editor_dict_for_user(user: User | None = None):
    if user is None:
        user = current_user
    if user is None:
        return {"id": "Anonymous", "full_name": "Anonymous", "affiliations": ""}
    user_profile =  getattr(user, "user_profile", {})
    user_name = user_profile.get("full_name", "")
    if not user_name:
        user_email = getattr(user, "email", "")
        user_name = user_email.split("@")[0][:-3] + "***"
    return {"id": str(user.id), "full_name": user_name, "affiliations": user_profile.get("affiliations", "")}


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
    return _update_editors_field_for_user(record, editor)


class UpdateEditorsComponent(ServiceComponent):
    """Modified by component."""
    field = "editors"

    def create(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
        register_editor(record)

    def update(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
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
