from typing import Any

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
