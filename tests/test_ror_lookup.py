from typing import cast

from invenio_access.permissions import system_identity
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.records import RecordService

from datasets.services.schema import resolve_ror


def test_ror_service_call(app):
    resolved = resolve_ror(
        "03yrm5c26",
        vocabulary="affiliations",
        create_vocabulary_record=False,
        check_existing=True,
    )
    assert resolved is not None
    assert resolved["id"] == "03yrm5c26"
    assert resolved["title"]["en"] == "California Digital Library"


def test_deserialization_with_ror(app):
    data = {
        "metadata": {
            "title": "Test Dataset with ROR",
            "resource_type": {"id": "dataset"},
            "publication_date": "2024-01-01",
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Creator, Test",
                        "family_name": "Creator",
                        "given_name": "Test",
                    },
                    "affiliations": [
                        {"name": "California Digital Library", "id": "03yrm5c26"}
                    ],
                }
            ],
        }
    }
    svc = cast(RecordService, current_service_registry.get("datasets"))
    schema = svc.schema
    loaded_data, errors = schema.load(
        data, raise_errors=False, context={"identity": system_identity}
    )
    assert not errors
    assert (
        loaded_data["metadata"]["creators"][0]["affiliations"][0]["id"] == "03yrm5c26"
    )


def test_deserialization_invalid_ror(app):
    data = {
        "metadata": {
            "title": "Test Dataset with ROR",
            "resource_type": {"id": "dataset"},
            "publication_date": "2024-01-01",
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Creator, Test",
                        "family_name": "Creator",
                        "given_name": "Test",
                    },
                    "affiliations": [
                        {"name": "California Digital Library", "id": "f3yrm5c26"}
                    ],
                }
            ],
        }
    }
    svc = cast(RecordService, current_service_registry.get("datasets"))
    schema = svc.schema
    loaded_data, errors = schema.load(
        data, raise_errors=False, context={"identity": system_identity}
    )
    assert errors == [
        {
            "field": "metadata.creators.0.affiliations.0",
            "messages": ["ROR ID f3yrm5c26 could not be resolved."],
        }
    ]
