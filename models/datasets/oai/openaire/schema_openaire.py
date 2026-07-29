"""DataCite v4.3 JSON to OpenAIRE XML transformations."""

from lxml import etree
from lxml.builder import E

from datacite.xmlutils import (
    Rules,
    dump_etree_helper,
    etree_to_string,
    set_elem_attr,
    set_non_empty_attr,
)

from datacite import schema43 as base_schema43

rules = Rules()

ns = base_schema43.ns
root_attribs = base_schema43.root_attribs
validator = base_schema43.validator

OAI_DATACITE_NS = "http://schema.datacite.org/oai/oai-1.1/"
OAI_DATACITE_SCHEMA_VERSION = "4.3"
OAI_DATACITE_DATACENTRE_SYMBOL = "NMD"


def dump_etree(data):
    """Convert JSON dictionary to DataCite v4.3 XML as ElementTree."""
    resource = dump_etree_helper(data, rules, ns, root_attribs)
    root = etree.Element(f"{{{OAI_DATACITE_NS}}}oai_datacite", nsmap={None: OAI_DATACITE_NS})
    etree.SubElement(root, f"{{{OAI_DATACITE_NS}}}schemaVersion").text = OAI_DATACITE_SCHEMA_VERSION
    etree.SubElement(root, f"{{{OAI_DATACITE_NS}}}datacentreSymbol").text = OAI_DATACITE_DATACENTRE_SYMBOL
    payload = etree.SubElement(root, f"{{{OAI_DATACITE_NS}}}payload")
    payload.append(resource)
    return root


def tostring(data, **kwargs):
    """Convert JSON dictionary to DataCite v4.3 XML as string."""
    return etree_to_string(dump_etree(data), **kwargs)


@rules.rule("identifiers")
def identifiers(path, values):
    primary = None
    alt = None

    type_mapping = {
        "ark": "ARK",
        "doi": "DOI",
        "handle": "Handle",
        "purl": "PURL",
        "urn": "URN",
        "url": "URL",
    }

    for i, value in enumerate(values):
        raw_type = value.get("identifierType", "")
        identifier = value.get("identifier")
        id_type = type_mapping.get(raw_type.lower())
        if not id_type:
            continue

        if i == 0:
            primary = E.identifier(identifier, identifierType=id_type)
        else:
            if alt is None:
                alt = E.alternateIdentifiers()
            elem = E.alternateIdentifier(identifier)
            elem.set("alternateIdentifierType", id_type)
            alt.append(elem)

    if alt is None:
        return primary
    return primary, alt


@rules.rule("creators")
def creators(path, values):
    return base_schema43.creators(path, values)


@rules.rule("titles")
def titles(path, values):
    return base_schema43.titles(path, values)


@rules.rule("publisher")
def publisher(path, value):
    return base_schema43.publisher(path, value)


@rules.rule("publicationYear")
def publication_year(path, value):
    return base_schema43.publication_year(path, value)


@rules.rule("subjects")
def subjects(path, values):
    return base_schema43.subjects(path, values)


@rules.rule("contributors")
def contributors(path, values):
    return base_schema43.contributors(path, values)


@rules.rule("dates")
def dates(path, values):
    """Transform dates."""
    allowed_date_types = {"Issued", "Created", "Available", "Updated"}

    if not values:
        return

    root = E.dates()
    for value in values:
        dtype = value.get("dateType")
        if dtype not in allowed_date_types:
            continue
        elem = E.date(value["date"], dateType=dtype)
        set_elem_attr(elem, "dateInformation", value)
        root.append(elem)

    return root


@rules.rule("language")
def language(path, value):
    return base_schema43.language(path, value)


@rules.rule("types")
def resource_type(path, value):
    """Transform resourceType."""
    allowed_resource_types = {
        "Collection",
        "Other",
        "Sound",
        "Text",
        "Workflow",
        "Software",
        "Image",
        "Dataset",
        "InteractiveResource",
    }
    elem = E.resourceType()

    rtype = value.get("resourceTypeGeneral")
    if rtype not in allowed_resource_types:
        rtype = "Dataset"

    elem.set("resourceTypeGeneral", rtype)
    if value.get("resourceType"):
        elem.text = value["resourceType"]

    return elem


@rules.rule("relatedIdentifiers")
def related_identifiers(path, values):
    """Transform relatedIdentifiers (drop unsupported relationTypes)."""
    if not values:
        return

    type_map = {
        "DOI": "DOI",
        "URL": "URL",
        "URN": "URN",
        "Handle": "Handle",
    }
    allowed_identifier_types = {"DOI", "URL", "URN", "Handle"}

    allowed_relations = {
        "IsCitedBy",
        "References",
        "IsSupplementTo",
        "IsSupplementedBy",
        "IsPartOf",
        "HasPart",
        "IsReferencedBy",
    }

    root = E.relatedIdentifiers()

    for value in values:
        rid_type = type_map.get(value.get("relatedIdentifierType"))
        if rid_type not in allowed_identifier_types:
            continue
        rel_type = value.get("relationType")
        if rel_type not in allowed_relations:
            continue

        elem = E.relatedIdentifier()
        elem.text = value["relatedIdentifier"]
        elem.set("relatedIdentifierType", rid_type)
        elem.set("relationType", rel_type)
        root.append(elem)

    if len(root) == 0:
        return
    return root


@rules.rule("sizes")
def sizes(path, values):
    return base_schema43.sizes(path, values)


@rules.rule("formats")
def formats(path, values):
    return base_schema43.formats(path, values)


@rules.rule("version")
def version(path, value):
    return base_schema43.version(path, value)


@rules.rule("rightsList")
def rights(path, values):
    """Transform rights."""
    if not values:
        return

    root = E.rightsList()
    root.append(E.rights(rightsURI="info:eu-repo/semantics/openAccess"))

    for value in values:
        if "rights" in value and value["rights"] is not None:
            elem = E.rights(value["rights"])
        else:
            elem = E.rights()

        if value.get("rightsUri"):
            elem.set("rightsURI", value["rightsUri"])

        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        root.append(elem)

    return root


@rules.rule("descriptions")
def descriptions(path, values):
    return base_schema43.descriptions(path, values)


@rules.rule("geoLocations")
def geolocations(path, values):
    return base_schema43.geolocations(path, values)


@rules.rule("fundingReferences")
def fundingreferences(path, values):
    return base_schema43.fundingreferences(path, values)
