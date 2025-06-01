"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.i18n import lazy_gettext as _
from oarepo_runtime.services.facets import MultilingualFacet
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
    field="metadata.alternate_titles.title_cs.keyword",
    label=_("metadata/alternate_titles/title.label"),
)

metadata_alternate_titles_title_en = TermsFacet(
    field="metadata.alternate_titles.title_en.keyword",
    label=_("metadata/alternate_titles/title.label"),
)

metadata_alternate_titles_title = MultilingualFacet(
    lang_facets={
        "cs": metadata_alternate_titles_title_cs,
        "en": metadata_alternate_titles_title_en,
    },
    label=_("metadata/alternate_titles/title.label"),
)

metadata_alternate_titles_title_lang = NestedLabeledFacet(
    path="metadata.alternate_titles.title",
    nested_facet=TermsFacet(
        field="metadata.alternate_titles.title.lang",
        label=_("metadata/alternate_titles/title/lang.label"),
    ),
)

metadata_alternate_titles_type = VocabularyFacet(
    field="metadata.alternate_titles.type",
    label=_("metadata/alternate_titles/type.label"),
    vocabulary="title-types",
)

metadata_descriptions_cs = TermsFacet(
    field="metadata.descriptions_cs.keyword", label=_("metadata/descriptions.label")
)

metadata_descriptions_en = TermsFacet(
    field="metadata.descriptions_en.keyword", label=_("metadata/descriptions.label")
)

metadata_descriptions = MultilingualFacet(
    lang_facets={
        "cs": metadata_descriptions_cs,
        "en": metadata_descriptions_en,
    },
    label=_("metadata/descriptions.label"),
)

metadata_descriptions_lang = NestedLabeledFacet(
    path="metadata.descriptions",
    nested_facet=TermsFacet(
        field="metadata.descriptions.lang", label=_("metadata/descriptions/lang.label")
    ),
)

metadata_distributions_access_urls = TermsFacet(
    field="metadata.distributions.access_urls",
    label=_("metadata/distributions/access_urls.label"),
)

metadata_distributions_byte_size = TermsFacet(
    field="metadata.distributions.byte_size",
    label=_("metadata/distributions/byte_size.label"),
)

metadata_distributions_checksum_algorithm = VocabularyFacet(
    field="metadata.distributions.checksum.algorithm",
    label=_("metadata/distributions/checksum/algorithm.label"),
    vocabulary="checksum-algorithms",
)

metadata_distributions_checksum_iri = TermsFacet(
    field="metadata.distributions.checksum.iri",
    label=_("metadata/distributions/checksum/iri.label"),
)

metadata_distributions_checksum_value = TermsFacet(
    field="metadata.distributions.checksum.value",
    label=_("metadata/distributions/checksum/value.label"),
)

metadata_distributions_conforms_to_schemas_iri = TermsFacet(
    field="metadata.distributions.conforms_to_schemas.iri",
    label=_("metadata/distributions/conforms_to_schemas/iri.label"),
)

metadata_distributions_conforms_to_schemas_labels_cs = TermsFacet(
    field="metadata.distributions.conforms_to_schemas.labels_cs.keyword",
    label=_("metadata/distributions/conforms_to_schemas/labels.label"),
)

metadata_distributions_conforms_to_schemas_labels_en = TermsFacet(
    field="metadata.distributions.conforms_to_schemas.labels_en.keyword",
    label=_("metadata/distributions/conforms_to_schemas/labels.label"),
)

metadata_distributions_conforms_to_schemas_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_distributions_conforms_to_schemas_labels_cs,
        "en": metadata_distributions_conforms_to_schemas_labels_en,
    },
    label=_("metadata/distributions/conforms_to_schemas/labels.label"),
)

metadata_distributions_conforms_to_schemas_labels_lang = NestedLabeledFacet(
    path="metadata.distributions.conforms_to_schemas.labels",
    nested_facet=TermsFacet(
        field="metadata.distributions.conforms_to_schemas.labels.lang",
        label=_("metadata/distributions/conforms_to_schemas/labels/lang.label"),
    ),
)

metadata_distributions_download_urls = TermsFacet(
    field="metadata.distributions.download_urls",
    label=_("metadata/distributions/download_urls.label"),
)

metadata_distributions_format = VocabularyFacet(
    field="metadata.distributions.format",
    label=_("metadata/distributions/format.label"),
    vocabulary="file-types",
)

metadata_distributions_iri = TermsFacet(
    field="metadata.distributions.iri", label=_("metadata/distributions/iri.label")
)

metadata_distributions_media_type = VocabularyFacet(
    field="metadata.distributions.media_type",
    label=_("metadata/distributions/media_type.label"),
    vocabulary="media-types",
)

metadata_distributions_title = TermsFacet(
    field="metadata.distributions.title", label=_("metadata/distributions/title.label")
)

metadata_funding_references_award_title = TermsFacet(
    field="metadata.funding_references.award_title",
    label=_("metadata/funding_references/award_title.label"),
)

metadata_funding_references_funders_organization_alternate_names_cs = TermsFacet(
    field="metadata.funding_references.funders.organization.alternate_names_cs.keyword",
    label=_("metadata/funding_references/funders/organization/alternate_names.label"),
)

metadata_funding_references_funders_organization_alternate_names_en = TermsFacet(
    field="metadata.funding_references.funders.organization.alternate_names_en.keyword",
    label=_("metadata/funding_references/funders/organization/alternate_names.label"),
)

metadata_funding_references_funders_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": metadata_funding_references_funders_organization_alternate_names_cs,
        "en": metadata_funding_references_funders_organization_alternate_names_en,
    },
    label=_("metadata/funding_references/funders/organization/alternate_names.label"),
)

