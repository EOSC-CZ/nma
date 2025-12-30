from typing import cast

from invenio_access.permissions import system_identity
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.records import RecordService

from datasets.services.schema import resolve_orcid


def test_orcid_service_call(app):
    resolved = resolve_orcid(
        "0000-0003-0852-6632",
        vocabulary="names",
        create_vocabulary_record=False,
        check_existing=False,
    )
    assert resolved is not None
    assert any(
        id_["identifier"] == "0000-0003-0852-6632" and id_["scheme"] == "orcid"
        for id_ in resolved["identifiers"]
    )
    assert resolved["given_name"] == "Miroslav"
    assert resolved["family_name"] == "Simek"
    assert resolved["name"] == "Simek, Miroslav"


def test_orcid_service_call_with_local_cache(app):
    # create and put to the local cache. We use both True so that the test works
    # even if the orcid is already in the local cache.
    resolve_orcid(
        "0000-0003-0852-6632",
        vocabulary="names",
        create_vocabulary_record=True,
        check_existing=True,
    )
    # call again to test local cache retrieval
    resolved = resolve_orcid(
        "0000-0003-0852-6632",
        vocabulary="names",
        create_vocabulary_record=False,
        check_existing=True,
    )
    assert resolved is not None
    assert any(
        id_["identifier"] == "0000-0003-0852-6632" and id_["scheme"] == "orcid"
        for id_ in resolved["identifiers"]
    )
    assert resolved["given_name"] == "Miroslav"
    assert resolved["family_name"] == "Simek"
    assert resolved["name"] == "Simek, Miroslav"


def test_deserialization_with_orcid(app):
    data = {
        "metadata": {
            "title": "Test Dataset with ORCID",
            "resource_type": {"id": "dataset"},
            "publication_date": "2024-01-01",
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Simek, Miroslav",
                        "family_name": "Simek",
                        "given_name": "Miroslav",
                        "identifiers": [
                            {"identifier": "0000-0003-0852-6632", "scheme": "orcid"}
                        ],
                    }
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
        loaded_data["metadata"]["creators"][0]["person_or_org"]["identifiers"][0][
            "identifier"
        ]
        == "0000-0003-0852-6632"
    )


def test_deserialization_invalid_orcid(app):
    data = {
        "metadata": {
            "title": "Test Dataset with Invalid ORCID",
            "resource_type": {"id": "dataset"},
            "publication_date": "2024-01-01",
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Test, User",
                        "family_name": "Test",
                        "given_name": "User",
                        "identifiers": [
                            {"identifier": "0009-0009-9999-9996", "scheme": "orcid"}
                        ],
                    }
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
            "field": "metadata.creators.0.person_or_org.identifiers.0",
            "messages": ["ORCID 0009-0009-9999-9996 could not be resolved."],
        }
    ]
