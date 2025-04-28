"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_runtime.services.facets.date import DateTimeFacet
from oarepo_runtime.services.facets.nested_facet import NestedLabeledFacet
from oarepo_vocabularies.services.facets import VocabularyFacet

access_embargo_active = TermsFacet(
    field="access.embargo.active", label=_("access/embargo/active.label")
)

access_embargo_until = DateTimeFacet(
    field="access.embargo.until", label=_("access/embargo/until.label")
)

access_files = TermsFacet(field="access.files", label=_("access/files.label"))

access_record = TermsFacet(field="access.record", label=_("access/record.label"))

access_status = TermsFacet(field="access.status", label=_("access/status.label"))

metadata_alternate_titles_iri = TermsFacet(
    field="metadata.alternate_titles.iri",
    label=_("metadata/alternate_titles/iri.label"),
)

metadata_alternate_titles_title_cs = TermsFacet(
    field="metadata.alternate_titles.title.cs.keyword",
    label=_("metadata/alternate_titles/title.label"),
)

metadata_alternate_titles_title_en = TermsFacet(
    field="metadata.alternate_titles.title.en.keyword",
    label=_("metadata/alternate_titles/title.label"),
)

metadata_alternate_titles_title_lang = NestedLabeledFacet(
    path="metadata.alternate_titles.title",
    nested_facet=TermsFacet(
        field="metadata.alternate_titles.title.lang",
        label=_("metadata/alternate_titles/title/lang.label"),
    ),
)

metadata_alternate_titles_type = TermsFacet(
    field="metadata.alternate_titles.type",
    label=_("metadata/alternate_titles/type.label"),
)

metadata_descriptions_cs = TermsFacet(
    field="metadata.descriptions.cs.keyword", label=_("metadata/descriptions.label")
)

metadata_descriptions_en = TermsFacet(
    field="metadata.descriptions.en.keyword", label=_("metadata/descriptions.label")
)

metadata_descriptions_lang = NestedLabeledFacet(
    path="metadata.descriptions",
    nested_facet=TermsFacet(
        field="metadata.descriptions.lang", label=_("metadata/descriptions/lang.label")
    ),
)

metadata_distribution_data_services_access_services_endpoint_urls = TermsFacet(
    field="metadata.distribution_data_services.access_services.endpoint_urls",
    label=_("metadata/distribution_data_services/access_services/endpoint_urls.label"),
)

metadata_distribution_data_services_access_services_iri = TermsFacet(
    field="metadata.distribution_data_services.access_services.iri",
    label=_("metadata/distribution_data_services/access_services/iri.label"),
)

metadata_distribution_data_services_access_services_labels_cs = TermsFacet(
    field="metadata.distribution_data_services.access_services.labels.cs.keyword",
    label=_("metadata/distribution_data_services/access_services/labels.label"),
)

metadata_distribution_data_services_access_services_labels_en = TermsFacet(
    field="metadata.distribution_data_services.access_services.labels.en.keyword",
    label=_("metadata/distribution_data_services/access_services/labels.label"),
)

metadata_distribution_data_services_access_services_labels_lang = NestedLabeledFacet(
    path="metadata.distribution_data_services.access_services.labels",
    nested_facet=TermsFacet(
        field="metadata.distribution_data_services.access_services.labels.lang",
        label=_(
            "metadata/distribution_data_services/access_services/labels/lang.label"
        ),
    ),
)

metadata_distribution_data_services_descriptions_cs = TermsFacet(
    field="metadata.distribution_data_services.descriptions.cs.keyword",
    label=_("metadata/distribution_data_services/descriptions.label"),
)

metadata_distribution_data_services_descriptions_en = TermsFacet(
    field="metadata.distribution_data_services.descriptions.en.keyword",
    label=_("metadata/distribution_data_services/descriptions.label"),
)

metadata_distribution_data_services_descriptions_lang = NestedLabeledFacet(
    path="metadata.distribution_data_services.descriptions",
    nested_facet=TermsFacet(
        field="metadata.distribution_data_services.descriptions.lang",
        label=_("metadata/distribution_data_services/descriptions/lang.label"),
    ),
)

metadata_distribution_data_services_documentations_iri = TermsFacet(
    field="metadata.distribution_data_services.documentations.iri",
    label=_("metadata/distribution_data_services/documentations/iri.label"),
)

metadata_distribution_data_services_documentations_labels_cs = TermsFacet(
    field="metadata.distribution_data_services.documentations.labels.cs.keyword",
    label=_("metadata/distribution_data_services/documentations/labels.label"),
)

metadata_distribution_data_services_documentations_labels_en = TermsFacet(
    field="metadata.distribution_data_services.documentations.labels.en.keyword",
    label=_("metadata/distribution_data_services/documentations/labels.label"),
)

metadata_distribution_data_services_documentations_labels_lang = NestedLabeledFacet(
    path="metadata.distribution_data_services.documentations.labels",
    nested_facet=TermsFacet(
        field="metadata.distribution_data_services.documentations.labels.lang",
        label=_("metadata/distribution_data_services/documentations/labels/lang.label"),
    ),
)

metadata_distribution_data_services_iri = TermsFacet(
    field="metadata.distribution_data_services.iri",
    label=_("metadata/distribution_data_services/iri.label"),
)

metadata_distribution_data_services_specifications_iri = TermsFacet(
    field="metadata.distribution_data_services.specifications.iri",
    label=_("metadata/distribution_data_services/specifications/iri.label"),
)

metadata_distribution_data_services_specifications_labels_cs = TermsFacet(
    field="metadata.distribution_data_services.specifications.labels.cs.keyword",
    label=_("metadata/distribution_data_services/specifications/labels.label"),
)

