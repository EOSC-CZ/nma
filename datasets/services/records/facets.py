"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_runtime.services.facets.date import DateTimeFacet

metadata_alternateIdentifiers_alternateIdentifier = TermsFacet(
    field="metadata.alternateIdentifiers.alternateIdentifier",
    label=_("metadata/alternateIdentifiers/alternateIdentifier.label"),
)

metadata_alternateIdentifiers_alternateIdentifierType = TermsFacet(
    field="metadata.alternateIdentifiers.alternateIdentifierType",
    label=_("metadata/alternateIdentifiers/alternateIdentifierType.label"),
)

metadata_container_firstPage = TermsFacet(
    field="metadata.container.firstPage", label=_("metadata/container/firstPage.label")
)

metadata_container_title = TermsFacet(
    field="metadata.container.title", label=_("metadata/container/title.label")
)

metadata_container_type = TermsFacet(
    field="metadata.container.type", label=_("metadata/container/type.label")
)

metadata_contributors_affiliation_affiliationIdentifier = TermsFacet(
    field="metadata.contributors.affiliation.affiliationIdentifier",
    label=_("metadata/contributors/affiliation/affiliationIdentifier.label"),
)

metadata_contributors_affiliation_affiliationIdentifierScheme = TermsFacet(
    field="metadata.contributors.affiliation.affiliationIdentifierScheme",
    label=_("metadata/contributors/affiliation/affiliationIdentifierScheme.label"),
)

metadata_contributors_affiliation_name = TermsFacet(
    field="metadata.contributors.affiliation.name",
    label=_("metadata/contributors/affiliation/name.label"),
)

metadata_contributors_affiliation_schemeURI = TermsFacet(
    field="metadata.contributors.affiliation.schemeURI",
    label=_("metadata/contributors/affiliation/schemeURI.label"),
)

metadata_contributors_contributorType = TermsFacet(
    field="metadata.contributors.contributorType",
    label=_("metadata/contributors/contributorType.label"),
)

metadata_contributors_familyName = TermsFacet(
    field="metadata.contributors.familyName",
    label=_("metadata/contributors/familyName.label"),
)

metadata_contributors_givenName = TermsFacet(
    field="metadata.contributors.givenName",
    label=_("metadata/contributors/givenName.label"),
)

metadata_contributors_lang = TermsFacet(
    field="metadata.contributors.lang", label=_("metadata/contributors/lang.label")
)

metadata_contributors_name = TermsFacet(
    field="metadata.contributors.name", label=_("metadata/contributors/name.label")
)

metadata_contributors_nameIdentifiers_nameIdentifier = TermsFacet(
    field="metadata.contributors.nameIdentifiers.nameIdentifier",
    label=_("metadata/contributors/nameIdentifiers/nameIdentifier.label"),
)

metadata_contributors_nameIdentifiers_nameIdentifierScheme = TermsFacet(
    field="metadata.contributors.nameIdentifiers.nameIdentifierScheme",
    label=_("metadata/contributors/nameIdentifiers/nameIdentifierScheme.label"),
)

metadata_contributors_nameIdentifiers_schemeURI = TermsFacet(
    field="metadata.contributors.nameIdentifiers.schemeURI",
    label=_("metadata/contributors/nameIdentifiers/schemeURI.label"),
)

metadata_contributors_nameType = TermsFacet(
    field="metadata.contributors.nameType",
    label=_("metadata/contributors/nameType.label"),
)

metadata_creators_affiliation_affiliationIdentifier = TermsFacet(
    field="metadata.creators.affiliation.affiliationIdentifier",
    label=_("metadata/creators/affiliation/affiliationIdentifier.label"),
)

metadata_creators_affiliation_affiliationIdentifierScheme = TermsFacet(
    field="metadata.creators.affiliation.affiliationIdentifierScheme",
    label=_("metadata/creators/affiliation/affiliationIdentifierScheme.label"),
)

metadata_creators_affiliation_name = TermsFacet(
    field="metadata.creators.affiliation.name",
    label=_("metadata/creators/affiliation/name.label"),
)

metadata_creators_affiliation_schemeURI = TermsFacet(
    field="metadata.creators.affiliation.schemeURI",
    label=_("metadata/creators/affiliation/schemeURI.label"),
)

