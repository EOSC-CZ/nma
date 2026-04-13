
"""DataCite v4.3 JSON to OpenAIRE XML transformations."""

import importlib.resources as importlib_resources

from lxml import etree
from lxml.builder import E

from datacite.jsonutils import validator_factory
from datacite.xmlutils import (
    Rules,
    dump_etree_helper,
    etree_to_string,
    set_elem_attr,
    set_non_empty_attr,
)

rules = Rules()

ns = {
    None: "http://datacite.org/schema/kernel-4",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xml": "xml",
}

root_attribs = {
    "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": "http://datacite.org/schema/kernel-4 "
    "http://schema.datacite.org/meta/kernel-4.3/metadata.xsd",
}

validator = validator_factory(
    importlib_resources.files("datacite") / "schemas/datacite-v4.3.json"
)


def dump_etree(data):
    """Convert JSON dictionary to DataCite v4.3 XML as ElementTree."""
    return dump_etree_helper(data, rules, ns, root_attribs)


def tostring(data, **kwargs):
    """Convert JSON dictionary to DataCite v4.3 XML as string."""
    return etree_to_string(dump_etree(data), **kwargs)



@rules.rule("identifiers")
def identifiers(path, values):
    primary = None
    alt = None

    TYPE_MAPPING = {
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

        id_type_lower = raw_type.lower()

        id_type = TYPE_MAPPING.get(id_type_lower, "URL")

        if i == 0:
            primary = E.identifier(
                identifier,
                identifierType=id_type
            )
        else:
            if alt is None:
                alt = E.alternateIdentifiers()

            elem = E.alternateIdentifier(identifier)
            elem.set("alternateIdentifierType", id_type)
            alt.append(elem)

    if alt is None:
        return primary
    else:
        return primary, alt

def affiliation(root, values):
    """Extract affiliation."""
    vals = values.get("affiliation", [])
    for val in vals:
        if val.get("name"):
            elem = E.affiliation(val["name"])
            # affiliationIdentifier metadata as Attributes
            # (0-1 cardinality, instead of 0-n as list of objects)
            set_elem_attr(elem, "affiliationIdentifier", val)
            set_elem_attr(elem, "affiliationIdentifierScheme", val)
            if val.get("schemeUri"):
                elem.set("schemeURI", val["schemeUri"])
            root.append(elem)


def familyname(root, value):
    """Extract family name."""
    val = value.get("familyName")
    if val:
        root.append(E.familyName(val))


def givenname(root, value):
    """Extract family name."""
    val = value.get("givenName")
    if val:
        root.append(E.givenName(val))


def person_or_org_name(root, value, xml_tagname, json_tagname):
    """Extract creator/contributor name and it's 'nameType' attribute."""
    elem = E(xml_tagname, value[json_tagname])
    set_elem_attr(elem, "nameType", value)
    set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
    root.append(elem)


def nameidentifiers(root, values):
    """Extract nameidentifier."""
    vals = values.get("nameIdentifiers", [])
    for val in vals:
        if val.get("nameIdentifier"):
            elem = E.nameIdentifier(val["nameIdentifier"])
            elem.set("nameIdentifierScheme", val["nameIdentifierScheme"])
            if val.get("schemeUri"):
                elem.set("schemeURI", val["schemeUri"])
            root.append(elem)


@rules.rule("creators")
def creators(path, values):
    """Transform creators."""
    if not values:
        return

    root = E.creators()
    for value in values:
        creator = E.creator()
        person_or_org_name(creator, value, "creatorName", "name")
        givenname(creator, value)
        familyname(creator, value)
        nameidentifiers(creator, value)
        affiliation(creator, value)
        root.append(creator)

    return root


@rules.rule("titles")
def titles(path, values):
    """Transform titles."""
    if not values:
        return
    root = E.titles()

    for value in values:
        elem = etree.Element("title", nsmap=ns)
        elem.text = value["title"]
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        # for backwards compatibility until kernel 5 is released.
        set_non_empty_attr(elem, "titleType", value.get("type"))
        # 'titleType' will supersede 'type' if available
        set_non_empty_attr(elem, "titleType", value.get("titleType"))
        root.append(elem)

    return root


@rules.rule("publisher")
def publisher(path, value):
    """Transform publisher."""
    if not value:
        return
    return E.publisher(value)


@rules.rule("publicationYear")
def publication_year(path, value):
    """Transform publicationYear."""
    if not value:
        return
    return E.publicationYear(str(value))


@rules.rule("pid")
def pid(path, value):
    """Transform internal PID."""
    if not value:
        return
    return E.pid(str(value))


@rules.rule("subjects")
def subjects(path, values):
    """Transform subjects."""
    if not values:
        return

    root = E.subjects()
    for value in values:
        elem = E.subject(value["subject"])
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        set_elem_attr(elem, "subjectScheme", value)
        if value.get("schemeUri"):
            elem.set("schemeURI", value["schemeUri"])
        if value.get("valueUri"):
            elem.set("valueURI", value["valueUri"])
        root.append(elem)
    return root


@rules.rule("contributors")
def contributors(path, values):
    """Transform contributors."""
    if not values:
        return
    allowed_types = {
        "ContactPerson",
        "DataCollector",
        "HostingInstitution",
        "Producer",
        "ProjectLeader",
        "ProjectMember",
        "Researcher",
        "Supervisor",
        "Sponsor",
        "RightsHolder",
    }
    root = E.contributors()
    for value in values:
        contributor = E.contributor()
        person_or_org_name(contributor, value, "contributorName", "name")

        ctype = value.get("contributorType")
        if ctype not in allowed_types:
            ctype = "Other"
        set_elem_attr(contributor, "contributorType", {"contributorType": ctype})

        givenname(contributor, value)
        familyname(contributor, value)
        nameidentifiers(contributor, value)
        affiliation(contributor, value)
        root.append(contributor)

    return root


@rules.rule("dates")
def dates(path, values):
    """Transform dates."""
    ALLOWED_DATE_TYPES = {
        "Issued",
        "Created",
        "Available",
        "Updated"
    }

    DATE_TYPE_MAPPING = {
        "Accepted": "Issued",
        "Submitted": "Created",
        "Copyrighted": "Issued",
        "Valid": "Available",
        "Withdrawn": "Updated",
        "Other": "Updated"
    }
    if not values:
        return

    root = E.dates()

    for value in values:
        dtype = value["dateType"]

        # map unsupported types
        dtype = DATE_TYPE_MAPPING.get(dtype, dtype)

        # fallback safety
        if dtype not in ALLOWED_DATE_TYPES:
            continue  # radši zahodit než fail validátoru

        elem = E.date(value["date"], dateType=dtype)
        set_elem_attr(elem, "dateInformation", value)
        root.append(elem)

    return root


@rules.rule("language")
def language(path, value):
    """Transform language."""
    if not value:
        return
    return E.language(value)

@rules.rule("types")
def resource_type(path, value):
    """Transform resourceType."""
    ALLOWED_RESOURCE_TYPES = {
        "Publication",
        "Dataset",
        "Software",
        "Other"
    }

    RESOURCE_TYPE_MAPPING = {
        "Image": "Dataset",
        "Audio": "Dataset",
        "Video": "Dataset",
        "Model": "Dataset",
        "PhysicalObject": "Other",
        "Workflow": "Software",
        "InteractiveResource": "Other",
        "Event": "Publication",
        "Presentation": "Publication",
        "Poster": "Publication",
        "Lesson": "Publication",
    }
    elem = E.resourceType()

    rtype = value.get("resourceTypeGeneral")

    # map unsupported types
    rtype = RESOURCE_TYPE_MAPPING.get(rtype, rtype)

    # fallback
    if rtype not in ALLOWED_RESOURCE_TYPES:
        rtype = "Other"

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
        "ARK": "URL",
        "PURL": "URL",
        "w3id": "URL",
        "EAN13": "URN",
        "UPC": "URN",
        "ISBN": "URN",
        "ISSN": "URN",
        "EISSN": "URN",
        "PMID": "URN",
        "ISTC": "URN",
        "IGSN": "URN",
    }

    allowed_relations = {
        "IsCitedBy",
        "References",
        "IsSupplementTo",
        "IsSupplementedBy",
        "IsPartOf",
        "HasPart",
        "IsReferencedBy",
    }

    relation_map = {
        "Cites": "References",
        "Describes": "References",
        "Documents": "References",
        "Reviews": "References",
        "Requires": "References",
        "Obsoletes": "References",

        "IsDescribedBy": "IsReferencedBy",
        "IsDocumentedBy": "IsReferencedBy",
        "IsReviewedBy": "IsReferencedBy",
        "IsRequiredBy": "IsReferencedBy",
        "IsObsoletedBy": "IsReferencedBy",
    }

    root = E.relatedIdentifiers()

    for value in values:
        raw_type = value.get("relatedIdentifierType")
        raw_relation = value.get("relationType")

        rid_type = type_map.get(raw_type, "URL")

        rel_type = relation_map.get(raw_relation, raw_relation)

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


