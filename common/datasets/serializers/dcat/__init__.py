from marshmallow.utils import get_value

from flask_resources import (
    ResponseHandler,
    BaseListSchema,
    JSONSerializer,
    MarshmallowSerializer,
)
from flask import request
from invenio_records_resources.resources.records.headers import etag_headers

from common.datasets.serializers.dcat.schema import DCATAPMetadataSchema

class DCATAPSerializer(JSONSerializer):
    def serialize_object(self, obj, **kwargs):
        try:
            metadata = obj.get('metadata', {})
            schema = DCATAPMetadataSchema()
            metadata = schema.transform_metadata(metadata)
            metadata = schema.load(metadata)
            obj['metadata'] = metadata
        except Exception as e:
            raise ValueError(f"Invalid metadata: {e}")
            
        return super().serialize_object(obj, **kwargs)

    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping."""
        if attr == "files":
            return getattr(obj, attr, default)
        else:
            return get_value(obj, attr, default)
    

def _dcatap_headers(obj_or_list, code, many=False):
    """Override content type for 'application/json'."""
    _etag_headers = etag_headers(obj_or_list, code, many=False)
    _etag_headers["content-type"] = "application/vnd.dcatap+json"
    return _etag_headers

dcatap_response_handlers = {
    "application/vnd.dcatap+json": ResponseHandler(
        DCATAPSerializer(), headers=_dcatap_headers
    ),
}

    



        