metadata_distribution_data_services_specifications_labels_en = TermsFacet(
    field="metadata.distribution_data_services.specifications.labels.en.keyword",
    label=_("metadata/distribution_data_services/specifications/labels.label"),
)

metadata_distribution_data_services_specifications_labels_lang = NestedLabeledFacet(
    path="metadata.distribution_data_services.specifications.labels",
    nested_facet=TermsFacet(
        field="metadata.distribution_data_services.specifications.labels.lang",
        label=_("metadata/distribution_data_services/specifications/labels/lang.label"),
    ),
)

metadata_distribution_data_services_title = TermsFacet(
    field="metadata.distribution_data_services.title",
    label=_("metadata/distribution_data_services/title.label"),
)

metadata_distribution_downloadable_files_access_urls = TermsFacet(
    field="metadata.distribution_downloadable_files.access_urls",
    label=_("metadata/distribution_downloadable_files/access_urls.label"),
)

metadata_distribution_downloadable_files_byte_size = TermsFacet(
    field="metadata.distribution_downloadable_files.byte_size",
    label=_("metadata/distribution_downloadable_files/byte_size.label"),
)

metadata_distribution_downloadable_files_checksum = TermsFacet(
    field="metadata.distribution_downloadable_files.checksum",
    label=_("metadata/distribution_downloadable_files/checksum.label"),
)

metadata_distribution_downloadable_files_conforms_to_schemas_iri = TermsFacet(
    field="metadata.distribution_downloadable_files.conforms_to_schemas.iri",
    label=_("metadata/distribution_downloadable_files/conforms_to_schemas/iri.label"),
)

metadata_distribution_downloadable_files_conforms_to_schemas_labels_cs = TermsFacet(
    field="metadata.distribution_downloadable_files.conforms_to_schemas.labels.cs.keyword",
    label=_(
        "metadata/distribution_downloadable_files/conforms_to_schemas/labels.label"
    ),
)

metadata_distribution_downloadable_files_conforms_to_schemas_labels_en = TermsFacet(
    field="metadata.distribution_downloadable_files.conforms_to_schemas.labels.en.keyword",
    label=_(
        "metadata/distribution_downloadable_files/conforms_to_schemas/labels.label"
    ),
)

metadata_distribution_downloadable_files_conforms_to_schemas_labels_lang = NestedLabeledFacet(
    path="metadata.distribution_downloadable_files.conforms_to_schemas.labels",
    nested_facet=TermsFacet(
        field="metadata.distribution_downloadable_files.conforms_to_schemas.labels.lang",
        label=_(
            "metadata/distribution_downloadable_files/conforms_to_schemas/labels/lang.label"
        ),
    ),
)

metadata_distribution_downloadable_files_download_urls = TermsFacet(
    field="metadata.distribution_downloadable_files.download_urls",
    label=_("metadata/distribution_downloadable_files/download_urls.label"),
)

metadata_distribution_downloadable_files_format = VocabularyFacet(
    field="metadata.distribution_downloadable_files.format",
    label=_("metadata/distribution_downloadable_files/format.label"),
    vocabulary="file-types",
)

metadata_distribution_downloadable_files_iri = TermsFacet(
    field="metadata.distribution_downloadable_files.iri",
    label=_("metadata/distribution_downloadable_files/iri.label"),
)

metadata_distribution_downloadable_files_media_type_iri = TermsFacet(
    field="metadata.distribution_downloadable_files.media_type.iri",
    label=_("metadata/distribution_downloadable_files/media_type/iri.label"),
)

metadata_distribution_downloadable_files_media_type_labels_cs = TermsFacet(
    field="metadata.distribution_downloadable_files.media_type.labels.cs.keyword",
    label=_("metadata/distribution_downloadable_files/media_type/labels.label"),
)

metadata_distribution_downloadable_files_media_type_labels_en = TermsFacet(
    field="metadata.distribution_downloadable_files.media_type.labels.en.keyword",
    label=_("metadata/distribution_downloadable_files/media_type/labels.label"),
)

metadata_distribution_downloadable_files_media_type_labels_lang = NestedLabeledFacet(
    path="metadata.distribution_downloadable_files.media_type.labels",
    nested_facet=TermsFacet(
        field="metadata.distribution_downloadable_files.media_type.labels.lang",
        label=_(
            "metadata/distribution_downloadable_files/media_type/labels/lang.label"
        ),
    ),
)

metadata_distribution_downloadable_files_title = TermsFacet(
    field="metadata.distribution_downloadable_files.title",
    label=_("metadata/distribution_downloadable_files/title.label"),
)

metadata_funding_references_award_title = TermsFacet(
    field="metadata.funding_references.award_title",
    label=_("metadata/funding_references/award_title.label"),
)

metadata_funding_references_funders_funder_identifier_scheme_uri = TermsFacet(
    field="metadata.funding_references.funders.funder_identifier_scheme_uri",
    label=_("metadata/funding_references/funders/funder_identifier_scheme_uri.label"),
)

metadata_funding_references_funders_funder_identifier_type = TermsFacet(
    field="metadata.funding_references.funders.funder_identifier_type",
    label=_("metadata/funding_references/funders/funder_identifier_type.label"),
)

metadata_funding_references_funders_funder_identifier_value = TermsFacet(
    field="metadata.funding_references.funders.funder_identifier_value",
    label=_("metadata/funding_references/funders/funder_identifier_value.label"),
)

metadata_funding_references_funders_funder_name = TermsFacet(
    field="metadata.funding_references.funders.funder_name",
    label=_("metadata/funding_references/funders/funder_name.label"),
)

metadata_funding_references_funders_iri = TermsFacet(
    field="metadata.funding_references.funders.iri",
    label=_("metadata/funding_references/funders/iri.label"),
)

metadata_funding_references_funding_program = TermsFacet(
    field="metadata.funding_references.funding_program",
    label=_("metadata/funding_references/funding_program.label"),
)