metadata_funding_references_funders_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.funding_references.funders.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.funding_references.funders.organization.alternate_names.lang",
        label=_(
            "metadata/funding_references/funders/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.iri",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/iri.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_funding_references_funders_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_funding_references_funders_organization_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.funding_references.funders.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.funding_references.funders.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/funding_references/funders/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.dataBoxes",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/dataBoxes.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_emails = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.emails",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/emails.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_iri = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.iri",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/iri.label"
    ),
)

metadata_funding_references_funders_organization_contact_points_phones = TermsFacet(
    field="metadata.funding_references.funders.organization.contact_points.phones",
    label=_(
        "metadata/funding_references/funders/organization/contact_points/phones.label"
    ),
)

metadata_funding_references_funders_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.funding_references.funders.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/funding_references/funders/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_funding_references_funders_organization_identifiers_iri = TermsFacet(
    field="metadata.funding_references.funders.organization.identifiers.iri",
    label=_("metadata/funding_references/funders/organization/identifiers/iri.label"),
)

metadata_funding_references_funders_organization_identifiers_value = TermsFacet(
    field="metadata.funding_references.funders.organization.identifiers.value",
    label=_("metadata/funding_references/funders/organization/identifiers/value.label"),
)

metadata_funding_references_funders_organization_iri = TermsFacet(
    field="metadata.funding_references.funders.organization.iri",
    label=_("metadata/funding_references/funders/organization/iri.label"),
)

metadata_funding_references_funders_organization_name = TermsFacet(
    field="metadata.funding_references.funders.organization.name",
    label=_("metadata/funding_references/funders/organization/name.label"),
)

metadata_funding_references_funders_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.alternate_names_cs.keyword",
    label=_(
        "metadata/funding_references/funders/person/affiliations/alternate_names.label"
    ),
)

metadata_funding_references_funders_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.alternate_names_en.keyword",
    label=_(
        "metadata/funding_references/funders/person/affiliations/alternate_names.label"
    ),
)

metadata_funding_references_funders_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_funding_references_funders_person_affiliations_alternate_names_cs
        ),
        "en": (
            metadata_funding_references_funders_person_affiliations_alternate_names_en
        ),
    },
    label=_(
        "metadata/funding_references/funders/person/affiliations/alternate_names.label"
    ),
)

metadata_funding_references_funders_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.funding_references.funders.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.funding_references.funders.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/funding_references/funders/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.funding_references.funders.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/funding_references/funders/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.emails",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/emails.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.iri",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/iri.label"
    ),
)

metadata_funding_references_funders_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.contact_points.phones",
    label=_(
        "metadata/funding_references/funders/person/affiliations/contact_points/phones.label"
    ),
)

metadata_funding_references_funders_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.funding_references.funders.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/funding_references/funders/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_funding_references_funders_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.identifiers.iri",
    label=_(
        "metadata/funding_references/funders/person/affiliations/identifiers/iri.label"
    ),
)

metadata_funding_references_funders_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.identifiers.value",
    label=_(
        "metadata/funding_references/funders/person/affiliations/identifiers/value.label"
    ),
)

metadata_funding_references_funders_person_affiliations_iri = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.iri",
    label=_("metadata/funding_references/funders/person/affiliations/iri.label"),
)

metadata_funding_references_funders_person_affiliations_name = TermsFacet(
    field="metadata.funding_references.funders.person.affiliations.name",
    label=_("metadata/funding_references/funders/person/affiliations/name.label"),
)

metadata_funding_references_funders_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.full_address",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/full_address.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.iri",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/iri.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_funding_references_funders_person_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_funding_references_funders_person_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/labels.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.funding_references.funders.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.funding_references.funders.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/funding_references/funders/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.po_box",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/po_box.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.post_code",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/post_code.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.post_names",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/post_names.label"
    ),
)

metadata_funding_references_funders_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/funding_references/funders/person/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_funding_references_funders_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.dataBoxes",
    label=_(
        "metadata/funding_references/funders/person/contact_points/dataBoxes.label"
    ),
)

metadata_funding_references_funders_person_contact_points_emails = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.emails",
    label=_("metadata/funding_references/funders/person/contact_points/emails.label"),
)

metadata_funding_references_funders_person_contact_points_iri = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.iri",
    label=_("metadata/funding_references/funders/person/contact_points/iri.label"),
)

metadata_funding_references_funders_person_contact_points_phones = TermsFacet(
    field="metadata.funding_references.funders.person.contact_points.phones",
    label=_("metadata/funding_references/funders/person/contact_points/phones.label"),
)

metadata_funding_references_funders_person_family_names = TermsFacet(
    field="metadata.funding_references.funders.person.family_names",
    label=_("metadata/funding_references/funders/person/family_names.label"),
)

metadata_funding_references_funders_person_given_names = TermsFacet(
    field="metadata.funding_references.funders.person.given_names",
    label=_("metadata/funding_references/funders/person/given_names.label"),
)

metadata_funding_references_funders_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.funding_references.funders.person.identifiers.identifier_scheme",
    label=_(
        "metadata/funding_references/funders/person/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_funding_references_funders_person_identifiers_iri = TermsFacet(
    field="metadata.funding_references.funders.person.identifiers.iri",
    label=_("metadata/funding_references/funders/person/identifiers/iri.label"),
)

metadata_funding_references_funders_person_identifiers_value = TermsFacet(
    field="metadata.funding_references.funders.person.identifiers.value",
    label=_("metadata/funding_references/funders/person/identifiers/value.label"),
)

metadata_funding_references_funders_person_iri = TermsFacet(
    field="metadata.funding_references.funders.person.iri",
    label=_("metadata/funding_references/funders/person/iri.label"),
)

