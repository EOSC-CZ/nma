import re

from idutils.validators import is_doi

DATE_REGEX = re.compile(
    r"^(?:"r"\d{4}"r"|"r"\d{4}-\d{2}"r"|"r"\d{4}-\d{2}-\d{2}"r")$"
)
CREATORS_PLACEHOLDER = [
    {
        "person_or_org": {
            "name": "Unknown",
            "type": "personal",
            "family_name": "Unknown",
        }
    }
]
PUBLICATION_DATE_PLACEHOLDER = "2025-01-01"
TITLE_PLACEHOLDER = "Unknown title"
RESOURCE_TYPE_PLACEHOLDER = "dataset"

def validate_date(value: str) -> bool:
    return bool(DATE_REGEX.fullmatch(value))


def normalize_identifier_into_resolution_url(identifier: str) -> str:
    """Normalizes raw DOIs (`10.xxxx/...`), prefixed identifiers (`doi:10.xxxx/...` or `DOI:10.xxxx/...`)
    and almost fully resolvable URLS (`http://doi.org/10.xxxx/...` - notice `http`, not `https`) into resolvable URLs (`https://doi.org/10.xxxx/...`).
    If the input is already a resolvable URL (`https://doi.org/10.xxxx/...`) or doesn't match known patterns, it returs the original string.
    """
    if not identifier:
        return ""

    identifier = identifier.strip()

    # Prefixed identifier or raw DOI.
    prefixed_doi_match = is_doi(identifier)
    if prefixed_doi_match:
        return f"https://doi.org/{prefixed_doi_match.group(2)}"

    return identifier