metadata_funding_references_iri = TermsFacet(
    field="metadata.funding_references.iri",
    label=_("metadata/funding_references/iri.label"),
)

metadata_funding_references_local_identifier = TermsFacet(
    field="metadata.funding_references.local_identifier",
    label=_("metadata/funding_references/local_identifier.label"),
)

metadata_identifiers_identifier_scheme = TermsFacet(
    field="metadata.identifiers.identifier_scheme",
    label=_("metadata/identifiers/identifier_scheme.label"),
)

metadata_identifiers_iri = TermsFacet(
    field="metadata.identifiers.iri", label=_("metadata/identifiers/iri.label")
)

metadata_identifiers_value = TermsFacet(
    field="metadata.identifiers.value", label=_("metadata/identifiers/value.label")
)

metadata_iri = TermsFacet(field="metadata.iri", label=_("metadata/iri.label"))

metadata_is_described_by_conforms_to_standards_iri = TermsFacet(
    field="metadata.is_described_by.conforms_to_standards.iri",
    label=_("metadata/is_described_by/conforms_to_standards/iri.label"),
)

metadata_is_described_by_conforms_to_standards_labels_cs = TermsFacet(
    field="metadata.is_described_by.conforms_to_standards.labels.cs.keyword",
    label=_("metadata/is_described_by/conforms_to_standards/labels.label"),
)

metadata_is_described_by_conforms_to_standards_labels_en = TermsFacet(
    field="metadata.is_described_by.conforms_to_standards.labels.en.keyword",
    label=_("metadata/is_described_by/conforms_to_standards/labels.label"),
)

metadata_is_described_by_conforms_to_standards_labels_lang = NestedLabeledFacet(
    path="metadata.is_described_by.conforms_to_standards.labels",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.conforms_to_standards.labels.lang",
        label=_("metadata/is_described_by/conforms_to_standards/labels/lang.label"),
    ),
)

metadata_is_described_by_date_created = DateTimeFacet(
    field="metadata.is_described_by.date_created",
    label=_("metadata/is_described_by/date_created.label"),
)

metadata_is_described_by_dates_updated = DateTimeFacet(
    field="metadata.is_described_by.dates_updated",
    label=_("metadata/is_described_by/dates_updated.label"),
)

metadata_is_described_by_iri = TermsFacet(
    field="metadata.is_described_by.iri", label=_("metadata/is_described_by/iri.label")
)

metadata_is_described_by_languages = VocabularyFacet(
    field="metadata.is_described_by.languages",
    label=_("metadata/is_described_by/languages.label"),
    vocabulary="languages",
)

metadata_is_described_by_original_repositories_iri = TermsFacet(
    field="metadata.is_described_by.original_repositories.iri",
    label=_("metadata/is_described_by/original_repositories/iri.label"),
)

metadata_is_described_by_original_repositories_labels_cs = TermsFacet(
    field="metadata.is_described_by.original_repositories.labels.cs.keyword",
    label=_("metadata/is_described_by/original_repositories/labels.label"),
)

metadata_is_described_by_original_repositories_labels_en = TermsFacet(
    field="metadata.is_described_by.original_repositories.labels.en.keyword",
    label=_("metadata/is_described_by/original_repositories/labels.label"),
)

metadata_is_described_by_original_repositories_labels_lang = NestedLabeledFacet(
    path="metadata.is_described_by.original_repositories.labels",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.original_repositories.labels.lang",
        label=_("metadata/is_described_by/original_repositories/labels/lang.label"),
    ),
)

metadata_is_described_by_qualified_relations_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.iri",
    label=_("metadata/is_described_by/qualified_relations/iri.label"),
)

metadata_is_described_by_qualified_relations_organization_alternate_names_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.alternate_names.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.alternate_names.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.organization.alternate_names.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.dataBoxes",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/dataBoxes.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_emails = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.emails",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/emails.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_phones = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.phones",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/phones.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_external_identifier_type = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.external_identifier_type",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/external_identifier_type.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_external_identifiers = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.external_identifiers",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/external_identifiers.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.iri",
    label=_("metadata/is_described_by/qualified_relations/organization/iri.label"),
)

metadata_is_described_by_qualified_relations_organization_name_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.name.cs.keyword",
    label=_("metadata/is_described_by/qualified_relations/organization/name.label"),
)

metadata_is_described_by_qualified_relations_organization_name_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.name.en.keyword",
    label=_("metadata/is_described_by/qualified_relations/organization/name.label"),
)

metadata_is_described_by_qualified_relations_organization_name_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.organization.name",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.organization.name.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/organization/name/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.emails",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/emails.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.phones",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/phones.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_external_identifier_type = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.external_identifier_type",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/external_identifier_type.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_external_identifiers = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.external_identifiers",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/external_identifiers.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_name_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.name.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_name_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.name.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_name_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.person.affiliations.name",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.person.affiliations.name.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/person/affiliations/name/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.dataBoxes",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/dataBoxes.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_emails = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.emails",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/emails.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_phones = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.phones",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/phones.label"
    ),
)

metadata_is_described_by_qualified_relations_person_external_identifier_type = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.external_identifier_type",
    label=_(
        "metadata/is_described_by/qualified_relations/person/external_identifier_type.label"
    ),
)

metadata_is_described_by_qualified_relations_person_external_identifiers = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.external_identifiers",
    label=_(
        "metadata/is_described_by/qualified_relations/person/external_identifiers.label"
    ),
)

metadata_is_described_by_qualified_relations_person_family_name = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.family_name",
    label=_("metadata/is_described_by/qualified_relations/person/family_name.label"),
)

metadata_is_described_by_qualified_relations_person_given_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.given_names",
    label=_("metadata/is_described_by/qualified_relations/person/given_names.label"),
)

