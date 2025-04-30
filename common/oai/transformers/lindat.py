import sys
from urllib.parse import urljoin, urlparse

import lxml.html
import pycountry
import requests
import tqdm
import yaml
from invenio_access.permissions import system_identity
from oarepo_oaipmh_harvester.readers.sickle import SickleReader
from oarepo_oaipmh_harvester.transformers.rule import (
    OAIRuleTransformer,
    matches,
)
from oarepo_runtime.datastreams import StreamBatch, StreamEntry

LINDAT_LANGUAGE = "en"
LINDAT_LANGUAGE_IRI = "https://publications.europa.eu/resource/authority/language/ENG"

requests_session = requests.Session()


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
        transform_relation(md, entry)
        transform_coverage(md, entry)
        transform_right(md, entry)

        md["is_described_by"] = [
            {
                "iri": md.get("iri"),
                "dates_updated": [],
                "languages": [{"iri": LINDAT_LANGUAGE_IRI}],
                "original_repositories": [
                    {
                        "iri": "https://lindat.mff.cuni.cz/repository/",
                        "labels": [
                            {"lang": "en", "value": "LINDAT/CLARIAH-CZ"},
                        ],
                    }
                ],
            }
        ]
        md.setdefault("descriptions", [])


@matches("right")
def transform_right(md, entry, value):
    raise Exception("Rights not supported yet", value)


@matches("coverage")
def transform_coverage(md, entry, value):
    md.setdefault("locations", []).append({"location_names": [value]})


@matches("relation")
def transform_relation(md, entry, value):
    identifier_scheme = identifier_scheme_from_value(value)
    rel = {
        "relation_type": {
            "iri": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/#references"
        },
        "identifier": {
            "value": value,
            "identifier_scheme": identifier_scheme,
        },
    }
    relation_title = get_page_title(value)
    if relation_title:
        rel["title"] = relation_title
    md.setdefault("related_resources", []).append(rel)


def convert_language_code_3_to_3(code):
    try:
        lang = pycountry.languages.get(alpha_3=code)
        return lang.alpha_3
    except AttributeError:
        return "und"  # or raise an exception if preferred


@matches("language")
def transform_language(md, entry, value):
    md["primary_language"] = {
        "iri": "https://publications.europa.eu/resource/authority/language/{}".format(
            convert_language_code_3_to_3(value).upper()
        ),
    }


@matches("source")
def transform_source(md, entry, value):
    rel = {
        "relation_type": {
            "iri": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/#issourceof"
        },
        "identifier": {
            "value": value,
            "identifier_scheme": "urn:iri",
        },
    }

    relation_title = get_page_title(value)
    if relation_title:
        rel["title"] = relation_title

    md.setdefault("related_resources", []).append(rel)


@matches("identifier")
def transform_identifier(md, entry, value):
    id_type = identifier_scheme_from_value(value)

    md.setdefault("identifiers", []).append(
        {"value": value, "identifier_scheme": id_type}
    )
    if id_type == "https://handle.net/":
        md["iri"] = value


@matches("format")
def transform_format(md, entry, value):
    # formats are only on distribution level in ccmm, so can not transform the top-level ones
    pass


@matches("type")
def transform_type(md, entry, value):
    type, match = type_general_converter(value)
    md["resource_type"] = {"iri": type}


@matches("date")
def transform_date(md, entry, value):
    md.setdefault("time_references", []).append(
        {
            "date": value,
            "date_type": {
                "iri": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/dateType/#issued",
            },
        }
    )


@matches("publisher")
def transform_publisher(md, entry, value):
    transform_organization(
        md,
        value,
        "https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/publisher/",
    )


@matches("description")
def transform_description(md, entry, value):
    md.setdefault("descriptions", []).append({"value": value, "lang": LINDAT_LANGUAGE})


@matches("subject")
def transform_subject(md, entry, value):
    md.setdefault("subjects", []).append(
        {"title": {"lang": LINDAT_LANGUAGE, "value": value}}
    )


@matches("contributor")
def transform_contributor(md, entry, value):
    transform_person(
        md,
        value,
        "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/contributorType/#other",
    )


@matches("creator")
def transform_creator(md, entry, value):
    transform_person(
        md,
        value,
        "https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/creator/",
    )


def transform_person(md, value, role):
    value = value.split(", ")
    if len(value) > 1:
        family_name = value[0]
        given_names = value[1:]
    else:
        family_name = value[0]
        given_names = []

    md.setdefault("qualified_relations", []).append(
        {
            "role": {
                "iri": role,
            },
            "person": {
                "family_name": family_name,
                "given_names": given_names,
            },
        }
    )


def transform_organization(md, value, role):
    md.setdefault("qualified_relations", []).append(
        {
            "role": {
                "iri": role,
            },
            "organization": {
                "name": {
                    "lang": "und",
                    "value": value,
                }
            },
        }
    )


@matches("title")
def transform_title(md, entry, value):
    if "title" not in md:
        md["title"] = value
    else:
        # set alternate title
        md.setdefault("alternate_titles", []).append(
            {"title": {"lang": LINDAT_LANGUAGE, "value": value}, "type": "Other"}
        )


def extract_protocol_and_host(url_string):
    try:
        result = urlparse(url_string)
        if all([result.scheme, result.netloc]):  # Valid URL has both scheme and netloc
            return f"{result.scheme}://{result.netloc}/"
        return None
    except:
        return None


