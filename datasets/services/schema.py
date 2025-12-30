from __future__ import annotations

import contextlib
import json
from typing import Any, Callable, Generator, cast
from urllib.parse import quote

from flask import current_app
from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PersistentIdentifierError
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.records import RecordService
from invenio_vocabularies.contrib.common.ror.datastreams import RORTransformer
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from marshmallow import ValidationError, pre_load
from opensearchpy.exceptions import OpenSearchException
from sqlalchemy.exc import NoResultFound

from datasets.tasks import create_vocabulary_item_task


def get_with_default(data: dict | None, key: str, default: Any) -> Any:
    """Get value from dict, returning default if key is missing or value is None.

    Args:
        data: Dictionary to get value from (can be None)
        key: Key to lookup
        default: Default value to return if key is missing or value is None

    Returns:
        Value from dict, or default if missing or None
    """
    if data is None:
        return default
    value = data.get(key)
    return default if value is None else value


def get_object(data: dict | None, key: str) -> dict:
    """Get object from dict, returning empty dict if key is missing or value is None.

    Args:
        data: Dictionary to get value from (can be None)
        key: Key to lookup

    Returns:
        Object from dict, or empty dict if missing or None
    """
    return get_with_default(data, key, {})


def dict_lookup_with_arrays(
    data: dict, path: str
) -> Generator[tuple[Any, Any, str], None, None]:
    """Lookup a value in a nested dictionary using a dot-separated path.

    Supports lists by applying the lookup to each item in the list.

    returns tuples of (value, parent, full_path).
    """

    def __lookup(
        data: Any, parts: list[str], path: list[str], parent: Any
    ) -> Generator[tuple[Any, Any, str], None, None]:
        if not parts:
            if isinstance(data, list):
                for didx, d in enumerate(data):
                    yield from __lookup(d, [], path + [str(didx)], parent)
            else:
                yield data, parent, ".".join(path)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                yield from __lookup(item, parts, path + [str(idx)], parent)
        elif isinstance(data, dict):
            part = parts[0]
            rest = parts[1:]
            if part in data:
                yield from __lookup(data[part], rest, path + [part], data)

    yield from __lookup(data, path.split("."), [], None)


def resolve_identifiers(data: dict):
    identifier_locations = {
        "metadata.creators.person_or_org.identifiers": "names",
        "metadata.creators.affiliations": "affiliations",
        "metadata.contributors.person_or_org.identifiers": "names",
        "metadata.contributors.affiliations": "affiliations",
        "metadata.funding.funder": "funders",
        "metadata.funding.award.identifiers": "funders",
    }
    for location, vocabulary in identifier_locations.items():
        with contextlib.suppress(KeyError):
            loc = list(dict_lookup_with_arrays(data, location))
            for identifier, parent, path in loc:
                try:
                    resolve_identifier(identifier, parent, path, vocabulary)
                except Exception as e:
                    current_app.logger.exception(
                        f"Error resolving identifier {identifier} at {path}",
                        exc_info=e,
                    )


def resolve_identifier(
    identifier: dict,
    parent: Any,
    path: str,
    vocabulary: str,
    vocabulary_key: str = "id",
):
    """Resolve a single identifier dictionary."""

    id_key = "identifier" if "identifier" in identifier else "id"
    if id_key not in identifier:
        return
    scheme = identifier.get("scheme")
    if (vocabulary, scheme) not in identifier_resolvers:
        return
    resolver = identifier_resolvers[(vocabulary, scheme)]
    resolved = resolver(
        identifier[id_key],
        vocabulary=vocabulary,
        parent=parent,
        create_vocabulary_record=True,
        check_existing=True,
        path=path,
    )
    identifier[id_key] = resolved[vocabulary_key]


