from oarepo_runtime.records.dumpers.multilingual_dumper import MultilingualDumper


class MultilingualSearchDumperExt(MultilingualDumper):
    """Multilingual search dumper."""

    paths = [
        "metadata/alternate_titles/title",
        "metadata/descriptions",
        "metadata/distributions/conforms_to_schemas/labels",
        "metadata/funding_references/funders/organization/alternate_names",
        "metadata/funding_references/funders/organization/contact_points/addresses/labels",
        "metadata/funding_references/funders/person/affiliations/alternate_names",
        "metadata/funding_references/funders/person/affiliations/contact_points/addresses/labels",
        "metadata/funding_references/funders/person/contact_points/addresses/labels",
        "metadata/is_described_by/conforms_to_standards/labels",
        "metadata/is_described_by/original_repositories/labels",
        "metadata/is_described_by/qualified_relations/organization/alternate_names",
        "metadata/is_described_by/qualified_relations/organization/contact_points/addresses/labels",
        "metadata/is_described_by/qualified_relations/person/affiliations/alternate_names",
        "metadata/is_described_by/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "metadata/is_described_by/qualified_relations/person/contact_points/addresses/labels",
        "metadata/locations/geometry/labels",
        "metadata/locations/related_objects/qualified_relations/organization/alternate_names",
        "metadata/locations/related_objects/qualified_relations/organization/contact_points/addresses/labels",
        "metadata/locations/related_objects/qualified_relations/person/affiliations/alternate_names",
        "metadata/locations/related_objects/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "metadata/locations/related_objects/qualified_relations/person/contact_points/addresses/labels",
        "metadata/locations/related_objects/time_references/date_information",
        "metadata/provenances/labels",
        "metadata/qualified_relations/organization/alternate_names",
        "metadata/qualified_relations/organization/contact_points/addresses/labels",
        "metadata/qualified_relations/person/affiliations/alternate_names",
        "metadata/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "metadata/qualified_relations/person/contact_points/addresses/labels",
        "metadata/related_resources/qualified_relations/organization/alternate_names",
        "metadata/related_resources/qualified_relations/organization/contact_points/addresses/labels",
        "metadata/related_resources/qualified_relations/person/affiliations/alternate_names",
        "metadata/related_resources/qualified_relations/person/affiliations/contact_points/addresses/labels",
        "metadata/related_resources/qualified_relations/person/contact_points/addresses/labels",
        "metadata/related_resources/time_references/date_information",
        "metadata/subjects/definitions",
        "metadata/subjects/title",
        "metadata/terms_of_use/contacts/organization/alternate_names",
        "metadata/terms_of_use/contacts/organization/contact_points/addresses/labels",
        "metadata/terms_of_use/contacts/person/affiliations/alternate_names",
        "metadata/terms_of_use/contacts/person/affiliations/contact_points/addresses/labels",
        "metadata/terms_of_use/contacts/person/contact_points/addresses/labels",
        "metadata/terms_of_use/description",
        "metadata/terms_of_use/license/labels",
        "metadata/time_references/date_information",
        "metadata/validation_results/labels",
    ]
    SUPPORTED_LANGS = ["cs", "en"]

    def dump(self, record, data):
        super().dump(record, data)

    def load(self, record, data):
        super().load(record, data)
