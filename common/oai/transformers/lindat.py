from typing import Any

from oarepo_oaipmh_harvester.transformers.rule import (
    OAIRuleTransformer,
    matches,
)
from oarepo_runtime.datastreams import (
    StreamEntry,
)


class LinDatTransformer(OAIRuleTransformer):
    def transform(self, entry: StreamEntry):

        md: dict[str, Any] = entry.transformed.setdefault("metadata", {})
        entry.transformed.setdefault("files", {}).setdefault("enabled", False)
        entry.entry = entry.context["oai"]["metadata"]

        transform_title(md, entry)
        transform_creator(md, entry)
        transform_contributor(md, entry)
        transform_subject(md, entry)
        transform_description(md, entry)
        transform_publisher(md, entry)
        transform_date(md, entry)
        transform_type(md, entry)
        transform_format(md, entry)
        transform_identifier(md, entry)
        transform_source(md, entry)
        transform_language(md, entry)
        transform_relation(md, entry)  # required schema with enum...
        transform_coverage(md, entry)  # no corresponding field
        transform_right(md, entry)


@matches("right")
def transform_right(md, entry, value):
    md["terms_of_use"] = {"description": {"lang": "und", "value": value}}


@matches("coverage")
def transform_coverage(md, entry, value):
    # country
    md.setdefault("locations", []).append(
        {"location_names": [value], "dataset_relation": "coverage"}
    )


@matches("relation")
def transform_relation(md, entry, value):
    md.setdefault("related_resources", []).append(
        {
            "resource_URLs": [value],
            "relation_type": "IsRelatedTo",
        }
    )


@matches("language")
def transform_language(md, entry, value):
    # TODO: should be a vocabulary of languages
    md["primary_language"] = value


@matches("source")
def transform_source(md, entry, value):
    md.setdefault("related_resources", []).append(
        {
            "resource_URLs": [value],
            "relation_type": "IsSourceOf",
        }
    )


@matches("identifier")
def transform_identifier(md, entry, value):
    id_type = type_alternate_id(value)
    md.setdefault("identifiers", []).append(
        {
            # "iri": "",
            "value": value,
            "identifier_scheme": id_type,
        }
    )
    if id_type == "Handle":
        md["iri"] = value


@matches("format")
def transform_format(md, entry, value):
    # TODO: not in the CCMM metadata schema
    # md.setdefault("formats", []).append(value)
    pass


@matches("type")
def transform_type(md, entry, value):
    # TODO: need a dictionary here !!!
    type, match = type_general_converter(value)
    if match:
        md["resource_type"] = type
    else:
        md["resource_type"] = value


@matches("date")
def transform_date(md, entry, value):
    md.setdefault("time_references", []).append({"date": value, "date_type": "Issued"})


@matches("publisher")
def transform_publisher(md, entry, value):
    creator_relation = {
        # "iri": "",
        "role": {
            # "iri": "..."
            "labels": [
                {
                    "lang": "en",
                    "label": "Publisher",
                },
                {
                    "lang": "cs",
                    "label": "Vydavatel",
                },
            ]
        },
        "organization": {"name": value},
    }
    md.setdefault("qualified_relations", []).append(creator_relation)


@matches("description")
def transform_description(md, entry, value):
    md.setdefault("descriptions", []).append({"value": value, "lang": "und"})


@matches("subject")
def transform_subject(md, entry, value):
    subject = {
        # "iri": "",
        # "definition": {},
        "title": {
            "lang": "und",
            "label": value,
        },
        # "classification_code": "",
        # "scheme": ""
    }
    md.setdefault("subjects", []).append(subject)


@matches("contributor")
def transform_contributor(md, entry, value):
    creator_relation = {
        # "iri": "",
        "role": {
            # "iri": "..."
            "labels": [
                {
                    "lang": "en",
                    "label": "Contributor",
                },
                {
                    "lang": "cs",
                    "label": "Přispěvatel",
                },
            ]
        },
        "person": {"full_name": value},
    }
    md.setdefault("qualified_relations", []).append(creator_relation)


@matches("creator")
def transform_creator(md, entry, value):
    creator_relation = {
        # "iri": "",
        "role": {
            # "iri": "..."
            "labels": [
                {
                    "lang": "en",
                    "label": "Creator",
                },
                {
                    "lang": "cs",
                    "label": "Autor",
                },
            ]
        },
        "person": {"full_name": value},
    }
    md.setdefault("qualified_relations", []).append(creator_relation)


@matches("title")
def transform_title(md, entry, value):
    assert isinstance(value, str), "Title must be a string"
    md["title"] = value


def type_alternate_id(id):
    if id.startswith("http://hdl.handle.net"):
        return "Handle"
    else:
        return "ID"


def type_general_converter(input_type):
    enum_types = [
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

    input_type_lower = input_type.lower()
    for enum_type in enum_types:
        if input_type_lower == enum_type.lower():
            return enum_type, True

    return "Other", False