metadata_is_described_by_qualified_relations_person_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.iri",
    label=_("metadata/is_described_by/qualified_relations/person/iri.label"),
)

metadata_is_described_by_qualified_relations_role = VocabularyFacet(
    field="metadata.is_described_by.qualified_relations.role",
    label=_("metadata/is_described_by/qualified_relations/role.label"),
    vocabulary="contributor-types",
)

metadata_locations_bbox_LowerCorners = TermsFacet(
    field="metadata.locations.bbox.LowerCorners",
    label=_("metadata/locations/bbox/LowerCorners.label"),
)

metadata_locations_bbox_UpperCorners = TermsFacet(
    field="metadata.locations.bbox.UpperCorners",
    label=_("metadata/locations/bbox/UpperCorners.label"),
)

metadata_locations_bbox_crs = TermsFacet(
    field="metadata.locations.bbox.crs", label=_("metadata/locations/bbox/crs.label")
)

metadata_locations_bbox_dimensions = TermsFacet(
    field="metadata.locations.bbox.dimensions",
    label=_("metadata/locations/bbox/dimensions.label"),
)

metadata_locations_dataset_relations = TermsFacet(
    field="metadata.locations.dataset_relations",
    label=_("metadata/locations/dataset_relations.label"),
)

metadata_locations_geometry_iri = TermsFacet(
    field="metadata.locations.geometry.iri",
    label=_("metadata/locations/geometry/iri.label"),
)

metadata_locations_geometry_labels_cs = TermsFacet(
    field="metadata.locations.geometry.labels.cs.keyword",
    label=_("metadata/locations/geometry/labels.label"),
)

metadata_locations_geometry_labels_en = TermsFacet(
    field="metadata.locations.geometry.labels.en.keyword",
    label=_("metadata/locations/geometry/labels.label"),
)

metadata_locations_geometry_labels_lang = NestedLabeledFacet(
    path="metadata.locations.geometry.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.geometry.labels.lang",
        label=_("metadata/locations/geometry/labels/lang.label"),
    ),
)

metadata_locations_iri = TermsFacet(
    field="metadata.locations.iri", label=_("metadata/locations/iri.label")
)

metadata_locations_location_names = TermsFacet(
    field="metadata.locations.location_names",
    label=_("metadata/locations/location_names.label"),
)

metadata_locations_related_object_identifiers_identifier_identifier_scheme = TermsFacet(
    field="metadata.locations.related_object_identifiers.identifier.identifier_scheme",
    label=_(
        "metadata/locations/related_object_identifiers/identifier/identifier_scheme.label"
    ),
)

metadata_locations_related_object_identifiers_identifier_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.identifier.iri",
    label=_("metadata/locations/related_object_identifiers/identifier/iri.label"),
)

metadata_locations_related_object_identifiers_identifier_value = TermsFacet(
    field="metadata.locations.related_object_identifiers.identifier.value",
    label=_("metadata/locations/related_object_identifiers/identifier/value.label"),
)

metadata_locations_related_object_identifiers_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.iri",
    label=_("metadata/locations/related_object_identifiers/iri.label"),
)

metadata_locations_related_object_identifiers_qualified_relations_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.alternate_names.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.alternate_names.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.organization.alternate_names.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_emails = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.emails",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/emails.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_phones = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.contact_points.phones",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/phones.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifier_type = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.external_identifier_type",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/external_identifier_type.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifiers = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.external_identifiers",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/external_identifiers.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_name_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.name.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/name.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_name_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.organization.name.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/organization/name.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_organization_name_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.organization.name",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.organization.name.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/organization/name/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.alternate_names.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.alternate_names.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.emails",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/emails.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.contact_points.phones",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/phones.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifier_type = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.external_identifier_type",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/external_identifier_type.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifiers = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.external_identifiers",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/external_identifiers.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.name.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.name.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.name",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.person.affiliations.name.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/name/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_emails = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.emails",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/emails.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_phones = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.contact_points.phones",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/phones.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_external_identifier_type = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.external_identifier_type",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/external_identifier_type.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_external_identifiers = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.external_identifiers",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/external_identifiers.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_family_name = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.family_name",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/family_name.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_given_names = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.given_names",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/given_names.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_person_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.person.iri",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/person/iri.label"
    ),
)

metadata_locations_related_object_identifiers_qualified_relations_role = VocabularyFacet(
    field="metadata.locations.related_object_identifiers.qualified_relations.role",
    label=_(
        "metadata/locations/related_object_identifiers/qualified_relations/role.label"
    ),
    vocabulary="contributor-types",
)

metadata_locations_related_object_identifiers_relation_type = VocabularyFacet(
    field="metadata.locations.related_object_identifiers.relation_type",
    label=_("metadata/locations/related_object_identifiers/relation_type.label"),
    vocabulary="relation-types",
)

metadata_locations_related_object_identifiers_time_references_date = DateTimeFacet(
    field="metadata.locations.related_object_identifiers.time_references.date",
    label=_("metadata/locations/related_object_identifiers/time_references/date.label"),
)

metadata_locations_related_object_identifiers_time_references_date_information = TermsFacet(
    field="metadata.locations.related_object_identifiers.time_references.date_information",
    label=_(
        "metadata/locations/related_object_identifiers/time_references/date_information.label"
    ),
)

metadata_locations_related_object_identifiers_time_references_date_type = VocabularyFacet(
    field="metadata.locations.related_object_identifiers.time_references.date_type",
    label=_(
        "metadata/locations/related_object_identifiers/time_references/date_type.label"
    ),
    vocabulary="time-reference-types",
)

metadata_locations_related_object_identifiers_time_references_iri = TermsFacet(
    field="metadata.locations.related_object_identifiers.time_references.iri",
    label=_("metadata/locations/related_object_identifiers/time_references/iri.label"),
)