metadata_funding_references_funders_person_name = TermsFacet(
    field="metadata.funding_references.funders.person.name",
    label=_("metadata/funding_references/funders/person/name.label"),
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

metadata_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.identifiers.identifier_scheme",
    label=_("metadata/identifiers/identifier_scheme.label"),
    vocabulary="identifier-schemes",
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
    field="metadata.is_described_by.conforms_to_standards.labels_cs.keyword",
    label=_("metadata/is_described_by/conforms_to_standards/labels.label"),
)

metadata_is_described_by_conforms_to_standards_labels_en = TermsFacet(
    field="metadata.is_described_by.conforms_to_standards.labels_en.keyword",
    label=_("metadata/is_described_by/conforms_to_standards/labels.label"),
)

metadata_is_described_by_conforms_to_standards_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_is_described_by_conforms_to_standards_labels_cs,
        "en": metadata_is_described_by_conforms_to_standards_labels_en,
    },
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
    field="metadata.is_described_by.original_repositories.labels_cs.keyword",
    label=_("metadata/is_described_by/original_repositories/labels.label"),
)

metadata_is_described_by_original_repositories_labels_en = TermsFacet(
    field="metadata.is_described_by.original_repositories.labels_en.keyword",
    label=_("metadata/is_described_by/original_repositories/labels.label"),
)

metadata_is_described_by_original_repositories_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_is_described_by_original_repositories_labels_cs,
        "en": metadata_is_described_by_original_repositories_labels_en,
    },
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
    field="metadata.is_described_by.qualified_relations.organization.alternate_names_cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.alternate_names_en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_is_described_by_qualified_relations_organization_alternate_names_cs
        ),
        "en": (
            metadata_is_described_by_qualified_relations_organization_alternate_names_en
        ),
    },
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

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en
        ),
    },
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

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/thoroughfares.label"
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

metadata_is_described_by_qualified_relations_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.is_described_by.qualified_relations.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_is_described_by_qualified_relations_organization_identifiers_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.identifiers.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/identifiers/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_identifiers_value = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.identifiers.value",
    label=_(
        "metadata/is_described_by/qualified_relations/organization/identifiers/value.label"
    ),
)

metadata_is_described_by_qualified_relations_organization_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.iri",
    label=_("metadata/is_described_by/qualified_relations/organization/iri.label"),
)

metadata_is_described_by_qualified_relations_organization_name = TermsFacet(
    field="metadata.is_described_by.qualified_relations.organization.name",
    label=_("metadata/is_described_by/qualified_relations/organization/name.label"),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names_cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.alternate_names_en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "en": (
            metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en
        ),
    },
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

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
    },
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

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/thoroughfares.label"
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

metadata_is_described_by_qualified_relations_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_is_described_by_qualified_relations_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.identifiers.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/identifiers/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.identifiers.value",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/identifiers/value.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_affiliations_name = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.affiliations.name",
    label=_(
        "metadata/is_described_by/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.full_address",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/full_address.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en
        ),
    },
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

metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.po_box",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/po_box.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.post_code",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/post_code.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.post_names",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/post_names.label"
    ),
)

metadata_is_described_by_qualified_relations_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/thoroughfares.label"
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

metadata_is_described_by_qualified_relations_person_family_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.family_names",
    label=_("metadata/is_described_by/qualified_relations/person/family_names.label"),
)

metadata_is_described_by_qualified_relations_person_given_names = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.given_names",
    label=_("metadata/is_described_by/qualified_relations/person/given_names.label"),
)

metadata_is_described_by_qualified_relations_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.is_described_by.qualified_relations.person.identifiers.identifier_scheme",
    label=_(
        "metadata/is_described_by/qualified_relations/person/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_is_described_by_qualified_relations_person_identifiers_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.identifiers.iri",
    label=_(
        "metadata/is_described_by/qualified_relations/person/identifiers/iri.label"
    ),
)

metadata_is_described_by_qualified_relations_person_identifiers_value = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.identifiers.value",
    label=_(
        "metadata/is_described_by/qualified_relations/person/identifiers/value.label"
    ),
)

metadata_is_described_by_qualified_relations_person_iri = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.iri",
    label=_("metadata/is_described_by/qualified_relations/person/iri.label"),
)

metadata_is_described_by_qualified_relations_person_name = TermsFacet(
    field="metadata.is_described_by.qualified_relations.person.name",
    label=_("metadata/is_described_by/qualified_relations/person/name.label"),
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

metadata_locations_geometry_iri = TermsFacet(
    field="metadata.locations.geometry.iri",
    label=_("metadata/locations/geometry/iri.label"),
)

metadata_locations_geometry_labels_cs = TermsFacet(
    field="metadata.locations.geometry.labels_cs.keyword",
    label=_("metadata/locations/geometry/labels.label"),
)

metadata_locations_geometry_labels_en = TermsFacet(
    field="metadata.locations.geometry.labels_en.keyword",
    label=_("metadata/locations/geometry/labels.label"),
)

metadata_locations_geometry_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_locations_geometry_labels_cs,
        "en": metadata_locations_geometry_labels_en,
    },
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

metadata_locations_names = TermsFacet(
    field="metadata.locations.names", label=_("metadata/locations/names.label")
)

metadata_locations_related_objects_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.locations.related_objects.identifiers.identifier_scheme",
    label=_("metadata/locations/related_objects/identifiers/identifier_scheme.label"),
    vocabulary="identifier-schemes",
)

metadata_locations_related_objects_identifiers_iri = TermsFacet(
    field="metadata.locations.related_objects.identifiers.iri",
    label=_("metadata/locations/related_objects/identifiers/iri.label"),
)

metadata_locations_related_objects_identifiers_value = TermsFacet(
    field="metadata.locations.related_objects.identifiers.value",
    label=_("metadata/locations/related_objects/identifiers/value.label"),
)

