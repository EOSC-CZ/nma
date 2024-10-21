from marshmallow.utils import get_value

from flask_resources import (
    ResponseHandler,
    BaseListSchema,
    JSONSerializer,
    MarshmallowSerializer,
)
from flask import current_app, request
from invenio_records_resources.resources.records.headers import etag_headers

from common.datasets.serializers.dcat.schema import DCATAPMetadataSchema


class DCATAPSerializer(MarshmallowSerializer):
    """DCAT-AP serializer for metadata. DataCite-based JSON schema."""
    def __init__(self, **options):
        """Constructor.""" 
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=DCATAPMetadataSchema,
            list_schema_cls=BaseListSchema,
            **options,
        )

    def serialize_object(self, obj, **kwargs):
        """Serialize object."""
        metadata = obj.get("metadata", {})
        schema = DCATAPMetadataSchema()
        loaded_metadata = schema.load(metadata)
        dump = schema.dump(loaded_metadata)
        obj["metadata"] = dump
        return super().serialize_object(dump)
        
    def get_attribute(self, obj, attr, default):
        """Retrieve attributes, with special handling for 'files'."""
        return getattr(obj, attr, default) if attr == "files" else get_value(obj, attr, default)
    

def _dcatap_headers(obj_or_list, code, many=False):
    """Override content type for 'application/json'."""
    _etag_headers = etag_headers(obj_or_list, code, many=False)
    _etag_headers["content-type"] = "application/vnd.dcatap+json"
    return _etag_headers

dcatap_response_handlers = {
    "application/vnd.dcatap+json": ResponseHandler(
        DCATAPSerializer(), headers=_dcatap_headers
    )
}

    



        
