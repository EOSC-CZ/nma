from invenio_records_resources.references.entity_resolvers.results import ServiceResultResolver

class RecordServiceResultResolver(ServiceResultResolver):
    """Resolver for rdm record result items."""

    def _reference_entity(self, entity):
        """Create a reference dict for the given result item."""
        pid = entity.id if isinstance(entity, self.item_cls) else entity.pid.pid_value
        return {self.type_key: str(pid)}