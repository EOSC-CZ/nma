from invenio_drafts_resources.records import Record, Draft
from invenio_pidstore.models import PersistentIdentifier
from invenio_records_resources.records.systemfields import PIDField
from invenio_records_resources.records.systemfields.pid_statuscheck import PIDStatusCheckField as InvenioPIDStatusCheckField
from invenio_records_resources.records.api import Record

class PIDStatusCheckField(InvenioPIDStatusCheckField):
    """PID status field that returns False when PID is not set."""

    def __get__(self, instance: Record, owner: type[Record]=None)->bool:
        """Get the pid status."""
        try:
            super().__get__(instance, owner)
        except AttributeError:
            pid = getattr(instance, self.key)
            if pid is None:
                return False


class ExternalPIDFieldContextMixin:

    def create(self, record: Record)->PersistentIdentifier:
        """Proxy to the field's create method."""
        return self.field.create(record)

    def delete(self, record: Record)->None:
        """Proxy to the field's delete method."""
        return self.field.delete(record)


class ExternalPIDField(PIDField):
    """Persistent identifier system field."""

    def post_create(self, record: Record) -> PersistentIdentifier | None:
        # or we can just pass this since PIDField doesn't create a PID if it already exists, as happens during publish.
        """Called after a record is created."""
        if not isinstance(record, Draft):
            if self._provider and self._create:
                self.create(record)