def identifier_scheme_from_value(id):
    if id.startswith("http://hdl.handle.net"):
        return "https://handle.net/"
    elif (
        id.startswith("doi:")
        or id.startswith("https://doi.org/")
        or id.startswith("http://doi.org/")
    ):
        return "https://doi.org/"
    elif id.startswith("http://") or id.startswith("https://"):
        return "urn:iri"
    else:
        return "ID"


def type_general_converter(input_type):
    enum_types = {
        "Audiovisual": "http://purl.org/coar/resource_type/F8RT-TJK0",  # artistic work
        "Book": "http://purl.org/coar/resource_type/c_2f33",  # book
        "BookChapter": "http://purl.org/coar/resource_type/c_3248",  # book part
        "Collection": "http://purl.org/coar/resource_type/RMP5-3GQ6",  # collection
        "ComputationalNotebook": "http://purl.org/coar/resource_type/H41Y-FW7B",  # laboratory notebook
        "ConferencePaper": "http://purl.org/coar/resource_type/c_5794",  # conference paper
        "ConferenceProceeding": "http://purl.org/coar/resource_type/c_f744",  # conference proceedings
        "DataPaper": "http://purl.org/coar/resource_type/c_beb9",  # data paper
        "Dataset": "http://purl.org/coar/resource_type/c_ddb1",  # dataset
        "Dissertation": "http://purl.org/coar/resource_type/c_db06",  # doctoral thesis
        "Event": "http://purl.org/coar/resource_type/c_c94f",  # conference output
        "Image": "http://purl.org/coar/resource_type/c_ecc8",  # still image
        "Instrument": "http://purl.org/coar/resource_type/8KJG-QS0Y",  # research instrument
        "InteractiveResource": "http://purl.org/coar/resource_type/c_e9a0",  # interactive resource
        "Journal": "http://purl.org/coar/resource_type/c_0640",  # journal
        "JournalArticle": "http://purl.org/coar/resource_type/c_6501",  # journal article
        "Model": "http://purl.org/coar/resource_type/c_1843",  # other
        "OutputManagementPlan": "http://purl.org/coar/resource_type/c_ab20",  # data management plan
        "PeerReview": "http://purl.org/coar/resource_type/H9BQ-739P",  # peer review
        "PhysicalObject": "http://purl.org/coar/resource_type/S7R1-K5P0",  # physical sample
        "Preprint": "http://purl.org/coar/resource_type/c_816b",  # preprint
        "Report": "http://purl.org/coar/resource_type/c_93fc",  # report
        "Service": "http://purl.org/coar/resource_type/c_1843",  # other
        "Software": "http://purl.org/coar/resource_type/c_c950",  # research software
        "Sound": "http://purl.org/coar/resource_type/c_18cc",  # sound
        "Standard": "http://purl.org/coar/resource_type/c_71bd",  # technical documentation
        "StudyRegistration": "http://purl.org/coar/resource_type/YZ1N-ZFT9",  # research protocol
        "Text": "http://purl.org/coar/resource_type/c_18cf",  # text
        "Workflow": "http://purl.org/coar/resource_type/c_393c",  # workflow
        "Other": "http://purl.org/coar/resource_type/c_1843",  # other
    }

    input_type_lower = input_type.lower()
    for enum_type, enum_value in enum_types.items():
        if input_type_lower == enum_type.lower():
            return enum_value, True

    return enum_types["Other"], False


def get_page_title(url, allow_refresh=True) -> str | None:
    try:
        # Fetch the page content
        response = requests_session.get(
            url,
            headers={"User-Agent": "Lindat Harvester"},  # Some sites require user-agent
            timeout=(2, 5),  # Connect timeout, read timeout
        )
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parse the HTML with lxml
        tree = lxml.html.fromstring(response.content)

        # check for <meta http-equiv="refresh" content="0;url=" and redirect there
        refresh_meta = tree.xpath("//meta[@http-equiv='refresh']/@content")
        if refresh_meta and allow_refresh:
            redirect_url = refresh_meta[0].split("url=")[-1]
            # the redirect_url might be relative, so we need to resolve it
            if not redirect_url.startswith("http"):
                base_url = urlparse(response.url)
                redirect_url = urljoin(base_url.geturl(), redirect_url)
            return get_page_title(redirect_url, allow_refresh=False)

        # Extract the title using XPath
        title = tree.xpath("//title/text()")

        return title[0].strip() if title else None

    except Exception:
        return None


if __name__ == "__main__":

    def harvest():
        with open("lindat_harvested.yaml", "w") as f:
            reader = SickleReader(
                oai_config={"setspecs": "", "metadataprefix": "oai_dc"},
                source="http://lindat.mff.cuni.cz/repository/oai/request?",
            )
            transformer = LinDatTransformer(identity=system_identity)
            first = True
            for entry in tqdm.tqdm(reader):
                if entry.deleted:
                    continue
                batch = StreamBatch(entries=[entry], context={})
                transformer.apply(batch)
                if entry.errors:
                    print(
                        "Transformation failed with errors for entry",
                        entry.context["oai"]["identifier"],
                        file=sys.stderr,
                    )
                    print(entry.errors, file=sys.stderr)
                    continue
                if not entry.entry:
                    print(
                        "Transformation failed for entry - empty entry returned",
                        entry.context["oai"]["identifier"],
                        file=sys.stderr,
                    )
                    continue
                if first:
                    first = False
                else:
                    f.write("---\n")
                yaml.safe_dump(entry.entry, f, allow_unicode=True)
                f.flush()

    harvest()