metadata_locations_related_object_identifiers_title = TermsFacet(
    field="metadata.locations.related_object_identifiers.title",
    label=_("metadata/locations/related_object_identifiers/title.label"),
)

metadata_locations_related_object_identifiers_type = TermsFacet(
    field="metadata.locations.related_object_identifiers.type",
    label=_("metadata/locations/related_object_identifiers/type.label"),
)

metadata_other_languages = VocabularyFacet(
    field="metadata.other_languages",
    label=_("metadata/other_languages.label"),
    vocabulary="languages",
)

metadata_primary_language = VocabularyFacet(
    field="metadata.primary_language",
    label=_("metadata/primary_language.label"),
    vocabulary="languages",
)

metadata_provenances_iri = TermsFacet(
    field="metadata.provenances.iri", label=_("metadata/provenances/iri.label")
)

metadata_provenances_labels_cs = TermsFacet(
    field="metadata.provenances.labels.cs.keyword",
    label=_("metadata/provenances/labels.label"),
)

metadata_provenances_labels_en = TermsFacet(
    field="metadata.provenances.labels.en.keyword",
    label=_("metadata/provenances/labels.label"),
)

metadata_provenances_labels_lang = NestedLabeledFacet(
    path="metadata.provenances.labels",
    nested_facet=TermsFacet(
        field="metadata.provenances.labels.lang",
        label=_("metadata/provenances/labels/lang.label"),
    ),
)

metadata_publication_year = TermsFacet(
    field="metadata.publication_year", label=_("metadata/publication_year.label")
)

metadata_qualified_relations_iri = TermsFacet(
    field="metadata.qualified_relations.iri",
    label=_("metadata/qualified_relations/iri.label"),
)

metadata_qualified_relations_organization_alternate_names_cs = TermsFacet(
    field="metadata.qualified_relations.organization.alternate_names.cs.keyword",
    label=_("metadata/qualified_relations/organization/alternate_names.label"),
)

metadata_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.qualified_relations.organization.alternate_names.en.keyword",
    label=_("metadata/qualified_relations/organization/alternate_names.label"),
)

metadata_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.organization.alternate_names.lang",
        label=_("metadata/qualified_relations/organization/alternate_names/lang.label"),
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/qualified_relations/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_qualified_relations_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.dataBoxes",
    label=_("metadata/qualified_relations/organization/contact_points/dataBoxes.label"),
)

metadata_qualified_relations_organization_contact_points_emails = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.emails",
    label=_("metadata/qualified_relations/organization/contact_points/emails.label"),
)

metadata_qualified_relations_organization_contact_points_iri = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.iri",
    label=_("metadata/qualified_relations/organization/contact_points/iri.label"),
)

metadata_qualified_relations_organization_contact_points_phones = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.phones",
    label=_("metadata/qualified_relations/organization/contact_points/phones.label"),
)

metadata_qualified_relations_organization_external_identifier_type = TermsFacet(
    field="metadata.qualified_relations.organization.external_identifier_type",
    label=_("metadata/qualified_relations/organization/external_identifier_type.label"),
)

metadata_qualified_relations_organization_external_identifiers = TermsFacet(
    field="metadata.qualified_relations.organization.external_identifiers",
    label=_("metadata/qualified_relations/organization/external_identifiers.label"),
)

metadata_qualified_relations_organization_iri = TermsFacet(
    field="metadata.qualified_relations.organization.iri",
    label=_("metadata/qualified_relations/organization/iri.label"),
)

metadata_qualified_relations_organization_name_cs = TermsFacet(
    field="metadata.qualified_relations.organization.name.cs.keyword",
    label=_("metadata/qualified_relations/organization/name.label"),
)

metadata_qualified_relations_organization_name_en = TermsFacet(
    field="metadata.qualified_relations.organization.name.en.keyword",
    label=_("metadata/qualified_relations/organization/name.label"),
)

metadata_qualified_relations_organization_name_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.organization.name",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.organization.name.lang",
        label=_("metadata/qualified_relations/organization/name/lang.label"),
    ),
)

metadata_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.alternate_names.cs.keyword",
    label=_("metadata/qualified_relations/person/affiliations/alternate_names.label"),
)

metadata_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.alternate_names.en.keyword",
    label=_("metadata/qualified_relations/person/affiliations/alternate_names.label"),
)

metadata_qualified_relations_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/qualified_relations/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.emails",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/emails.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.iri",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/iri.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.phones",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/phones.label"
    ),
)

metadata_qualified_relations_person_affiliations_external_identifier_type = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.external_identifier_type",
    label=_(
        "metadata/qualified_relations/person/affiliations/external_identifier_type.label"
    ),
)

metadata_qualified_relations_person_affiliations_external_identifiers = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.external_identifiers",
    label=_(
        "metadata/qualified_relations/person/affiliations/external_identifiers.label"
    ),
)

metadata_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.iri",
    label=_("metadata/qualified_relations/person/affiliations/iri.label"),
)

metadata_qualified_relations_person_affiliations_name_cs = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.name.cs.keyword",
    label=_("metadata/qualified_relations/person/affiliations/name.label"),
)

metadata_qualified_relations_person_affiliations_name_en = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.name.en.keyword",
    label=_("metadata/qualified_relations/person/affiliations/name.label"),
)

metadata_qualified_relations_person_affiliations_name_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.person.affiliations.name",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.person.affiliations.name.lang",
        label=_("metadata/qualified_relations/person/affiliations/name/lang.label"),
    ),
)

metadata_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.iri",
    label=_("metadata/qualified_relations/person/contact_points/addresses/iri.label"),
)

