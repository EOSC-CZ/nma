import copy
import re
import sys
import traceback
from typing import Union

import bleach
import tqdm
import yaml
from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams import BaseTransformer, StreamBatch, StreamEntry
from oarepo_runtime.datastreams.types import StreamEntryError

from common.oai.ccmm_tools import full_name_to_person, get_ccmm_lang_iri, get_ccmm_role

UNKNOWN_LANGUAGE_IRI = "https://publications.europa.eu/resource/authority/language/UND"

allowed_tags = set([*bleach.ALLOWED_TAGS, "span", "p", "br"])


class DataRepoTransformer(BaseTransformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, batch: StreamBatch, *args, **kwargs) -> Union[StreamBatch, None]:
        """Applies the transformation to the entry.
        :returns: A StreamEntry. The transformed entry.
                  Raises TransformerError in case of errors.
        """
        for entry in batch.entries:
            try:
                self.transform_entry(entry)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                entry.errors.append(StreamEntryError.from_exception(e))
        return batch

    def transform_entry(self, entry: StreamEntry):
        """
        Transforms the entry.
        """
        entry.entry = convert_record_to_ccmm({**entry.entry})


def convert_record_to_ccmm(rec):
    rec = copy.deepcopy(rec)
    links = rec.pop("links")
    link = links["self"]
    files = rec.pop("files", [])

    id = rec.pop("id")
    orig_md = rec.pop("metadata")

    language = orig_md.pop("language")[0]["slug"]

    transformed = {
        "files": {
            "enabled": False,
        },
        "metadata": {
            "is_described_by": [
                {
                    "iri": link,
                    "dates_updated": [],
                    "languages": [{"iri": get_ccmm_lang_iri(language)}],
                    "original_repositories": [
                        {
                            "iri": "https://datarepo.eosc.cz",
                            "labels": [
                                {"lang": "en", "value": "LINDAT/CLARIAH-CZ"},
                            ],
                        }
                    ],
                }
            ],
        },
    }
    md = transformed["metadata"]
    md["primary_language"] = {
        "iri": get_ccmm_lang_iri(language),
    }

    persistent_identifiers = orig_md.pop("persistentIdentifiers", [])
    if persistent_identifiers:
        print("Persistent identifiers found", persistent_identifiers)
        sys.exit(1)

    for orig_creator in orig_md.pop("creators", []):
        convert_creator(md, orig_creator)

    for orig_contributor in orig_md.pop("contributors", []):
        convert_contributor(md, orig_contributor)
    md["descriptions"] = convert_abstract(orig_md.pop("abstract", {}))

    md["time_references"] = convert_dates(orig_md)
    md["resource_type"] = convert_resource_type(orig_md.pop("resourceType", None))
    md["terms_of_use"] = convert_rights(orig_md.pop("rights", []))

    md["subjects"] = convert_subject_categories(orig_md.pop("subjectCategories", []))
    md["subjects"] += convert_keywords(orig_md.pop("keywords", []))

    md["title"], md["alternate_titles"] = convert_titles(orig_md.pop("titles"))

    md["related_resources"] = convert_related_items(orig_md.pop("relatedItems", []))

    # converted_md["publisher"] = {"name": "data.narodni-repozitar.cz"}

    ensureEmpty(
        orig_md,
        "$schema",
        "InvenioID",
        "_files",
        "accessRights",
        "oarepo:primaryCommunity",
        "oarepo:recordStatus",
    )
    return transformed


def ensureEmpty(data, *exceptions, filter=True):
    for key in data.keys():
        if key not in exceptions:
            if filter:
                filtered_data = {k: v for k, v in data.items() if k not in exceptions}
            else:
                filtered_data = data
            raise Exception(f"Unhandled key: {key} inside data: {filtered_data}")


def convert_creator(md, orig_creator):
    convert_creator_contributor(
        md,
        orig_creator,
        "https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/creator/",
    )


def convert_contributor(md, orig_contributor):
    roles = orig_contributor.pop("role", None)
    role = next(r for r in roles if not r.get("is_ancestor"))
    data_cite_code = role["dataCiteCode"]
    convert_creator_contributor(
        md,
        orig_contributor,
        get_ccmm_role(data_cite_code),
    )