def orcid_to_names(orcid_response: dict, parent: Any = None) -> dict:
    """Convert ORCID API response to names vocabulary schema.

    Args:
        orcid_response: The JSON response from ORCID API
        parent: Parent element (e.g., person_or_org) to use for fallback data

    Returns:
        Dictionary conforming to the names vocabulary schema
    """
    result_identifiers: list[dict[str, str]] = []
    result: dict[str, Any] = {"identifiers": result_identifiers}

    # Extract person name information. is None if private.
    person = get_object(orcid_response, "person")
    name_data = get_object(person, "name")

    given_name = get_with_default(get_object(name_data, "given-names"), "value", "")
    family_name = get_with_default(get_object(name_data, "family-name"), "value", "")

    # If name data is missing (private), use parent data as fallback
    if not given_name and not family_name and parent:
        given_name = parent.get("given_name", "")
        family_name = parent.get("family_name", "")

    if given_name:
        result["given_name"] = given_name
    if family_name:
        result["family_name"] = family_name

    # Construct full name
    name_parts = []
    if family_name:
        name_parts.append(family_name)
    if given_name:
        name_parts.append(given_name)
    if name_parts:
        result["name"] = ", ".join(name_parts)
    elif parent:
        # If no name parts but parent has a name, use it
        result["name"] = parent.get("name", "")

    # Add ORCID identifier
    orcid_identifier = get_object(orcid_response, "orcid-identifier")
    orcid_path = orcid_identifier.get("path")
    if orcid_path:
        result_identifiers.append({"identifier": orcid_path, "scheme": "orcid"})
        result["id"] = orcid_path

    # Extract affiliations from employments
    affiliations = []
    activities = get_object(orcid_response, "activities-summary")
    employments = get_object(activities, "employments")
    affiliation_groups = get_with_default(employments, "affiliation-group", [])

    seen_affiliations = set()
    for group in affiliation_groups:
        summaries = get_with_default(group, "summaries", [])
        for summary_wrapper in summaries:
            employment = get_object(summary_wrapper, "employment-summary")
            organization = get_object(employment, "organization")
            org_name = organization.get("name")

            if org_name:
                affiliation = {"name": org_name}

                # Try to get ROR identifier if available
                disambiguated_org = get_object(
                    organization, "disambiguated-organization"
                )
                if disambiguated_org:
                    disambiguation_source = disambiguated_org.get(
                        "disambiguation-source"
                    )
                    org_identifier = disambiguated_org.get(
                        "disambiguated-organization-identifier"
                    )

                    if disambiguation_source == "ROR" and org_identifier:
                        # Extract ROR ID from URL if it's a full URL
                        if org_identifier.startswith("https://ror.org/"):
                            ror_id = org_identifier.split("https://ror.org/")[-1]
                            affiliation["id"] = ror_id
                        else:
                            affiliation["id"] = org_identifier
                        resolve_ror(
                            affiliation["id"],
                            vocabulary="affiliations",
                            create_vocabulary_record=True,
                            check_existing=True,
                        )

                # Only append if this affiliation hasn't been seen before
                affiliation_fingerprint = affiliation.get("id") or json.dumps(
                    affiliation, sort_keys=True
                )
                if affiliation_fingerprint not in seen_affiliations:
                    seen_affiliations.add(affiliation_fingerprint)
                    affiliations.append(affiliation)

    if affiliations:
        result["affiliations"] = affiliations

    return result