metadata_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/qualified_relations/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_qualified_relations_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.dataBoxes",
    label=_("metadata/qualified_relations/person/contact_points/dataBoxes.label"),
)

metadata_qualified_relations_person_contact_points_emails = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.emails",
    label=_("metadata/qualified_relations/person/contact_points/emails.label"),
)

metadata_qualified_relations_person_contact_points_iri = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.iri",
    label=_("metadata/qualified_relations/person/contact_points/iri.label"),
)

metadata_qualified_relations_person_contact_points_phones = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.phones",
    label=_("metadata/qualified_relations/person/contact_points/phones.label"),
)

metadata_qualified_relations_person_external_identifier_type = TermsFacet(
    field="metadata.qualified_relations.person.external_identifier_type",
    label=_("metadata/qualified_relations/person/external_identifier_type.label"),
)

metadata_qualified_relations_person_external_identifiers = TermsFacet(
    field="metadata.qualified_relations.person.external_identifiers",
    label=_("metadata/qualified_relations/person/external_identifiers.label"),
)

metadata_qualified_relations_person_family_name = TermsFacet(
    field="metadata.qualified_relations.person.family_name",
    label=_("metadata/qualified_relations/person/family_name.label"),
)

metadata_qualified_relations_person_given_names = TermsFacet(
    field="metadata.qualified_relations.person.given_names",
    label=_("metadata/qualified_relations/person/given_names.label"),
)

metadata_qualified_relations_person_iri = TermsFacet(
    field="metadata.qualified_relations.person.iri",
    label=_("metadata/qualified_relations/person/iri.label"),
)

metadata_qualified_relations_role = VocabularyFacet(
    field="metadata.qualified_relations.role",
    label=_("metadata/qualified_relations/role.label"),
    vocabulary="contributor-types",
)

metadata_related_resources_identifier_identifier_scheme = TermsFacet(
    field="metadata.related_resources.identifier.identifier_scheme",
    label=_("metadata/related_resources/identifier/identifier_scheme.label"),
)

metadata_related_resources_identifier_iri = TermsFacet(
    field="metadata.related_resources.identifier.iri",
    label=_("metadata/related_resources/identifier/iri.label"),
)

metadata_related_resources_identifier_value = TermsFacet(
    field="metadata.related_resources.identifier.value",
    label=_("metadata/related_resources/identifier/value.label"),
)

metadata_related_resources_iri = TermsFacet(
    field="metadata.related_resources.iri",
    label=_("metadata/related_resources/iri.label"),
)

metadata_related_resources_qualified_relations_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.iri",
    label=_("metadata/related_resources/qualified_relations/iri.label"),
)

metadata_related_resources_qualified_relations_organization_alternate_names_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.alternate_names.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.alternate_names.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.organization.alternate_names.lang",
        label=_(
            "metadata/related_resources/qualified_relations/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.dataBoxes",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/dataBoxes.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_emails = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.emails",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/emails.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.iri",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/iri.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_phones = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.phones",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/phones.label"
    ),
)

metadata_related_resources_qualified_relations_organization_external_identifier_type = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.external_identifier_type",
    label=_(
        "metadata/related_resources/qualified_relations/organization/external_identifier_type.label"
    ),
)

metadata_related_resources_qualified_relations_organization_external_identifiers = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.external_identifiers",
    label=_(
        "metadata/related_resources/qualified_relations/organization/external_identifiers.label"
    ),
)

metadata_related_resources_qualified_relations_organization_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.iri",
    label=_("metadata/related_resources/qualified_relations/organization/iri.label"),
)

metadata_related_resources_qualified_relations_organization_name_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.name.cs.keyword",
    label=_("metadata/related_resources/qualified_relations/organization/name.label"),
)

metadata_related_resources_qualified_relations_organization_name_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.name.en.keyword",
    label=_("metadata/related_resources/qualified_relations/organization/name.label"),
)

metadata_related_resources_qualified_relations_organization_name_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.organization.name",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.organization.name.lang",
        label=_(
            "metadata/related_resources/qualified_relations/organization/name/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.alternate_names.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.alternate_names.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/related_resources/qualified_relations/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.emails",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/emails.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.phones",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/phones.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_external_identifier_type = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.external_identifier_type",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/external_identifier_type.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_external_identifiers = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.external_identifiers",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/external_identifiers.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_name_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.name.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_name_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.name.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_name_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.person.affiliations.name",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.person.affiliations.name.lang",
        label=_(
            "metadata/related_resources/qualified_relations/person/affiliations/name/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.dataBoxes",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/dataBoxes.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_emails = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.emails",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/emails.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_phones = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.phones",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/phones.label"
    ),
)

metadata_related_resources_qualified_relations_person_external_identifier_type = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.external_identifier_type",
    label=_(
        "metadata/related_resources/qualified_relations/person/external_identifier_type.label"
    ),
)

metadata_related_resources_qualified_relations_person_external_identifiers = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.external_identifiers",
    label=_(
        "metadata/related_resources/qualified_relations/person/external_identifiers.label"
    ),
)

metadata_related_resources_qualified_relations_person_family_name = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.family_name",
    label=_("metadata/related_resources/qualified_relations/person/family_name.label"),
)

metadata_related_resources_qualified_relations_person_given_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.given_names",
    label=_("metadata/related_resources/qualified_relations/person/given_names.label"),
)

metadata_related_resources_qualified_relations_person_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.iri",
    label=_("metadata/related_resources/qualified_relations/person/iri.label"),
)

metadata_related_resources_qualified_relations_role = VocabularyFacet(
    field="metadata.related_resources.qualified_relations.role",
    label=_("metadata/related_resources/qualified_relations/role.label"),
    vocabulary="contributor-types",
)

metadata_related_resources_relation_type = VocabularyFacet(
    field="metadata.related_resources.relation_type",
    label=_("metadata/related_resources/relation_type.label"),
    vocabulary="relation-types",
)

