from oarepo_runtime.services.search import (
    I18nRDMDraftsSearchOptions,
    I18nRDMSearchOptions,
)

from . import facets


class DatasetsSearchOptions(I18nRDMSearchOptions):
    """DatasetsRecord search options."""

    facet_groups = {
        "default": {
            "metadata_funding_references_award_title": facets.metadata_funding_references_award_title,
            "metadata_funding_references_funders_organization_name": facets.metadata_funding_references_funders_organization_name,
            "metadata_funding_references_funding_program": facets.metadata_funding_references_funding_program,
            "metadata_is_described_by_original_repositories_labels_cs": (
                facets.metadata_is_described_by_original_repositories_labels_cs
            ),
            "metadata_locations_names": facets.metadata_locations_names,
            "metadata_primary_language": facets.metadata_primary_language,
            "metadata_publication_year": facets.metadata_publication_year,
            "metadata_subjects_title_cs": facets.metadata_subjects_title_cs,
            "metadata_terms_of_use_access_rights": facets.metadata_terms_of_use_access_rights,
            **getattr(I18nRDMSearchOptions, "facet_groups", {}).get("default", {}),
        }
    }

    facets = {
        **getattr(I18nRDMSearchOptions, "facets", {}),
        "access_embargo_active": facets.access_embargo_active,
        "access_embargo_until": facets.access_embargo_until,
        "access_files": facets.access_files,
        "access_record": facets.access_record,
        "access_status": facets.access_status,
        "metadata_alternate_titles_iri": facets.metadata_alternate_titles_iri,
        "metadata_alternate_titles_title_cs": facets.metadata_alternate_titles_title_cs,
        "metadata_alternate_titles_title_en": facets.metadata_alternate_titles_title_en,
        "metadata_alternate_titles_title": facets.metadata_alternate_titles_title,
        "metadata_alternate_titles_title_lang": (
            facets.metadata_alternate_titles_title_lang
        ),
        "metadata_alternate_titles_type": facets.metadata_alternate_titles_type,
        "metadata_descriptions_cs": facets.metadata_descriptions_cs,
        "metadata_descriptions_en": facets.metadata_descriptions_en,
        "metadata_descriptions": facets.metadata_descriptions,
        "metadata_descriptions_lang": facets.metadata_descriptions_lang,
        "metadata_distributions_access_urls": facets.metadata_distributions_access_urls,
        "metadata_distributions_byte_size": facets.metadata_distributions_byte_size,
        "metadata_distributions_checksum_algorithm": (
            facets.metadata_distributions_checksum_algorithm
        ),
        "metadata_distributions_checksum_iri": (
            facets.metadata_distributions_checksum_iri
        ),
        "metadata_distributions_checksum_value": (
            facets.metadata_distributions_checksum_value
        ),
        "metadata_distributions_conforms_to_schemas_iri": (
            facets.metadata_distributions_conforms_to_schemas_iri
        ),
        "metadata_distributions_conforms_to_schemas_labels_cs": (
            facets.metadata_distributions_conforms_to_schemas_labels_cs
        ),
        "metadata_distributions_conforms_to_schemas_labels_en": (
            facets.metadata_distributions_conforms_to_schemas_labels_en
        ),
        "metadata_distributions_conforms_to_schemas_labels": (
            facets.metadata_distributions_conforms_to_schemas_labels
        ),
        "metadata_distributions_conforms_to_schemas_labels_lang": (
            facets.metadata_distributions_conforms_to_schemas_labels_lang
        ),
        "metadata_distributions_download_urls": (
            facets.metadata_distributions_download_urls
        ),
        "metadata_distributions_format": facets.metadata_distributions_format,
        "metadata_distributions_iri": facets.metadata_distributions_iri,
        "metadata_distributions_media_type": facets.metadata_distributions_media_type,
        "metadata_distributions_title": facets.metadata_distributions_title,
        "metadata_funding_references_award_title": (
            facets.metadata_funding_references_award_title
        ),
        "metadata_funding_references_funders_organization_alternate_names_cs": (
            facets.metadata_funding_references_funders_organization_alternate_names_cs
        ),
        "metadata_funding_references_funders_organization_alternate_names_en": (
            facets.metadata_funding_references_funders_organization_alternate_names_en
        ),
        "metadata_funding_references_funders_organization_alternate_names": (
            facets.metadata_funding_references_funders_organization_alternate_names
        ),
        "metadata_funding_references_funders_organization_alternate_names_lang": (
            facets.metadata_funding_references_funders_organization_alternate_names_lang
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_organization_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_organization_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_organization_contact_points_emails": (
            facets.metadata_funding_references_funders_organization_contact_points_emails
        ),
        "metadata_funding_references_funders_organization_contact_points_iri": (
            facets.metadata_funding_references_funders_organization_contact_points_iri
        ),
        "metadata_funding_references_funders_organization_contact_points_phones": (
            facets.metadata_funding_references_funders_organization_contact_points_phones
        ),
        "metadata_funding_references_funders_organization_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_organization_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_organization_identifiers_iri": (
            facets.metadata_funding_references_funders_organization_identifiers_iri
        ),
        "metadata_funding_references_funders_organization_identifiers_value": (
            facets.metadata_funding_references_funders_organization_identifiers_value
        ),
        "metadata_funding_references_funders_organization_iri": (
            facets.metadata_funding_references_funders_organization_iri
        ),
        "metadata_funding_references_funders_organization_name": (
            facets.metadata_funding_references_funders_organization_name
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_cs": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_cs
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_en": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_en
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_lang": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_lang
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_emails": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_emails
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_iri": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_iri
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_phones": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_phones
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_iri": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_iri
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_value": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_value
        ),
        "metadata_funding_references_funders_person_affiliations_iri": (
            facets.metadata_funding_references_funders_person_affiliations_iri
        ),
        "metadata_funding_references_funders_person_affiliations_name": (
            facets.metadata_funding_references_funders_person_affiliations_name
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_person_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_person_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_person_contact_points_emails": (
            facets.metadata_funding_references_funders_person_contact_points_emails
        ),
        "metadata_funding_references_funders_person_contact_points_iri": (
            facets.metadata_funding_references_funders_person_contact_points_iri
        ),
        "metadata_funding_references_funders_person_contact_points_phones": (
            facets.metadata_funding_references_funders_person_contact_points_phones
        ),
        "metadata_funding_references_funders_person_family_names": (
            facets.metadata_funding_references_funders_person_family_names
        ),
        "metadata_funding_references_funders_person_given_names": (
            facets.metadata_funding_references_funders_person_given_names
        ),
        "metadata_funding_references_funders_person_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_person_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_person_identifiers_iri": (
            facets.metadata_funding_references_funders_person_identifiers_iri
        ),
        "metadata_funding_references_funders_person_identifiers_value": (
            facets.metadata_funding_references_funders_person_identifiers_value
        ),
        "metadata_funding_references_funders_person_iri": (
            facets.metadata_funding_references_funders_person_iri
        ),
        "metadata_funding_references_funders_person_name": (
            facets.metadata_funding_references_funders_person_name
        ),
        "metadata_funding_references_funding_program": (
            facets.metadata_funding_references_funding_program
        ),
        "metadata_funding_references_iri": facets.metadata_funding_references_iri,
        "metadata_funding_references_local_identifier": (
            facets.metadata_funding_references_local_identifier
        ),
        "metadata_identifiers_identifier_scheme": (
            facets.metadata_identifiers_identifier_scheme
        ),
        "metadata_identifiers_iri": facets.metadata_identifiers_iri,
        "metadata_identifiers_value": facets.metadata_identifiers_value,
        "metadata_iri": facets.metadata_iri,
        "metadata_is_described_by_conforms_to_standards_iri": (
            facets.metadata_is_described_by_conforms_to_standards_iri
        ),
        "metadata_is_described_by_conforms_to_standards_labels_cs": (
            facets.metadata_is_described_by_conforms_to_standards_labels_cs
        ),
        "metadata_is_described_by_conforms_to_standards_labels_en": (
            facets.metadata_is_described_by_conforms_to_standards_labels_en
        ),
        "metadata_is_described_by_conforms_to_standards_labels": (
            facets.metadata_is_described_by_conforms_to_standards_labels
        ),
        "metadata_is_described_by_conforms_to_standards_labels_lang": (
            facets.metadata_is_described_by_conforms_to_standards_labels_lang
        ),
        "metadata_is_described_by_date_created": (
            facets.metadata_is_described_by_date_created
        ),
        "metadata_is_described_by_dates_updated": (
            facets.metadata_is_described_by_dates_updated
        ),
        "metadata_is_described_by_iri": facets.metadata_is_described_by_iri,
        "metadata_is_described_by_languages": facets.metadata_is_described_by_languages,
        "metadata_is_described_by_original_repositories_iri": (
            facets.metadata_is_described_by_original_repositories_iri
        ),
        "metadata_is_described_by_original_repositories_labels_cs": (
            facets.metadata_is_described_by_original_repositories_labels_cs
        ),
        "metadata_is_described_by_original_repositories_labels_en": (
            facets.metadata_is_described_by_original_repositories_labels_en
        ),
        "metadata_is_described_by_original_repositories_labels": (
            facets.metadata_is_described_by_original_repositories_labels
        ),
        "metadata_is_described_by_original_repositories_labels_lang": (
            facets.metadata_is_described_by_original_repositories_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_iri": (
            facets.metadata_is_described_by_qualified_relations_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_organization_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_name": (
            facets.metadata_is_described_by_qualified_relations_organization_name
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_person_family_names": (
            facets.metadata_is_described_by_qualified_relations_person_family_names
        ),
        "metadata_is_described_by_qualified_relations_person_given_names": (
            facets.metadata_is_described_by_qualified_relations_person_given_names
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_person_iri": (
            facets.metadata_is_described_by_qualified_relations_person_iri
        ),
        "metadata_is_described_by_qualified_relations_person_name": (
            facets.metadata_is_described_by_qualified_relations_person_name
        ),
        "metadata_is_described_by_qualified_relations_role": (
            facets.metadata_is_described_by_qualified_relations_role
        ),
        "metadata_locations_bbox_LowerCorners": (
            facets.metadata_locations_bbox_LowerCorners
        ),
        "metadata_locations_bbox_UpperCorners": (
            facets.metadata_locations_bbox_UpperCorners
        ),
        "metadata_locations_bbox_crs": facets.metadata_locations_bbox_crs,
        "metadata_locations_bbox_dimensions": facets.metadata_locations_bbox_dimensions,
        "metadata_locations_geometry_iri": facets.metadata_locations_geometry_iri,
        "metadata_locations_geometry_labels_cs": (
            facets.metadata_locations_geometry_labels_cs
        ),
        "metadata_locations_geometry_labels_en": (
            facets.metadata_locations_geometry_labels_en
        ),
        "metadata_locations_geometry_labels": facets.metadata_locations_geometry_labels,
        "metadata_locations_geometry_labels_lang": (
            facets.metadata_locations_geometry_labels_lang
        ),
        "metadata_locations_iri": facets.metadata_locations_iri,
        "metadata_locations_names": facets.metadata_locations_names,
        "metadata_locations_related_objects_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_identifiers_iri": (
            facets.metadata_locations_related_objects_identifiers_iri
        ),
        "metadata_locations_related_objects_identifiers_value": (
            facets.metadata_locations_related_objects_identifiers_value
        ),
        "metadata_locations_related_objects_iri": (
            facets.metadata_locations_related_objects_iri
        ),
        "metadata_locations_related_objects_qualified_relations_iri": (
            facets.metadata_locations_related_objects_qualified_relations_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_en": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_en
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_organization_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_name": (
            facets.metadata_locations_related_objects_qualified_relations_organization_name
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_name": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_name
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_person_family_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_family_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_given_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_given_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_person_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_name": (
            facets.metadata_locations_related_objects_qualified_relations_person_name
        ),
        "metadata_locations_related_objects_qualified_relations_role": (
            facets.metadata_locations_related_objects_qualified_relations_role
        ),
        "metadata_locations_related_objects_relation_type": (
            facets.metadata_locations_related_objects_relation_type
        ),
        "metadata_locations_related_objects_resource_url": (
            facets.metadata_locations_related_objects_resource_url
        ),
        "metadata_locations_related_objects_time_references_date": (
            facets.metadata_locations_related_objects_time_references_date
        ),
        "metadata_locations_related_objects_time_references_date_information_cs": (
            facets.metadata_locations_related_objects_time_references_date_information_cs
        ),
        "metadata_locations_related_objects_time_references_date_information_en": (
            facets.metadata_locations_related_objects_time_references_date_information_en
        ),
        "metadata_locations_related_objects_time_references_date_information": (
            facets.metadata_locations_related_objects_time_references_date_information
        ),
        "metadata_locations_related_objects_time_references_date_information_lang": (
            facets.metadata_locations_related_objects_time_references_date_information_lang
        ),
        "metadata_locations_related_objects_time_references_date_type": (
            facets.metadata_locations_related_objects_time_references_date_type
        ),
        "metadata_locations_related_objects_time_references_iri": (
            facets.metadata_locations_related_objects_time_references_iri
        ),
        "metadata_locations_related_objects_title": (
            facets.metadata_locations_related_objects_title
        ),
        "metadata_locations_related_objects_type": (
            facets.metadata_locations_related_objects_type
        ),
        "metadata_locations_relation_type": facets.metadata_locations_relation_type,
        "metadata_other_languages": facets.metadata_other_languages,
        "metadata_primary_language": facets.metadata_primary_language,
        "metadata_provenances_iri": facets.metadata_provenances_iri,
        "metadata_provenances_labels_cs": facets.metadata_provenances_labels_cs,
        "metadata_provenances_labels_en": facets.metadata_provenances_labels_en,
        "metadata_provenances_labels": facets.metadata_provenances_labels,
        "metadata_provenances_labels_lang": facets.metadata_provenances_labels_lang,
        "metadata_publication_year": facets.metadata_publication_year,
        "metadata_qualified_relations_iri": facets.metadata_qualified_relations_iri,
        "metadata_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_qualified_relations_organization_alternate_names_en": (
            facets.metadata_qualified_relations_organization_alternate_names_en
        ),
        "metadata_qualified_relations_organization_alternate_names": (
            facets.metadata_qualified_relations_organization_alternate_names
        ),
        "metadata_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_organization_contact_points_emails": (
            facets.metadata_qualified_relations_organization_contact_points_emails
        ),
        "metadata_qualified_relations_organization_contact_points_iri": (
            facets.metadata_qualified_relations_organization_contact_points_iri
        ),
        "metadata_qualified_relations_organization_contact_points_phones": (
            facets.metadata_qualified_relations_organization_contact_points_phones
        ),
        "metadata_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_organization_identifiers_iri": (
            facets.metadata_qualified_relations_organization_identifiers_iri
        ),
        "metadata_qualified_relations_organization_identifiers_value": (
            facets.metadata_qualified_relations_organization_identifiers_value
        ),
        "metadata_qualified_relations_organization_iri": (
            facets.metadata_qualified_relations_organization_iri
        ),
        "metadata_qualified_relations_organization_name": (
            facets.metadata_qualified_relations_organization_name
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_qualified_relations_person_affiliations_iri": (
            facets.metadata_qualified_relations_person_affiliations_iri
        ),
        "metadata_qualified_relations_person_affiliations_name": (
            facets.metadata_qualified_relations_person_affiliations_name
        ),
        "metadata_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_person_contact_points_emails": (
            facets.metadata_qualified_relations_person_contact_points_emails
        ),
        "metadata_qualified_relations_person_contact_points_iri": (
            facets.metadata_qualified_relations_person_contact_points_iri
        ),
        "metadata_qualified_relations_person_contact_points_phones": (
            facets.metadata_qualified_relations_person_contact_points_phones
        ),
        "metadata_qualified_relations_person_family_names": (
            facets.metadata_qualified_relations_person_family_names
        ),
        "metadata_qualified_relations_person_given_names": (
            facets.metadata_qualified_relations_person_given_names
        ),
        "metadata_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_person_identifiers_iri": (
            facets.metadata_qualified_relations_person_identifiers_iri
        ),
        "metadata_qualified_relations_person_identifiers_value": (
            facets.metadata_qualified_relations_person_identifiers_value
        ),
        "metadata_qualified_relations_person_iri": (
            facets.metadata_qualified_relations_person_iri
        ),
        "metadata_qualified_relations_person_name": (
            facets.metadata_qualified_relations_person_name
        ),
        "metadata_qualified_relations_role": facets.metadata_qualified_relations_role,
        "metadata_related_resources_identifiers_identifier_scheme": (
            facets.metadata_related_resources_identifiers_identifier_scheme
        ),
        "metadata_related_resources_identifiers_iri": (
            facets.metadata_related_resources_identifiers_iri
        ),
        "metadata_related_resources_identifiers_value": (
            facets.metadata_related_resources_identifiers_value
        ),
        "metadata_related_resources_iri": facets.metadata_related_resources_iri,
        "metadata_related_resources_qualified_relations_iri": (
            facets.metadata_related_resources_qualified_relations_iri
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_organization_iri": (
            facets.metadata_related_resources_qualified_relations_organization_iri
        ),
        "metadata_related_resources_qualified_relations_organization_name": (
            facets.metadata_related_resources_qualified_relations_organization_name
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_person_family_names": (
            facets.metadata_related_resources_qualified_relations_person_family_names
        ),
        "metadata_related_resources_qualified_relations_person_given_names": (
            facets.metadata_related_resources_qualified_relations_person_given_names
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_person_iri": (
            facets.metadata_related_resources_qualified_relations_person_iri
        ),
        "metadata_related_resources_qualified_relations_person_name": (
            facets.metadata_related_resources_qualified_relations_person_name
        ),
        "metadata_related_resources_qualified_relations_role": (
            facets.metadata_related_resources_qualified_relations_role
        ),
        "metadata_related_resources_relation_type": (
            facets.metadata_related_resources_relation_type
        ),
        "metadata_related_resources_resource_url": (
            facets.metadata_related_resources_resource_url
        ),
        "metadata_related_resources_time_references_date": (
            facets.metadata_related_resources_time_references_date
        ),
        "metadata_related_resources_time_references_date_information_cs": (
            facets.metadata_related_resources_time_references_date_information_cs
        ),
        "metadata_related_resources_time_references_date_information_en": (
            facets.metadata_related_resources_time_references_date_information_en
        ),
        "metadata_related_resources_time_references_date_information": (
            facets.metadata_related_resources_time_references_date_information
        ),
        "metadata_related_resources_time_references_date_information_lang": (
            facets.metadata_related_resources_time_references_date_information_lang
        ),
        "metadata_related_resources_time_references_date_type": (
            facets.metadata_related_resources_time_references_date_type
        ),
        "metadata_related_resources_time_references_iri": (
            facets.metadata_related_resources_time_references_iri
        ),
        "metadata_related_resources_title": facets.metadata_related_resources_title,
        "metadata_related_resources_type": facets.metadata_related_resources_type,
        "metadata_resource_type": facets.metadata_resource_type,
        "metadata_subjects_classification_code": (
            facets.metadata_subjects_classification_code
        ),
        "metadata_subjects_definitions_cs": facets.metadata_subjects_definitions_cs,
        "metadata_subjects_definitions_en": facets.metadata_subjects_definitions_en,
        "metadata_subjects_definitions": facets.metadata_subjects_definitions,
        "metadata_subjects_definitions_lang": facets.metadata_subjects_definitions_lang,
        "metadata_subjects_iri": facets.metadata_subjects_iri,
        "metadata_subjects_scheme": facets.metadata_subjects_scheme,
        "metadata_subjects_title_cs": facets.metadata_subjects_title_cs,
        "metadata_subjects_title_en": facets.metadata_subjects_title_en,
        "metadata_subjects_title": facets.metadata_subjects_title,
        "metadata_subjects_title_lang": facets.metadata_subjects_title_lang,
        "metadata_terms_of_use_access_rights": (
            facets.metadata_terms_of_use_access_rights
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_lang
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_value": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_value
        ),
        "metadata_terms_of_use_contacts_organization_iri": (
            facets.metadata_terms_of_use_contacts_organization_iri
        ),
        "metadata_terms_of_use_contacts_organization_name": (
            facets.metadata_terms_of_use_contacts_organization_name
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_value": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_value
        ),
        "metadata_terms_of_use_contacts_person_affiliations_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_person_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_person_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_person_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_person_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_person_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_person_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_person_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_person_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_person_family_names": (
            facets.metadata_terms_of_use_contacts_person_family_names
        ),
        "metadata_terms_of_use_contacts_person_given_names": (
            facets.metadata_terms_of_use_contacts_person_given_names
        ),
        "metadata_terms_of_use_contacts_person_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_person_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_person_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_person_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_person_identifiers_value": (
            facets.metadata_terms_of_use_contacts_person_identifiers_value
        ),
        "metadata_terms_of_use_contacts_person_iri": (
            facets.metadata_terms_of_use_contacts_person_iri
        ),
        "metadata_terms_of_use_contacts_person_name": (
            facets.metadata_terms_of_use_contacts_person_name
        ),
        "metadata_terms_of_use_description_cs": (
            facets.metadata_terms_of_use_description_cs
        ),
        "metadata_terms_of_use_description_en": (
            facets.metadata_terms_of_use_description_en
        ),
        "metadata_terms_of_use_description": facets.metadata_terms_of_use_description,
        "metadata_terms_of_use_description_lang": (
            facets.metadata_terms_of_use_description_lang
        ),
        "metadata_terms_of_use_iri": facets.metadata_terms_of_use_iri,
        "metadata_terms_of_use_license_iri": facets.metadata_terms_of_use_license_iri,
        "metadata_terms_of_use_license_labels_cs": (
            facets.metadata_terms_of_use_license_labels_cs
        ),
        "metadata_terms_of_use_license_labels_en": (
            facets.metadata_terms_of_use_license_labels_en
        ),
        "metadata_terms_of_use_license_labels": (
            facets.metadata_terms_of_use_license_labels
        ),
        "metadata_terms_of_use_license_labels_lang": (
            facets.metadata_terms_of_use_license_labels_lang
        ),
        "metadata_time_references_date": facets.metadata_time_references_date,
        "metadata_time_references_date_information_cs": (
            facets.metadata_time_references_date_information_cs
        ),
        "metadata_time_references_date_information_en": (
            facets.metadata_time_references_date_information_en
        ),
        "metadata_time_references_date_information": (
            facets.metadata_time_references_date_information
        ),
        "metadata_time_references_date_information_lang": (
            facets.metadata_time_references_date_information_lang
        ),
        "metadata_time_references_date_type": facets.metadata_time_references_date_type,
        "metadata_time_references_iri": facets.metadata_time_references_iri,
        "metadata_title": facets.metadata_title,
        "metadata_validation_results_iri": facets.metadata_validation_results_iri,
        "metadata_validation_results_labels_cs": (
            facets.metadata_validation_results_labels_cs
        ),
        "metadata_validation_results_labels_en": (
            facets.metadata_validation_results_labels_en
        ),
        "metadata_validation_results_labels": facets.metadata_validation_results_labels,
        "metadata_validation_results_labels_lang": (
            facets.metadata_validation_results_labels_lang
        ),
        "metadata_version": facets.metadata_version,
        "metadata_versions": facets.metadata_versions,
        "oai_harvest_datestamp": facets.oai_harvest_datestamp,
        "oai_harvest_identifier": facets.oai_harvest_identifier,
        "state": facets.state,
        "state_timestamp": facets.state_timestamp,
        "record_status": facets.record_status,
        "has_draft": facets.has_draft,
    }


