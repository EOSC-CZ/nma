import re

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
RESOURCE_TYPE_PLACEHOLDER = "c_1843" #=other

def validate_date(value: str) -> bool:
    return bool(DATE_REGEX.fullmatch(value))