metadata_creators_familyName = TermsFacet(
    field="metadata.creators.familyName", label=_("metadata/creators/familyName.label")
)

metadata_creators_givenName = TermsFacet(
    field="metadata.creators.givenName", label=_("metadata/creators/givenName.label")
)

metadata_creators_lang = TermsFacet(
    field="metadata.creators.lang", label=_("metadata/creators/lang.label")
)

metadata_creators_name = TermsFacet(
    field="metadata.creators.name", label=_("metadata/creators/name.label")
)

metadata_creators_nameIdentifiers_nameIdentifier = TermsFacet(
    field="metadata.creators.nameIdentifiers.nameIdentifier",
    label=_("metadata/creators/nameIdentifiers/nameIdentifier.label"),
)

metadata_creators_nameIdentifiers_nameIdentifierScheme = TermsFacet(
    field="metadata.creators.nameIdentifiers.nameIdentifierScheme",
    label=_("metadata/creators/nameIdentifiers/nameIdentifierScheme.label"),
)

metadata_creators_nameIdentifiers_schemeURI = TermsFacet(
    field="metadata.creators.nameIdentifiers.schemeURI",
    label=_("metadata/creators/nameIdentifiers/schemeURI.label"),
)

metadata_creators_nameType = TermsFacet(
    field="metadata.creators.nameType", label=_("metadata/creators/nameType.label")
)

metadata_dates_date = DateTimeFacet(
    field="metadata.dates.date", label=_("metadata/dates/date.label")
)

metadata_dates_dateInformation = TermsFacet(
    field="metadata.dates.dateInformation",
    label=_("metadata/dates/dateInformation.label"),
)

metadata_dates_dateType = TermsFacet(
    field="metadata.dates.dateType", label=_("metadata/dates/dateType.label")
)

metadata_descriptions_descriptionType = TermsFacet(
    field="metadata.descriptions.descriptionType",
    label=_("metadata/descriptions/descriptionType.label"),
)

metadata_descriptions_lang = TermsFacet(
    field="metadata.descriptions.lang", label=_("metadata/descriptions/lang.label")
)

metadata_doi = TermsFacet(field="metadata.doi", label=_("metadata/doi.label"))

metadata_formats = TermsFacet(
    field="metadata.formats", label=_("metadata/formats.label")
)

metadata_fundingReferences_awardNumber = TermsFacet(
    field="metadata.fundingReferences.awardNumber",
    label=_("metadata/fundingReferences/awardNumber.label"),
)

metadata_fundingReferences_awardTitle = TermsFacet(
    field="metadata.fundingReferences.awardTitle",
    label=_("metadata/fundingReferences/awardTitle.label"),
)

metadata_fundingReferences_awardURI = TermsFacet(
    field="metadata.fundingReferences.awardURI",
    label=_("metadata/fundingReferences/awardURI.label"),
)

metadata_fundingReferences_funderIdentifier = TermsFacet(
    field="metadata.fundingReferences.funderIdentifier",
    label=_("metadata/fundingReferences/funderIdentifier.label"),
)

metadata_fundingReferences_funderIdentifierType = TermsFacet(
    field="metadata.fundingReferences.funderIdentifierType",
    label=_("metadata/fundingReferences/funderIdentifierType.label"),
)

metadata_fundingReferences_funderName = TermsFacet(
    field="metadata.fundingReferences.funderName",
    label=_("metadata/fundingReferences/funderName.label"),
)

metadata_geoLocations_geoLocationBox_eastBoundLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationBox.eastBoundLongitude",
    label=_("metadata/geoLocations/geoLocationBox/eastBoundLongitude.label"),
)

metadata_geoLocations_geoLocationBox_northBoundLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationBox.northBoundLatitude",
    label=_("metadata/geoLocations/geoLocationBox/northBoundLatitude.label"),
)

metadata_geoLocations_geoLocationBox_southBoundLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationBox.southBoundLatitude",
    label=_("metadata/geoLocations/geoLocationBox/southBoundLatitude.label"),
)

metadata_geoLocations_geoLocationBox_westBoundLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationBox.westBoundLongitude",
    label=_("metadata/geoLocations/geoLocationBox/westBoundLongitude.label"),
)