metadata_locations_related_objects_iri = TermsFacet(
    field="metadata.locations.related_objects.iri",
    label=_("metadata/locations/related_objects/iri.label"),
)

metadata_locations_related_objects_qualified_relations_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.iri",
    label=_("metadata/locations/related_objects/qualified_relations/iri.label"),
)

metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.alternate_names_cs.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.alternate_names_en.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs
        ),
        "en": (
            metadata_locations_related_objects_qualified_relations_organization_alternate_names_en
        ),
    },
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.qualified_relations.organization.alternate_names.lang",
        label=_(
            "metadata/locations/related_objects/qualified_relations/organization/alternate_names/lang.label"
        ),
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_emails = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.emails",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/emails.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_contact_points_phones = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.contact_points.phones",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/phones.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_locations_related_objects_qualified_relations_organization_identifiers_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.identifiers.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/identifiers/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_identifiers_value = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.identifiers.value",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/identifiers/value.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_organization_name = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.organization.name",
    label=_(
        "metadata/locations/related_objects/qualified_relations/organization/name.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.alternate_names_cs.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.alternate_names_en.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "en": (
            metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en
        ),
    },
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.qualified_relations.person.affiliations.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.qualified_relations.person.affiliations.alternate_names.lang",
        label=_(
            "metadata/locations/related_objects/qualified_relations/person/affiliations/alternate_names/lang.label"
        ),
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_emails = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.emails",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/emails.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_phones = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.contact_points.phones",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/phones.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.identifiers.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/identifiers/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.identifiers.value",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/identifiers/value.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_affiliations_name = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.affiliations.name",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.full_address",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/full_address.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en
        ),
    },
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.labels",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.labels.lang",
        label=_(
            "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/labels/lang.label"
        ),
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.po_box",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/po_box.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.post_code",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/post_code.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.post_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/post_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/thoroughfares.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_dataBoxes = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.dataBoxes",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/dataBoxes.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_emails = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.emails",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/emails.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_contact_points_phones = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.contact_points.phones",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/contact_points/phones.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_family_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.family_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/family_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_given_names = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.given_names",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/given_names.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.locations.related_objects.qualified_relations.person.identifiers.identifier_scheme",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_locations_related_objects_qualified_relations_person_identifiers_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.identifiers.iri",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/identifiers/iri.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_identifiers_value = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.identifiers.value",
    label=_(
        "metadata/locations/related_objects/qualified_relations/person/identifiers/value.label"
    ),
)

metadata_locations_related_objects_qualified_relations_person_iri = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.iri",
    label=_("metadata/locations/related_objects/qualified_relations/person/iri.label"),
)

metadata_locations_related_objects_qualified_relations_person_name = TermsFacet(
    field="metadata.locations.related_objects.qualified_relations.person.name",
    label=_("metadata/locations/related_objects/qualified_relations/person/name.label"),
)

metadata_locations_related_objects_qualified_relations_role = VocabularyFacet(
    field="metadata.locations.related_objects.qualified_relations.role",
    label=_("metadata/locations/related_objects/qualified_relations/role.label"),
    vocabulary="contributor-types",
)

metadata_locations_related_objects_relation_type = VocabularyFacet(
    field="metadata.locations.related_objects.relation_type",
    label=_("metadata/locations/related_objects/relation_type.label"),
    vocabulary="relation-types",
)

metadata_locations_related_objects_resource_url = TermsFacet(
    field="metadata.locations.related_objects.resource_url",
    label=_("metadata/locations/related_objects/resource_url.label"),
)

metadata_locations_related_objects_time_references_date = DateTimeFacet(
    field="metadata.locations.related_objects.time_references.date",
    label=_("metadata/locations/related_objects/time_references/date.label"),
)

metadata_locations_related_objects_time_references_date_information_cs = TermsFacet(
    field="metadata.locations.related_objects.time_references.date_information_cs.keyword",
    label=_(
        "metadata/locations/related_objects/time_references/date_information.label"
    ),
)

metadata_locations_related_objects_time_references_date_information_en = TermsFacet(
    field="metadata.locations.related_objects.time_references.date_information_en.keyword",
    label=_(
        "metadata/locations/related_objects/time_references/date_information.label"
    ),
)

metadata_locations_related_objects_time_references_date_information = MultilingualFacet(
    lang_facets={
        "cs": metadata_locations_related_objects_time_references_date_information_cs,
        "en": metadata_locations_related_objects_time_references_date_information_en,
    },
    label=_(
        "metadata/locations/related_objects/time_references/date_information.label"
    ),
)

metadata_locations_related_objects_time_references_date_information_lang = NestedLabeledFacet(
    path="metadata.locations.related_objects.time_references.date_information",
    nested_facet=TermsFacet(
        field="metadata.locations.related_objects.time_references.date_information.lang",
        label=_(
            "metadata/locations/related_objects/time_references/date_information/lang.label"
        ),
    ),
)

metadata_locations_related_objects_time_references_date_type = VocabularyFacet(
    field="metadata.locations.related_objects.time_references.date_type",
    label=_("metadata/locations/related_objects/time_references/date_type.label"),
    vocabulary="time-reference-types",
)

metadata_locations_related_objects_time_references_iri = TermsFacet(
    field="metadata.locations.related_objects.time_references.iri",
    label=_("metadata/locations/related_objects/time_references/iri.label"),
)

metadata_locations_related_objects_title = TermsFacet(
    field="metadata.locations.related_objects.title",
    label=_("metadata/locations/related_objects/title.label"),
)

metadata_locations_related_objects_type = VocabularyFacet(
    field="metadata.locations.related_objects.type",
    label=_("metadata/locations/related_objects/type.label"),
    vocabulary="resource-types",
)