metadata_related_resources_time_references_date = DateTimeFacet(
    field="metadata.related_resources.time_references.date",
    label=_("metadata/related_resources/time_references/date.label"),
)

metadata_related_resources_time_references_date_information = TermsFacet(
    field="metadata.related_resources.time_references.date_information",
    label=_("metadata/related_resources/time_references/date_information.label"),
)

metadata_related_resources_time_references_date_type = VocabularyFacet(
    field="metadata.related_resources.time_references.date_type",
    label=_("metadata/related_resources/time_references/date_type.label"),
    vocabulary="time-reference-types",
)

metadata_related_resources_time_references_iri = TermsFacet(
    field="metadata.related_resources.time_references.iri",
    label=_("metadata/related_resources/time_references/iri.label"),
)

metadata_related_resources_title = TermsFacet(
    field="metadata.related_resources.title",
    label=_("metadata/related_resources/title.label"),
)

metadata_related_resources_type = TermsFacet(
    field="metadata.related_resources.type",
    label=_("metadata/related_resources/type.label"),
)

metadata_resource_type = VocabularyFacet(
    field="metadata.resource_type",
    label=_("metadata/resource_type.label"),
    vocabulary="resource-types",
)

metadata_subjects_classification_code = TermsFacet(
    field="metadata.subjects.classification_code",
    label=_("metadata/subjects/classification_code.label"),
)

metadata_subjects_definition_cs = TermsFacet(
    field="metadata.subjects.definition.cs.keyword",
    label=_("metadata/subjects/definition.label"),
)

metadata_subjects_definition_en = TermsFacet(
    field="metadata.subjects.definition.en.keyword",
    label=_("metadata/subjects/definition.label"),
)

metadata_subjects_definition_lang = NestedLabeledFacet(
    path="metadata.subjects.definition",
    nested_facet=TermsFacet(
        field="metadata.subjects.definition.lang",
        label=_("metadata/subjects/definition/lang.label"),
    ),
)

metadata_subjects_in_subject_scheme_iri = TermsFacet(
    field="metadata.subjects.in_subject_scheme.iri",
    label=_("metadata/subjects/in_subject_scheme/iri.label"),
)

metadata_subjects_in_subject_scheme_labels_cs = TermsFacet(
    field="metadata.subjects.in_subject_scheme.labels.cs.keyword",
    label=_("metadata/subjects/in_subject_scheme/labels.label"),
)

metadata_subjects_in_subject_scheme_labels_en = TermsFacet(
    field="metadata.subjects.in_subject_scheme.labels.en.keyword",
    label=_("metadata/subjects/in_subject_scheme/labels.label"),
)

metadata_subjects_in_subject_scheme_labels_lang = NestedLabeledFacet(
    path="metadata.subjects.in_subject_scheme.labels",
    nested_facet=TermsFacet(
        field="metadata.subjects.in_subject_scheme.labels.lang",
        label=_("metadata/subjects/in_subject_scheme/labels/lang.label"),
    ),
)

metadata_subjects_iri = TermsFacet(
    field="metadata.subjects.iri", label=_("metadata/subjects/iri.label")
)

metadata_subjects_title_cs = TermsFacet(
    field="metadata.subjects.title.cs.keyword", label=_("metadata/subjects/title.label")
)

metadata_subjects_title_en = TermsFacet(
    field="metadata.subjects.title.en.keyword", label=_("metadata/subjects/title.label")
)

metadata_subjects_title_lang = NestedLabeledFacet(
    path="metadata.subjects.title",
    nested_facet=TermsFacet(
        field="metadata.subjects.title.lang",
        label=_("metadata/subjects/title/lang.label"),
    ),
)

metadata_terms_of_use_access_rights = VocabularyFacet(
    field="metadata.terms_of_use.access_rights",
    label=_("metadata/terms_of_use/access_rights.label"),
    vocabulary="access-rights",
)

metadata_terms_of_use_contacts_organization_alternate_names_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.alternate_names.cs.keyword",
    label=_("metadata/terms_of_use/contacts/organization/alternate_names.label"),
)

metadata_terms_of_use_contacts_organization_alternate_names_en = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.alternate_names.en.keyword",
    label=_("metadata/terms_of_use/contacts/organization/alternate_names.label"),
)

metadata_terms_of_use_contacts_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.organization.alternate_names.lang",
        label=_(
            "metadata/terms_of_use/contacts/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.iri",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/iri.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.dataBoxes",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/dataBoxes.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_emails = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.emails",
    label=_("metadata/terms_of_use/contacts/organization/contact_points/emails.label"),
)

metadata_terms_of_use_contacts_organization_contact_points_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.iri",
    label=_("metadata/terms_of_use/contacts/organization/contact_points/iri.label"),
)

metadata_terms_of_use_contacts_organization_contact_points_phones = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.phones",
    label=_("metadata/terms_of_use/contacts/organization/contact_points/phones.label"),
)

metadata_terms_of_use_contacts_organization_external_identifier_type = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.external_identifier_type",
    label=_(
        "metadata/terms_of_use/contacts/organization/external_identifier_type.label"
    ),
)

metadata_terms_of_use_contacts_organization_external_identifiers = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.external_identifiers",
    label=_("metadata/terms_of_use/contacts/organization/external_identifiers.label"),
)

metadata_terms_of_use_contacts_organization_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.iri",
    label=_("metadata/terms_of_use/contacts/organization/iri.label"),
)

metadata_terms_of_use_contacts_organization_name_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.name.cs.keyword",
    label=_("metadata/terms_of_use/contacts/organization/name.label"),
)

metadata_terms_of_use_contacts_organization_name_en = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.name.en.keyword",
    label=_("metadata/terms_of_use/contacts/organization/name.label"),
)

