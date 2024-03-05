import marshmallow as ma
from edtf import Date as EDTFDate
from marshmallow import fields as ma_fields
from marshmallow.validate import OneOf
from marshmallow_utils.fields import TrimmedString
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema
from oarepo_runtime.services.schema.validation import CachedMultilayerEDTFValidator


class GeoLocationSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    geoLocationBox = ma_fields.Nested(lambda: GeoLocationBoxSchema())

    geoLocationPlace = ma_fields.String()

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointSchema())

    geoLocationPolygons = ma_fields.List(
        ma_fields.Nested(lambda: GeoLocationPolygonSchema())
    )


class RelatedItemSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorSchema()))

    creators = ma_fields.List(ma_fields.Nested(lambda: CreatorSchema()))

    edition = ma_fields.String()

    firstPage = ma_fields.String()

    issue = ma_fields.String()

    lastPage = ma_fields.String()

    number = ma_fields.String()

    numberType = ma_fields.String(
        validate=[OneOf(["Article", "Chapter", "Report", "Other"])]
    )

    publicationYear = ma_fields.String()

    publisher = ma_fields.String()

    relatedItemIdentifier = ma_fields.Nested(
        lambda: RelatedItemIdentifierSchema(), required=True
    )

    relatedItemType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "Audiovisual",
                    "Book",
                    "BookChapter",
                    "Collection",
                    "ComputationalNotebook",
                    "ConferencePaper",
                    "ConferenceProceeding",
                    "DataPaper",
                    "Dataset",
                    "Dissertation",
                    "Event",
                    "Image",
                    "Instrument",
                    "InteractiveResource",
                    "Journal",
                    "JournalArticle",
                    "Model",
                    "OutputManagementPlan",
                    "PeerReview",
                    "PhysicalObject",
                    "Preprint",
                    "Report",
                    "Service",
                    "Software",
                    "Sound",
                    "Standard",
                    "StudyRegistration",
                    "Text",
                    "Workflow",
                    "Other",
                ]
            )
        ],
    )

    relatedMetadataScheme = ma_fields.String()

    relationType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "IsCitedBy",
                    "Cites",
                    "IsCollectedBy",
                    "Collects",
                    "IsSupplementTo",
                    "IsSupplementedBy",
                    "IsContinuedBy",
                    "Continues",
                    "IsDescribedBy",
                    "Describes",
                    "HasMetadata",
                    "IsMetadataFor",
                    "HasVersion",
                    "IsVersionOf",
                    "IsNewVersionOf",
                    "IsPartOf",
                    "IsPreviousVersionOf",
                    "IsPublishedIn",
                    "HasPart",
                    "IsReferencedBy",
                    "References",
                    "IsDocumentedBy",
                    "Documents",
                    "IsCompiledBy",
                    "Compiles",
                    "IsVariantFormOf",
                    "IsOriginalFormOf",
                    "IsIdenticalTo",
                    "IsReviewedBy",
                    "Reviews",
                    "IsDerivedFrom",
                    "IsSourceOf",
                    "IsRequiredBy",
                    "Requires",
                    "IsObsoletedBy",
                    "Obsoletes",
                ]
            )
        ],
    )

    resourceTypeGeneral = ma_fields.String(
        validate=[
            OneOf(
                [
                    "Audiovisual",
                    "Book",
                    "BookChapter",
                    "Collection",
                    "ComputationalNotebook",
                    "ConferencePaper",
                    "ConferenceProceeding",
                    "DataPaper",
                    "Dataset",
                    "Dissertation",
                    "Event",
                    "Image",
                    "Instrument",
                    "InteractiveResource",
                    "Journal",
                    "JournalArticle",
                    "Model",
                    "OutputManagementPlan",
                    "PeerReview",
                    "PhysicalObject",
                    "Preprint",
                    "Report",
                    "Service",
                    "Software",
                    "Sound",
                    "Standard",
                    "StudyRegistration",
                    "Text",
                    "Workflow",
                    "Other",
                ]
            )
        ]
    )

    schemeType = ma_fields.String()

    schemeURI = ma_fields.String()

    titles = ma_fields.List(
        ma_fields.Nested(lambda: RelatedItemTitleSchema()), required=True
    )

    volume = ma_fields.String()


class ContributorSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliation = ma_fields.List(ma_fields.Nested(lambda: AffiliationSchema()))

    contributorType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "ContactPerson",
                    "DataCollector",
                    "DataCurator",
                    "DataManager",
                    "Distributor",
                    "Editor",
                    "HostingInstitution",
                    "Producer",
                    "ProjectLeader",
                    "ProjectManager",
                    "ProjectMember",
                    "RegistrationAgency",
                    "RegistrationAuthority",
                    "RelatedPerson",
                    "Researcher",
                    "ResearchGroup",
                    "RightsHolder",
                    "Sponsor",
                    "Supervisor",
                    "WorkPackageLeader",
                    "Other",
                ]
            )
        ],
    )

    familyName = ma_fields.String()

    givenName = ma_fields.String()

    lang = ma_fields.String()

    name = ma_fields.String(required=True)

    nameIdentifiers = ma_fields.List(ma_fields.Nested(lambda: NameIdentifierSchema()))

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])


class CreatorSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliation = ma_fields.List(ma_fields.Nested(lambda: AffiliationSchema()))

    familyName = ma_fields.String()

    givenName = ma_fields.String()

    lang = ma_fields.String()

    name = ma_fields.String(required=True)

    nameIdentifiers = ma_fields.List(ma_fields.Nested(lambda: NameIdentifierSchema()))

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])


class GeoLocationPolygonSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    inPolygonPoint = ma_fields.Nested(lambda: GeoLocationPointSchema())

    polygonPoints = ma_fields.List(
        ma_fields.Nested(lambda: GeoLocationPointSchema()), required=True
    )


class AffiliationSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    affiliationIdentifier = ma_fields.String()

    affiliationIdentifierScheme = ma_fields.String()

    name = ma_fields.String(required=True)

    schemeURI = ma_fields.String()


class AlternateIdentifierSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    alternateIdentifier = ma_fields.String(required=True)

    alternateIdentifierType = ma_fields.String(required=True)


class ContainerSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    firstPage = ma_fields.String()

    title = ma_fields.String()

    type = ma_fields.String()


class DateSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    date = TrimmedString(
        required=True, validate=[CachedMultilayerEDTFValidator(types=(EDTFDate,))]
    )

    dateInformation = ma_fields.String()

    dateType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "Accepted",
                    "Available",
                    "Copyrighted",
                    "Collected",
                    "Created",
                    "Issued",
                    "Submitted",
                    "Updated",
                    "Valid",
                    "Withdrawn",
                    "Other",
                ]
            )
        ],
    )


class DescriptionSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    description = ma_fields.String(required=True)

    descriptionType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "Abstract",
                    "Methods",
                    "SeriesInformation",
                    "TableOfContents",
                    "TechnicalInfo",
                    "Other",
                ]
            )
        ],
    )

    lang = ma_fields.String()


class FundingReferenceSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    awardNumber = ma_fields.String()

    awardTitle = ma_fields.String()

    awardURI = ma_fields.String()

    funderIdentifier = ma_fields.String()

    funderIdentifierType = ma_fields.String(
        validate=[OneOf(["ISNI", "GRID", "Crossref Funder ID", "ROR", "Other"])]
    )

    funderName = ma_fields.String(required=True)


class GeoLocationBoxSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    eastBoundLongitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-180.0, max=180.0)]
    )

    northBoundLatitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-90.0, max=90.0)]
    )

    southBoundLatitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-90.0, max=90.0)]
    )

    westBoundLongitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-180.0, max=180.0)]
    )


class GeoLocationPointSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    pointLatitude = ma_fields.Float(validate=[ma.validate.Range(min=-90.0, max=90.0)])

    pointLongitude = ma_fields.Float(
        validate=[ma.validate.Range(min=-180.0, max=180.0)]
    )


class NameIdentifierSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    nameIdentifier = ma_fields.String(required=True)

    nameIdentifierScheme = ma_fields.String(required=True)

    schemeURI = ma_fields.String()


class PublisherSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    lang = ma_fields.String()

    name = ma_fields.String(required=True)

    publisherIdentifier = ma_fields.String()

    publisherIdentifierScheme = ma_fields.String()

    schemeURI = ma_fields.String()


class RelatedIdentifierSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    relatedIdentifier = ma_fields.String()

    relatedIdentifierType = ma_fields.String(
        validate=[
            OneOf(
                [
                    "ARK",
                    "arXiv",
                    "bibcode",
                    "DOI",
                    "EAN13",
                    "EISSN",
                    "Handle",
                    "IGSN",
                    "ISBN",
                    "ISSN",
                    "ISTC",
                    "LISSN",
                    "LSID",
                    "PMID",
                    "PURL",
                    "UPC",
                    "URL",
                    "URN",
                    "w3id",
                ]
            )
        ]
    )

    relatedMetadataScheme = ma_fields.String()

    relationType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "IsCitedBy",
                    "Cites",
                    "IsCollectedBy",
                    "Collects",
                    "IsSupplementTo",
                    "IsSupplementedBy",
                    "IsContinuedBy",
                    "Continues",
                    "IsDescribedBy",
                    "Describes",
                    "HasMetadata",
                    "IsMetadataFor",
                    "HasVersion",
                    "IsVersionOf",
                    "IsNewVersionOf",
                    "IsPartOf",
                    "IsPreviousVersionOf",
                    "IsPublishedIn",
                    "HasPart",
                    "IsReferencedBy",
                    "References",
                    "IsDocumentedBy",
                    "Documents",
                    "IsCompiledBy",
                    "Compiles",
                    "IsVariantFormOf",
                    "IsOriginalFormOf",
                    "IsIdenticalTo",
                    "IsReviewedBy",
                    "Reviews",
                    "IsDerivedFrom",
                    "IsSourceOf",
                    "IsRequiredBy",
                    "Requires",
                    "IsObsoletedBy",
                    "Obsoletes",
                ]
            )
        ],
    )

    resourceTypeGeneral = ma_fields.String(
        validate=[
            OneOf(
                [
                    "Audiovisual",
                    "Book",
                    "BookChapter",
                    "Collection",
                    "ComputationalNotebook",
                    "ConferencePaper",
                    "ConferenceProceeding",
                    "DataPaper",
                    "Dataset",
                    "Dissertation",
                    "Event",
                    "Image",
                    "Instrument",
                    "InteractiveResource",
                    "Journal",
                    "JournalArticle",
                    "Model",
                    "OutputManagementPlan",
                    "PeerReview",
                    "PhysicalObject",
                    "Preprint",
                    "Report",
                    "Service",
                    "Software",
                    "Sound",
                    "Standard",
                    "StudyRegistration",
                    "Text",
                    "Workflow",
                    "Other",
                ]
            )
        ]
    )

    schemeType = ma_fields.String()

    schemeURI = ma_fields.String()


class RelatedItemIdentifierSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    relatedItemIdentifier = ma_fields.String(required=True)

    relatedItemIdentifierType = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "ARK",
                    "arXiv",
                    "bibcode",
                    "DOI",
                    "EAN13",
                    "EISSN",
                    "Handle",
                    "IGSN",
                    "ISBN",
                    "ISSN",
                    "ISTC",
                    "LISSN",
                    "LSID",
                    "PMID",
                    "PURL",
                    "UPC",
                    "URL",
                    "URN",
                    "w3id",
                ]
            )
        ],
    )


class RelatedItemTitleSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    lang = ma_fields.String()

    title = ma_fields.String(required=True)

    titleType = ma_fields.String(
        validate=[OneOf(["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"])]
    )


class ResourceTypeSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    resourceType = ma_fields.String()

    resourceTypeGeneral = ma_fields.String(
        required=True,
        validate=[
            OneOf(
                [
                    "Audiovisual",
                    "Book",
                    "BookChapter",
                    "Collection",
                    "ComputationalNotebook",
                    "ConferencePaper",
                    "ConferenceProceeding",
                    "DataPaper",
                    "Dataset",
                    "Dissertation",
                    "Event",
                    "Image",
                    "Instrument",
                    "InteractiveResource",
                    "Journal",
                    "JournalArticle",
                    "Model",
                    "OutputManagementPlan",
                    "PeerReview",
                    "PhysicalObject",
                    "Preprint",
                    "Report",
                    "Service",
                    "Software",
                    "Sound",
                    "Standard",
                    "StudyRegistration",
                    "Text",
                    "Workflow",
                    "Other",
                ]
            )
        ],
    )


class RightsSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    lang = ma_fields.String()

    rights = ma_fields.String()

    rightsIdentifier = ma_fields.String()

    rightsIdentifierScheme = ma_fields.String()

    rightsURI = ma_fields.String()

    schemeURI = ma_fields.String()


class SubjectSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    classificationCode = ma_fields.String()

    lang = ma_fields.String()

    schemeURI = ma_fields.String()

    subject = ma_fields.String(required=True)

    subjectScheme = ma_fields.String()

    valueURI = ma_fields.String()


class TitleSchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    lang = ma_fields.String()

    title = ma_fields.String(required=True)

    titleType = ma_fields.String(
        validate=[OneOf(["AlternativeTitle", "Subtitle", "TranslatedTitle", "Other"])]
    )