metadata_locations_relation_type = VocabularyFacet(
    field="metadata.locations.relation_type",
    label=_("metadata/locations/relation_type.label"),
    vocabulary="location-relation-types",
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
    field="metadata.provenances.labels_cs.keyword",
    label=_("metadata/provenances/labels.label"),
)

metadata_provenances_labels_en = TermsFacet(
    field="metadata.provenances.labels_en.keyword",
    label=_("metadata/provenances/labels.label"),
)

metadata_provenances_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_provenances_labels_cs,
        "en": metadata_provenances_labels_en,
    },
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
    field="metadata.qualified_relations.organization.alternate_names_cs.keyword",
    label=_("metadata/qualified_relations/organization/alternate_names.label"),
)

metadata_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.qualified_relations.organization.alternate_names_en.keyword",
    label=_("metadata/qualified_relations/organization/alternate_names.label"),
)

metadata_qualified_relations_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": metadata_qualified_relations_organization_alternate_names_cs,
        "en": metadata_qualified_relations_organization_alternate_names_en,
    },
    label=_("metadata/qualified_relations/organization/alternate_names.label"),
)

metadata_qualified_relations_organization_alternate_names_lang = NestedLabeledFacet(
    path="metadata.qualified_relations.organization.alternate_names",
    nested_facet=TermsFacet(
        field="metadata.qualified_relations.organization.alternate_names.lang",
        label=_("metadata/qualified_relations/organization/alternate_names/lang.label"),
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_qualified_relations_organization_contact_points_addresses_labels_en
        ),
    },
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

metadata_qualified_relations_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_qualified_relations_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.qualified_relations.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/qualified_relations/organization/contact_points/addresses/thoroughfares.label"
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

metadata_qualified_relations_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.qualified_relations.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/qualified_relations/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_qualified_relations_organization_identifiers_iri = TermsFacet(
    field="metadata.qualified_relations.organization.identifiers.iri",
    label=_("metadata/qualified_relations/organization/identifiers/iri.label"),
)

metadata_qualified_relations_organization_identifiers_value = TermsFacet(
    field="metadata.qualified_relations.organization.identifiers.value",
    label=_("metadata/qualified_relations/organization/identifiers/value.label"),
)

metadata_qualified_relations_organization_iri = TermsFacet(
    field="metadata.qualified_relations.organization.iri",
    label=_("metadata/qualified_relations/organization/iri.label"),
)

metadata_qualified_relations_organization_name = TermsFacet(
    field="metadata.qualified_relations.organization.name",
    label=_("metadata/qualified_relations/organization/name.label"),
)

metadata_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.alternate_names_cs.keyword",
    label=_("metadata/qualified_relations/person/affiliations/alternate_names.label"),
)

metadata_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.alternate_names_en.keyword",
    label=_("metadata/qualified_relations/person/affiliations/alternate_names.label"),
)

metadata_qualified_relations_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": metadata_qualified_relations_person_affiliations_alternate_names_cs,
        "en": metadata_qualified_relations_person_affiliations_alternate_names_en,
    },
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

metadata_qualified_relations_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
    },
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

metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/thoroughfares.label"
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

metadata_qualified_relations_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.qualified_relations.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/qualified_relations/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_qualified_relations_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.identifiers.iri",
    label=_("metadata/qualified_relations/person/affiliations/identifiers/iri.label"),
)

metadata_qualified_relations_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.identifiers.value",
    label=_("metadata/qualified_relations/person/affiliations/identifiers/value.label"),
)

metadata_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.iri",
    label=_("metadata/qualified_relations/person/affiliations/iri.label"),
)

metadata_qualified_relations_person_affiliations_name = TermsFacet(
    field="metadata.qualified_relations.person.affiliations.name",
    label=_("metadata/qualified_relations/person/affiliations/name.label"),
)

metadata_qualified_relations_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.full_address",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/full_address.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.iri",
    label=_("metadata/qualified_relations/person/contact_points/addresses/iri.label"),
)

metadata_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_qualified_relations_person_contact_points_addresses_labels_cs,
        "en": metadata_qualified_relations_person_contact_points_addresses_labels_en,
    },
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

metadata_qualified_relations_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.po_box",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/po_box.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.post_code",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/post_code.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.post_names",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/post_names.label"
    ),
)

metadata_qualified_relations_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.qualified_relations.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/qualified_relations/person/contact_points/addresses/thoroughfares.label"
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

metadata_qualified_relations_person_family_names = TermsFacet(
    field="metadata.qualified_relations.person.family_names",
    label=_("metadata/qualified_relations/person/family_names.label"),
)

metadata_qualified_relations_person_given_names = TermsFacet(
    field="metadata.qualified_relations.person.given_names",
    label=_("metadata/qualified_relations/person/given_names.label"),
)

metadata_qualified_relations_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.qualified_relations.person.identifiers.identifier_scheme",
    label=_("metadata/qualified_relations/person/identifiers/identifier_scheme.label"),
    vocabulary="identifier-schemes",
)

metadata_qualified_relations_person_identifiers_iri = TermsFacet(
    field="metadata.qualified_relations.person.identifiers.iri",
    label=_("metadata/qualified_relations/person/identifiers/iri.label"),
)

metadata_qualified_relations_person_identifiers_value = TermsFacet(
    field="metadata.qualified_relations.person.identifiers.value",
    label=_("metadata/qualified_relations/person/identifiers/value.label"),
)

metadata_qualified_relations_person_iri = TermsFacet(
    field="metadata.qualified_relations.person.iri",
    label=_("metadata/qualified_relations/person/iri.label"),
)

metadata_qualified_relations_person_name = TermsFacet(
    field="metadata.qualified_relations.person.name",
    label=_("metadata/qualified_relations/person/name.label"),
)

metadata_qualified_relations_role = VocabularyFacet(
    field="metadata.qualified_relations.role",
    label=_("metadata/qualified_relations/role.label"),
    vocabulary="contributor-types",
)

