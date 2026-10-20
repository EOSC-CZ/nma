#!/usr/bin/env python3
"""Fix known problems in downloaded NMA records (see validate_records.py).

- creators' affiliations: drop the dereferenced "identifiers" (not accepted by
  the schema); the affiliation id and name are kept
- Scopus author id given as a URL: keep only the authorId value
- language "enc": replace with "eng"
"""

import json
from urllib.parse import parse_qs, urlparse

import click


def fix_record(record):
    metadata = record.get("metadata", {})

    for creator in metadata.get("creators", []):
        for affiliation in creator.get("affiliations", []):
            affiliation.pop("identifiers", None)

        for identifier in creator.get("person_or_org", {}).get("identifiers", []):
            value = identifier.get("identifier", "")
            if identifier.get("scheme") == "scopusid" and value.startswith("http"):
                identifier["identifier"] = parse_qs(urlparse(value).query)["authorId"][0]

    metadata["languages"] = [
        {"id": "eng"} if language.get("id") == "enc" else language for language in metadata.get("languages", [])
    ]
    if not metadata["languages"]:
        del metadata["languages"]

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