metadata_geoLocations_geoLocationPlace = TermsFacet(
    field="metadata.geoLocations.geoLocationPlace",
    label=_("metadata/geoLocations/geoLocationPlace.label"),
)

metadata_geoLocations_geoLocationPoint_pointLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLatitude",
    label=_("metadata/geoLocations/geoLocationPoint/pointLatitude.label"),
)

metadata_geoLocations_geoLocationPoint_pointLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPoint.pointLongitude",
    label=_("metadata/geoLocations/geoLocationPoint/pointLongitude.label"),
)

metadata_geoLocations_geoLocationPolygons_inPolygonPoint_pointLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPolygons.inPolygonPoint.pointLatitude",
    label=_(
        "metadata/geoLocations/geoLocationPolygons/inPolygonPoint/pointLatitude.label"
    ),
)

metadata_geoLocations_geoLocationPolygons_inPolygonPoint_pointLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPolygons.inPolygonPoint.pointLongitude",
    label=_(
        "metadata/geoLocations/geoLocationPolygons/inPolygonPoint/pointLongitude.label"
    ),
)

metadata_geoLocations_geoLocationPolygons_polygonPoints_pointLatitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPolygons.polygonPoints.pointLatitude",
    label=_(
        "metadata/geoLocations/geoLocationPolygons/polygonPoints/pointLatitude.label"
    ),
)

metadata_geoLocations_geoLocationPolygons_polygonPoints_pointLongitude = TermsFacet(
    field="metadata.geoLocations.geoLocationPolygons.polygonPoints.pointLongitude",
    label=_(
        "metadata/geoLocations/geoLocationPolygons/polygonPoints/pointLongitude.label"
    ),
)

metadata_language = TermsFacet(
    field="metadata.language", label=_("metadata/language.label")
)

metadata_publicationYear = TermsFacet(
    field="metadata.publicationYear", label=_("metadata/publicationYear.label")
)

metadata_publisher_lang = TermsFacet(
    field="metadata.publisher.lang", label=_("metadata/publisher/lang.label")
)

metadata_publisher_name = TermsFacet(
    field="metadata.publisher.name", label=_("metadata/publisher/name.label")
)

metadata_publisher_publisherIdentifier = TermsFacet(
    field="metadata.publisher.publisherIdentifier",
    label=_("metadata/publisher/publisherIdentifier.label"),
)

metadata_publisher_publisherIdentifierScheme = TermsFacet(
    field="metadata.publisher.publisherIdentifierScheme",
    label=_("metadata/publisher/publisherIdentifierScheme.label"),
)

metadata_publisher_schemeURI = TermsFacet(
    field="metadata.publisher.schemeURI", label=_("metadata/publisher/schemeURI.label")
)

metadata_relatedIdentifiers_relatedIdentifier = TermsFacet(
    field="metadata.relatedIdentifiers.relatedIdentifier",
    label=_("metadata/relatedIdentifiers/relatedIdentifier.label"),
)

metadata_relatedIdentifiers_relatedIdentifierType = TermsFacet(
    field="metadata.relatedIdentifiers.relatedIdentifierType",
    label=_("metadata/relatedIdentifiers/relatedIdentifierType.label"),
)

metadata_relatedIdentifiers_relatedMetadataScheme = TermsFacet(
    field="metadata.relatedIdentifiers.relatedMetadataScheme",
    label=_("metadata/relatedIdentifiers/relatedMetadataScheme.label"),
)

metadata_relatedIdentifiers_relationType = TermsFacet(
    field="metadata.relatedIdentifiers.relationType",
    label=_("metadata/relatedIdentifiers/relationType.label"),
)

metadata_relatedIdentifiers_resourceTypeGeneral = TermsFacet(
    field="metadata.relatedIdentifiers.resourceTypeGeneral",
    label=_("metadata/relatedIdentifiers/resourceTypeGeneral.label"),
)

metadata_relatedIdentifiers_schemeType = TermsFacet(
    field="metadata.relatedIdentifiers.schemeType",
    label=_("metadata/relatedIdentifiers/schemeType.label"),
)