metadata_related_resources_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.related_resources.identifiers.identifier_scheme",
    label=_("metadata/related_resources/identifiers/identifier_scheme.label"),
    vocabulary="identifier-schemes",
)

metadata_related_resources_identifiers_iri = TermsFacet(
    field="metadata.related_resources.identifiers.iri",
    label=_("metadata/related_resources/identifiers/iri.label"),
)

metadata_related_resources_identifiers_value = TermsFacet(
    field="metadata.related_resources.identifiers.value",
    label=_("metadata/related_resources/identifiers/value.label"),
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
    field="metadata.related_resources.qualified_relations.organization.alternate_names_cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_alternate_names_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.alternate_names_en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_related_resources_qualified_relations_organization_alternate_names_cs
        ),
        "en": (
            metadata_related_resources_qualified_relations_organization_alternate_names_en
        ),
    },
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

metadata_related_resources_qualified_relations_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en
        ),
    },
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

metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_related_resources_qualified_relations_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/thoroughfares.label"
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

metadata_related_resources_qualified_relations_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.related_resources.qualified_relations.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/related_resources/qualified_relations/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_related_resources_qualified_relations_organization_identifiers_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.identifiers.iri",
    label=_(
        "metadata/related_resources/qualified_relations/organization/identifiers/iri.label"
    ),
)

metadata_related_resources_qualified_relations_organization_identifiers_value = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.identifiers.value",
    label=_(
        "metadata/related_resources/qualified_relations/organization/identifiers/value.label"
    ),
)

metadata_related_resources_qualified_relations_organization_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.iri",
    label=_("metadata/related_resources/qualified_relations/organization/iri.label"),
)

metadata_related_resources_qualified_relations_organization_name = TermsFacet(
    field="metadata.related_resources.qualified_relations.organization.name",
    label=_("metadata/related_resources/qualified_relations/organization/name.label"),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.alternate_names_cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.alternate_names_en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/alternate_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "en": (
            metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en
        ),
    },
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

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
    },
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

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/thoroughfares.label"
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

metadata_related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_related_resources_qualified_relations_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.identifiers.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/identifiers/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.identifiers.value",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/identifiers/value.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_affiliations_name = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.affiliations.name",
    label=_(
        "metadata/related_resources/qualified_relations/person/affiliations/name.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.full_address",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/full_address.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en
        ),
    },
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

metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.po_box",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/po_box.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.post_code",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/post_code.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.post_names",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/post_names.label"
    ),
)

metadata_related_resources_qualified_relations_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/thoroughfares.label"
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

metadata_related_resources_qualified_relations_person_family_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.family_names",
    label=_("metadata/related_resources/qualified_relations/person/family_names.label"),
)

metadata_related_resources_qualified_relations_person_given_names = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.given_names",
    label=_("metadata/related_resources/qualified_relations/person/given_names.label"),
)

metadata_related_resources_qualified_relations_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.related_resources.qualified_relations.person.identifiers.identifier_scheme",
    label=_(
        "metadata/related_resources/qualified_relations/person/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_related_resources_qualified_relations_person_identifiers_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.identifiers.iri",
    label=_(
        "metadata/related_resources/qualified_relations/person/identifiers/iri.label"
    ),
)

metadata_related_resources_qualified_relations_person_identifiers_value = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.identifiers.value",
    label=_(
        "metadata/related_resources/qualified_relations/person/identifiers/value.label"
    ),
)

metadata_related_resources_qualified_relations_person_iri = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.iri",
    label=_("metadata/related_resources/qualified_relations/person/iri.label"),
)

metadata_related_resources_qualified_relations_person_name = TermsFacet(
    field="metadata.related_resources.qualified_relations.person.name",
    label=_("metadata/related_resources/qualified_relations/person/name.label"),
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

metadata_related_resources_resource_url = TermsFacet(
    field="metadata.related_resources.resource_url",
    label=_("metadata/related_resources/resource_url.label"),
)

metadata_related_resources_time_references_date = DateTimeFacet(
    field="metadata.related_resources.time_references.date",
    label=_("metadata/related_resources/time_references/date.label"),
)

metadata_related_resources_time_references_date_information_cs = TermsFacet(
    field="metadata.related_resources.time_references.date_information_cs.keyword",
    label=_("metadata/related_resources/time_references/date_information.label"),
)

metadata_related_resources_time_references_date_information_en = TermsFacet(
    field="metadata.related_resources.time_references.date_information_en.keyword",
    label=_("metadata/related_resources/time_references/date_information.label"),
)

metadata_related_resources_time_references_date_information = MultilingualFacet(
    lang_facets={
        "cs": metadata_related_resources_time_references_date_information_cs,
        "en": metadata_related_resources_time_references_date_information_en,
    },
    label=_("metadata/related_resources/time_references/date_information.label"),
)

metadata_related_resources_time_references_date_information_lang = NestedLabeledFacet(
    path="metadata.related_resources.time_references.date_information",
    nested_facet=TermsFacet(
        field="metadata.related_resources.time_references.date_information.lang",
        label=_(
            "metadata/related_resources/time_references/date_information/lang.label"
        ),
    ),
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

metadata_related_resources_type = VocabularyFacet(
    field="metadata.related_resources.type",
    label=_("metadata/related_resources/type.label"),
    vocabulary="resource-types",
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

metadata_subjects_definitions_cs = TermsFacet(
    field="metadata.subjects.definitions_cs.keyword",
    label=_("metadata/subjects/definitions.label"),
)

metadata_subjects_definitions_en = TermsFacet(
    field="metadata.subjects.definitions_en.keyword",
    label=_("metadata/subjects/definitions.label"),
)

metadata_subjects_definitions = MultilingualFacet(
    lang_facets={
        "cs": metadata_subjects_definitions_cs,
        "en": metadata_subjects_definitions_en,
    },
    label=_("metadata/subjects/definitions.label"),
)

metadata_subjects_definitions_lang = NestedLabeledFacet(
    path="metadata.subjects.definitions",
    nested_facet=TermsFacet(
        field="metadata.subjects.definitions.lang",
        label=_("metadata/subjects/definitions/lang.label"),
    ),
)

metadata_subjects_iri = TermsFacet(
    field="metadata.subjects.iri", label=_("metadata/subjects/iri.label")
)

metadata_subjects_scheme = VocabularyFacet(
    field="metadata.subjects.scheme",
    label=_("metadata/subjects/scheme.label"),
    vocabulary="subject-schemes",
)

metadata_subjects_title_cs = TermsFacet(
    field="metadata.subjects.title_cs.keyword", label=_("metadata/subjects/title.label")
)

metadata_subjects_title_en = TermsFacet(
    field="metadata.subjects.title_en.keyword", label=_("metadata/subjects/title.label")
)

metadata_subjects_title = MultilingualFacet(
    lang_facets={
        "cs": metadata_subjects_title_cs,
        "en": metadata_subjects_title_en,
    },
    label=_("metadata/subjects/title.label"),
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
    field="metadata.terms_of_use.contacts.organization.alternate_names_cs.keyword",
    label=_("metadata/terms_of_use/contacts/organization/alternate_names.label"),
)

metadata_terms_of_use_contacts_organization_alternate_names_en = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.alternate_names_en.keyword",
    label=_("metadata/terms_of_use/contacts/organization/alternate_names.label"),
)

metadata_terms_of_use_contacts_organization_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": metadata_terms_of_use_contacts_organization_alternate_names_cs,
        "en": metadata_terms_of_use_contacts_organization_alternate_names_en,
    },
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

metadata_terms_of_use_contacts_organization_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.address_areas",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/address_areas.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_full_address = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.full_address",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/full_address.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.iri",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/iri.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en
        ),
    },
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

metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.locator_designators",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/locator_designators.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.locator_names",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/locator_names.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_po_box = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.po_box",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/po_box.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_post_code = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.post_code",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/post_code.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_post_names = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.post_names",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/post_names.label"
    ),
)

metadata_terms_of_use_contacts_organization_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/thoroughfares.label"
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

metadata_terms_of_use_contacts_organization_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.terms_of_use.contacts.organization.identifiers.identifier_scheme",
    label=_(
        "metadata/terms_of_use/contacts/organization/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_terms_of_use_contacts_organization_identifiers_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.identifiers.iri",
    label=_("metadata/terms_of_use/contacts/organization/identifiers/iri.label"),
)

metadata_terms_of_use_contacts_organization_identifiers_value = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.identifiers.value",
    label=_("metadata/terms_of_use/contacts/organization/identifiers/value.label"),
)

metadata_terms_of_use_contacts_organization_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.iri",
    label=_("metadata/terms_of_use/contacts/organization/iri.label"),
)

metadata_terms_of_use_contacts_organization_name = TermsFacet(
    field="metadata.terms_of_use.contacts.organization.name",
    label=_("metadata/terms_of_use/contacts/organization/name.label"),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.alternate_names_cs.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/alternate_names.label"),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.alternate_names_en.keyword",
    label=_("metadata/terms_of_use/contacts/person/affiliations/alternate_names.label"),
)

metadata_terms_of_use_contacts_person_affiliations_alternate_names = MultilingualFacet(
    lang_facets={
        "cs": metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs,
        "en": metadata_terms_of_use_contacts_person_affiliations_alternate_names_en,
    },
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

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.address_areas",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/address_areas.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_full_address = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.full_address",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/full_address.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.iri",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/iri.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": (
            metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs
        ),
        "en": (
            metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en
        ),
    },
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

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.locator_designators",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/locator_designators.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.locator_names",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/locator_names.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_po_box = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.po_box",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/po_box.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_code = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.post_code",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/post_code.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.post_names",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/post_names.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/thoroughfares.label"
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

metadata_terms_of_use_contacts_person_affiliations_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.identifiers.identifier_scheme",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_terms_of_use_contacts_person_affiliations_identifiers_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.identifiers.iri",
    label=_("metadata/terms_of_use/contacts/person/affiliations/identifiers/iri.label"),
)

metadata_terms_of_use_contacts_person_affiliations_identifiers_value = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.identifiers.value",
    label=_(
        "metadata/terms_of_use/contacts/person/affiliations/identifiers/value.label"
    ),
)

metadata_terms_of_use_contacts_person_affiliations_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.iri",
    label=_("metadata/terms_of_use/contacts/person/affiliations/iri.label"),
)

metadata_terms_of_use_contacts_person_affiliations_name = TermsFacet(
    field="metadata.terms_of_use.contacts.person.affiliations.name",
    label=_("metadata/terms_of_use/contacts/person/affiliations/name.label"),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_address_areas = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.address_areas",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/address_areas.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_1 = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.administrative_unit_level_1",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/administrative_unit_level_1.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_2 = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.administrative_unit_level_2",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/administrative_unit_level_2.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_full_address = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.full_address",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/full_address.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.iri",
    label=_("metadata/terms_of_use/contacts/person/contact_points/addresses/iri.label"),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.labels_cs.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.labels_en.keyword",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/labels.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs,
        "en": metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en,
    },
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

metadata_terms_of_use_contacts_person_contact_points_addresses_locator_designators = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.locator_designators",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/locator_designators.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_locator_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.locator_names",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/locator_names.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_po_box = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.po_box",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/po_box.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_post_code = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.post_code",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/post_code.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_post_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.post_names",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/post_names.label"
    ),
)