def convert_creator_contributor(md, orig_creator, role_iri):
    name_type = orig_creator.pop("nameType")
    if name_type == "Personal":
        creator = {"person": convert_person(orig_creator)}
    elif name_type == "Organizational":
        creator = {"organization": convert_organization(orig_creator)}
    else:
        raise Exception(f"Unknown name type: {name_type}")
    ensureEmpty(
        orig_creator,
        # if organization, these will be ignored
        "data",
        *(vocabulary_system_fields if name_type == "Organizational" else []),
        "institutionCategory",
        "nameTranslated",
        "noTick",
        "relatedURI",
        "tickable",
    )

    md.setdefault("qualified_relations", []).append(
        {
            "role": {
                "iri": role_iri,
            },
            **creator,
        }
    )


def convert_person(orig_creator):
    converted_person = full_name_to_person(orig_creator.pop("fullName"))
    converted_person["external_identifiers"] = convert_name_identifiers(orig_creator)
    converted_person["affiliations"] = convert_affiliations(orig_creator)
    return converted_person


def convert_organization(orig_creator):
    converted_organization = {
        "name": {
            "lang": "und",
            "value": orig_creator.pop("fullName"),
        },
        "alternate_names": [
            {
                "lang": lang,
                "value": title,
            }
            for lang, title in orig_creator.pop("title", {}).items()
        ],
    }
    converted_organization["external_identifiers"] = convert_name_identifiers(
        orig_creator
    )
    ico = orig_creator.pop("ico", None)
    if ico:
        converted_organization["external_identifiers"].append(
            {
                "value": ico,
                "identifier_scheme": "https://ares.gov.cz/",
            }
        )
    return converted_organization


vocabulary_system_fields = [
    "busy_count",
    "descendants_busy_count",
    "descendants_count",
    "label",
    "level",
    "links",
    "self",
    "slug",
    "status",
    "selectable",
    "ancestors",
]


def convert_affiliations(orig_creator):
    affiliations = []
    for aff in orig_creator.pop("affiliation", []):
        if aff.get("is_ancestor"):
            continue

        affiliation = {"name": aff.pop("fullName"), "external_identifiers": []}
        affiliations.append(affiliation)

        related_uri = aff.pop("relatedURI", {})
        if "ROR" in related_uri:
            affiliation["external_identifiers"].append(
                {
                    "value": related_uri["ROR"],
                    "identifier_scheme": "https://ror.org/",
                }
            )

        ensureEmpty(
            aff,
            *vocabulary_system_fields,
            "aliases",
            "ancestor",
            "data",
            "relatedRID",
            "ico",
            "institutionCategory",
            "nameTranslated",
            "nameType",
            "title",
        )
    return affiliations


def convert_name_identifiers(orig_creator):
    name_identifiers = []
    for ni in orig_creator.pop("authorityIdentifiers", []):
        identifier = ni.pop("identifier")
        identifier_scheme = {
            "orcid": "https://orcid.org/",
            "scopusID": "https://www.scopus.com/",
            "researcherID": "https://www.webofscience.com/",
        }[ni.pop("scheme")]
        name_identifiers.append(
            {"value": identifier, "identifier_scheme": identifier_scheme}
        )
        ensureEmpty(ni)

    return name_identifiers


def convert_abstract(orig_abstract):
    return [
        {
            "lang": lang,
            "value": bleach.clean(text, tags=allowed_tags),
        }
        for lang, text in orig_abstract.items()
    ]


def convert_dates(orig_md):
    dates = []
    dateAvailable = orig_md.pop("dateAvailable", None)
    if dateAvailable:
        dates.append(
            {
                "date": dateAvailable,
                "date_type": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/dateType/#issued",
            }
        )
    dateCreated = orig_md.pop("dateCreated", None)
    if dateCreated and re.match(r"^\d\d\d\d-\d\d-\d\d$", dateCreated):
        dates.append(
            {
                "date": dateCreated,
                "date_type": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/dateType/#created",
            }
        )
    return dates


def convert_resource_type(rts):
    if not rts:
        return {
            # generic dataset
            "iri": "http://purl.org/coar/resource_type/c_ddb1"
        }
    rt = next(
        (rt for rt in rts if not rt.get("is_ancestor")),
        None,
    )
    return {"iri": rt["relatedURI"]["COAR"]}


def convert_rights(orig_rights):
    converted_rights = []

    for r in orig_rights:
        if r.get("is_ancestor"):
            continue
        converted_rights.append(
            {
                "iri": r["relatedURI"]["URL"],
                "description": [
                    {
                        lang: get_ccmm_lang_iri(lang),
                        "value": text,
                    }
                    for lang, text in r["title"].items()
                ],
            }
        )
    return converted_rights


