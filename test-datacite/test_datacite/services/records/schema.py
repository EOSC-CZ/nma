import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.marshmallow import BaseRecordSchema, DictOnlySchema
from test_datacite.services.records.schema_datatypes import (
    AlternateIdentifierSchema,
    ContainerSchema,
    ContributorSchema,
    CreatorSchema,
    DateSchema,
    DescriptionSchema,
    FundingReferenceSchema,
    GeoLocationSchema,
    PublisherSchema,
    RelatedIdentifierSchema,
    RelatedItemSchema,
    ResourceTypeSchema,
    RightsSchema,
    SubjectSchema,
    TitleSchema,
)


class DataCiteRecordSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDataCiteMetadataSchema())

    oai = ma_fields.Nested(lambda: OaiSchema())


class OaiSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestSchema())


class HarvestSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class NRDataCiteMetadataSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    alternateIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AlternateIdentifierSchema())
    )

    container = ma_fields.Nested(lambda: ContainerSchema())

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorSchema()))

    creators = ma_fields.List(ma_fields.Nested(lambda: CreatorSchema()))

    dates = ma_fields.List(ma_fields.Nested(lambda: DateSchema()))

    descriptions = ma_fields.List(ma_fields.Nested(lambda: DescriptionSchema()))

    doi = ma_fields.String()

    formats = ma_fields.List(ma_fields.String())

    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferenceSchema())
    )

    geoLocations = ma_fields.List(ma_fields.Nested(lambda: GeoLocationSchema()))

    language = ma_fields.String()

    publicationYear = ma_fields.String()

    publisher = ma_fields.Nested(lambda: PublisherSchema())

    relatedIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: RelatedIdentifierSchema())
    )

    relatedItems = ma_fields.List(ma_fields.Nested(lambda: RelatedItemSchema()))

    rightsList = ma_fields.List(ma_fields.Nested(lambda: RightsSchema()))

    schemaVersion = ma_fields.String()

    sizes = ma_fields.List(ma_fields.String())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectSchema()))

    titles = ma_fields.List(ma_fields.Nested(lambda: TitleSchema()))

    types = ma_fields.List(ma_fields.Nested(lambda: ResourceTypeSchema()))

    url = ma_fields.String()

    version = ma_fields.String()
