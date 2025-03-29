from oarepo_runtime.services.search import (
    I18nRDMDraftsSearchOptions,
    I18nRDMSearchOptions,
)

from . import facets


class DatasetsSearchOptions(I18nRDMSearchOptions):
    """DatasetsRecord search options."""

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
        "metadata_alternate_titles_title_lang": (
            facets.metadata_alternate_titles_title_lang
        ),
        "metadata_alternate_titles_type": facets.metadata_alternate_titles_type,
        "metadata_descriptions_cs": facets.metadata_descriptions_cs,
        "metadata_descriptions_en": facets.metadata_descriptions_en,
        "metadata_descriptions_lang": facets.metadata_descriptions_lang,
        "metadata_distribution_data_services_access_services_endpoint_urls": (
            facets.metadata_distribution_data_services_access_services_endpoint_urls
        ),
        "metadata_distribution_data_services_access_services_iri": (
            facets.metadata_distribution_data_services_access_services_iri
        ),
        "metadata_distribution_data_services_access_services_labels_cs": (
            facets.metadata_distribution_data_services_access_services_labels_cs
        ),
        "metadata_distribution_data_services_access_services_labels_en": (
            facets.metadata_distribution_data_services_access_services_labels_en
        ),
        "metadata_distribution_data_services_access_services_labels_lang": (
            facets.metadata_distribution_data_services_access_services_labels_lang
        ),
        "metadata_distribution_data_services_descriptions_cs": (
            facets.metadata_distribution_data_services_descriptions_cs
        ),
        "metadata_distribution_data_services_descriptions_en": (
            facets.metadata_distribution_data_services_descriptions_en
        ),
        "metadata_distribution_data_services_descriptions_lang": (
            facets.metadata_distribution_data_services_descriptions_lang
        ),
        "metadata_distribution_data_services_documentations_iri": (
            facets.metadata_distribution_data_services_documentations_iri
        ),
        "metadata_distribution_data_services_documentations_labels_cs": (
            facets.metadata_distribution_data_services_documentations_labels_cs
        ),
        "metadata_distribution_data_services_documentations_labels_en": (
            facets.metadata_distribution_data_services_documentations_labels_en
        ),
        "metadata_distribution_data_services_documentations_labels_lang": (
            facets.metadata_distribution_data_services_documentations_labels_lang
        ),
        "metadata_distribution_data_services_iri": (
            facets.metadata_distribution_data_services_iri
        ),
        "metadata_distribution_data_services_specifications_iri": (
            facets.metadata_distribution_data_services_specifications_iri
        ),
        "metadata_distribution_data_services_specifications_labels_cs": (
            facets.metadata_distribution_data_services_specifications_labels_cs
        ),
        "metadata_distribution_data_services_specifications_labels_en": (
            facets.metadata_distribution_data_services_specifications_labels_en
        ),
        "metadata_distribution_data_services_specifications_labels_lang": (
            facets.metadata_distribution_data_services_specifications_labels_lang
        ),
        "metadata_distribution_data_services_title": (
            facets.metadata_distribution_data_services_title
        ),
        "metadata_distribution_downloadable_files_access_urls": (
            facets.metadata_distribution_downloadable_files_access_urls
        ),
        "metadata_distribution_downloadable_files_byte_size": (
            facets.metadata_distribution_downloadable_files_byte_size
        ),
        "metadata_distribution_downloadable_files_checksum": (
            facets.metadata_distribution_downloadable_files_checksum
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_iri": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_iri
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_cs": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_cs
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_en": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_en
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_lang": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_lang
        ),
        "metadata_distribution_downloadable_files_download_urls": (
            facets.metadata_distribution_downloadable_files_download_urls
        ),
        "metadata_distribution_downloadable_files_format": (
            facets.metadata_distribution_downloadable_files_format
        ),
        "metadata_distribution_downloadable_files_iri": (
            facets.metadata_distribution_downloadable_files_iri
        ),
        "metadata_distribution_downloadable_files_media_type_iri": (
            facets.metadata_distribution_downloadable_files_media_type_iri
        ),
        "metadata_distribution_downloadable_files_media_type_labels_cs": (
            facets.metadata_distribution_downloadable_files_media_type_labels_cs
        ),
        "metadata_distribution_downloadable_files_media_type_labels_en": (
            facets.metadata_distribution_downloadable_files_media_type_labels_en
        ),
        "metadata_distribution_downloadable_files_media_type_labels_lang": (
            facets.metadata_distribution_downloadable_files_media_type_labels_lang
        ),
        "metadata_distribution_downloadable_files_title": (
            facets.metadata_distribution_downloadable_files_title
        ),
        "metadata_funding_references_award_title": (
            facets.metadata_funding_references_award_title
        ),
        "metadata_funding_references_funders_funder_identifier_scheme_uri": (
            facets.metadata_funding_references_funders_funder_identifier_scheme_uri
        ),
        "metadata_funding_references_funders_funder_identifier_type": (
            facets.metadata_funding_references_funders_funder_identifier_type
        ),
        "metadata_funding_references_funders_funder_identifier_value": (
            facets.metadata_funding_references_funders_funder_identifier_value
        ),
        "metadata_funding_references_funders_funder_name": (
            facets.metadata_funding_references_funders_funder_name
        ),
        "metadata_funding_references_funders_iri": (
            facets.metadata_funding_references_funders_iri
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
        "metadata_is_described_by_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_lang
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
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_organization_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_organization_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_organization_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_organization_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_organization_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_name_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_name_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_name_en": (
            facets.metadata_is_described_by_qualified_relations_organization_name_en
        ),
        "metadata_is_described_by_qualified_relations_organization_name_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_name_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_lang
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
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_person_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_person_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_person_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_person_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_person_family_name": (
            facets.metadata_is_described_by_qualified_relations_person_family_name
        ),
        "metadata_is_described_by_qualified_relations_person_given_names": (
            facets.metadata_is_described_by_qualified_relations_person_given_names
        ),
        "metadata_is_described_by_qualified_relations_person_iri": (
            facets.metadata_is_described_by_qualified_relations_person_iri
        ),
        "metadata_is_described_by_qualified_relations_role_iri": (
            facets.metadata_is_described_by_qualified_relations_role_iri
        ),
        "metadata_is_described_by_qualified_relations_role_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_role_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_role_labels_en": (
            facets.metadata_is_described_by_qualified_relations_role_labels_en
        ),
        "metadata_is_described_by_qualified_relations_role_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_role_labels_lang
        ),
        "metadata_locations_bbox_LowerCorners": (
            facets.metadata_locations_bbox_LowerCorners
        ),
        "metadata_locations_bbox_UpperCorners": (
            facets.metadata_locations_bbox_UpperCorners
        ),
        "metadata_locations_bbox_crs": facets.metadata_locations_bbox_crs,
        "metadata_locations_bbox_dimensions": facets.metadata_locations_bbox_dimensions,
        "metadata_locations_dataset_relations": (
            facets.metadata_locations_dataset_relations
        ),
        "metadata_locations_geometry_iri": facets.metadata_locations_geometry_iri,
        "metadata_locations_geometry_labels_cs": (
            facets.metadata_locations_geometry_labels_cs
        ),
        "metadata_locations_geometry_labels_en": (
            facets.metadata_locations_geometry_labels_en
        ),
        "metadata_locations_geometry_labels_lang": (
            facets.metadata_locations_geometry_labels_lang
        ),
        "metadata_locations_iri": facets.metadata_locations_iri,
        "metadata_locations_location_names": facets.metadata_locations_location_names,
        "metadata_locations_related_object_identifiers_identifier_identifier_scheme": (
            facets.metadata_locations_related_object_identifiers_identifier_identifier_scheme
        ),
        "metadata_locations_related_object_identifiers_identifier_iri": (
            facets.metadata_locations_related_object_identifiers_identifier_iri
        ),
        "metadata_locations_related_object_identifiers_identifier_value": (
            facets.metadata_locations_related_object_identifiers_identifier_value
        ),
        "metadata_locations_related_object_identifiers_iri": (
            facets.metadata_locations_related_object_identifiers_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_family_name": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_family_name
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_given_names": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_given_names
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_lang
        ),
        "metadata_locations_related_object_identifiers_relation_type": (
            facets.metadata_locations_related_object_identifiers_relation_type
        ),
        "metadata_locations_related_object_identifiers_time_references_date": (
            facets.metadata_locations_related_object_identifiers_time_references_date
        ),
        "metadata_locations_related_object_identifiers_time_references_date_information": (
            facets.metadata_locations_related_object_identifiers_time_references_date_information
        ),
        "metadata_locations_related_object_identifiers_time_references_date_type": (
            facets.metadata_locations_related_object_identifiers_time_references_date_type
        ),
        "metadata_locations_related_object_identifiers_time_references_iri": (
            facets.metadata_locations_related_object_identifiers_time_references_iri
        ),
        "metadata_locations_related_object_identifiers_title": (
            facets.metadata_locations_related_object_identifiers_title
        ),
        "metadata_locations_related_object_identifiers_type": (
            facets.metadata_locations_related_object_identifiers_type
        ),
        "metadata_other_languages": facets.metadata_other_languages,
        "metadata_primary_language": facets.metadata_primary_language,
        "metadata_provenances_iri": facets.metadata_provenances_iri,
        "metadata_provenances_labels_cs": facets.metadata_provenances_labels_cs,
        "metadata_provenances_labels_en": facets.metadata_provenances_labels_en,
        "metadata_provenances_labels_lang": facets.metadata_provenances_labels_lang,
        "metadata_publication_year": facets.metadata_publication_year,
        "metadata_qualified_relations_iri": facets.metadata_qualified_relations_iri,
        "metadata_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_qualified_relations_organization_alternate_names_en": (
            facets.metadata_qualified_relations_organization_alternate_names_en
        ),
        "metadata_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_qualified_relations_organization_alternate_names_lang
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
        "metadata_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_organization_external_identifier_type": (
            facets.metadata_qualified_relations_organization_external_identifier_type
        ),
        "metadata_qualified_relations_organization_external_identifiers": (
            facets.metadata_qualified_relations_organization_external_identifiers
        ),
        "metadata_qualified_relations_organization_iri": (
            facets.metadata_qualified_relations_organization_iri
        ),
        "metadata_qualified_relations_organization_name_cs": (
            facets.metadata_qualified_relations_organization_name_cs
        ),
        "metadata_qualified_relations_organization_name_en": (
            facets.metadata_qualified_relations_organization_name_en
        ),
        "metadata_qualified_relations_organization_name_lang": (
            facets.metadata_qualified_relations_organization_name_lang
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_qualified_relations_person_affiliations_iri": (
            facets.metadata_qualified_relations_person_affiliations_iri
        ),
        "metadata_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_qualified_relations_person_affiliations_name_en": (
            facets.metadata_qualified_relations_person_affiliations_name_en
        ),
        "metadata_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_qualified_relations_person_affiliations_name_lang
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
        "metadata_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_person_external_identifier_type": (
            facets.metadata_qualified_relations_person_external_identifier_type
        ),
        "metadata_qualified_relations_person_external_identifiers": (
            facets.metadata_qualified_relations_person_external_identifiers
        ),
        "metadata_qualified_relations_person_family_name": (
            facets.metadata_qualified_relations_person_family_name
        ),
        "metadata_qualified_relations_person_given_names": (
            facets.metadata_qualified_relations_person_given_names
        ),
        "metadata_qualified_relations_person_iri": (
            facets.metadata_qualified_relations_person_iri
        ),
        "metadata_qualified_relations_role_iri": (
            facets.metadata_qualified_relations_role_iri
        ),
        "metadata_qualified_relations_role_labels_cs": (
            facets.metadata_qualified_relations_role_labels_cs
        ),
        "metadata_qualified_relations_role_labels_en": (
            facets.metadata_qualified_relations_role_labels_en
        ),
        "metadata_qualified_relations_role_labels_lang": (
            facets.metadata_qualified_relations_role_labels_lang
        ),
        "metadata_related_resources_identifier_identifier_scheme": (
            facets.metadata_related_resources_identifier_identifier_scheme
        ),
        "metadata_related_resources_identifier_iri": (
            facets.metadata_related_resources_identifier_iri
        ),
        "metadata_related_resources_identifier_value": (
            facets.metadata_related_resources_identifier_value
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
        "metadata_related_resources_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_lang
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
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_organization_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_organization_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_organization_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_organization_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_organization_iri": (
            facets.metadata_related_resources_qualified_relations_organization_iri
        ),
        "metadata_related_resources_qualified_relations_organization_name_cs": (
            facets.metadata_related_resources_qualified_relations_organization_name_cs
        ),
        "metadata_related_resources_qualified_relations_organization_name_en": (
            facets.metadata_related_resources_qualified_relations_organization_name_en
        ),
        "metadata_related_resources_qualified_relations_organization_name_lang": (
            facets.metadata_related_resources_qualified_relations_organization_name_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_lang
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
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_person_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_person_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_person_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_person_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_person_family_name": (
            facets.metadata_related_resources_qualified_relations_person_family_name
        ),
        "metadata_related_resources_qualified_relations_person_given_names": (
            facets.metadata_related_resources_qualified_relations_person_given_names
        ),
        "metadata_related_resources_qualified_relations_person_iri": (
            facets.metadata_related_resources_qualified_relations_person_iri
        ),
        "metadata_related_resources_qualified_relations_role_iri": (
            facets.metadata_related_resources_qualified_relations_role_iri
        ),
        "metadata_related_resources_qualified_relations_role_labels_cs": (
            facets.metadata_related_resources_qualified_relations_role_labels_cs
        ),
        "metadata_related_resources_qualified_relations_role_labels_en": (
            facets.metadata_related_resources_qualified_relations_role_labels_en
        ),
        "metadata_related_resources_qualified_relations_role_labels_lang": (
            facets.metadata_related_resources_qualified_relations_role_labels_lang
        ),
        "metadata_related_resources_relation_type": (
            facets.metadata_related_resources_relation_type
        ),
        "metadata_related_resources_time_references_date": (
            facets.metadata_related_resources_time_references_date
        ),
        "metadata_related_resources_time_references_date_information": (
            facets.metadata_related_resources_time_references_date_information
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
        "metadata_subjects_definition_cs": facets.metadata_subjects_definition_cs,
        "metadata_subjects_definition_en": facets.metadata_subjects_definition_en,
        "metadata_subjects_definition_lang": facets.metadata_subjects_definition_lang,
        "metadata_subjects_in_subject_scheme_iri": (
            facets.metadata_subjects_in_subject_scheme_iri
        ),
        "metadata_subjects_in_subject_scheme_labels_cs": (
            facets.metadata_subjects_in_subject_scheme_labels_cs
        ),
        "metadata_subjects_in_subject_scheme_labels_en": (
            facets.metadata_subjects_in_subject_scheme_labels_en
        ),
        "metadata_subjects_in_subject_scheme_labels_lang": (
            facets.metadata_subjects_in_subject_scheme_labels_lang
        ),
        "metadata_subjects_iri": facets.metadata_subjects_iri,
        "metadata_subjects_title_cs": facets.metadata_subjects_title_cs,
        "metadata_subjects_title_en": facets.metadata_subjects_title_en,
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
        "metadata_terms_of_use_contacts_organization_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_lang
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
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_organization_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_organization_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_organization_external_identifiers": (
            facets.metadata_terms_of_use_contacts_organization_external_identifiers
        ),
        "metadata_terms_of_use_contacts_organization_iri": (
            facets.metadata_terms_of_use_contacts_organization_iri
        ),
        "metadata_terms_of_use_contacts_organization_name_cs": (
            facets.metadata_terms_of_use_contacts_organization_name_cs
        ),
        "metadata_terms_of_use_contacts_organization_name_en": (
            facets.metadata_terms_of_use_contacts_organization_name_en
        ),
        "metadata_terms_of_use_contacts_organization_name_lang": (
            facets.metadata_terms_of_use_contacts_organization_name_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang
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
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_person_affiliations_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_person_affiliations_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_person_affiliations_external_identifiers": (
            facets.metadata_terms_of_use_contacts_person_affiliations_external_identifiers
        ),
        "metadata_terms_of_use_contacts_person_affiliations_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_lang
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
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_person_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_person_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_person_external_identifiers": (
            facets.metadata_terms_of_use_contacts_person_external_identifiers
        ),
        "metadata_terms_of_use_contacts_person_family_name": (
            facets.metadata_terms_of_use_contacts_person_family_name
        ),
        "metadata_terms_of_use_contacts_person_given_names": (
            facets.metadata_terms_of_use_contacts_person_given_names
        ),
        "metadata_terms_of_use_contacts_person_iri": (
            facets.metadata_terms_of_use_contacts_person_iri
        ),
        "metadata_terms_of_use_description_cs": (
            facets.metadata_terms_of_use_description_cs
        ),
        "metadata_terms_of_use_description_en": (
            facets.metadata_terms_of_use_description_en
        ),
        "metadata_terms_of_use_description_lang": (
            facets.metadata_terms_of_use_description_lang
        ),
        "metadata_terms_of_use_iri": facets.metadata_terms_of_use_iri,
        "metadata_terms_of_use_license": facets.metadata_terms_of_use_license,
        "metadata_time_references_date": facets.metadata_time_references_date,
        "metadata_time_references_date_information": (
            facets.metadata_time_references_date_information
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
        "metadata_validation_results_labels_lang": (
            facets.metadata_validation_results_labels_lang
        ),
        "metadata_version": facets.metadata_version,
        "state": facets.state,
        "state_timestamp": facets.state_timestamp,
        **getattr(I18nRDMSearchOptions, "facets", {}),
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
        "metadata_alternate_titles_title_lang": (
            facets.metadata_alternate_titles_title_lang
        ),
        "metadata_alternate_titles_type": facets.metadata_alternate_titles_type,
        "metadata_descriptions_cs": facets.metadata_descriptions_cs,
        "metadata_descriptions_en": facets.metadata_descriptions_en,
        "metadata_descriptions_lang": facets.metadata_descriptions_lang,
        "metadata_distribution_data_services_access_services_endpoint_urls": (
            facets.metadata_distribution_data_services_access_services_endpoint_urls
        ),
        "metadata_distribution_data_services_access_services_iri": (
            facets.metadata_distribution_data_services_access_services_iri
        ),
        "metadata_distribution_data_services_access_services_labels_cs": (
            facets.metadata_distribution_data_services_access_services_labels_cs
        ),
        "metadata_distribution_data_services_access_services_labels_en": (
            facets.metadata_distribution_data_services_access_services_labels_en
        ),
        "metadata_distribution_data_services_access_services_labels_lang": (
            facets.metadata_distribution_data_services_access_services_labels_lang
        ),
        "metadata_distribution_data_services_descriptions_cs": (
            facets.metadata_distribution_data_services_descriptions_cs
        ),
        "metadata_distribution_data_services_descriptions_en": (
            facets.metadata_distribution_data_services_descriptions_en
        ),
        "metadata_distribution_data_services_descriptions_lang": (
            facets.metadata_distribution_data_services_descriptions_lang
        ),
        "metadata_distribution_data_services_documentations_iri": (
            facets.metadata_distribution_data_services_documentations_iri
        ),
        "metadata_distribution_data_services_documentations_labels_cs": (
            facets.metadata_distribution_data_services_documentations_labels_cs
        ),
        "metadata_distribution_data_services_documentations_labels_en": (
            facets.metadata_distribution_data_services_documentations_labels_en
        ),
        "metadata_distribution_data_services_documentations_labels_lang": (
            facets.metadata_distribution_data_services_documentations_labels_lang
        ),
        "metadata_distribution_data_services_iri": (
            facets.metadata_distribution_data_services_iri
        ),
        "metadata_distribution_data_services_specifications_iri": (
            facets.metadata_distribution_data_services_specifications_iri
        ),
        "metadata_distribution_data_services_specifications_labels_cs": (
            facets.metadata_distribution_data_services_specifications_labels_cs
        ),
        "metadata_distribution_data_services_specifications_labels_en": (
            facets.metadata_distribution_data_services_specifications_labels_en
        ),
        "metadata_distribution_data_services_specifications_labels_lang": (
            facets.metadata_distribution_data_services_specifications_labels_lang
        ),
        "metadata_distribution_data_services_title": (
            facets.metadata_distribution_data_services_title
        ),
        "metadata_distribution_downloadable_files_access_urls": (
            facets.metadata_distribution_downloadable_files_access_urls
        ),
        "metadata_distribution_downloadable_files_byte_size": (
            facets.metadata_distribution_downloadable_files_byte_size
        ),
        "metadata_distribution_downloadable_files_checksum": (
            facets.metadata_distribution_downloadable_files_checksum
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_iri": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_iri
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_cs": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_cs
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_en": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_en
        ),
        "metadata_distribution_downloadable_files_conforms_to_schemas_labels_lang": (
            facets.metadata_distribution_downloadable_files_conforms_to_schemas_labels_lang
        ),
        "metadata_distribution_downloadable_files_download_urls": (
            facets.metadata_distribution_downloadable_files_download_urls
        ),
        "metadata_distribution_downloadable_files_format": (
            facets.metadata_distribution_downloadable_files_format
        ),
        "metadata_distribution_downloadable_files_iri": (
            facets.metadata_distribution_downloadable_files_iri
        ),
        "metadata_distribution_downloadable_files_media_type_iri": (
            facets.metadata_distribution_downloadable_files_media_type_iri
        ),
        "metadata_distribution_downloadable_files_media_type_labels_cs": (
            facets.metadata_distribution_downloadable_files_media_type_labels_cs
        ),
        "metadata_distribution_downloadable_files_media_type_labels_en": (
            facets.metadata_distribution_downloadable_files_media_type_labels_en
        ),
        "metadata_distribution_downloadable_files_media_type_labels_lang": (
            facets.metadata_distribution_downloadable_files_media_type_labels_lang
        ),
        "metadata_distribution_downloadable_files_title": (
            facets.metadata_distribution_downloadable_files_title
        ),
        "metadata_funding_references_award_title": (
            facets.metadata_funding_references_award_title
        ),
        "metadata_funding_references_funders_funder_identifier_scheme_uri": (
            facets.metadata_funding_references_funders_funder_identifier_scheme_uri
        ),
        "metadata_funding_references_funders_funder_identifier_type": (
            facets.metadata_funding_references_funders_funder_identifier_type
        ),
        "metadata_funding_references_funders_funder_identifier_value": (
            facets.metadata_funding_references_funders_funder_identifier_value
        ),
        "metadata_funding_references_funders_funder_name": (
            facets.metadata_funding_references_funders_funder_name
        ),
        "metadata_funding_references_funders_iri": (
            facets.metadata_funding_references_funders_iri
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
        "metadata_is_described_by_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_alternate_names_lang
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
        "metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_organization_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_organization_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_organization_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_organization_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_organization_iri": (
            facets.metadata_is_described_by_qualified_relations_organization_iri
        ),
        "metadata_is_described_by_qualified_relations_organization_name_cs": (
            facets.metadata_is_described_by_qualified_relations_organization_name_cs
        ),
        "metadata_is_described_by_qualified_relations_organization_name_en": (
            facets.metadata_is_described_by_qualified_relations_organization_name_en
        ),
        "metadata_is_described_by_qualified_relations_organization_name_lang": (
            facets.metadata_is_described_by_qualified_relations_organization_name_lang
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_iri": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_iri
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_en": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_en
        ),
        "metadata_is_described_by_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_is_described_by_qualified_relations_person_affiliations_name_lang
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
        "metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_is_described_by_qualified_relations_person_external_identifier_type": (
            facets.metadata_is_described_by_qualified_relations_person_external_identifier_type
        ),
        "metadata_is_described_by_qualified_relations_person_external_identifiers": (
            facets.metadata_is_described_by_qualified_relations_person_external_identifiers
        ),
        "metadata_is_described_by_qualified_relations_person_family_name": (
            facets.metadata_is_described_by_qualified_relations_person_family_name
        ),
        "metadata_is_described_by_qualified_relations_person_given_names": (
            facets.metadata_is_described_by_qualified_relations_person_given_names
        ),
        "metadata_is_described_by_qualified_relations_person_iri": (
            facets.metadata_is_described_by_qualified_relations_person_iri
        ),
        "metadata_is_described_by_qualified_relations_role_iri": (
            facets.metadata_is_described_by_qualified_relations_role_iri
        ),
        "metadata_is_described_by_qualified_relations_role_labels_cs": (
            facets.metadata_is_described_by_qualified_relations_role_labels_cs
        ),
        "metadata_is_described_by_qualified_relations_role_labels_en": (
            facets.metadata_is_described_by_qualified_relations_role_labels_en
        ),
        "metadata_is_described_by_qualified_relations_role_labels_lang": (
            facets.metadata_is_described_by_qualified_relations_role_labels_lang
        ),
        "metadata_locations_bbox_LowerCorners": (
            facets.metadata_locations_bbox_LowerCorners
        ),
        "metadata_locations_bbox_UpperCorners": (
            facets.metadata_locations_bbox_UpperCorners
        ),
        "metadata_locations_bbox_crs": facets.metadata_locations_bbox_crs,
        "metadata_locations_bbox_dimensions": facets.metadata_locations_bbox_dimensions,
        "metadata_locations_dataset_relations": (
            facets.metadata_locations_dataset_relations
        ),
        "metadata_locations_geometry_iri": facets.metadata_locations_geometry_iri,
        "metadata_locations_geometry_labels_cs": (
            facets.metadata_locations_geometry_labels_cs
        ),
        "metadata_locations_geometry_labels_en": (
            facets.metadata_locations_geometry_labels_en
        ),
        "metadata_locations_geometry_labels_lang": (
            facets.metadata_locations_geometry_labels_lang
        ),
        "metadata_locations_iri": facets.metadata_locations_iri,
        "metadata_locations_location_names": facets.metadata_locations_location_names,
        "metadata_locations_related_object_identifiers_identifier_identifier_scheme": (
            facets.metadata_locations_related_object_identifiers_identifier_identifier_scheme
        ),
        "metadata_locations_related_object_identifiers_identifier_iri": (
            facets.metadata_locations_related_object_identifiers_identifier_iri
        ),
        "metadata_locations_related_object_identifiers_identifier_value": (
            facets.metadata_locations_related_object_identifiers_identifier_value
        ),
        "metadata_locations_related_object_identifiers_iri": (
            facets.metadata_locations_related_object_identifiers_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_alternate_names_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_organization_name_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_organization_name_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_alternate_names_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_affiliations_name_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_addresses_labels_lang
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_dataBoxes": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_dataBoxes
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_emails": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_emails
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_phones": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_contact_points_phones
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_external_identifier_type": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_external_identifier_type
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_external_identifiers": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_external_identifiers
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_family_name": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_family_name
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_given_names": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_given_names
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_person_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_person_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_iri": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_iri
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_cs": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_cs
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_en": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_en
        ),
        "metadata_locations_related_object_identifiers_qualified_relations_role_labels_lang": (
            facets.metadata_locations_related_object_identifiers_qualified_relations_role_labels_lang
        ),
        "metadata_locations_related_object_identifiers_relation_type": (
            facets.metadata_locations_related_object_identifiers_relation_type
        ),
        "metadata_locations_related_object_identifiers_time_references_date": (
            facets.metadata_locations_related_object_identifiers_time_references_date
        ),
        "metadata_locations_related_object_identifiers_time_references_date_information": (
            facets.metadata_locations_related_object_identifiers_time_references_date_information
        ),
        "metadata_locations_related_object_identifiers_time_references_date_type": (
            facets.metadata_locations_related_object_identifiers_time_references_date_type
        ),
        "metadata_locations_related_object_identifiers_time_references_iri": (
            facets.metadata_locations_related_object_identifiers_time_references_iri
        ),
        "metadata_locations_related_object_identifiers_title": (
            facets.metadata_locations_related_object_identifiers_title
        ),
        "metadata_locations_related_object_identifiers_type": (
            facets.metadata_locations_related_object_identifiers_type
        ),
        "metadata_other_languages": facets.metadata_other_languages,
        "metadata_primary_language": facets.metadata_primary_language,
        "metadata_provenances_iri": facets.metadata_provenances_iri,
        "metadata_provenances_labels_cs": facets.metadata_provenances_labels_cs,
        "metadata_provenances_labels_en": facets.metadata_provenances_labels_en,
        "metadata_provenances_labels_lang": facets.metadata_provenances_labels_lang,
        "metadata_publication_year": facets.metadata_publication_year,
        "metadata_qualified_relations_iri": facets.metadata_qualified_relations_iri,
        "metadata_qualified_relations_organization_alternate_names_cs": (
            facets.metadata_qualified_relations_organization_alternate_names_cs
        ),
        "metadata_qualified_relations_organization_alternate_names_en": (
            facets.metadata_qualified_relations_organization_alternate_names_en
        ),
        "metadata_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_qualified_relations_organization_alternate_names_lang
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
        "metadata_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_organization_external_identifier_type": (
            facets.metadata_qualified_relations_organization_external_identifier_type
        ),
        "metadata_qualified_relations_organization_external_identifiers": (
            facets.metadata_qualified_relations_organization_external_identifiers
        ),
        "metadata_qualified_relations_organization_iri": (
            facets.metadata_qualified_relations_organization_iri
        ),
        "metadata_qualified_relations_organization_name_cs": (
            facets.metadata_qualified_relations_organization_name_cs
        ),
        "metadata_qualified_relations_organization_name_en": (
            facets.metadata_qualified_relations_organization_name_en
        ),
        "metadata_qualified_relations_organization_name_lang": (
            facets.metadata_qualified_relations_organization_name_lang
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_qualified_relations_person_affiliations_iri": (
            facets.metadata_qualified_relations_person_affiliations_iri
        ),
        "metadata_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_qualified_relations_person_affiliations_name_en": (
            facets.metadata_qualified_relations_person_affiliations_name_en
        ),
        "metadata_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_qualified_relations_person_affiliations_name_lang
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
        "metadata_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_qualified_relations_person_external_identifier_type": (
            facets.metadata_qualified_relations_person_external_identifier_type
        ),
        "metadata_qualified_relations_person_external_identifiers": (
            facets.metadata_qualified_relations_person_external_identifiers
        ),
        "metadata_qualified_relations_person_family_name": (
            facets.metadata_qualified_relations_person_family_name
        ),
        "metadata_qualified_relations_person_given_names": (
            facets.metadata_qualified_relations_person_given_names
        ),
        "metadata_qualified_relations_person_iri": (
            facets.metadata_qualified_relations_person_iri
        ),
        "metadata_qualified_relations_role_iri": (
            facets.metadata_qualified_relations_role_iri
        ),
        "metadata_qualified_relations_role_labels_cs": (
            facets.metadata_qualified_relations_role_labels_cs
        ),
        "metadata_qualified_relations_role_labels_en": (
            facets.metadata_qualified_relations_role_labels_en
        ),
        "metadata_qualified_relations_role_labels_lang": (
            facets.metadata_qualified_relations_role_labels_lang
        ),
        "metadata_related_resources_identifier_identifier_scheme": (
            facets.metadata_related_resources_identifier_identifier_scheme
        ),
        "metadata_related_resources_identifier_iri": (
            facets.metadata_related_resources_identifier_iri
        ),
        "metadata_related_resources_identifier_value": (
            facets.metadata_related_resources_identifier_value
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
        "metadata_related_resources_qualified_relations_organization_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_organization_alternate_names_lang
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
        "metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_organization_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_organization_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_organization_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_organization_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_organization_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_organization_iri": (
            facets.metadata_related_resources_qualified_relations_organization_iri
        ),
        "metadata_related_resources_qualified_relations_organization_name_cs": (
            facets.metadata_related_resources_qualified_relations_organization_name_cs
        ),
        "metadata_related_resources_qualified_relations_organization_name_en": (
            facets.metadata_related_resources_qualified_relations_organization_name_en
        ),
        "metadata_related_resources_qualified_relations_organization_name_lang": (
            facets.metadata_related_resources_qualified_relations_organization_name_lang
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_alternate_names_lang
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
        "metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_person_affiliations_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_iri": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_iri
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_cs": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_cs
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_en": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_en
        ),
        "metadata_related_resources_qualified_relations_person_affiliations_name_lang": (
            facets.metadata_related_resources_qualified_relations_person_affiliations_name_lang
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
        "metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang": (
            facets.metadata_related_resources_qualified_relations_person_contact_points_addresses_labels_lang
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
        "metadata_related_resources_qualified_relations_person_external_identifier_type": (
            facets.metadata_related_resources_qualified_relations_person_external_identifier_type
        ),
        "metadata_related_resources_qualified_relations_person_external_identifiers": (
            facets.metadata_related_resources_qualified_relations_person_external_identifiers
        ),
        "metadata_related_resources_qualified_relations_person_family_name": (
            facets.metadata_related_resources_qualified_relations_person_family_name
        ),
        "metadata_related_resources_qualified_relations_person_given_names": (
            facets.metadata_related_resources_qualified_relations_person_given_names
        ),
        "metadata_related_resources_qualified_relations_person_iri": (
            facets.metadata_related_resources_qualified_relations_person_iri
        ),
        "metadata_related_resources_qualified_relations_role_iri": (
            facets.metadata_related_resources_qualified_relations_role_iri
        ),
        "metadata_related_resources_qualified_relations_role_labels_cs": (
            facets.metadata_related_resources_qualified_relations_role_labels_cs
        ),
        "metadata_related_resources_qualified_relations_role_labels_en": (
            facets.metadata_related_resources_qualified_relations_role_labels_en
        ),
        "metadata_related_resources_qualified_relations_role_labels_lang": (
            facets.metadata_related_resources_qualified_relations_role_labels_lang
        ),
        "metadata_related_resources_relation_type": (
            facets.metadata_related_resources_relation_type
        ),
        "metadata_related_resources_time_references_date": (
            facets.metadata_related_resources_time_references_date
        ),
        "metadata_related_resources_time_references_date_information": (
            facets.metadata_related_resources_time_references_date_information
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
        "metadata_subjects_definition_cs": facets.metadata_subjects_definition_cs,
        "metadata_subjects_definition_en": facets.metadata_subjects_definition_en,
        "metadata_subjects_definition_lang": facets.metadata_subjects_definition_lang,
        "metadata_subjects_in_subject_scheme_iri": (
            facets.metadata_subjects_in_subject_scheme_iri
        ),
        "metadata_subjects_in_subject_scheme_labels_cs": (
            facets.metadata_subjects_in_subject_scheme_labels_cs
        ),
        "metadata_subjects_in_subject_scheme_labels_en": (
            facets.metadata_subjects_in_subject_scheme_labels_en
        ),
        "metadata_subjects_in_subject_scheme_labels_lang": (
            facets.metadata_subjects_in_subject_scheme_labels_lang
        ),
        "metadata_subjects_iri": facets.metadata_subjects_iri,
        "metadata_subjects_title_cs": facets.metadata_subjects_title_cs,
        "metadata_subjects_title_en": facets.metadata_subjects_title_en,
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
        "metadata_terms_of_use_contacts_organization_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_organization_alternate_names_lang
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
        "metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_organization_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_organization_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_organization_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_organization_external_identifiers": (
            facets.metadata_terms_of_use_contacts_organization_external_identifiers
        ),
        "metadata_terms_of_use_contacts_organization_iri": (
            facets.metadata_terms_of_use_contacts_organization_iri
        ),
        "metadata_terms_of_use_contacts_organization_name_cs": (
            facets.metadata_terms_of_use_contacts_organization_name_cs
        ),
        "metadata_terms_of_use_contacts_organization_name_en": (
            facets.metadata_terms_of_use_contacts_organization_name_en
        ),
        "metadata_terms_of_use_contacts_organization_name_lang": (
            facets.metadata_terms_of_use_contacts_organization_name_lang
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_alternate_names_lang
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
        "metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_person_affiliations_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_person_affiliations_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_person_affiliations_external_identifiers": (
            facets.metadata_terms_of_use_contacts_person_affiliations_external_identifiers
        ),
        "metadata_terms_of_use_contacts_person_affiliations_iri": (
            facets.metadata_terms_of_use_contacts_person_affiliations_iri
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_cs": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_cs
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_en": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_en
        ),
        "metadata_terms_of_use_contacts_person_affiliations_name_lang": (
            facets.metadata_terms_of_use_contacts_person_affiliations_name_lang
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
        "metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang": (
            facets.metadata_terms_of_use_contacts_person_contact_points_addresses_labels_lang
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
        "metadata_terms_of_use_contacts_person_external_identifier_type": (
            facets.metadata_terms_of_use_contacts_person_external_identifier_type
        ),
        "metadata_terms_of_use_contacts_person_external_identifiers": (
            facets.metadata_terms_of_use_contacts_person_external_identifiers
        ),
        "metadata_terms_of_use_contacts_person_family_name": (
            facets.metadata_terms_of_use_contacts_person_family_name
        ),
        "metadata_terms_of_use_contacts_person_given_names": (
            facets.metadata_terms_of_use_contacts_person_given_names
        ),
        "metadata_terms_of_use_contacts_person_iri": (
            facets.metadata_terms_of_use_contacts_person_iri
        ),
        "metadata_terms_of_use_description_cs": (
            facets.metadata_terms_of_use_description_cs
        ),
        "metadata_terms_of_use_description_en": (
            facets.metadata_terms_of_use_description_en
        ),
        "metadata_terms_of_use_description_lang": (
            facets.metadata_terms_of_use_description_lang
        ),
        "metadata_terms_of_use_iri": facets.metadata_terms_of_use_iri,
        "metadata_terms_of_use_license": facets.metadata_terms_of_use_license,
        "metadata_time_references_date": facets.metadata_time_references_date,
        "metadata_time_references_date_information": (
            facets.metadata_time_references_date_information
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
        "metadata_validation_results_labels_lang": (
            facets.metadata_validation_results_labels_lang
        ),
        "metadata_version": facets.metadata_version,
        "state": facets.state,
        "state_timestamp": facets.state_timestamp,
        "expires_at": facets.expires_at,
        "fork_version_id": facets.fork_version_id,
        **getattr(I18nRDMDraftsSearchOptions, "facets", {}),
        "record_status": facets.record_status,
        "has_draft": facets.has_draft,
    }