def convert_subject_categories(orig_subjects):
    converted_subjects = []
    for subject in orig_subjects:
        if subject.get("is_ancestor"):
            continue
        iri = subject["links"]["self"].replace(
            "https://data.narodni-repozitar.cz/2.0/taxonomies/subjectCategories/",
            "https://vocabs.ccmm.cz/registry/SubjectCategories/",
        )
        classification_code = subject["links"]["self"].replace(
            "https://data.narodni-repozitar.cz/2.0/taxonomies/subjectCategories/", ""
        )
        in_scheme = "https://vocabs.ccmm.cz/registry/SubjectCategories/"
        for lang, title in subject["title"].items():
            converted_subjects.append(
                {
                    "iri": iri,
                    "title": {
                        "lang": lang,
                        "value": title,
                    },
                    "classification_code": classification_code,
                    "in_subject_scheme": in_scheme,
                }
            )
    return converted_subjects


def convert_keywords(orig_keywords):
    created_subjects = []
    for keyword in orig_keywords:
        for lang, title in keyword.items():
            created_subjects.append({"title": {"value": title, "lang": lang}})
    return created_subjects


def convert_titles(orig_titles):
    converted_title = None
    alternate_titles = []

    for title in orig_titles:
        for lang, text in title["title"].items():
            if title.get("titleType") == "mainTitle":
                converted_title = text
            elif title.get("titleType") == "subtitle":
                alternate_titles.append(
                    {
                        "type": "Subtitle",
                        "title": {
                            lang: get_ccmm_lang_iri(lang),
                            "value": text,
                        },
                    }
                )
            else:
                raise Exception(f"Unknown title type: {title['titleType']}")
    return converted_title, alternate_titles


def convert_related_items(orig_related_items):
    converted_related_items = []

    for orig_related_item in orig_related_items:
        item_resource_type = orig_related_item.pop("itemResourceType", [])
        converted_item = {
            "iri": orig_related_item.pop("itemURL"),
            "type": (
                convert_resource_type(item_resource_type)
                if item_resource_type
                else None
            ),
            "relation_type": convert_relation_type(
                orig_related_item.pop("itemRelationType")
            ),
            "title": orig_related_item.pop("itemTitle", None),
        }
        for c in orig_related_item.pop("itemCreators", []):
            convert_creator(converted_item, c)
        for c in orig_related_item.pop("itemContributors", []):
            convert_contributor(c)

        converted_item["identifier"] = convert_related_item_identifiers(
            orig_related_item.pop("itemPIDs", []),
        )

        if "itemYear" in orig_related_item:
            converted_item["time_references"] = [
                {
                    "date": orig_related_item.pop("itemYear"),
                    "date_type": "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/dateType/#issued",
                }
            ]
        converted_related_items.append(
            {k: v for k, v in converted_item.items() if v is not None}
        )

        ensureEmpty(orig_related_item)  # not present in datacite schema
    return converted_related_items


def convert_relation_type(orig_relation_type):
    rt = next(r for r in (orig_relation_type or []) if not r.get("is_ancestor"))
    if not rt:
        return None
    link = rt["links"]["self"]
    return {
        "iri": link.replace(
            "https://data.narodni-repozitar.cz/2.0/taxonomies/itemRelationType/",
            "https://datacite-metadata-schema.readthedocs.io/en/4.6/appendices/appendix-1/relationType/#",
        )
    }


def convert_related_item_identifiers(orig_identifiers):
    converted = []
    for orig_identifier in orig_identifiers:
        identifier = orig_identifier.pop("identifier")
        scheme = orig_identifier.pop("scheme")
        if scheme == "doi":
            converted.append(
                {
                    "identifier_scheme": "https://doi.org/",
                    "value": identifier,
                    "iri": "https://doi.org/" + identifier,
                }
            )
        else:
            raise Exception(
                f"Unknown identifier scheme: {scheme} for identifier: {identifier}"
            )
    if len(converted) > 1:
        raise Exception(
            f"More than one identifier found for related item: {orig_identifiers}"
        )
    if len(converted) == 0:
        return None
    return converted[0]


if __name__ == "__main__":
    from oarepo_runtime.cli import oarepo

    from common.oai.loaders.datarepo import DataRepoLoader

    @oarepo.command("sample-harvest-to-file")
    def harvest():
        with open("datarepo_harvested.yaml", "w") as f:
            reader = DataRepoLoader(
                source="https://datarepo.eosc.cz/datasets/all/",
            )
            transformer = DataRepoTransformer(identity=system_identity)
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

    # run invenio with this command
    # to test the transformer
    from invenio_app.cli import cli

    cli.main(["oarepo", "sample-harvest-to-file"])