metadata_terms_of_use_contacts_person_contact_points_addresses_thoroughfares = TermsFacet(
    field="metadata.terms_of_use.contacts.person.contact_points.addresses.thoroughfares",
    label=_(
        "metadata/terms_of_use/contacts/person/contact_points/addresses/thoroughfares.label"
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

metadata_terms_of_use_contacts_person_family_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.family_names",
    label=_("metadata/terms_of_use/contacts/person/family_names.label"),
)

metadata_terms_of_use_contacts_person_given_names = TermsFacet(
    field="metadata.terms_of_use.contacts.person.given_names",
    label=_("metadata/terms_of_use/contacts/person/given_names.label"),
)

metadata_terms_of_use_contacts_person_identifiers_identifier_scheme = VocabularyFacet(
    field="metadata.terms_of_use.contacts.person.identifiers.identifier_scheme",
    label=_(
        "metadata/terms_of_use/contacts/person/identifiers/identifier_scheme.label"
    ),
    vocabulary="identifier-schemes",
)

metadata_terms_of_use_contacts_person_identifiers_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.identifiers.iri",
    label=_("metadata/terms_of_use/contacts/person/identifiers/iri.label"),
)

metadata_terms_of_use_contacts_person_identifiers_value = TermsFacet(
    field="metadata.terms_of_use.contacts.person.identifiers.value",
    label=_("metadata/terms_of_use/contacts/person/identifiers/value.label"),
)

metadata_terms_of_use_contacts_person_iri = TermsFacet(
    field="metadata.terms_of_use.contacts.person.iri",
    label=_("metadata/terms_of_use/contacts/person/iri.label"),
)

metadata_terms_of_use_contacts_person_name = TermsFacet(
    field="metadata.terms_of_use.contacts.person.name",
    label=_("metadata/terms_of_use/contacts/person/name.label"),
)

metadata_terms_of_use_description_cs = TermsFacet(
    field="metadata.terms_of_use.description_cs.keyword",
    label=_("metadata/terms_of_use/description.label"),
)

metadata_terms_of_use_description_en = TermsFacet(
    field="metadata.terms_of_use.description_en.keyword",
    label=_("metadata/terms_of_use/description.label"),
)

metadata_terms_of_use_description = MultilingualFacet(
    lang_facets={
        "cs": metadata_terms_of_use_description_cs,
        "en": metadata_terms_of_use_description_en,
    },
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

metadata_terms_of_use_license_iri = TermsFacet(
    field="metadata.terms_of_use.license.iri",
    label=_("metadata/terms_of_use/license/iri.label"),
)

metadata_terms_of_use_license_labels_cs = TermsFacet(
    field="metadata.terms_of_use.license.labels_cs.keyword",
    label=_("metadata/terms_of_use/license/labels.label"),
)

metadata_terms_of_use_license_labels_en = TermsFacet(
    field="metadata.terms_of_use.license.labels_en.keyword",
    label=_("metadata/terms_of_use/license/labels.label"),
)

metadata_terms_of_use_license_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_terms_of_use_license_labels_cs,
        "en": metadata_terms_of_use_license_labels_en,
    },
    label=_("metadata/terms_of_use/license/labels.label"),
)

metadata_terms_of_use_license_labels_lang = NestedLabeledFacet(
    path="metadata.terms_of_use.license.labels",
    nested_facet=TermsFacet(
        field="metadata.terms_of_use.license.labels.lang",
        label=_("metadata/terms_of_use/license/labels/lang.label"),
    ),
)

metadata_time_references_date = DateTimeFacet(
    field="metadata.time_references.date",
    label=_("metadata/time_references/date.label"),
)

metadata_time_references_date_information_cs = TermsFacet(
    field="metadata.time_references.date_information_cs.keyword",
    label=_("metadata/time_references/date_information.label"),
)

metadata_time_references_date_information_en = TermsFacet(
    field="metadata.time_references.date_information_en.keyword",
    label=_("metadata/time_references/date_information.label"),
)

metadata_time_references_date_information = MultilingualFacet(
    lang_facets={
        "cs": metadata_time_references_date_information_cs,
        "en": metadata_time_references_date_information_en,
    },
    label=_("metadata/time_references/date_information.label"),
)

metadata_time_references_date_information_lang = NestedLabeledFacet(
    path="metadata.time_references.date_information",
    nested_facet=TermsFacet(
        field="metadata.time_references.date_information.lang",
        label=_("metadata/time_references/date_information/lang.label"),
    ),
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
    field="metadata.validation_results.labels_cs.keyword",
    label=_("metadata/validation_results/labels.label"),
)

metadata_validation_results_labels_en = TermsFacet(
    field="metadata.validation_results.labels_en.keyword",
    label=_("metadata/validation_results/labels.label"),
)

metadata_validation_results_labels = MultilingualFacet(
    lang_facets={
        "cs": metadata_validation_results_labels_cs,
        "en": metadata_validation_results_labels_en,
    },
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

metadata_versions = TermsFacet(
    field="metadata.versions", label=_("metadata/versions.label")
)

oai_harvest_datestamp = TermsFacet(
    field="oai.harvest.datestamp", label=_("oai/harvest/datestamp.label")
)

oai_harvest_identifier = TermsFacet(
    field="oai.harvest.identifier", label=_("oai/harvest/identifier.label")
)

state = TermsFacet(field="state", label=_("state.label"))

state_timestamp = DateTimeFacet(
    field="state_timestamp", label=_("state_timestamp.label")
)


record_status = TermsFacet(field="record_status", label=_("record_status"))

has_draft = TermsFacet(field="has_draft", label=_("has_draft"))

expires_at = DateTimeFacet(field="expires_at", label=_("expires_at.label"))

fork_version_id = TermsFacet(field="fork_version_id", label=_("fork_version_id.label"))
