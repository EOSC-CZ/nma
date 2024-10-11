from oarepo_runtime.datastreams import (
    StreamEntry,
)

from oarepo_oaipmh_harvester.transformers.rule import (
    OAIRuleTransformer,
    matches,
)

class LinDatTransformer(OAIRuleTransformer):
    def transform(self, entry: StreamEntry):

        md = entry.transformed.setdefault("metadata", {})
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
        # transform_relation(md, entry) #required schema with enum...
        # transform_coverage(md, entry) #no corresponding field
        transform_right(md, entry)




@matches("right")
def transform_right(md, entry, value):
    md.setdefault("rightsList", []).append({"rights": value})

@matches("coverage")
def transform_coverage(md, entry, value):
    pass

@matches("relation")
def transform_relation(md, entry, value):
    pass

@matches("language")
def transform_language(md, entry, value):
    md["language"] = value

@matches("source")
def transform_source(md, entry, value):
    md.setdefault("relatedIdentifiers", []).append({"relatedIdentifier": value, "relatedIdentifierType": "URL", "relationType": "IsSourceOf"})

@matches("identifier")
def transform_identifier(md, entry, value):
    id_type = type_alternate_id(value)
    md.setdefault("alternateIdentifiers", []).append({"alternateIdentifier": value, "alternateIdentifierType": id_type})
    if id_type == "Handle":
        md["url"] = value

@matches("format")
def transform_format(md, entry, value):
    md.setdefault("formats", []).append(value)

@matches("type")
def transform_type(md, entry, value):
    type, match = type_general_converter(value)
    if match:
        md["resourceType"] = {"resourceTypeGeneral": type}
    else:
        md["resourceType"] = {"resourceType": value, "resourceTypeGeneral": "Other"}


@matches("date")
def transform_date(md, entry, value):

    md.setdefault("dates", []).append({"date": value, "dateType": "Issued"})

@matches("publisher")
def transform_publisher(md, entry, value):
    md["publisher"] = {"name": value}

@matches("description")
def transform_description(md, entry, value):
    md.setdefault("descriptions", []).append({"description": value, "descriptionType": "Abstract"})

@matches("subject")
def transform_subject(md, entry, value):
    md.setdefault("subjects", []).append({"subject": value})

@matches("contributor")
def transform_contributor(md, entry, value):
    raise Exception(f'contributor {value}')
    # md.setdefault("contributors", []).append({"name": value, "contributorType": "Other"}) #todo type? required..

@matches("creator")
def transform_creator(md, entry, value):
    md.setdefault("creators", []).append({"name": value})

@matches("title")
def transform_title(md, entry, value):
    md.setdefault("titles", []).append({ "title" : value})


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