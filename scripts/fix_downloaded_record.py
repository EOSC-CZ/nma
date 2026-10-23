#!/usr/bin/env python3
"""Fix known problems in downloaded NMA records (see validate_records.py).

- creators' and contributors' affiliations: drop dereferenced "identifiers" and
  deduplicate them, preferring the variant with an affiliation id
- Scopus author id given as a URL: keep only the authorId value
- language "enc": replace with "eng"
- related identifiers: converted to ccmm related resources (title = the
  identifier); ccmm derives the related identifiers from them and drops any
  others
"""

import json
from urllib.parse import parse_qs, urlparse

import click


def fix_affiliations(person):
    """Remove rejected fields and duplicate affiliations, preferring IDs."""
    affiliations = person.get("affiliations", [])

    for affiliation in affiliations:
        affiliation.pop("identifiers", None)

    names_with_id = {
        affiliation["name"]
        for affiliation in affiliations
        if affiliation.get("id") and affiliation.get("name")
    }

    unique = []
    seen = set()
    for affiliation in affiliations:
        if not affiliation.get("id") and affiliation.get("name") in names_with_id:
            continue

        key = (affiliation.get("id"), affiliation.get("name"))
        if key not in seen:
            seen.add(key)
            unique.append(affiliation)

    person["affiliations"] = unique


def related_resource(related_identifier):
    resource = {
        "title": related_identifier["identifier"],
        "identifiers": [{"identifier": related_identifier["identifier"], "scheme": related_identifier["scheme"]}],
        "relation_type": {"id": related_identifier["relation_type"]["id"]},
    }
    if resource_type := related_identifier.get("resource_type"):
        resource["resource_type"] = {"id": resource_type["id"]}
    return resource


def fix_record(record):
    metadata = record.get("metadata", {})

    for creator in metadata.get("creators", []):
        fix_affiliations(creator)

        for identifier in creator.get("person_or_org", {}).get("identifiers", []):
            value = identifier.get("identifier", "")
            if identifier.get("scheme") == "scopusid" and value.startswith("http"):
                identifier["identifier"] = parse_qs(urlparse(value).query)["authorId"][0]

    for contributor in metadata.get("contributors", []):
        fix_affiliations(contributor)

    metadata["languages"] = [
        {"id": "eng"} if language.get("id") == "enc" else language for language in metadata.get("languages", [])
    ]
    if not metadata["languages"]:
        del metadata["languages"]

    if related_identifiers := metadata.pop("related_identifiers", []):
        metadata.setdefault("related_resources", []).extend(
            related_resource(related_identifier) for related_identifier in related_identifiers
        )

    return record


@click.command(help=__doc__)
@click.argument("source", type=click.File("r", encoding="utf-8"))
@click.argument("dest", type=click.File("w", encoding="utf-8"))
def main(source, dest):
    for line in source:
        if line.strip():
            dest.write(json.dumps(fix_record(json.loads(line)), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
