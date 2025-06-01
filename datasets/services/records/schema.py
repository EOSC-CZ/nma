import marshmallow as ma
from edtf import Date as EDTFDate
from edtf import DateAndTime as EDTFDateAndTime
from invenio_rdm_records.services.schemas.access import AccessSchema
from invenio_rdm_records.services.schemas.pids import PIDSchema
from invenio_rdm_records.services.schemas.record import validate_scheme
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import Dict, Nested
from marshmallow.utils import get_value
from marshmallow_utils.fields import SanitizedUnicode, TrimmedString
from marshmallow_utils.fields.nestedattr import NestedAttribute
from oarepo_communities.schemas.parent import CommunitiesParentSchema
from oarepo_runtime.services.schema.i18n import I18nStrField
from oarepo_runtime.services.schema.marshmallow import (
    DictOnlySchema,
    RDMBaseRecordSchema,
)
from oarepo_runtime.services.schema.validation import (
    CachedMultilayerEDTFValidator,
    validate_date,
    validate_datetime,
)
from oarepo_workflows.services.records.schema import RDMWorkflowParentSchema

from common.services.schema import (
    CCMMAccessRightsVocabularySchema,
    CCMMChecksumAlgorithmsVocabularySchema,
    CCMMContributorTypesVocabularySchema,
    CCMMFileTypesVocabularySchema,
    CCMMIdentifierSchemesVocabularySchema,
    CCMMLanguagesVocabularySchema,
    CCMMLocationRelationTypesVocabularySchema,
    CCMMMediaTypesVocabularySchema,
    CCMMRelationTypesVocabularySchema,
    CCMMResourceTypesVocabularySchema,
    CCMMSubjectSchemesVocabularySchema,
    CCMMTimeReferenceTypesVocabularySchema,
    CCMMTitleTypesVocabularySchema,
)


class GeneratedParentSchema(RDMWorkflowParentSchema):
    """"""

    owners = ma.fields.List(ma.fields.Dict(), load_only=True)

    communities = ma_fields.Nested(CommunitiesParentSchema)


