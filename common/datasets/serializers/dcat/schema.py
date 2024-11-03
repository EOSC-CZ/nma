
from flask import current_app
import idutils
import marshmallow as ma
from marshmallow import Schema, fields as ma_fields, missing, post_load, pre_load
from marshmallow_utils.html import sanitize_unicode
from marshmallow_utils.fields import SanitizedUnicode
from nr_metadata.datacite.services.records.schema import (
    NRDataCiteMetadataSchema,
)
from nr_metadata.datacite.services.records.schema_datatypes import (
    ResourceTypeSchema
)

class IdentifierSchema(ma.Schema):
    identifier = ma_fields.String()
    identifierType = ma_fields.String(default="OriginalURL")

    @staticmethod
    def create_identifier(url_value):
        return {
            'identifier': url_value,
            'identifierType': 'OriginalURL'
        }


class PublisherSchema(ma.Schema):
    name = ma_fields.String()


class ResourceTypeSchema(ma.Schema):
    resourceType = ma_fields.String()
    resourceTypeGeneral = ma_fields.String()

class Datacite43MetadataSchema(NRDataCiteMetadataSchema):
    class Meta:
        unknown = ma.RAISE
    
    schemaVersion = ma_fields.String()
    identifiers = ma_fields.List(ma_fields.Nested(IdentifierSchema))
    publisher = ma_fields.String()
    types = ma_fields.Nested(lambda: ResourceTypeSchema)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @pre_load
    def preprocess_metadata(self, metadata, **kwargs):
        if not metadata:
            return {}
        if 'publisher' in metadata and isinstance(metadata['publisher'], dict):
            metadata['publisher'] = metadata['publisher'].get('name')
        if 'resourceType' in metadata:
            metadata['types'] = metadata.pop('resourceType')
        if 'url' in metadata:
            metadata['identifiers'] = metadata.get('identifiers', [])
            metadata['identifiers'].append(IdentifierSchema.create_identifier(metadata.pop('url')))
        if 'schemaVersion' not in metadata:
            metadata['schemaVersion'] = "http://datacite.org/schema/kernel-4"
        if 'version' in metadata:
            del metadata['version']
        if 'files' in metadata:
            metadata['_files'] = metadata.pop('files')
    
        return metadata

    @post_load
    def assign_metadata(self, data, **kwargs):
        """Assign metadata to obj['metadata'] after loading."""
        obj = data.get('obj', {})
        obj['metadata'] = data.get('metadata', {})
        return data

class DCATAPMetadataSchema(Datacite43MetadataSchema):
    """DCAT-AP Marshmallow Schema based on invenio-rdm-records schema."""

    _files = ma.fields.Method("get_files")

    def get_files(self, obj):
        """Get files."""
        if "files" not in obj:
            return missing
        files_enabled = obj["files"].get("enabled", False)
        if not files_enabled:
            return missing
        files_entries = obj["files"].get("entries", {})
        record_id = obj["id"]
        files_list = []
        for key, value in files_entries.items():
            file_name = sanitize_unicode(
                value["key"]
            )  # There can be inconsistencies in the file name i.e. if the file name consists of invalid XML characters
            url = f"{current_app.config['SITE_UI_URL']}/records/{record_id}/files/{file_name}"
            access_url = None
            if "doi" in obj["pids"]:
                access_url = idutils.to_url(
                    obj["pids"]["doi"]["identifier"], "doi", url_scheme="https"
                )

            files_list.append(
                dict(
                    size=str(value["size"]),
                    access_url=access_url,
                    download_url=url,
                    key=value["key"],
                )
            )

        return files_list or missing

    
    
