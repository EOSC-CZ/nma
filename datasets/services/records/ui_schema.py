import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.validate import OneOf
from oarepo_requests.services.ui_schema import UIRequestsSerializationMixin
from oarepo_runtime.services.schema.i18n_ui import I18nStrUIField
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.ui import (
    InvenioRDMUISchema,
    LocalizedDate,
    LocalizedDateTime,
    LocalizedEDTFTime,
)

from common.services.ui_schema import CCMMVocabularyUISchema


class DatasetsUISchema(UIRequestsSerializationMixin, InvenioRDMUISchema):
    class Meta:
        unknown = ma.RAISE

    deletion_status = ma_fields.String()

    is_deleted = ma_fields.Boolean()

    is_published = ma_fields.Boolean()

    metadata = ma_fields.Nested(lambda: DatasetsMetadataUISchema())

    state = ma_fields.String(dump_only=True)

    state_timestamp = LocalizedDateTime(dump_only=True)

    version_id = ma_fields.Integer()


class DatasetsMetadataUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    alternate_titles = ma_fields.List(
        ma_fields.Nested(lambda: AlternateTitlesItemUISchema())
    )

    descriptions = ma_fields.List(I18nStrUIField(), required=True)

    distribution_data_services = ma_fields.List(
        ma_fields.Nested(lambda: DistributionDataServicesItemUISchema())
    )

    distribution_downloadable_files = ma_fields.List(
        ma_fields.Nested(lambda: DistributionDownloadableFilesItemUISchema())
    )

    funding_references = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferencesItemUISchema())
    )

    identifiers = ma_fields.List(
        ma_fields.Nested(lambda: IdentifiersItemUISchema()), required=True
    )

    iri = ma_fields.String()

    is_described_by = ma_fields.List(
        ma_fields.Nested(lambda: IsDescribedByItemUISchema()), required=True
    )

    locations = ma_fields.List(ma_fields.Nested(lambda: LocationsItemUISchema()))

    other_languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularyUISchema()))

    primary_language = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    provenances = ma_fields.List(ma_fields.Nested(lambda: DocumentationsItemUISchema()))

    publication_year = ma_fields.Integer()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )

    related_resources = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectIdentifiersItemUISchema())
    )

    resource_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectsItemUISchema()))

    terms_of_use = ma_fields.List(ma_fields.Nested(lambda: TermsOfUseItemUISchema()))

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemUISchema())
    )

    title = ma_fields.String(required=True)

    validation_results = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    version = ma_fields.String()


class LocationsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    bbox = ma_fields.Nested(lambda: BboxUISchema())

    dataset_relations = ma_fields.List(ma_fields.String())

    geometry = ma_fields.Nested(lambda: DocumentationsItemUISchema())

    iri = ma_fields.String()

    location_names = ma_fields.List(ma_fields.String())

    related_object_identifiers = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectIdentifiersItemUISchema())
    )


class IsDescribedByItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    conforms_to_standards = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    date_created = LocalizedDate()

    dates_updated = ma_fields.List(LocalizedDate())

    iri = ma_fields.String()

    languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularyUISchema()))

    original_repositories = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )


class RelatedObjectIdentifiersItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier = ma_fields.Nested(lambda: IdentifiersItemUISchema())

    iri = ma_fields.String()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )

    relation_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemUISchema())
    )

    title = ma_fields.String()

    type = ma_fields.String()


class TermsOfUseItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_rights = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularyUISchema()))

    contacts = ma_fields.List(ma_fields.Nested(lambda: ContactsItemUISchema()))

    description = I18nStrUIField()

    iri = ma_fields.String()

    license = ma_fields.String()


class ContactsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    organization = ma_fields.Nested(lambda: OrganizationUISchema())

    person = ma_fields.Nested(lambda: PersonUISchema())


class QualifiedRelationsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    organization = ma_fields.Nested(lambda: OrganizationUISchema())

    person = ma_fields.Nested(lambda: PersonUISchema())

    role = ma_fields.Nested(lambda: CCMMVocabularyUISchema(), required=True)


class PersonUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(ma_fields.Nested(lambda: OrganizationUISchema()))

    contact_points = ma_fields.List(
        ma_fields.Nested(lambda: ContactPointsItemUISchema())
    )

    external_identifier_type = ma_fields.String()

    external_identifiers = ma_fields.List(ma_fields.String())

    family_name = ma_fields.String(required=True)

    given_names = ma_fields.List(ma_fields.String(), required=True)

    iri = ma_fields.String()


class OrganizationUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    alternate_names = ma_fields.List(I18nStrUIField())

    contact_points = ma_fields.List(
        ma_fields.Nested(lambda: ContactPointsItemUISchema())
    )

    external_identifier_type = ma_fields.String()

    external_identifiers = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    name = I18nStrUIField(required=True)


class ContactPointsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    addresses = ma_fields.List(ma_fields.Nested(lambda: DocumentationsItemUISchema()))

    dataBoxes = ma_fields.List(ma_fields.String())

    emails = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    phones = ma_fields.List(ma_fields.String())


class DistributionDataServicesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_services = ma_fields.List(
        ma_fields.Nested(lambda: AccessServicesItemUISchema())
    )

    descriptions = ma_fields.List(I18nStrUIField())

    documentations = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    iri = ma_fields.String()

    specifications = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    title = ma_fields.String()


class DistributionDownloadableFilesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_urls = ma_fields.List(ma_fields.String(), required=True)

    byte_size = ma_fields.Integer()

    checksum = ma_fields.String(required=True)

    conforms_to_schemas = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemUISchema())
    )

    download_urls = ma_fields.List(ma_fields.String())

    format = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    iri = ma_fields.String()

    media_type = ma_fields.Nested(lambda: DocumentationsItemUISchema())

    title = ma_fields.String()


class FundingReferencesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    award_title = ma_fields.String()

    funders = ma_fields.List(ma_fields.Nested(lambda: FundersItemUISchema()))

    funding_program = ma_fields.String()

    iri = ma_fields.String()

    local_identifier = ma_fields.String()


class SubjectsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    classification_code = ma_fields.String()

    definition = I18nStrUIField()

    in_subject_scheme = ma_fields.Nested(lambda: DocumentationsItemUISchema())

    iri = ma_fields.String()

    title = I18nStrUIField(required=True)


class AccessServicesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    endpoint_urls = ma_fields.List(ma_fields.String(), required=True)

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrUIField())


class AlternateTitlesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    title = I18nStrUIField(required=True)

    type = ma_fields.String(
        validate=[OneOf(["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"])]
    )


class BboxUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    LowerCorners = ma_fields.List(ma_fields.Float(), required=True)

    UpperCorners = ma_fields.List(ma_fields.Float(), required=True)

    crs = ma_fields.String()

    dimensions = ma_fields.Integer()


class DocumentationsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrUIField())


class FundersItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    funder_identifier_scheme_uri = ma_fields.String()

    funder_identifier_type = ma_fields.String(required=True)

    funder_identifier_value = ma_fields.String(required=True)

    funder_name = ma_fields.String()

    iri = ma_fields.String()


class IdentifiersItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier_scheme = ma_fields.String(required=True)

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


class TimeReferencesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    date = LocalizedEDTFTime()

    date_information = ma_fields.String()

    date_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    iri = ma_fields.String()