metadata_relatedIdentifiers_schemeURI = TermsFacet(
    field="metadata.relatedIdentifiers.schemeURI",
    label=_("metadata/relatedIdentifiers/schemeURI.label"),
)

metadata_relatedItems_contributors_affiliation_affiliationIdentifier = TermsFacet(
    field="metadata.relatedItems.contributors.affiliation.affiliationIdentifier",
    label=_(
        "metadata/relatedItems/contributors/affiliation/affiliationIdentifier.label"
    ),
)

metadata_relatedItems_contributors_affiliation_affiliationIdentifierScheme = TermsFacet(
    field="metadata.relatedItems.contributors.affiliation.affiliationIdentifierScheme",
    label=_(
        "metadata/relatedItems/contributors/affiliation/affiliationIdentifierScheme.label"
    ),
)

metadata_relatedItems_contributors_affiliation_name = TermsFacet(
    field="metadata.relatedItems.contributors.affiliation.name",
    label=_("metadata/relatedItems/contributors/affiliation/name.label"),
)

metadata_relatedItems_contributors_affiliation_schemeURI = TermsFacet(
    field="metadata.relatedItems.contributors.affiliation.schemeURI",
    label=_("metadata/relatedItems/contributors/affiliation/schemeURI.label"),
)

metadata_relatedItems_contributors_contributorType = TermsFacet(
    field="metadata.relatedItems.contributors.contributorType",
    label=_("metadata/relatedItems/contributors/contributorType.label"),
)

metadata_relatedItems_contributors_familyName = TermsFacet(
    field="metadata.relatedItems.contributors.familyName",
    label=_("metadata/relatedItems/contributors/familyName.label"),
)

metadata_relatedItems_contributors_givenName = TermsFacet(
    field="metadata.relatedItems.contributors.givenName",
    label=_("metadata/relatedItems/contributors/givenName.label"),
)

metadata_relatedItems_contributors_lang = TermsFacet(
    field="metadata.relatedItems.contributors.lang",
    label=_("metadata/relatedItems/contributors/lang.label"),
)

metadata_relatedItems_contributors_name = TermsFacet(
    field="metadata.relatedItems.contributors.name",
    label=_("metadata/relatedItems/contributors/name.label"),
)

metadata_relatedItems_contributors_nameIdentifiers_nameIdentifier = TermsFacet(
    field="metadata.relatedItems.contributors.nameIdentifiers.nameIdentifier",
    label=_("metadata/relatedItems/contributors/nameIdentifiers/nameIdentifier.label"),
)

metadata_relatedItems_contributors_nameIdentifiers_nameIdentifierScheme = TermsFacet(
    field="metadata.relatedItems.contributors.nameIdentifiers.nameIdentifierScheme",
    label=_(
        "metadata/relatedItems/contributors/nameIdentifiers/nameIdentifierScheme.label"
    ),
)

metadata_relatedItems_contributors_nameIdentifiers_schemeURI = TermsFacet(
    field="metadata.relatedItems.contributors.nameIdentifiers.schemeURI",
    label=_("metadata/relatedItems/contributors/nameIdentifiers/schemeURI.label"),
)

metadata_relatedItems_contributors_nameType = TermsFacet(
    field="metadata.relatedItems.contributors.nameType",
    label=_("metadata/relatedItems/contributors/nameType.label"),
)

metadata_relatedItems_creators_affiliation_affiliationIdentifier = TermsFacet(
    field="metadata.relatedItems.creators.affiliation.affiliationIdentifier",
    label=_("metadata/relatedItems/creators/affiliation/affiliationIdentifier.label"),
)

metadata_relatedItems_creators_affiliation_affiliationIdentifierScheme = TermsFacet(
    field="metadata.relatedItems.creators.affiliation.affiliationIdentifierScheme",
    label=_(
        "metadata/relatedItems/creators/affiliation/affiliationIdentifierScheme.label"
    ),
)

metadata_relatedItems_creators_affiliation_name = TermsFacet(
    field="metadata.relatedItems.creators.affiliation.name",
    label=_("metadata/relatedItems/creators/affiliation/name.label"),
)

metadata_relatedItems_creators_affiliation_schemeURI = TermsFacet(
    field="metadata.relatedItems.creators.affiliation.schemeURI",
    label=_("metadata/relatedItems/creators/affiliation/schemeURI.label"),
)

