import re

PREFIXED_DOI_REGEX = re.compile(
    r"^(?:doi:)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)$", re.IGNORECASE
)

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
    """
    Normalizes raw DOIs (`10.xxxx/...`) and prefixed identifiers (`doi:10.xxxx/...` or `DOI:10.xxxx/...`) into resolvable URLs (`https://doi.org/10.xxxx/...`).
    If the input is already a resolvable URL or doesn't match known patterns, it returs the original string.
    """
    if not identifier:
        return ""

    identifier = identifier.strip()

    # Resolvable URL.
    if identifier.startswith("http://") or identifier.startswith("https://"):
        return identifier

    # Prefixed identifier or raw DOI.
    prefixed_doi_match = PREFIXED_DOI_REGEX.match(identifier)
    if prefixed_doi_match:
        return f"https://doi.org/{prefixed_doi_match.group(1)}"

    return identifier