def free_text_list(plural, singular, values):
    """List of elements with free text."""
    if not values:
        return
    root = etree.Element(plural)
    for value in values:
        etree.SubElement(root, singular).text = value
    return root


@rules.rule("sizes")
def sizes(path, values):
    """Transform sizes."""
    return free_text_list("sizes", "size", values)


@rules.rule("formats")
def formats(path, values):
    """Transform sizes."""
    return free_text_list("formats", "format", values)


@rules.rule("version")
def version(path, value):
    """Transform version."""
    if not value:
        return
    return E.version(value)


@rules.rule("rightsList")
def rights(path, values):
    """Transform rights."""
    if not values:
        return

    root = E.rightsList()

    root.append(E.rights(rightsURI="info:eu-repo/semantics/openAccess")) #chce tam vzdy info o access u nas vzdy open...

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
    """Transform descriptions."""
    ALLOWED_TYPES = {"Abstract", "Other"}

    TYPE_MAPPING = {
        "Methods": "Other",
        "SeriesInformation": "Other",
        "TableOfContents": "Other",
        "TechnicalInfo": "Other",
    }
    if not values:
        return

    root = E.descriptions()
    for value in values:
        dtype = value["descriptionType"]

        dtype = TYPE_MAPPING.get(dtype, dtype)

        if dtype not in ALLOWED_TYPES:
            dtype = "Other"

        elem = E.description(
            value["description"],
            descriptionType=dtype
        )
        set_non_empty_attr(elem, "{xml}lang", value.get("lang"))
        root.append(elem)

    return root


