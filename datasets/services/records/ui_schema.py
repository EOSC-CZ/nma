from flask_resources import JSONSerializer
import marshmallow as ma
from marshmallow import Schema, ValidationError, fields as ma_fields
from nr_metadata.datacite.services.records.ui_schema import (
    DataCiteRecordUISchema,
    NRDataCiteMetadataUISchema,
)
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema

class DateUISchema(Schema):
    date = ma_fields.String(required=True)
    dateType = ma_fields.String(required=True)


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()
    identifier = ma_fields.String()

class DatasetsUISchema(DataCiteRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDataCiteMetadataUISchema())
    oai = ma_fields.Nested(lambda: OaiUISchema())

class AffiliationSchema(Schema):
    name = ma_fields.String()

class NameIdentifierSchema(Schema):
    nameIdentifier = ma_fields.String()
    nameIdentifierScheme = ma_fields.String()

class CreatorSchema(Schema):
    affiliation = ma_fields.List(ma_fields.Nested(AffiliationSchema))
    familyName = ma_fields.String()
    name = ma_fields.String()
    nameIdentifiers = ma_fields.List(ma_fields.Nested(NameIdentifierSchema))
    nameType = ma_fields.String()

class DateSchema(Schema):
    date = ma_fields.String()
    dateType = ma_fields.String()

class DescriptionSchema(Schema):
    description = ma_fields.String()
    descriptionType = ma_fields.String()

class FundingReferenceSchema(Schema):
    awardNumber = ma_fields.String()
    awardTitle = ma_fields.String()
    awardURI = ma_fields.String()
    funderIdentifier = ma_fields.String()
    funderIdentifierType = ma_fields.String()
    funderName = ma_fields.String()

class RightsSchema(Schema):
    rights = ma_fields.String()
    rightsIdentifier = ma_fields.String()
    rightsIdentifierScheme = ma_fields.String()
    rightsURI = ma_fields.String()

class TitleSchema(Schema):
    title = ma_fields.String()
    titleType = ma_fields.String()

class ResourceTypeSchema(Schema):
    resourceType = ma_fields.String()
    resourceTypeGeneral = ma_fields.String()

class IdentifierSchema(Schema):
    identifier = ma_fields.String()
    identifierType = ma_fields.String(default="OriginalURL")

class NRDCATMetadataSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    creators = ma_fields.List(ma_fields.Nested(CreatorSchema))
    dates = ma_fields.List(ma_fields.Nested(DateSchema))
    descriptions = ma_fields.List(ma_fields.Nested(DescriptionSchema))
    fundingReferences = ma_fields.List(ma_fields.Nested(FundingReferenceSchema))
    language = ma_fields.String()
    publicationYear = ma_fields.String()
    publisher = ma_fields.String()
    rightsList = ma_fields.List(ma_fields.Nested(RightsSchema))
    titles = ma_fields.List(ma_fields.Nested(TitleSchema))
    types = ma_fields.Nested(ResourceTypeSchema)
    schemaVersion = ma_fields.String(default="http://datacite.org/schema/kernel-4")
    identifiers = ma_fields.List(ma_fields.Nested(IdentifierSchema))
    version = ma_fields.String()
    url = ma_fields.String()

class DatasetsDCATAPMetadataSchema(NRDCATMetadataSchema):
    class Meta:
        unknown = ma.RAISE

    def __init__(self, *args, **kwargs):
        url_value = kwargs.pop('url', None)
        super().__init__(*args, **kwargs)
        if url_value:
            if 'identifiers' not in self.fields:
                self.fields['identifiers'] = ma_fields.List(ma_fields.Nested(IdentifierSchema))
            self.fields['identifiers'].default = [{
                'identifier': url_value,
                'identifierType': 'OriginalURL'
            }]
        if 'version' in kwargs:
            del kwargs['version']

class DCATAPSerializer(JSONSerializer):
    def serialize_object(self, obj, **kwargs):
        try:
            metadata = obj.get('metadata', {})
            if 'publisher' in metadata and isinstance(metadata['publisher'], dict):
                metadata['publisher'] = metadata['publisher'].get('name', '')
            if 'resourceType' in metadata:
                metadata['types'] = metadata.pop('resourceType')
            if 'url' in metadata:
                metadata['identifiers'] = metadata.get('identifiers', [])
                metadata['identifiers'].append({
                    'identifier': metadata.pop('url'),
                    'identifierType': 'OriginalURL'
                })
            if 'schemaVersion' not in metadata:
                metadata['schemaVersion'] = "http://datacite.org/schema/kernel-4"
            if 'version' in metadata:
                del metadata['version']
            schema = DatasetsDCATAPMetadataSchema()
            try:
                metadata = schema.load(metadata)
            except ValidationError as err:
                raise ValueError(f"Invalid metadata: {err.messages}")
            obj['metadata'] = metadata
        except Exception as e:
            raise ValueError(f"Invalid metadata: {e}")
            
        return super().serialize_object(obj, **kwargs)