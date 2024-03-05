from oarepo_runtime.datastreams import (
    StreamEntry,
)

from langdetect import detect
from oarepo_oaipmh_harvester.transformers.rule import (
    OAIRuleTransformer,
    matches,
)

class LinDatTransformer(OAIRuleTransformer):
    def transform(self, entry: StreamEntry):

        md = entry.transformed.setdefault("metadata", {})
        entry.entry = entry.context["oai"]["metadata"]
        entry.context.pop("oai") #todo?

        transform_title(md, entry)
        # transform_creator(md, entry)
        # transform_contributor(md, entry)
        # transform_subject(md, entry)
        # transform_description(md, entry)
        # transform_publisher(md, entry)
        # transform_date(md, entry)
        # transform_type(md, entry)
        # transform_format(md, entry)
        # transform_identifier(md, entry)
        # transform_source(md, entry)
        # transform_language(md, entry)
        # # transform_relation(md, entry) #todo required schema with enum...
        # # transform_coverage(md, entry) #todo no correspondig field
        # transform_right(md, entry)

        print(md)


@matches("right")
def transform_right(md, entry, value):
    md.setdefault("rightsList", []).append({"relatedIdentifiers": value, "relatedIdentifiersType": "????"})

@matches("coverage")
def transform_coverage(md, entry, value):
    pass

@matches("relation")
def transform_relation(md, entry, value):
    md.setdefault("relatedIdentifiers", []).append({"rights": value})

@matches("language")
def transform_language(md, entry, value):
    md["language"] = value #todo multiple?

@matches("source")
def transform_source(md, entry, value):
    md["url"] = value #todo? what if multiple sources?

@matches("identifier")
def transform_identifier(md, entry, value): #todo required schema..
    md.setdefault("alternateIdentifiers", []).append({"alternateIdentifier": value, "alternateIdentifierType": "ID"})

@matches("format")
def transform_format(md, entry, value):
    md.setdefault("formats", []).append(value)

@matches("type")
def transform_type(md, entry, value):
    md.setdefault("types", []).append({"resourceType": value})

@matches("date")
def transform_date(md, entry, value):
    md.setdefault("dates", []).append({"date": value})

@matches("publisher")
def transform_publisher(md, entry, value):
    md["publisher"] = {"name": value} #todo multiple publishers?

@matches("description")
def transform_description(md, entry, value):
    md.setdefault("descriptions", []).append({"description": value})

@matches("subject")
def transform_subject(md, entry, value):
    md.setdefault("subjects", []).append({"subject": value})

@matches("contributor")
def transform_contributor(md, entry, value):
    md.setdefault("creators", []).append({"name": value, "contributorType": "Other"}) #todo type? required..

@matches("creator")
def transform_creator(md, entry, value):
    md.setdefault("contributors", []).append({"name": value})

@matches("title")
def transform_title(md, entry, value):
    # md["titles"] = value
    md.setdefault("titles", []).append({"lang": detect(value), "title" : value}) #todo lang?