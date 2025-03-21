from oarepo_runtime.records.dumpers.multilingual_dumper import MultilingualDumper


class MultilingualSearchDumperExt(MultilingualDumper):
    """Multilingual search dumper."""

    paths = [
        "/metadata/alternate_titles/title",
        "/metadata/descriptions",
        "/metadata/distribution_data_services/access_services/labels",
        "/metadata/distribution_data_services/descriptions",
        "/metadata/distribution_data_services/documentations/labels",
        "/metadata/distribution_data_services/specifications/labels",
        "/metadata/distribution_downloadable_files/conforms_to_schemas/labels",
        "/metadata/distribution_downloadable_files/media_type/labels",
        "/metadata/is_described_by/conforms_to_standards/labels",
        "/metadata/is_described_by/original_repositories/labels",
        "/metadata/is_described_by/qualified_relations/organization/alternate_names",
        "/metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels",
        "/metadata/is_described_by/qualified_relations/organization/name",
        "/metadata/is_described_by/qualified_relations/person/affiliations/alternate_names",
        "/metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "/metadata/is_described_by/qualified_relations/person/affiliations/name",
        "/metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels",
        "/metadata/is_described_by/qualified_relations/role/labels",
        "/metadata/locations/geometry/labels",
        "/metadata/locations/related_object_identifiers/qualified_relations/organization/alternate_names",
        "/metadata/locations/related_object_identifiers/qualified_relations/organization/contact_points/addresses/labels",
        "/metadata/locations/related_object_identifiers/qualified_relations/organization/name",
        "/metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/alternate_names",
        "/metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "/metadata/locations/related_object_identifiers/qualified_relations/person/affiliations/name",
        "/metadata/locations/related_object_identifiers/qualified_relations/person/contact_points/addresses/labels",
        "/metadata/locations/related_object_identifiers/qualified_relations/role/labels",
        "/metadata/provenances/labels",
        "/metadata/qualified_relations/organization/alternate_names",
        "/metadata/qualified_relations/organization/contact_points/addresses/labels",
        "/metadata/qualified_relations/organization/name",
        "/metadata/qualified_relations/person/affiliations/alternate_names",
        "/metadata/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "/metadata/qualified_relations/person/affiliations/name",
        "/metadata/qualified_relations/person/contact_points/addresses/labels",
        "/metadata/qualified_relations/role/labels",
        "/metadata/related_resources/qualified_relations/organization/alternate_names",
        "/metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels",
        "/metadata/related_resources/qualified_relations/organization/name",
        "/metadata/related_resources/qualified_relations/person/affiliations/alternate_names",
        "/metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "/metadata/related_resources/qualified_relations/person/affiliations/name",
        "/metadata/related_resources/qualified_relations/person/contact_points/addresses/labels",
        "/metadata/related_resources/qualified_relations/role/labels",
        "/metadata/subjects/definition",
        "/metadata/subjects/in_subject_scheme/labels",
        "/metadata/subjects/title",
        "/metadata/terms_of_use/contacts/organization/alternate_names",
        "/metadata/terms_of_use/contacts/organization/contact_points/addresses/labels",
        "/metadata/terms_of_use/contacts/organization/name",
        "/metadata/terms_of_use/contacts/person/affiliations/alternate_names",
        "/metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels",
        "/metadata/terms_of_use/contacts/person/affiliations/name",
        "/metadata/terms_of_use/contacts/person/contact_points/addresses/labels",
        "/metadata/validation_results/labels",
    ]
    SUPPORTED_LANGS = ["cs", "en"]

    def dump(self, record, data):
        super().dump(record, data)

    def load(self, record, data):
        super().load(record, data)