metadata_relatedItems_creators_familyName = TermsFacet(
    field="metadata.relatedItems.creators.familyName",
    label=_("metadata/relatedItems/creators/familyName.label"),
)

metadata_relatedItems_creators_givenName = TermsFacet(
    field="metadata.relatedItems.creators.givenName",
    label=_("metadata/relatedItems/creators/givenName.label"),
)

metadata_relatedItems_creators_lang = TermsFacet(
    field="metadata.relatedItems.creators.lang",
    label=_("metadata/relatedItems/creators/lang.label"),
)

metadata_relatedItems_creators_name = TermsFacet(
    field="metadata.relatedItems.creators.name",
    label=_("metadata/relatedItems/creators/name.label"),
)

metadata_relatedItems_creators_nameIdentifiers_nameIdentifier = TermsFacet(
    field="metadata.relatedItems.creators.nameIdentifiers.nameIdentifier",
    label=_("metadata/relatedItems/creators/nameIdentifiers/nameIdentifier.label"),
)

metadata_relatedItems_creators_nameIdentifiers_nameIdentifierScheme = TermsFacet(
    field="metadata.relatedItems.creators.nameIdentifiers.nameIdentifierScheme",
    label=_(
        "metadata/relatedItems/creators/nameIdentifiers/nameIdentifierScheme.label"
    ),
)

metadata_relatedItems_creators_nameIdentifiers_schemeURI = TermsFacet(
    field="metadata.relatedItems.creators.nameIdentifiers.schemeURI",
    label=_("metadata/relatedItems/creators/nameIdentifiers/schemeURI.label"),
)

metadata_relatedItems_creators_nameType = TermsFacet(
    field="metadata.relatedItems.creators.nameType",
    label=_("metadata/relatedItems/creators/nameType.label"),
)

metadata_relatedItems_edition = TermsFacet(
    field="metadata.relatedItems.edition",
    label=_("metadata/relatedItems/edition.label"),
)

metadata_relatedItems_firstPage = TermsFacet(
    field="metadata.relatedItems.firstPage",
    label=_("metadata/relatedItems/firstPage.label"),
)

metadata_relatedItems_issue = TermsFacet(
    field="metadata.relatedItems.issue", label=_("metadata/relatedItems/issue.label")
)

metadata_relatedItems_lastPage = TermsFacet(
    field="metadata.relatedItems.lastPage",
    label=_("metadata/relatedItems/lastPage.label"),
)

metadata_relatedItems_number = TermsFacet(
    field="metadata.relatedItems.number", label=_("metadata/relatedItems/number.label")
)

metadata_relatedItems_numberType = TermsFacet(
    field="metadata.relatedItems.numberType",
    label=_("metadata/relatedItems/numberType.label"),
)

metadata_relatedItems_publicationYear = TermsFacet(
    field="metadata.relatedItems.publicationYear",
    label=_("metadata/relatedItems/publicationYear.label"),
)

metadata_relatedItems_publisher = TermsFacet(
    field="metadata.relatedItems.publisher",
    label=_("metadata/relatedItems/publisher.label"),
)

metadata_relatedItems_relatedItemIdentifier_relatedItemIdentifier = TermsFacet(
    field="metadata.relatedItems.relatedItemIdentifier.relatedItemIdentifier",
    label=_("metadata/relatedItems/relatedItemIdentifier/relatedItemIdentifier.label"),
)

metadata_relatedItems_relatedItemIdentifier_relatedItemIdentifierType = TermsFacet(
    field="metadata.relatedItems.relatedItemIdentifier.relatedItemIdentifierType",
    label=_(
        "metadata/relatedItems/relatedItemIdentifier/relatedItemIdentifierType.label"
    ),
)

metadata_relatedItems_relatedItemType = TermsFacet(
    field="metadata.relatedItems.relatedItemType",
    label=_("metadata/relatedItems/relatedItemType.label"),
)

metadata_relatedItems_relatedMetadataScheme = TermsFacet(
    field="metadata.relatedItems.relatedMetadataScheme",
    label=_("metadata/relatedItems/relatedMetadataScheme.label"),
)

