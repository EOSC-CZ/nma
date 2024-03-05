import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from oarepo_runtime.services.schema.ui import InvenioUISchema
from test_datacite.services.records.ui_schema_datatypes import (
    AlternateIdentifierUISchema,
    ContainerUISchema,
    ContributorUISchema,
    CreatorUISchema,
    DateUISchema,
    DescriptionUISchema,
    FundingReferenceUISchema,
    GeoLocationUISchema,
    PublisherUISchema,
    RelatedIdentifierUISchema,
    RelatedItemUISchema,
    ResourceTypeUISchema,
    RightsUISchema,
    SubjectUISchema,
    TitleUISchema,
)


class DataCiteRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDataCiteMetadataUISchema())


class NRDataCiteMetadataUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    alternateIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: AlternateIdentifierUISchema())
    )

    container = ma_fields.Nested(lambda: ContainerUISchema())

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorUISchema()))

    creators = ma_fields.List(ma_fields.Nested(lambda: CreatorUISchema()))

    dates = ma_fields.List(ma_fields.Nested(lambda: DateUISchema()))

    descriptions = ma_fields.List(ma_fields.Nested(lambda: DescriptionUISchema()))

    doi = ma_fields.String()

    formats = ma_fields.List(ma_fields.String())

    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferenceUISchema())
    )

    geoLocations = ma_fields.List(ma_fields.Nested(lambda: GeoLocationUISchema()))

    language = ma_fields.String()

    publicationYear = ma_fields.String()

    publisher = ma_fields.Nested(lambda: PublisherUISchema())

    relatedIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: RelatedIdentifierUISchema())
    )

    relatedItems = ma_fields.List(ma_fields.Nested(lambda: RelatedItemUISchema()))

    rightsList = ma_fields.List(ma_fields.Nested(lambda: RightsUISchema()))

    schemaVersion = ma_fields.String()

    sizes = ma_fields.List(ma_fields.String())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectUISchema()))

    titles = ma_fields.List(ma_fields.Nested(lambda: TitleUISchema()))

    types = ma_fields.List(ma_fields.Nested(lambda: ResourceTypeUISchema()))

    url = ma_fields.String()

    version = ma_fields.String()