def geopoint(root, value):
    """Extract a point (either geoLocationPoint or polygonPoint)."""
    root.append(E.pointLongitude(str(value["pointLongitude"])))
    root.append(E.pointLatitude(str(value["pointLatitude"])))


@rules.rule("geoLocations")
def geolocations(path, values):
    """Transform geolocations."""
    if not values:
        return

    root = E.geoLocations()
    for value in values:
        element = E.geoLocation()

        place = value.get("geoLocationPlace")
        if place:
            element.append(E.geoLocationPlace(place))

        point = value.get("geoLocationPoint")
        if point:
            elem = E.geoLocationPoint()
            geopoint(elem, point)
            element.append(elem)

        box = value.get("geoLocationBox")
        if box:
            elem = E.geoLocationBox()
            elem.append(E.westBoundLongitude(str(box["westBoundLongitude"])))
            elem.append(E.eastBoundLongitude(str(box["eastBoundLongitude"])))
            elem.append(E.southBoundLatitude(str(box["southBoundLatitude"])))
            elem.append(E.northBoundLatitude(str(box["northBoundLatitude"])))
            element.append(elem)

        polygons = value.get("geoLocationPolygons", [])
        for polygon in polygons:
            elem = E.geoLocationPolygon()
            points = polygon["polygonPoints"]
            for p in points:
                e = E.polygonPoint()
                geopoint(e, p)
                elem.append(e)
            inPoint = polygon.get("inPolygonPoint")
            if inPoint:
                e = E.inPolygonPoint()
                geopoint(e, inPoint)
                elem.append(e)
            element.append(elem)

        root.append(element)
    return root


@rules.rule("fundingReferences")
def fundingreferences(path, values):
    """Transform funding references."""
    if not values:
        return

    root = E.fundingReferences()
    for value in values:
        element = E.fundingReference()

        element.append(E.funderName(value.get("funderName")))

        identifier = value.get("funderIdentifier")
        if identifier:
            elem = E.funderIdentifier(identifier)
            typev = value.get("funderIdentifierType")
            if typev:
                elem.set("funderIdentifierType", typev)
            element.append(elem)

        number = value.get("awardNumber")
        if number:
            elem = E.awardNumber(number)
            uri = value.get("awardUri")
            if uri:
                elem.set("awardURI", uri)
            element.append(elem)

        title = value.get("awardTitle")
        if title:
            element.append(E.awardTitle(title))
        if len(element):
            root.append(element)
    return root
