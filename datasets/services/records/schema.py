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
from marshmallow.validate import OneOf
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

from common.services.schema import CCMMVocabularySchema


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

    descriptions = ma_fields.List(I18nStrField(), required=True)

    distribution_data_services = ma_fields.List(
        ma_fields.Nested(lambda: DistributionDataServicesItemSchema())
    )

    distribution_downloadable_files = ma_fields.List(
        ma_fields.Nested(lambda: DistributionDownloadableFilesItemSchema())
    )

    funding_references = ma_fields.List(
        ma_fields.Nested(lambda: FundingReferencesItemSchema())
    )

    identifiers = ma_fields.List(
        ma_fields.Nested(lambda: IdentifiersItemSchema()), required=True
    )

    iri = ma_fields.String()

    is_described_by = ma_fields.List(
        ma_fields.Nested(lambda: IsDescribedByItemSchema()), required=True
    )

    locations = ma_fields.List(ma_fields.Nested(lambda: LocationsItemSchema()))

    other_languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularySchema()))

    primary_language = ma_fields.Nested(lambda: CCMMVocabularySchema())

    provenances = ma_fields.List(ma_fields.Nested(lambda: DocumentationsItemSchema()))

    publication_year = ma_fields.Integer()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )

    related_resources = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectIdentifiersItemSchema())
    )

    resource_type = ma_fields.Nested(lambda: CCMMVocabularySchema())

    subjects = ma_fields.List(ma_fields.Nested(lambda: SubjectsItemSchema()))

    terms_of_use = ma_fields.List(ma_fields.Nested(lambda: TermsOfUseItemSchema()))

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemSchema())
    )

    title = ma_fields.String(required=True)

    validation_results = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    version = ma_fields.String()


class LocationsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    bbox = ma_fields.Nested(lambda: BboxSchema())

    dataset_relations = ma_fields.List(ma_fields.String())

    geometry = ma_fields.Nested(lambda: DocumentationsItemSchema())

    iri = ma_fields.String()

    location_names = ma_fields.List(ma_fields.String())

    related_object_identifiers = ma_fields.List(
        ma_fields.Nested(lambda: RelatedObjectIdentifiersItemSchema())
    )


class IsDescribedByItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    conforms_to_standards = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    date_created = ma_fields.String(validate=[validate_date("%Y-%m-%d")])

    dates_updated = ma_fields.List(
        ma_fields.String(validate=[validate_date("%Y-%m-%d")])
    )

    iri = ma_fields.String()

    languages = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularySchema()))

    original_repositories = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )


class RelatedObjectIdentifiersItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier = ma_fields.Nested(lambda: IdentifiersItemSchema())

    iri = ma_fields.String()

    qualified_relations = ma_fields.List(
        ma_fields.Nested(lambda: QualifiedRelationsItemSchema())
    )

    relation_type = ma_fields.Nested(lambda: CCMMVocabularySchema())

    time_references = ma_fields.List(
        ma_fields.Nested(lambda: TimeReferencesItemSchema())
    )

    title = ma_fields.String()

    type = ma_fields.String()


class TermsOfUseItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_rights = ma_fields.List(ma_fields.Nested(lambda: CCMMVocabularySchema()))

    contacts = ma_fields.List(ma_fields.Nested(lambda: ContactsItemSchema()))

    description = I18nStrField()

    iri = ma_fields.String()

    license = ma_fields.String()


class ContactsItemSchema(DictOnlySchema):
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

    role = ma_fields.Nested(lambda: CCMMVocabularySchema(), required=True)


class PersonSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(ma_fields.Nested(lambda: OrganizationSchema()))

    contact_points = ma_fields.List(ma_fields.Nested(lambda: ContactPointsItemSchema()))

    external_identifier_type = ma_fields.String()

    external_identifiers = ma_fields.List(ma_fields.String())

    family_name = ma_fields.String(required=True)

    given_names = ma_fields.List(ma_fields.String(), required=True)

    iri = ma_fields.String()


class OrganizationSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    alternate_names = ma_fields.List(I18nStrField())

    contact_points = ma_fields.List(ma_fields.Nested(lambda: ContactPointsItemSchema()))

    external_identifier_type = ma_fields.String()

    external_identifiers = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    name = I18nStrField(required=True)


class ContactPointsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    addresses = ma_fields.List(ma_fields.Nested(lambda: DocumentationsItemSchema()))

    dataBoxes = ma_fields.List(ma_fields.String())

    emails = ma_fields.List(ma_fields.String())

    iri = ma_fields.String()

    phones = ma_fields.List(ma_fields.String())


class DistributionDataServicesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_services = ma_fields.List(
        ma_fields.Nested(lambda: AccessServicesItemSchema())
    )

    descriptions = ma_fields.List(I18nStrField())

    documentations = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    iri = ma_fields.String()

    specifications = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    title = ma_fields.String()


class DistributionDownloadableFilesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    access_urls = ma_fields.List(ma_fields.String(), required=True)

    byte_size = ma_fields.Integer()

    checksum = ma_fields.String(required=True)

    conforms_to_schemas = ma_fields.List(
        ma_fields.Nested(lambda: DocumentationsItemSchema())
    )

    download_urls = ma_fields.List(ma_fields.String())

    format = ma_fields.Nested(lambda: CCMMVocabularySchema())

    iri = ma_fields.String()

    media_type = ma_fields.Nested(lambda: DocumentationsItemSchema())

    title = ma_fields.String()


class FundingReferencesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    award_title = ma_fields.String()

    funders = ma_fields.List(ma_fields.Nested(lambda: FundersItemSchema()))

    funding_program = ma_fields.String()

    iri = ma_fields.String()

    local_identifier = ma_fields.String()


class OaiSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestSchema())


class SubjectsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    classification_code = ma_fields.String()

    definition = I18nStrField()

    in_subject_scheme = ma_fields.Nested(lambda: DocumentationsItemSchema())

    iri = ma_fields.String()

    title = I18nStrField(required=True)


class AccessServicesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    endpoint_urls = ma_fields.List(ma_fields.String(), required=True)

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrField())


class AlternateTitlesItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    title = I18nStrField(required=True)

    type = ma_fields.String(
        validate=[OneOf(["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"])]
    )


class BboxSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    LowerCorners = ma_fields.List(ma_fields.Float(), required=True)

    UpperCorners = ma_fields.List(ma_fields.Float(), required=True)

    crs = ma_fields.String()

    dimensions = ma_fields.Integer()


class DocumentationsItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    iri = ma_fields.String()

    labels = ma_fields.List(I18nStrField())


class FundersItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    funder_identifier_scheme_uri = ma_fields.String()

    funder_identifier_type = ma_fields.String(required=True)

    funder_identifier_value = ma_fields.String(required=True)

    funder_name = ma_fields.String()

    iri = ma_fields.String()


class HarvestSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()


class IdentifiersItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    identifier_scheme = ma_fields.String(required=True)

    iri = ma_fields.String()

    value = ma_fields.String(required=True)


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

    date_information = ma_fields.String()

    date_type = ma_fields.Nested(lambda: CCMMVocabularySchema())

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