class DatasetsDraftSearchOptions(I18nRDMDraftsSearchOptions):
    """DatasetsDraft search options."""

    facet_groups = {}

    facets = {
        "access_embargo_active": facets.access_embargo_active,
        "access_embargo_until": facets.access_embargo_until,
        "access_files": facets.access_files,
        "access_record": facets.access_record,
        "access_status": facets.access_status,
        "metadata_alternate_titles_iri": facets.metadata_alternate_titles_iri,
        "metadata_alternate_titles_title_cs": facets.metadata_alternate_titles_title_cs,
        "metadata_alternate_titles_title_en": facets.metadata_alternate_titles_title_en,
        "metadata_alternate_titles_title": facets.metadata_alternate_titles_title,
        "metadata_alternate_titles_title_lang": (
            facets.metadata_alternate_titles_title_lang
        ),
        "metadata_alternate_titles_type": facets.metadata_alternate_titles_type,
        "metadata_descriptions_cs": facets.metadata_descriptions_cs,
        "metadata_descriptions_en": facets.metadata_descriptions_en,
        "metadata_descriptions": facets.metadata_descriptions,
        "metadata_descriptions_lang": facets.metadata_descriptions_lang,
        "metadata_distributions_access_urls": facets.metadata_distributions_access_urls,
        "metadata_distributions_byte_size": facets.metadata_distributions_byte_size,
        "metadata_distributions_checksum_algorithm": (
            facets.metadata_distributions_checksum_algorithm
        ),
        "metadata_distributions_checksum_iri": (
            facets.metadata_distributions_checksum_iri
        ),
        "metadata_distributions_checksum_value": (
            facets.metadata_distributions_checksum_value
        ),
        "metadata_distributions_conforms_to_schemas_iri": (
            facets.metadata_distributions_conforms_to_schemas_iri
        ),
        "metadata_distributions_conforms_to_schemas_labels_cs": (
            facets.metadata_distributions_conforms_to_schemas_labels_cs
        ),
        "metadata_distributions_conforms_to_schemas_labels_en": (
            facets.metadata_distributions_conforms_to_schemas_labels_en
        ),
        "metadata_distributions_conforms_to_schemas_labels": (
            facets.metadata_distributions_conforms_to_schemas_labels
        ),
        "metadata_distributions_conforms_to_schemas_labels_lang": (
            facets.metadata_distributions_conforms_to_schemas_labels_lang
        ),
        "metadata_distributions_download_urls": (
            facets.metadata_distributions_download_urls
        ),
        "metadata_distributions_format": facets.metadata_distributions_format,
        "metadata_distributions_iri": facets.metadata_distributions_iri,
        "metadata_distributions_media_type": facets.metadata_distributions_media_type,
        "metadata_distributions_title": facets.metadata_distributions_title,
        "metadata_funding_references_award_title": (
            facets.metadata_funding_references_award_title
        ),
        "metadata_funding_references_funders_organization_alternate_names_cs": (
            facets.metadata_funding_references_funders_organization_alternate_names_cs
        ),
        "metadata_funding_references_funders_organization_alternate_names_en": (
            facets.metadata_funding_references_funders_organization_alternate_names_en
        ),
        "metadata_funding_references_funders_organization_alternate_names": (
            facets.metadata_funding_references_funders_organization_alternate_names
        ),
        "metadata_funding_references_funders_organization_alternate_names_lang": (
            facets.metadata_funding_references_funders_organization_alternate_names_lang
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_organization_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_organization_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_organization_contact_points_emails": (
            facets.metadata_funding_references_funders_organization_contact_points_emails
        ),
        "metadata_funding_references_funders_organization_contact_points_iri": (
            facets.metadata_funding_references_funders_organization_contact_points_iri
        ),
        "metadata_funding_references_funders_organization_contact_points_phones": (
            facets.metadata_funding_references_funders_organization_contact_points_phones
        ),
        "metadata_funding_references_funders_organization_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_organization_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_organization_identifiers_iri": (
            facets.metadata_funding_references_funders_organization_identifiers_iri
        ),
        "metadata_funding_references_funders_organization_identifiers_value": (
            facets.metadata_funding_references_funders_organization_identifiers_value
        ),
        "metadata_funding_references_funders_organization_iri": (
            facets.metadata_funding_references_funders_organization_iri
        ),
        "metadata_funding_references_funders_organization_name": (
            facets.metadata_funding_references_funders_organization_name
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_cs": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_cs
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_en": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_en
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names
        ),
        "metadata_funding_references_funders_person_affiliations_alternate_names_lang": (
            facets.metadata_funding_references_funders_person_affiliations_alternate_names_lang
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_emails": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_emails
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_iri": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_iri
        ),
        "metadata_funding_references_funders_person_affiliations_contact_points_phones": (
            facets.metadata_funding_references_funders_person_affiliations_contact_points_phones
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_iri": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_iri
        ),
        "metadata_funding_references_funders_person_affiliations_identifiers_value": (
            facets.metadata_funding_references_funders_person_affiliations_identifiers_value
        ),
        "metadata_funding_references_funders_person_affiliations_iri": (
            facets.metadata_funding_references_funders_person_affiliations_iri
        ),
        "metadata_funding_references_funders_person_affiliations_name": (
            facets.metadata_funding_references_funders_person_affiliations_name
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_address_areas": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_address_areas
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_full_address": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_full_address
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_iri": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_iri
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_cs": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_cs
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_en": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_en
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_labels_lang": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_labels_lang
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_locator_designators": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_locator_designators
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_locator_names": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_locator_names
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_po_box": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_po_box
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_post_code": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_post_code
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_post_names": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_post_names
        ),
        "metadata_funding_references_funders_person_contact_points_addresses_thoroughfares": (
            facets.metadata_funding_references_funders_person_contact_points_addresses_thoroughfares
        ),
        "metadata_funding_references_funders_person_contact_points_dataBoxes": (
            facets.metadata_funding_references_funders_person_contact_points_dataBoxes
        ),
        "metadata_funding_references_funders_person_contact_points_emails": (
            facets.metadata_funding_references_funders_person_contact_points_emails
        ),
        "metadata_funding_references_funders_person_contact_points_iri": (
            facets.metadata_funding_references_funders_person_contact_points_iri
        ),
        "metadata_funding_references_funders_person_contact_points_phones": (
            facets.metadata_funding_references_funders_person_contact_points_phones
        ),
        "metadata_funding_references_funders_person_family_names": (
            facets.metadata_funding_references_funders_person_family_names
        ),
        "metadata_funding_references_funders_person_given_names": (
            facets.metadata_funding_references_funders_person_given_names
        ),
        "metadata_funding_references_funders_person_identifiers_identifier_scheme": (
            facets.metadata_funding_references_funders_person_identifiers_identifier_scheme
        ),
        "metadata_funding_references_funders_person_identifiers_iri": (
            facets.metadata_funding_references_funders_person_identifiers_iri
        ),
        "metadata_funding_references_funders_person_identifiers_value": (
            facets.metadata_funding_references_funders_person_identifiers_value
        ),
        "metadata_funding_references_funders_person_iri": (
            facets.metadata_funding_references_funders_person_iri
        ),
        "metadata_funding_references_funders_person_name": (
            facets.metadata_funding_references_funders_person_name
        ),
        "metadata_funding_references_funding_program": (
            facets.metadata_funding_references_funding_program
        ),
        "metadata_funding_references_iri": facets.metadata_funding_references_iri,
        "metadata_funding_references_local_identifier": (
            facets.metadata_funding_references_local_identifier
        ),
        "metadata_identifiers_identifier_scheme": (
            facets.metadata_identifiers_identifier_scheme
        ),
        "metadata_identifiers_iri": facets.metadata_identifiers_iri,
        "metadata_identifiers_value": facets.metadata_identifiers_value,
        "metadata_iri": facets.metadata_iri,
        "metadata_is_described_by_conforms_to_standards_iri": (
            facets.metadata_is_described_by_conforms_to_standards_iri
        ),
        "metadata_is_described_by_conforms_to_standards_labels_cs": (
            facets.metadata_is_described_by_conforms_to_standards_labels_cs
        ),
        "metadata_is_described_by_conforms_to_standards_labels_en": (
            facets.metadata_is_described_by_conforms_to_standards_labels_en
        ),
        "metadata_is_described_by_conforms_to_standards_labels": (
            facets.metadata_is_described_by_conforms_to_standards_labels
        ),
        "metadata_is_described_by_conforms_to_standards_labels_lang": (
            facets.metadata_is_described_by_conforms_to_standards_labels_lang
        ),
        "metadata_is_described_by_date_created": (
            facets.metadata_is_described_by_date_created
        ),
        "metadata_is_described_by_dates_updated": (
            facets.metadata_is_described_by_dates_updated
        ),
        "metadata_is_described_by_iri": facets.metadata_is_described_by_iri,
        "metadata_is_described_by_languages": facets.metadata_is_described_by_languages,
        "metadata_is_described_by_original_repositories_iri": (
            facets.metadata_is_described_by_original_repositories_iri
        ),
        "metadata_is_described_by_original_repositories_labels_cs": (
            facets.metadata_is_described_by_original_repositories_labels_cs
        ),
        "metadata_is_described_by_original_repositories_labels_en": (
            facets.metadata_is_described_by_original_repositories_labels_en
        ),
        "metadata_is_described_by_original_repositories_labels": (
            facets.metadata_is_described_by_original_repositories_labels
        ),
        "metadata_is_described_by_original_repositories_labels_lang": (
            facets.metadata_is_described_by_original_repositories_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_iri": (
            facets.metadata_is_described_by_qualified_relations_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names
        ),
        "metadata_is_described_by_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_organization_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_organization_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_name": (
            facets.metadata_is_described_by_qualified_relations_organization_name
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_emails": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_emails
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_iri": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_iri
        ),
        "metadata_is_described_by_qualified_relations_person_contact_points_phones": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_phones
        ),
        "metadata_is_described_by_qualified_relations_person_family_names": (
            facets.metadata_is_described_by_qualified_relations_person_family_names
        ),
        "metadata_is_described_by_qualified_relations_person_given_names": (
            facets.metadata_is_described_by_qualified_relations_person_given_names
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_iri": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_iri
        ),
        "metadata_is_described_by_qualified_relations_person_identifiers_value": (
            facets.metadata_is_described_by_qualified_relations_person_identifiers_value
        ),
        "metadata_is_described_by_qualified_relations_person_iri": (
            facets.metadata_is_described_by_qualified_relations_person_iri
        ),
        "metadata_is_described_by_qualified_relations_person_name": (
            facets.metadata_is_described_by_qualified_relations_person_name
        ),
        "metadata_is_described_by_qualified_relations_role": (
            facets.metadata_is_described_by_qualified_relations_role
        ),
        "metadata_locations_bbox_LowerCorners": (
            facets.metadata_locations_bbox_LowerCorners
        ),
        "metadata_locations_bbox_UpperCorners": (
            facets.metadata_locations_bbox_UpperCorners
        ),
        "metadata_locations_bbox_crs": facets.metadata_locations_bbox_crs,
        "metadata_locations_bbox_dimensions": facets.metadata_locations_bbox_dimensions,
        "metadata_locations_geometry_iri": facets.metadata_locations_geometry_iri,
        "metadata_locations_geometry_labels_cs": (
            facets.metadata_locations_geometry_labels_cs
        ),
        "metadata_locations_geometry_labels_en": (
            facets.metadata_locations_geometry_labels_en
        ),
        "metadata_locations_geometry_labels": facets.metadata_locations_geometry_labels,
        "metadata_locations_geometry_labels_lang": (
            facets.metadata_locations_geometry_labels_lang
        ),
        "metadata_locations_iri": facets.metadata_locations_iri,
        "metadata_locations_names": facets.metadata_locations_names,
        "metadata_locations_related_objects_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_identifiers_iri": (
            facets.metadata_locations_related_objects_identifiers_iri
        ),
        "metadata_locations_related_objects_identifiers_value": (
            facets.metadata_locations_related_objects_identifiers_value
        ),
        "metadata_locations_related_objects_iri": (
            facets.metadata_locations_related_objects_iri
        ),
        "metadata_locations_related_objects_qualified_relations_iri": (
            facets.metadata_locations_related_objects_qualified_relations_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_en": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_en
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_locations_related_objects_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_organization_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_organization_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_organization_iri": (
            facets.metadata_locations_related_objects_qualified_relations_organization_iri
        ),
        "metadata_locations_related_objects_qualified_relations_organization_name": (
            facets.metadata_locations_related_objects_qualified_relations_organization_name
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_affiliations_name": (
            facets.metadata_locations_related_objects_qualified_relations_person_affiliations_name
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_emails": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_emails
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_contact_points_phones": (
            facets.metadata_locations_related_objects_qualified_relations_person_contact_points_phones
        ),
        "metadata_locations_related_objects_qualified_relations_person_family_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_family_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_given_names": (
            facets.metadata_locations_related_objects_qualified_relations_person_given_names
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_identifiers_value": (
            facets.metadata_locations_related_objects_qualified_relations_person_identifiers_value
        ),
        "metadata_locations_related_objects_qualified_relations_person_iri": (
            facets.metadata_locations_related_objects_qualified_relations_person_iri
        ),
        "metadata_locations_related_objects_qualified_relations_person_name": (
            facets.metadata_locations_related_objects_qualified_relations_person_name
        ),
        "metadata_locations_related_objects_qualified_relations_role": (
            facets.metadata_locations_related_objects_qualified_relations_role
        ),
        "metadata_locations_related_objects_relation_type": (
            facets.metadata_locations_related_objects_relation_type
        ),
        "metadata_locations_related_objects_resource_url": (
            facets.metadata_locations_related_objects_resource_url
        ),
        "metadata_locations_related_objects_time_references_date": (
            facets.metadata_locations_related_objects_time_references_date
        ),
        "metadata_locations_related_objects_time_references_date_information_cs": (
            facets.metadata_locations_related_objects_time_references_date_information_cs
        ),
        "metadata_locations_related_objects_time_references_date_information_en": (
            facets.metadata_locations_related_objects_time_references_date_information_en
        ),
        "metadata_locations_related_objects_time_references_date_information": (
            facets.metadata_locations_related_objects_time_references_date_information
        ),
        "metadata_locations_related_objects_time_references_date_information_lang": (
            facets.metadata_locations_related_objects_time_references_date_information_lang
        ),
        "metadata_locations_related_objects_time_references_date_type": (
            facets.metadata_locations_related_objects_time_references_date_type
        ),
        "metadata_locations_related_objects_time_references_iri": (
            facets.metadata_locations_related_objects_time_references_iri
        ),
        "metadata_locations_related_objects_title": (
            facets.metadata_locations_related_objects_title
        ),
        "metadata_locations_related_objects_type": (
            facets.metadata_locations_related_objects_type
        ),
        "metadata_locations_relation_type": facets.metadata_locations_relation_type,
        "metadata_other_languages": facets.metadata_other_languages,
        "metadata_primary_language": facets.metadata_primary_language,
        "metadata_provenances_iri": facets.metadata_provenances_iri,
        "metadata_provenances_labels_cs": facets.metadata_provenances_labels_cs,
        "metadata_provenances_labels_en": facets.metadata_provenances_labels_en,
        "metadata_provenances_labels": facets.metadata_provenances_labels,
        "metadata_provenances_labels_lang": facets.metadata_provenances_labels_lang,
        "metadata_publication_year": facets.metadata_publication_year,
        "metadata_qualified_relations_iri": facets.metadata_qualified_relations_iri,
        "metadata_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_qualified_relations_organization_alternate_names_en": (
            facets.metadata_qualified_relations_organization_alternate_names_en
        ),
        "metadata_qualified_relations_organization_alternate_names": (
            facets.metadata_qualified_relations_organization_alternate_names
        ),
        "metadata_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_organization_contact_points_emails": (
            facets.metadata_qualified_relations_organization_contact_points_emails
        ),
        "metadata_qualified_relations_organization_contact_points_iri": (
            facets.metadata_qualified_relations_organization_contact_points_iri
        ),
        "metadata_qualified_relations_organization_contact_points_phones": (
            facets.metadata_qualified_relations_organization_contact_points_phones
        ),
        "metadata_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_organization_identifiers_iri": (
            facets.metadata_qualified_relations_organization_identifiers_iri
        ),
        "metadata_qualified_relations_organization_identifiers_value": (
            facets.metadata_qualified_relations_organization_identifiers_value
        ),
        "metadata_qualified_relations_organization_iri": (
            facets.metadata_qualified_relations_organization_iri
        ),
        "metadata_qualified_relations_organization_name": (
            facets.metadata_qualified_relations_organization_name
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_qualified_relations_person_affiliations_iri": (
            facets.metadata_qualified_relations_person_affiliations_iri
        ),
        "metadata_qualified_relations_person_affiliations_name": (
            facets.metadata_qualified_relations_person_affiliations_name
        ),
        "metadata_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_qualified_relations_person_contact_points_emails": (
            facets.metadata_qualified_relations_person_contact_points_emails
        ),
        "metadata_qualified_relations_person_contact_points_iri": (
            facets.metadata_qualified_relations_person_contact_points_iri
        ),
        "metadata_qualified_relations_person_contact_points_phones": (
            facets.metadata_qualified_relations_person_contact_points_phones
        ),
        "metadata_qualified_relations_person_family_names": (
            facets.metadata_qualified_relations_person_family_names
        ),
        "metadata_qualified_relations_person_given_names": (
            facets.metadata_qualified_relations_person_given_names
        ),
        "metadata_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_qualified_relations_person_identifiers_iri": (
            facets.metadata_qualified_relations_person_identifiers_iri
        ),
        "metadata_qualified_relations_person_identifiers_value": (
            facets.metadata_qualified_relations_person_identifiers_value
        ),
        "metadata_qualified_relations_person_iri": (
            facets.metadata_qualified_relations_person_iri
        ),
        "metadata_qualified_relations_person_name": (
            facets.metadata_qualified_relations_person_name
        ),
        "metadata_qualified_relations_role": facets.metadata_qualified_relations_role,
        "metadata_related_resources_identifiers_identifier_scheme": (
            facets.metadata_related_resources_identifiers_identifier_scheme
        ),
        "metadata_related_resources_identifiers_iri": (
            facets.metadata_related_resources_identifiers_iri
        ),
        "metadata_related_resources_identifiers_value": (
            facets.metadata_related_resources_identifiers_value
        ),
        "metadata_related_resources_iri": facets.metadata_related_resources_iri,
        "metadata_related_resources_qualified_relations_iri": (
            facets.metadata_related_resources_qualified_relations_iri
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names
        ),
        "metadata_related_resources_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_organization_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_organization_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_organization_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_organization_iri": (
            facets.metadata_related_resources_qualified_relations_organization_iri
        ),
        "metadata_related_resources_qualified_relations_organization_name": (
            facets.metadata_related_resources_qualified_relations_organization_name
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_address_areas": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_address_areas
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_full_address": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_full_address
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_designators": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_designators
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_names": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_locator_names
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_po_box": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_po_box
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_post_code": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_post_code
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_post_names": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_post_names
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_thoroughfares": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_thoroughfares
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_emails": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_emails
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_iri": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_iri
        ),
        "metadata_related_resources_qualified_relations_person_contact_points_phones": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_phones
        ),
        "metadata_related_resources_qualified_relations_person_family_names": (
            facets.metadata_related_resources_qualified_relations_person_family_names
        ),
        "metadata_related_resources_qualified_relations_person_given_names": (
            facets.metadata_related_resources_qualified_relations_person_given_names
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_identifier_scheme": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_identifier_scheme
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_iri": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_iri
        ),
        "metadata_related_resources_qualified_relations_person_identifiers_value": (
            facets.metadata_related_resources_qualified_relations_person_identifiers_value
        ),
        "metadata_related_resources_qualified_relations_person_iri": (
            facets.metadata_related_resources_qualified_relations_person_iri
        ),
        "metadata_related_resources_qualified_relations_person_name": (
            facets.metadata_related_resources_qualified_relations_person_name
        ),
        "metadata_related_resources_qualified_relations_role": (
            facets.metadata_related_resources_qualified_relations_role
        ),
        "metadata_related_resources_relation_type": (
            facets.metadata_related_resources_relation_type
        ),
        "metadata_related_resources_resource_url": (
            facets.metadata_related_resources_resource_url
        ),
        "metadata_related_resources_time_references_date": (
            facets.metadata_related_resources_time_references_date
        ),
        "metadata_related_resources_time_references_date_information_cs": (
            facets.metadata_related_resources_time_references_date_information_cs
        ),
        "metadata_related_resources_time_references_date_information_en": (
            facets.metadata_related_resources_time_references_date_information_en
        ),
        "metadata_related_resources_time_references_date_information": (
            facets.metadata_related_resources_time_references_date_information
        ),
        "metadata_related_resources_time_references_date_information_lang": (
            facets.metadata_related_resources_time_references_date_information_lang
        ),
        "metadata_related_resources_time_references_date_type": (
            facets.metadata_related_resources_time_references_date_type
        ),
        "metadata_related_resources_time_references_iri": (
            facets.metadata_related_resources_time_references_iri
        ),
        "metadata_related_resources_title": facets.metadata_related_resources_title,
        "metadata_related_resources_type": facets.metadata_related_resources_type,
        "metadata_resource_type": facets.metadata_resource_type,
        "metadata_subjects_classification_code": (
            facets.metadata_subjects_classification_code
        ),
        "metadata_subjects_definitions_cs": facets.metadata_subjects_definitions_cs,
        "metadata_subjects_definitions_en": facets.metadata_subjects_definitions_en,
        "metadata_subjects_definitions": facets.metadata_subjects_definitions,
        "metadata_subjects_definitions_lang": facets.metadata_subjects_definitions_lang,
        "metadata_subjects_iri": facets.metadata_subjects_iri,
        "metadata_subjects_scheme": facets.metadata_subjects_scheme,
        "metadata_subjects_title_cs": facets.metadata_subjects_title_cs,
        "metadata_subjects_title_en": facets.metadata_subjects_title_en,
        "metadata_subjects_title": facets.metadata_subjects_title,
        "metadata_subjects_title_lang": facets.metadata_subjects_title_lang,
        "metadata_terms_of_use_access_rights": (
            facets.metadata_terms_of_use_access_rights
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names
        ),
        "metadata_terms_of_use_contacts_organization_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_lang
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_organization_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_organization_identifiers_value": (
            facets.metadata_terms_of_use_contacts_organization_identifiers_value
        ),
        "metadata_terms_of_use_contacts_organization_iri": (
            facets.metadata_terms_of_use_contacts_organization_iri
        ),
        "metadata_terms_of_use_contacts_organization_name": (
            facets.metadata_terms_of_use_contacts_organization_name
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_identifiers_value": (
            facets.metadata_terms_of_use_contacts_person_affiliations_identifiers_value
        ),
        "metadata_terms_of_use_contacts_person_affiliations_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_address_areas": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_address_areas
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_1": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_1
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_2": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_administrative_unit_level_2
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_full_address": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_full_address
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_iri": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_iri
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_cs
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_en
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_locator_designators": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_locator_designators
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_locator_names": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_locator_names
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_po_box": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_po_box
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_post_code": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_post_code
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_post_names": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_post_names
        ),
        "metadata_terms_of_use_contacts_person_contact_points_addresses_thoroughfares": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_thoroughfares
        ),
        "metadata_terms_of_use_contacts_person_contact_points_dataBoxes": (
            facets.metadata_terms_of_use_contacts_person_contact_points_dataBoxes
        ),
        "metadata_terms_of_use_contacts_person_contact_points_emails": (
            facets.metadata_terms_of_use_contacts_person_contact_points_emails
        ),
        "metadata_terms_of_use_contacts_person_contact_points_iri": (
            facets.metadata_terms_of_use_contacts_person_contact_points_iri
        ),
        "metadata_terms_of_use_contacts_person_contact_points_phones": (
            facets.metadata_terms_of_use_contacts_person_contact_points_phones
        ),
        "metadata_terms_of_use_contacts_person_family_names": (
            facets.metadata_terms_of_use_contacts_person_family_names
        ),
        "metadata_terms_of_use_contacts_person_given_names": (
            facets.metadata_terms_of_use_contacts_person_given_names
        ),
        "metadata_terms_of_use_contacts_person_identifiers_identifier_scheme": (
            facets.metadata_terms_of_use_contacts_person_identifiers_identifier_scheme
        ),
        "metadata_terms_of_use_contacts_person_identifiers_iri": (
            facets.metadata_terms_of_use_contacts_person_identifiers_iri
        ),
        "metadata_terms_of_use_contacts_person_identifiers_value": (
            facets.metadata_terms_of_use_contacts_person_identifiers_value
        ),
        "metadata_terms_of_use_contacts_person_iri": (
            facets.metadata_terms_of_use_contacts_person_iri
        ),
        "metadata_terms_of_use_contacts_person_name": (
            facets.metadata_terms_of_use_contacts_person_name
        ),
        "metadata_terms_of_use_description_cs": (
            facets.metadata_terms_of_use_description_cs
        ),
        "metadata_terms_of_use_description_en": (
            facets.metadata_terms_of_use_description_en
        ),
        "metadata_terms_of_use_description": facets.metadata_terms_of_use_description,
        "metadata_terms_of_use_description_lang": (
            facets.metadata_terms_of_use_description_lang
        ),
        "metadata_terms_of_use_iri": facets.metadata_terms_of_use_iri,
        "metadata_terms_of_use_license_iri": facets.metadata_terms_of_use_license_iri,
        "metadata_terms_of_use_license_labels_cs": (
            facets.metadata_terms_of_use_license_labels_cs
        ),
        "metadata_terms_of_use_license_labels_en": (
            facets.metadata_terms_of_use_license_labels_en
        ),
        "metadata_terms_of_use_license_labels": (
            facets.metadata_terms_of_use_license_labels
        ),
        "metadata_terms_of_use_license_labels_lang": (
            facets.metadata_terms_of_use_license_labels_lang
        ),
        "metadata_time_references_date": facets.metadata_time_references_date,
        "metadata_time_references_date_information_cs": (
            facets.metadata_time_references_date_information_cs
        ),
        "metadata_time_references_date_information_en": (
            facets.metadata_time_references_date_information_en
        ),
        "metadata_time_references_date_information": (
            facets.metadata_time_references_date_information
        ),
        "metadata_time_references_date_information_lang": (
            facets.metadata_time_references_date_information_lang
        ),
        "metadata_time_references_date_type": facets.metadata_time_references_date_type,
        "metadata_time_references_iri": facets.metadata_time_references_iri,
        "metadata_title": facets.metadata_title,
        "metadata_validation_results_iri": facets.metadata_validation_results_iri,
        "metadata_validation_results_labels_cs": (
            facets.metadata_validation_results_labels_cs
        ),
        "metadata_validation_results_labels_en": (
            facets.metadata_validation_results_labels_en
        ),
        "metadata_validation_results_labels": facets.metadata_validation_results_labels,
        "metadata_validation_results_labels_lang": (
            facets.metadata_validation_results_labels_lang
        ),
        "metadata_version": facets.metadata_version,
        "metadata_versions": facets.metadata_versions,
        "oai_harvest_datestamp": facets.oai_harvest_datestamp,
        "oai_harvest_identifier": facets.oai_harvest_identifier,
        "state": facets.state,
        "state_timestamp": facets.state_timestamp,
        "expires_at": facets.expires_at,
        "fork_version_id": facets.fork_version_id,
        **getattr(I18nRDMDraftsSearchOptions, "facets", {}),
        "record_status": facets.record_status,
        "has_draft": facets.has_draft,
    }