def resolve_orcid(
    orcid: str,
    vocabulary: str,
    parent: Any = None,
    create_vocabulary_record: bool = True,
    check_existing: bool = True,
    path: str = "",
) -> dict:
    """Resolve ORCID identifier to URL.

    Args:
        orcid: ORCID identifier
        vocabulary: Vocabulary name
        parent: Parent element (e.g., person_or_org) for fallback data
        create_vocabulary_record: Whether to create a vocabulary record
        check_existing: Whether to check for existing records
        path: Path for error messages
    """
    # look up in the vocabulary service first
    svc = cast(RecordService, current_service_registry.get(vocabulary))
    if orcid.startswith("https://orcid.org/"):
        orcid = orcid.split("https://orcid.org/")[-1]
    elif orcid.startswith("http://orcid.org/"):
        orcid = orcid.split("http://orcid.org/")[-1]
    if check_existing:
        with contextlib.suppress(OpenSearchException):
            hits = svc.search(
                system_identity, params={"q": f"identifiers.identifier:{orcid}"}
            )
            for hit in hits:
                if any(
                    id_["identifier"] == orcid and id_["scheme"] == "orcid"
                    for id_ in hit["identifiers"]
                ):
                    return hit

    from riv.utils import create_session_with_retries

    session = create_session_with_retries()
    headers = {"Accept": "application/json"}

    orcid_key = current_app.config.get("ORCID_READ_PUBLIC_KEY")
    if orcid_key:
        headers["Authorization"] = f"Bearer {orcid_key}"

    url = f"https://pub.orcid.org/v3.0/{quote(orcid)}"
    resp = session.get(url, headers=headers)
    if resp.status_code != 200:
        raise ValidationError(f"ORCID {orcid} could not be resolved.", field_name=path)

    # Convert ORCID response to names vocabulary format
    orcid_data = resp.json()
    names_record = orcid_to_names(orcid_data, parent=parent)

    if create_vocabulary_record:
        # need to create the record in a worker, because we have an ongoing transaction
        # with its own uow, and creating the vocabulary record would commit it and
        # destroy the nested state.
        return create_vocabulary_item_task.delay(
            vocabulary_service_id=vocabulary, data=names_record
        ).get(propagate=True)
    return names_record


def resolve_ror(
    ror: str,
    vocabulary: str,
    parent: Any = None,
    create_vocabulary_record: bool = True,
    check_existing: bool = True,
    path: str = "",
) -> dict:
    """Resolve ROR identifier to URL.

    Args:
        ror: ROR identifier
        vocabulary: Vocabulary name ("affiliations" or "funders")
        parent: Parent element (unused for ROR, kept for signature consistency)
        create_vocabulary_record: Whether to create a vocabulary record
        check_existing: Whether to check for existing records
        path: Path for error messages
    """

    svc = cast(RecordService, current_service_registry.get(vocabulary))
    if check_existing:
        # note: maybe use just persistent identifier lookup here and return just an id
        # without any other metadata. Would be way faster.
        with contextlib.suppress(PersistentIdentifierError, NoResultFound):
            return svc.read(system_identity, ror).to_dict()

    client_id = current_app.config["ROR_CLIENT_ID"]
    from riv.utils import create_session_with_retries

    session = create_session_with_retries()
    headers = {"Accept": "application/json", "Client-ID": client_id}
    url = f"https://api.ror.org/v2/organizations/{quote(ror)}"
    resp = session.get(url, headers=headers)
    if resp.status_code != 200:
        raise ValidationError(f"ROR ID {ror} could not be resolved.", field_name=path)
    data = StreamEntry(entry=resp.json())
    transformer = RORTransformer(
        vocab_schemes={"affiliations": "ror", "funders": "ror"},
    )
    data = transformer.apply(data)
    if create_vocabulary_record:
        # need to create the record in a worker, because we have an ongoing transaction
        # with its own uow, and creating the vocabulary record would commit it and
        # destroy the nested state.
        return create_vocabulary_item_task.delay(
            vocabulary_service_id=vocabulary, data=data.entry
        ).get(propagate=True)
    return data.entry


identifier_resolvers: dict[tuple[str, str | None], Callable] = {
    ("names", "orcid"): resolve_orcid,
    ("affiliations", "ror"): resolve_ror,
    ("affiliations", None): resolve_ror,
    ("funders", "ror"): resolve_ror,
    ("funders", None): resolve_ror,
}


class IdentifiersDownloaderMixin:
    @pre_load
    def load_service_identifiers(self, data, **kwargs):
        """Post-load processing for service identifiers."""
        try:
            resolve_identifiers(data)
        except Exception as e:
            current_app.logger.exception(
                "Error resolving identifiers in record",
                exc_info=e,
            )
        return data
