from typing import Any

from flask_login import current_user
from flask_principal import Identity
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


class UpdateEditorsComponent(ServiceComponent):
    """Modified by component."""
    field = "editors"

    def _get_editor(self):
        return {"id": str(current_user.id), "full_name": current_user.user_profile.get("full_name", "")}

    def _update_editors(self, editors: list):
        editor = self._get_editor()
        for i, obj in enumerate(editors):
            if obj["id"] == editor["id"]:
                editors[i] = editor
                break
        return editors

    def create(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
        editor = self._get_editor()
        record["editors"] = [editor]

    def update(self, identity: Identity, data: dict[str, Any] = None, record: Record = None, **kwargs: Any) -> None:
        record["editors"] = self._update_editors(record.get("editors", []))

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        editor = self._get_editor()
        record["editors"] = [editor]

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record["editors"] = self._update_editors(record.get("editors", []))

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record["editors"] = self._update_editors(record.get("editors", []))
