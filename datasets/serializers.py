from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import BaseSerializerSchema, JSONSerializer

from invenio_rdm_records.resources.serializers.datacite.schema import DataCite43Schema as DataCiteSchema


class DataCiteJSONSerializer(MarshmallowSerializer):
    """Marshmallow based DataCite serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DataCiteSchema,
            list_schema_cls=BaseListSchema,
            schema_kwargs={},
            **options,
        )