metadata_terms_of_use_contacts_organization_name_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.organization.name",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.organization.name.lang",
        label=_("metadata/terms_of_use/contacts/organization/name/lang.label"),
    ),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.alternate_names.cs.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/alternate_names.label"),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.alternate_names.en.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/alternate_names.label"),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/terms_of_use/contacts/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.emails",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/emails.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.iri",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/iri.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.phones",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/phones.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_external_identifier_type = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.external_identifier_type",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/external_identifier_type.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_external_identifiers = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.external_identifiers",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/external_identifiers.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.iri",
    label=_("metadata/terms_of_use/contacts/person/affiliations/iri.label"),
)

metadata_terms_of_use_contacts_person_affiliations_name_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.name.cs.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/name.label"),
)

metadata_terms_of_use_contacts_person_affiliations_name_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.name.en.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/name.label"),
)

metadata_terms_of_use_contacts_person_affiliations_name_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.person.affiliations.name",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.person.affiliations.name.lang",
        label=_("metadata/terms_of_use/contacts/person/affiliations/name/lang.label"),
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.iri",
    label=_("metadata/terms_of_use/contacts/person/contact_points/addresses/iri.label"),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.labels.cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.labels.en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.contacts.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.contacts.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/terms_of_use/contacts/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_terms_of_use_contacts_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.dataBoxes",
    label=_("metadata/terms_of_use/contacts/person/contact_points/dataBoxes.label"),
)

metadata_terms_of_use_contacts_person_contact_points_emails = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.emails",
    label=_("metadata/terms_of_use/contacts/person/contact_points/emails.label"),
)

metadata_terms_of_use_contacts_person_contact_points_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.iri",
    label=_("metadata/terms_of_use/contacts/person/contact_points/iri.label"),
)

metadata_terms_of_use_contacts_person_contact_points_phones = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.phones",
    label=_("metadata/terms_of_use/contacts/person/contact_points/phones.label"),
)

metadata_terms_of_use_contacts_person_external_identifier_type = TermsFacet(
    field="metadata.terms_of_use.contacts.person.external_identifier_type",
    label=_("metadata/terms_of_use/contacts/person/external_identifier_type.label"),
)

metadata_terms_of_use_contacts_person_external_identifiers = TermsFacet(
    field="metadata.terms_of_use.contacts.person.external_identifiers",
    label=_("metadata/terms_of_use/contacts/person/external_identifiers.label"),
)

metadata_terms_of_use_contacts_person_family_name = TermsFacet(
    field="metadata.terms_of_use.contacts.person.family_name",
    label=_("metadata/terms_of_use/contacts/person/family_name.label"),
)

metadata_terms_of_use_contacts_person_given_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.given_names",
    label=_("metadata/terms_of_use/contacts/person/given_names.label"),
)

metadata_terms_of_use_contacts_person_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.iri",
    label=_("metadata/terms_of_use/contacts/person/iri.label"),
)

metadata_terms_of_use_description_cs = TermsFacet(
    field="metadata.terms_of_use.description.cs.keyword",
    label=_("metadata/terms_of_use/description.label"),
)

metadata_terms_of_use_description_en = TermsFacet(
    field="metadata.terms_of_use.description.en.keyword",
    label=_("metadata/terms_of_use/description.label"),
)

metadata_terms_of_use_description_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.description",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.description.lang",
        label=_("metadata/terms_of_use/description/lang.label"),
    ),
)

metadata_terms_of_use_iri = TermsFacet(
    field="metadata.terms_of_use.iri", label=_("metadata/terms_of_use/iri.label")
)

metadata_terms_of_use_license = TermsFacet(
    field="metadata.terms_of_use.license",
    label=_("metadata/terms_of_use/license.label"),
)

metadata_time_references_date = DateTimeFacet(
    field="metadata.time_references.date",
    label=_("metadata/time_references/date.label"),
)

metadata_time_references_date_information = TermsFacet(
    field="metadata.time_references.date_information",
    label=_("metadata/time_references/date_information.label"),
)

metadata_time_references_date_type = VocabularyFacet(
    field="metadata.time_references.date_type",
    label=_("metadata/time_references/date_type.label"),
    vocabulary="time-reference-types",
)

metadata_time_references_iri = TermsFacet(
    field="metadata.time_references.iri", label=_("metadata/time_references/iri.label")
)

metadata_title = TermsFacet(field="metadata.title", label=_("metadata/title.label"))

metadata_validation_results_iri = TermsFacet(
    field="metadata.validation_results.iri",
    label=_("metadata/validation_results/iri.label"),
)

metadata_validation_results_labels_cs = TermsFacet(
    field="metadata.validation_results.labels.cs.keyword",
    label=_("metadata/validation_results/labels.label"),
)

metadata_validation_results_labels_en = TermsFacet(
    field="metadata.validation_results.labels.en.keyword",
    label=_("metadata/validation_results/labels.label"),
)

metadata_validation_results_labels_lang = NestedLabeledFacet(
    path="metadata.validation_results.labels",
    nested_facet=TermsFacet(
        field="metadata.validation_results.labels.lang",
        label=_("metadata/validation_results/labels/lang.label"),
    ),
)

metadata_version = TermsFacet(
    field="metadata.version", label=_("metadata/version.label")
)

state = TermsFacet(field="state", label=_("state.label"))

state_timestamp = DateTimeFacet(
    field="state_timestamp", label=_("state_timestamp.label")
)


record_status = TermsFacet(field="record_status", label=_("record_status"))

has_draft = TermsFacet(field="has_draft", label=_("has_draft"))

expires_at = DateTimeFacet(field="expires_at", label=_("expires_at.label"))

fork_version_id = TermsFacet(field="fork_version_id", label=_("fork_version_id.label"))