metadata_relatedItems_relationType = TermsFacet(
    field="metadata.relatedItems.relationType",
    label=_("metadata/relatedItems/relationType.label"),
)

metadata_relatedItems_resourceTypeGeneral = TermsFacet(
    field="metadata.relatedItems.resourceTypeGeneral",
    label=_("metadata/relatedItems/resourceTypeGeneral.label"),
)

metadata_relatedItems_schemeType = TermsFacet(
    field="metadata.relatedItems.schemeType",
    label=_("metadata/relatedItems/schemeType.label"),
)

metadata_relatedItems_schemeURI = TermsFacet(
    field="metadata.relatedItems.schemeURI",
    label=_("metadata/relatedItems/schemeURI.label"),
)

metadata_relatedItems_titles_lang = TermsFacet(
    field="metadata.relatedItems.titles.lang",
    label=_("metadata/relatedItems/titles/lang.label"),
)

metadata_relatedItems_titles_titleType = TermsFacet(
    field="metadata.relatedItems.titles.titleType",
    label=_("metadata/relatedItems/titles/titleType.label"),
)

metadata_relatedItems_volume = TermsFacet(
    field="metadata.relatedItems.volume", label=_("metadata/relatedItems/volume.label")
)

metadata_rightsList_lang = TermsFacet(
    field="metadata.rightsList.lang", label=_("metadata/rightsList/lang.label")
)

metadata_rightsList_rights = TermsFacet(
    field="metadata.rightsList.rights", label=_("metadata/rightsList/rights.label")
)

metadata_rightsList_rightsIdentifier = TermsFacet(
    field="metadata.rightsList.rightsIdentifier",
    label=_("metadata/rightsList/rightsIdentifier.label"),
)

metadata_rightsList_rightsIdentifierScheme = TermsFacet(
    field="metadata.rightsList.rightsIdentifierScheme",
    label=_("metadata/rightsList/rightsIdentifierScheme.label"),
)

metadata_rightsList_rightsURI = TermsFacet(
    field="metadata.rightsList.rightsURI",
    label=_("metadata/rightsList/rightsURI.label"),
)

metadata_rightsList_schemeURI = TermsFacet(
    field="metadata.rightsList.schemeURI",
    label=_("metadata/rightsList/schemeURI.label"),
)

metadata_schemaVersion = TermsFacet(
    field="metadata.schemaVersion", label=_("metadata/schemaVersion.label")
)

metadata_sizes = TermsFacet(field="metadata.sizes", label=_("metadata/sizes.label"))

metadata_subjects_classificationCode = TermsFacet(
    field="metadata.subjects.classificationCode",
    label=_("metadata/subjects/classificationCode.label"),
)

metadata_subjects_lang = TermsFacet(
    field="metadata.subjects.lang", label=_("metadata/subjects/lang.label")
)

metadata_subjects_schemeURI = TermsFacet(
    field="metadata.subjects.schemeURI", label=_("metadata/subjects/schemeURI.label")
)

metadata_subjects_subject = TermsFacet(
    field="metadata.subjects.subject", label=_("metadata/subjects/subject.label")
)

metadata_subjects_subjectScheme = TermsFacet(
    field="metadata.subjects.subjectScheme",
    label=_("metadata/subjects/subjectScheme.label"),
)

metadata_subjects_valueURI = TermsFacet(
    field="metadata.subjects.valueURI", label=_("metadata/subjects/valueURI.label")
)

metadata_titles_lang = TermsFacet(
    field="metadata.titles.lang", label=_("metadata/titles/lang.label")
)

metadata_titles_titleType = TermsFacet(
    field="metadata.titles.titleType", label=_("metadata/titles/titleType.label")
)

metadata_types_resourceType = TermsFacet(
    field="metadata.types.resourceType", label=_("metadata/types/resourceType.label")
)

metadata_types_resourceTypeGeneral = TermsFacet(
    field="metadata.types.resourceTypeGeneral",
    label=_("metadata/types/resourceTypeGeneral.label"),
)

metadata_url = TermsFacet(field="metadata.url", label=_("metadata/url.label"))

metadata_version = TermsFacet(
    field="metadata.version", label=_("metadata/version.label")
)