class DatasetsSchema(RDMBaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    access = NestedAttribute(lambda: AccessSchema())

    metadata = ma_fields.Nested(lambda: DatasetsMetadataSchema())

    oai = ma_fields.Nested(lambda: OaiSchema())

    pids = Dict(
        keys=SanitizedUnicode(validate=validate_scheme),
        values=Nested(PIDSchema),
    )

    state = ma_fields.String(dump_only=True)

    state_timestamp = ma_fields.String(dump_only=True, validate=[validate_datetime])
    parent = ma.fields.Nested(GeneratedParentSchema)
    files = ma.fields.Nested(
        lambda: FilesOptionsSchema(), load_default={"enabled": True}
    )

    # todo this needs to be generated for [default preview] to work
    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping.

        NOTE: We have to access by attribute because although we are loading
              from an external pure dict, but we are dumping from a data-layer
              object whose fields should be accessed by attributes and not
              keys. Access by key runs into FilesManager key access protection
              and raises.
        """
        if attr == "files":
            return getattr(obj, attr, default)
        else:
            return get_value(obj, attr, default)


class DatasetsMetadataSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    alternate_titles = ma_fields.List(
        ma_fields.Nested(lambda: AlternateTitlesItemSchema())
    )

    descriptions = ma_fields.List(I18nStrField())

    distributions = ma_fields.List(ma_fields.Nested(lambda: DistributionsItemSchema()))

    funding_references = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferencesItemSchema())
    )

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemSchema()))

    iri = ma_fields.String()

    is_described_by = ma_fields.List(
        ma_fields.Nested(lambda: IsDescribedByItemSchema(), required=True)
    )

    locations = ma_fields.List(ma_fields.Nested(lambda: LocationsItemSchema()))

    other_languages = ma_fields.List(
        ma_fields.Nested(lambda: CCMMLanguagesVocabularySchema())
    )

    primary_language = ma_fields.Nested(lambda: CCMMLanguagesVocabularySchema())

    provenances = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemSchema())
    )

    publication_year = ma_fields.Integer()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )

    related_resources = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectsItemSchema())
    )

    resource_type = ma_fields.Nested(lambda: CCMMResourceTypesVocabularySchema())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectsItemSchema()))

    terms_of_use = ma_fields.Nested(lambda: TermsOfUseSchema())

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemSchema())
    )

    title = ma_fields.String(required=True)

    validation_results = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemSchema())
    )

    version = ma_fields.String()

    versions = ma_fields.List(ma_fields.String())


class LocationsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    bbox = ma_fields.Nested(lambda: BboxSchema())

    geometry = ma_fields.Nested(lambda: ConformsToSchemasItemSchema())

    iri = ma_fields.String()

    names = ma_fields.List(ma_fields.String())

    related_objects = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectsItemSchema())
    )

    relation_type = ma_fields.Nested(
        lambda: CCMMLocationRelationTypesVocabularySchema()
    )


class FundingReferencesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    award_title = ma_fields.String()

    funders = ma_fields.List(ma_fields.Nested(lambda: FundersItemSchema()))

    funding_program = ma_fields.String()

    iri = ma_fields.String()

    local_identifier = ma_fields.String()


class IsDescribedByItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    conforms_to_standards = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemSchema())
    )

    date_created = ma_fields.String(validate=[validate_date("%Y-%m-%d")])

    dates_updated = ma_fields.List(
        ma_fields.String(validate=[validate_date("%Y-%m-%d")])
    )

    iri = ma_fields.String()

    languages = ma_fields.List(
        ma_fields.Nested(lambda: CCMMLanguagesVocabularySchema())
    )

    original_repositories = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemSchema())
    )

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )


class RelatedObjectsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemSchema()))

    iri = ma_fields.String()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )

    relation_type = ma_fields.Nested(lambda: CCMMRelationTypesVocabularySchema())

    resource_url = ma_fields.String()

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemSchema())
    )

    title = ma_fields.String()

    type = ma_fields.Nested(lambda: CCMMResourceTypesVocabularySchema())


class TermsOfUseSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_rights = ma_fields.Nested(lambda: CCMMAccessRightsVocabularySchema())

    contacts = ma_fields.List(ma_fields.Nested(lambda: FundersItemSchema()))

    description = ma_fields.List(I18nStrField())

    iri = ma_fields.String()

    license = ma_fields.Nested(lambda: ConformsToSchemasItemSchema())


class FundersItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    organization = ma_fields.Nested(lambda: OrganizationSchema())

    person = ma_fields.Nested(lambda: PersonSchema())


class QualifiedRelationsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    organization = ma_fields.Nested(lambda: OrganizationSchema())

    person = ma_fields.Nested(lambda: PersonSchema())

    role = ma_fields.Nested(
        lambda: CCMMContributorTypesVocabularySchema(), required=True
    )


class PersonSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(ma_fields.Nested(lambda: OrganizationSchema()))

    contact_points = ma_fields.List(ma_fields.Nested(lambda: ContactPointsItemSchema()))

    family_names = ma_fields.List(ma_fields.String(required=True))

    given_names = ma_fields.List(ma_fields.String())

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemSchema()))

    iri = ma_fields.String()

    name = ma_fields.String()


class OrganizationSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    alternate_names = ma_fields.List(I18nStrField())

    contact_points = ma_fields.List(ma_fields.Nested(lambda: ContactPointsItemSchema()))

    identifiers = ma_fields.List(ma_fields.Nested(lambda: IdentifiersItemSchema()))

    iri = ma_fields.String()

    name = ma_fields.String(required=True)


class ContactPointsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    addresses = ma_fields.List(ma_fields.Nested(lambda: AddressesItemSchema()))

    dataBoxes = ma_fields.List(ma_fields.String())

    emails = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    phones = ma_fields.List(ma_fields.String())


class DistributionsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_urls = ma_fields.List(ma_fields.String())

    byte_size = ma_fields.Integer()

    checksum = ma_fields.Nested(lambda: ChecksumSchema())

    conforms_to_schemas = ma_fields.List(
        ma_fields.Nested(lambda: ConformsToSchemasItemSchema())
    )

    download_urls = ma_fields.List(ma_fields.String())

    format = ma_fields.Nested(lambda: CCMMFileTypesVocabularySchema())

    iri = ma_fields.String()

    media_type = ma_fields.Nested(lambda: CCMMMediaTypesVocabularySchema())

    title = ma_fields.String()


class OaiSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestSchema())


class AddressesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    address_areas = ma_fields.List(ma_fields.String())

    administrative_unit_level_1 = ma_fields.String()

    administrative_unit_level_2 = ma_fields.String()

    full_address = ma_fields.String()

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrField())

    locator_designators = ma_fields.List(ma_fields.String())

    locator_names = ma_fields.List(ma_fields.String())

    po_box = ma_fields.String()

    post_code = ma_fields.String()

    post_names = ma_fields.List(ma_fields.String())

    thoroughfares = ma_fields.List(ma_fields.String())


class AlternateTitlesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    title = ma_fields.List(I18nStrField(required=True))

    type = ma_fields.Nested(lambda: CCMMTitleTypesVocabularySchema())


class BboxSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    LowerCorners = ma_fields.List(ma_fields.Float(required=True))

    UpperCorners = ma_fields.List(ma_fields.Float(required=True))

    crs = ma_fields.String()

    dimensions = ma_fields.Integer()


class ChecksumSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    algorithm = ma_fields.Nested(
        lambda: CCMMChecksumAlgorithmsVocabularySchema(), required=True
    )

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


class ConformsToSchemasItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrField())


class HarvestSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class IdentifiersItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier_scheme = ma_fields.Nested(
        lambda: CCMMIdentifierSchemesVocabularySchema(), required=True
    )

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


class SubjectsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    classification_code = ma_fields.String()

    definitions = ma_fields.List(I18nStrField())

    iri = ma_fields.String()

    scheme = ma_fields.Nested(lambda: CCMMSubjectSchemesVocabularySchema())

    title = ma_fields.List(I18nStrField(required=True))


class TimeReferencesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    date = TrimmedString(
        validate=[
            CachedMultilayerEDTFValidator(
                types=(
                    EDTFDateAndTime,
                    EDTFDate,
                )
            )
        ]
    )

    date_information = I18nStrField()

    date_type = ma_fields.Nested(lambda: CCMMTimeReferenceTypesVocabularySchema())

    iri = ma_fields.String()


class FilesOptionsSchema(ma.Schema):
    """Basic files options schema class."""

    enabled = ma.fields.Bool(missing=True)
    # allow unsetting
    default_preview = SanitizedUnicode(allow_none=True)

    def get_attribute(self, obj, attr, default):
        """Override how attributes are retrieved when dumping.

        NOTE: We have to access by attribute because although we are loading
              from an external pure dict, but we are dumping from a data-layer
              object whose fields should be accessed by attributes and not
              keys. Access by key runs into FilesManager key access protection
              and raises.
        """
        value = getattr(obj, attr, default)

        if attr == "default_preview" and not value:
            return default

        return value
