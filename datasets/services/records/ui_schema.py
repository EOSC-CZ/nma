import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
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

    oai = ma_fields.Nested(lambda: OaiUISchema())

    state = ma_fields.String(dump_only=True)

    state_timestamp = LocalizedDateTime(dump_only=True)

    version_id = ma_fields.Integer()


class DatasetsMetadataUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    alternate_titles = ma_fields.List(
        ma_fields.Nested(lambda: AlternateTitlesItemUISchema())
    )

    descriptions = ma_fields.List(I18nStrUIField())

    distributions = ma_fields.List(
        ma_fields.Nested(lambda: DistributionsItemUISchema())
    )

    funding_references = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferencesItemUISchema())
    )

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemUISchema()))

    iri = ma_fields.String()

    is_described_by = ma_fields.List(
        ma_fields.Nested(lambda: IsDescribedByItemUISchema(), required=True)
    )

    locations = ma_fields.List(ma_fields.Nested(lambda: LocationsItemUISchema()))

    other_languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularyUISchema()))

    primary_language = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    provenances = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())
    )

    publication_year = ma_fields.Integer()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )

    related_resources = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectsItemUISchema())
    )

    resource_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectsItemUISchema()))

    terms_of_use = ma_fields.Nested(lambda: TermsOfUseUISchema())

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemUISchema())
    )

    title = ma_fields.String(required=True)

    validation_results = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())
    )

    version = ma_fields.String()

    versions = ma_fields.List(ma_fields.String())


class LocationsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    bbox = ma_fields.Nested(lambda: BboxUISchema())

    geometry = ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())

    iri = ma_fields.String()

    names = ma_fields.List(ma_fields.String())

    related_objects = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectsItemUISchema())
    )

    relation_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())


class FundingReferencesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    award_title = ma_fields.String()

    funders = ma_fields.List(ma_fields.Nested(lambda: FundersItemUISchema()))

    funding_program = ma_fields.String()

    iri = ma_fields.String()

    local_identifier = ma_fields.String()


class IsDescribedByItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    conforms_to_standards = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())
    )

    date_created = LocalizedDate()

    dates_updated = ma_fields.List(LocalizedDate())

    iri = ma_fields.String()

    languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularyUISchema()))

    original_repositories = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())
    )

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )


class RelatedObjectsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemUISchema()))

    iri = ma_fields.String()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemUISchema())
    )

    relation_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    resource_url = ma_fields.String()

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemUISchema())
    )

    title = ma_fields.String()

    type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())


class TermsOfUseUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_rights = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    contacts = ma_fields.List(ma_fields.Nested(lambda: FundersItemUISchema()))

    description = ma_fields.List(I18nStrUIField())

    iri = ma_fields.String()

    license = ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())


class FundersItemUISchema(DictOnlySchema):
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

    family_names = ma_fields.List(ma_fields.String(required=True))

    given_names = ma_fields.List(ma_fields.String())

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemUISchema()))

    iri = ma_fields.String()

    name = ma_fields.String()


class OrganizationUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    alternate_names = ma_fields.List(I18nStrUIField())

    contact_points = ma_fields.List(
        ma_fields.Nested(lambda: ContactPointsItemUISchema())
    )

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemUISchema()))

    iri = ma_fields.String()

    name = ma_fields.String(required=True)


class ContactPointsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    addresses = ma_fields.List(ma_fields.Nested(lambda: AddressesItemUISchema()))

    dataBoxes = ma_fields.List(ma_fields.String())

    emails = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    phones = ma_fields.List(ma_fields.String())


class DistributionsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_urls = ma_fields.List(ma_fields.String())

    byte_size = ma_fields.Integer()

    checksum = ma_fields.Nested(lambda: ChecksumUISchema())

    conforms_to_schemas = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemUISchema())
    )

    download_urls = ma_fields.List(ma_fields.String())

    format = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    iri = ma_fields.String()

    media_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    title = ma_fields.String()


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class AddressesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    address_areas = ma_fields.List(ma_fields.String())

    administrative_unit_level_1 = ma_fields.String()

    administrative_unit_level_2 = ma_fields.String()

    full_address = ma_fields.String()

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrUIField())

    locator_designators = ma_fields.List(ma_fields.String())

    locator_names = ma_fields.List(ma_fields.String())

    po_box = ma_fields.String()

    post_code = ma_fields.String()

    post_names = ma_fields.List(ma_fields.String())

    thoroughfares = ma_fields.List(ma_fields.String())


class AlternateTitlesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    title = ma_fields.List(I18nStrUIField(required=True))

    type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())


class BboxUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    LowerCorners = ma_fields.List(ma_fields.Float(required=True))

    UpperCorners = ma_fields.List(ma_fields.Float(required=True))

    crs = ma_fields.String()

    dimensions = ma_fields.Integer()


class ChecksumUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    algorithm = ma_fields.Nested(lambda: CCMMVocabularyUISchema(), required=True)

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


class ConformsToSchemasItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrUIField())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class IdentifiersItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier_scheme = ma_fields.Nested(
        lambda: CCMMVocabularyUISchema(), required=True
    )

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


class SubjectsItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    classification_code = ma_fields.String()

    definitions = ma_fields.List(I18nStrUIField())

    iri = ma_fields.String()

    scheme = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    title = ma_fields.List(I18nStrUIField(required=True))


class TimeReferencesItemUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    date = LocalizedEDTFTime()

    date_information = I18nStrUIField()

    date_type = ma_fields.Nested(lambda: CCMMVocabularyUISchema())

    iri = ma_fields.String()
