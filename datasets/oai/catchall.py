import copy
import dataclasses
import json
from functools import wraps
from typing import Any, Callable
from urllib import parse as urlparse

import bleach
from flask import current_app
from idutils import is_doi, normalize_doi
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.readers import BaseReader
from invenio_vocabularies.datastreams.transformers import BaseTransformer
from langcodes import Language

from riv.utils import create_session_with_retries


@dataclasses.dataclass
class APIOAIHeader:
    identifier: str
    datestamp: str
    deleted: bool


@dataclasses.dataclass
class APIOAIRecord:
    raw: str  # serialized json of the record
    json: dict  # dict of the record
    header: APIOAIHeader


class CatchAllReader(BaseReader):

    def __init__(self, origin=None, mode="r", identifiers=None, *args, **kwargs):
        super().__init__(
            origin=origin or "https://datarepo.eosc.cz/datasets/all/",
            mode=mode,
            *args,
            **kwargs,
        )
        self._identifiers = identifiers

    def _iter(self, fp, *args, **kwargs):
        session = create_session_with_retries()
        oai_prefix = f"oai:{urlparse.urlparse(self._origin).hostname}:"
        for seq, record in enumerate(self.fetch_records(session)):
            files_link = record["links"]["self"] + "/files/"
            files = session.get(files_link, headers={"Accept": "application/json"})
            files.raise_for_status()
            record["files"] = files.json()
            yield APIOAIRecord(
                raw=json.dumps(record),
                json=record,
                header=APIOAIHeader(
                    identifier=oai_prefix + record["id"],
                    datestamp=record["metadata"][
                        "dateAvailable"
                    ],  # Note: catch-all currently does not provide "modified" date!
                    deleted=False,
                ),
            )

    def read(self, item=None, *args, **kwargs):
        yield from self._iter(fp=None, *args, **kwargs)

    def fetch_records(self, session):
        url = self._origin

        if self._identifiers:
            if not url.endswith("/"):
                url += "/"
            oai_prefix = f"oai:{urlparse.urlparse(self._origin).hostname}:"
            for identifier in self._identifiers:
                if not identifier.startswith(oai_prefix):
                    raise ValueError(
                        f"Identifier {identifier} does not match oai prefix {oai_prefix}."
                    )
                record_id = identifier[len(oai_prefix) :]
                # can not construct catch-all url as it contains also the community
                # which is not known at this point. Will use search API to find the record.
                current_app.logger.info("Fetching record url for %s", record_id)
                response = session.get(
                    url,
                    params={"q": record_id},
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                payload = response.json()
                if len(payload["hits"]["hits"]) == 0:
                    raise ValueError(f"Record with identifier {identifier} not found.")
                elif len(payload["hits"]["hits"]) > 1:
                    raise ValueError(
                        f"Multiple records found for identifier {identifier}."
                    )
                record_url = payload["hits"]["hits"][0]["links"]["self"]
                current_app.logger.info("Fetching record %s", record_url)
                resp = session.get(record_url, headers={"Accept": "application/json"})
                resp.raise_for_status()
                yield resp.json()
        else:
            while True:
                # load a page of results
                current_app.logger.info("Fetching list of records from %s", url)
                response = session.get(url, headers={"Accept": "application/json"})
                response.raise_for_status()
                payload = response.json()
                current_app.logger.info(
                    "Fetched listing of %d records", len(payload["hits"]["hits"])
                )
                for hit in payload["hits"]["hits"]:
                    # need to re-get as we do not have all fields in the hit
                    current_app.logger.info("Fetching record %s", hit["id"])
                    yield session.get(
                        hit["links"]["self"], headers={"Accept": "application/json"}
                    ).json()
                # if there is a next page, continue there
                if "next" in payload["links"]:
                    url = payload["links"]["next"]
                else:
                    # otherwise we are done
                    break


def check_converted(exceptions: list[str]) -> Callable:
    """Check that required fields are converted."""

    def wrapper(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(self, metadata, *args, **kwargs) -> Any:
            original_metadata = copy.deepcopy(metadata)
            ret = f(self, metadata, *args, **kwargs)
            if isinstance(metadata, dict):
                unconverted_fields = set(metadata.keys()) - set(exceptions)
                if unconverted_fields:
                    raise ValueError(
                        f"Unconverted fields found for method {f.__name__}: {', '.join(unconverted_fields)}. Original metadata: {json.dumps(original_metadata)}"
                    )
            elif isinstance(metadata, list):
                for idx, item in enumerate(metadata):
                    unconverted_fields = set(item.keys()) - set(exceptions)
                    if unconverted_fields:
                        raise ValueError(
                            f"Unconverted fields found for method {f.__name__} at index {idx}: {', '.join(unconverted_fields)}. Original metadata: {json.dumps(item)}"
                        )
            return ret

        return wrapped

    return wrapper


vocabulary_exceptions = [
    "status",
    "links",
    "slug",
    "data",
    "self",
    "busy_count",
    "is_ancestor",
    "descendants_count",
    "title",
    "alpha2Code",
    "descendants_busy_count",
    "label",
    "level",
    "selectable",
    "noTick",
    "icon",
    "tickable",
    "relatedURI",
    "altLabels",
    "ancestors",
    "ancestor",
]

# Mapping from catch-all contributor role slugs to RDM role IDs
CATCHALL_TO_RDM_ROLES = {
    "advisor": "supervisor",  # Map advisor to supervisor (closest match)
    "collaborator": "projectmember",  # Map collaborator to project member
    "data-collector": "datacollector",  # Direct match
    "data-manager": "datamanager",  # Direct match
    "project-leader": "projectleader",  # Direct match
    "project-manager": "projectmanager",  # Direct match
    "researcher": "researcher",  # Direct match
    "supervisor": "supervisor",  # Direct match
}


def sanitize_html(text):
    """Sanitize HTML content using bleach.

    Allows common safe tags and attributes while removing potentially dangerous content.
    """
    if not text:
        return text

    # Allow common formatting tags
    allowed_tags = [
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "br",
        "code",
        "div",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "i",
        "li",
        "ol",
        "p",
        "pre",
        "span",
        "strong",
        "sub",
        "sup",
        "table",
        "tbody",
        "td",
        "th",
        "thead",
        "tr",
        "ul",
    ]

    allowed_attributes = {
        "a": ["href", "title"],
        "abbr": ["title"],
        "acronym": ["title"],
    }

    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
        protocols=["http", "https", "mailto"],
    )


def fix_malformed_identifier(identifier: str) -> str:
    """Fix known malformed identifiers."""
    if identifier and "0000-0002-5095-051X" in identifier:
        return "0000-0002-5095-051X"
    if identifier and "0000-0002-9746-5802" in identifier:
        return "0000-0002-9746-5802"
    return identifier


class CatchAllTransformer(BaseTransformer):

    def __init__(self, *args, **kwargs):
        pass

    def convert_lang2_to_lang3(self, lang_code):
        """Convert 2-letter language code to 3-letter code.

        Args:
            lang_code: 2-letter or 3-letter language code

        Returns:
            3-letter language code, or original code if conversion fails
        """
        try:
            return Language.get(lang_code).to_alpha3()
        except Exception:
            return lang_code

    def parse_edtf_date(self, date_value):
        """Parse EDTF date, handling intervals by taking the first part.

        Args:
            date_value: Date string, possibly in EDTF format (YYYY-MM-DD/YYYY-MM-DD)

        Returns:
            Normalized date string (first part if interval), or None if empty
        """
        if not date_value:
            return None

        # Handle EDTF intervals (e.g., "2024-01-09/2024-01-10")
        if "/" in date_value:
            return date_value.split("/")[0]

        return date_value

    def apply(self, stream_entry: StreamEntry, *args, **kwargs) -> StreamEntry:
        """
        Transforms the entry.
        """
        stream_entry.entry = {
            "oai_record": stream_entry.entry,
            "record": self.convert_catch_all_to_rdm(stream_entry.entry.json),
        }
        return stream_entry

    def convert_catch_all_to_rdm(self, rec):
        """Convert catch-all record to RDM format."""
        metadata = rec.get("metadata", {})

        # Parse fields that are used in multiple places
        parsed_date_created = self.parse_date_created(metadata.pop("dateCreated", None))

        languages = self.convert_languages(metadata.pop("language", []))
        if languages:
            preferred_language = languages[0]["id"]
        else:
            preferred_language = "en"

        # Convert title and get additional titles if any
        main_title, additional_titles = self.convert_title(
            metadata.pop("titles", []), preferred_language
        )

        # Extract DOI from persistentIdentifiers for record ID and persistent_url
        record_id = rec.get("id")
        doi_value = None
        persistent_ids = metadata.pop("persistentIdentifiers", [])
        for pid in persistent_ids:
            if pid.get("scheme") == "doi" and pid.get("status") == "registered":
                doi_value = pid.get("identifier")
                if doi_value:
                    record_id = f"doi/{doi_value}"
                    break
        else:
            # we save the record without doi, using our own pid prefix
            record_id = f"catchall/{record_id}"

        rdm_record = {
            "id": record_id,
            "metadata": {
                "title": main_title,
                "publication_date": self.convert_publication_date(
                    self.parse_date_available(metadata.pop("dateAvailable", None)),
                    parsed_date_created,
                ),
                "resource_type": self.convert_resource_type(
                    metadata.pop("resourceType", [])
                ),
                "creators": self.convert_creators(metadata.pop("creators", [])),
                "description": self.convert_description(metadata.pop("abstract", {})),
            },
        }

        # TODO: where to add the original DOI? It does not seem to be able to go here
        # or we might need to register our own provider for it.
        #
        # if doi_value:
        #     rdm_record["pids"] = {
        #         "doi": {
        #             "identifier": doi_value,
        #             "provider": "external",
        #         }
        #     }

        # Add persistent_url if DOI is available. Persistent URL is always doi or handle
        # going to the primary storage.
        if doi_value:
            rdm_record["metadata"]["persistent_url"] = f"https://doi.org/{doi_value}"

        # Add additional_titles if present
        if additional_titles:
            rdm_record["metadata"]["additional_titles"] = additional_titles

        # Optional fields
        contributors = self.convert_contributors(metadata.pop("contributors", []))
        if contributors:
            rdm_record["metadata"]["contributors"] = contributors

        subjects = self.convert_subjects(
            self.parse_keywords(metadata.pop("keywords", [])),
            self.parse_subject_categories(metadata.pop("subjectCategories", [])),
        )
        if subjects:
            rdm_record["metadata"]["subjects"] = subjects

        # Publisher is in RDM schema
        publisher = self.convert_publisher(metadata.pop("publisher", []))
        if publisher:
            rdm_record["metadata"]["publisher"] = publisher

        if languages:
            rdm_record["metadata"]["languages"] = languages

        rights = self.convert_rights(metadata.pop("rights", []))
        if rights:
            rdm_record["metadata"]["rights"] = rights

        dates = self.convert_dates(
            parsed_date_created,
            self.parse_date_collected(metadata.pop("dateCollected", None)),
        )
        if dates:
            rdm_record["metadata"]["dates"] = dates

        funding = self.convert_funding(metadata.pop("fundingReferences", []))
        if funding:
            rdm_record["metadata"]["funding"] = funding

        related_identifiers = self.convert_related_identifiers(
            metadata.pop("relatedItems", [])
        )
        if related_identifiers:
            rdm_record["metadata"]["related_identifiers"] = related_identifiers

        additional_descriptions = self.convert_additional_descriptions(
            metadata.pop("methods", {}),
            metadata.pop("technicalInfo", {}),
        )
        if additional_descriptions:
            rdm_record["metadata"]["additional_descriptions"] = additional_descriptions

        # Convert access rights to access.record and access.files
        access = self.convert_access_rights(metadata.pop("accessRights", []))
        if access:
            rdm_record["access"] = access

        # TODO: Handle files - not now
        rdm_record["files"] = {"enabled": False}
        rdm_record["media_files"] = {"enabled": False}
        rec.pop(
            "files", None
        )  # not in RDM schema at record level (files handled separately)

        # Handle notes field (convert to internal_notes if present)
        notes = metadata.pop("notes", [])
        notes = [note for note in notes if note.strip()]
        if notes:
            rdm_record["metadata"]["additional_descriptions"] += [
                self.convert_note(note) for note in notes
            ]

        # Pop fields not in RDM schema
        metadata.pop("$schema", None)  # not in RDM schema
        metadata.pop("InvenioID", None)  # not in RDM schema
        metadata.pop("_bucket", None)  # not in RDM schema (internal field)
        metadata.pop("_files", None)  # not in RDM schema (internal field)
        metadata.pop("oarepo:ownedBy", None)  # not in RDM schema (oarepo-specific)
        metadata.pop(
            "oarepo:primaryCommunity", None
        )  # not in RDM schema (oarepo-specific)
        metadata.pop("oarepo:recordStatus", None)  # not in RDM schema (oarepo-specific)
        metadata.pop("oarepo:doirequest", None)  # not in RDM schema (oarepo-specific)
        metadata.pop(
            "persistentIdentifiers", None
        )  # not in RDM schema (use pids instead)

        # check that the metadata is fully converted
        if metadata:
            raise ValueError(
                f"Unconverted metadata fields remain: {json.dumps(metadata)}"
            )

        return rdm_record

    @check_converted(exceptions=[])
    def parse_single_title(self, title_obj):
        """Parse a single title object."""
        title_type = title_obj.pop("titleType", None)
        title_dict = title_obj.pop("title", {})
        return title_type, title_dict

    @check_converted(exceptions=[])
    def convert_title(self, titles, preferred_language):
        """Convert title from catch-all to RDM format.

        Returns tuple: (main_title_string, additional_titles_list or None)
        """
        main_title_dicts = []
        additional_titles = []

        if titles:
            for title_obj in titles:
                title_type, title_dict = self.parse_single_title(title_obj)
                if title_type == "mainTitle":
                    main_title_dicts.append(title_dict)
                elif title_type in [
                    "subtitle",
                    "alternativeTitle",
                    "translatedTitle",
                    "other",
                ]:
                    # Add to additional_titles with type
                    for lang, text in title_dict.items():
                        if text:
                            additional_titles.append(
                                {
                                    "title": text,
                                    "type": {"id": title_type.lower()},
                                    "lang": {"id": self.convert_lang2_to_lang3(lang)},
                                }
                            )
                else:
                    # Unknown title type
                    raise NotImplementedError(
                        f"Title type '{title_type}' not implemented in convert_title."
                    )

        main_title = "Untitled"
        if len(main_title_dicts) > 1:
            raise ValueError("Multiple main titles found.")
        elif main_title_dicts:
            title_dict = main_title_dicts[0]
            if preferred_language in title_dict:
                main_title = title_dict[preferred_language]
            elif "en" in title_dict:
                main_title = title_dict["en"]
            else:
                main_title = next(iter(title_dict.values()))

        return main_title, (additional_titles if additional_titles else None)

    @check_converted(exceptions=[])
    def parse_date_available(self, date_available):
        """Parse dateAvailable field."""
        return self.parse_edtf_date(date_available)

    @check_converted(exceptions=[])
    def parse_date_created(self, date_created):
        """Parse dateCreated field."""
        return self.parse_edtf_date(date_created)

    def convert_publication_date(self, parsed_date_available, parsed_date_created):
        """Convert publication date from catch-all to RDM format."""
        # Use dateAvailable as publication date
        if parsed_date_available:
            return parsed_date_available
        # Fallback to created date
        if parsed_date_created:
            return parsed_date_created
        return None

    @check_converted(exceptions=vocabulary_exceptions)
    def convert_resource_type(self, resource_types):
        """Convert resource type from catch-all to RDM format."""
        if resource_types:
            rt = resource_types[0]
            coar_type = rt.pop("coarType", None)
            if coar_type:
                return {"id": coar_type}
        return {"id": "dataset"}

    @check_converted(
        exceptions=vocabulary_exceptions
        + [
            "institutionCategory",
            "ico",
            "nameTranslated",
            "relatedRID",
            "aliases",
            "formerTitles",
            "nameType",
            "fullName",
            "relatedURI",
        ]
    )
    def convert_creators(self, creators_list):
        """Convert creators from catch-all to RDM format."""
        creators = []
        for creator in creators_list:
            rdm_creator = {"person_or_org": self.convert_person_or_org(creator)}

            affiliations = self.convert_affiliations(creator.pop("affiliation", []))
            if affiliations:
                rdm_creator["affiliations"] = affiliations

            creators.append(rdm_creator)
        return creators

    @check_converted(exceptions=vocabulary_exceptions)
    def extract_role_slug(self, role_data):
        """Extract slug from role vocabulary structure.

        Args:
            role_data: Role data from catch-all (can be list or dict)

        Returns:
            Role slug string or None
        """
        if not role_data:
            return None

        # Role might be a list, take first non-ancestor item
        if isinstance(role_data, list):
            for role_item in role_data:
                # Skip ancestor items
                is_ancestor = role_item.get("is_ancestor", False)
                if is_ancestor:
                    role_item.pop("is_ancestor")
                    continue

                slug = role_item.pop("slug", None)
                # need to clear the rest of the role_data list, because some
                # of the items might be ancestors and not will not be processed
                # when this returns. That would mean that unconverted fields
                # remain and the check_converted decorator would raise an error.
                for _r in role_data:
                    _r.clear()
                return slug

        # If it's a dict, extract slug
        elif isinstance(role_data, dict):
            is_ancestor = role_data.pop("is_ancestor", False)
            if not is_ancestor:
                slug = role_data.pop("slug", None)
                role_data.clear()
                return slug

        return None

    @check_converted(exceptions=[])
    def convert_contributors(self, contributors_list):
        """Convert contributors from catch-all to RDM format."""
        contributors = []
        for contributor in contributors_list:
            rdm_contributor = {"person_or_org": self.convert_person_or_org(contributor)}

            affiliations = self.convert_affiliations(contributor.pop("affiliation", []))
            if affiliations:
                rdm_contributor["affiliations"] = affiliations

            # Add role if present
            role = contributor.pop("role", None)
            if role:
                role_slug = self.extract_role_slug(role)
                if role_slug:
                    # Map catch-all role to RDM role
                    rdm_role = CATCHALL_TO_RDM_ROLES.get(role_slug, "other")
                    rdm_contributor["role"] = {"id": rdm_role}

            contributors.append(rdm_contributor)
        return contributors

    @check_converted(
        exceptions=["affiliation", "role"]
        + vocabulary_exceptions
        + [
            "institutionCategory",
            "ico",
            "nameTranslated",
            "relatedRID",
            "aliases",
            "formerTitles",
        ]
    )
    def convert_person_or_org(self, person):
        """Convert person or organization from catch-all to RDM format."""
        full_name = person.pop("fullName", "")
        name_type = person.pop("nameType", "Personal")

        # Pop organization-specific fields that might be present
        person.pop("relatedURI", None)

        person_or_org = {
            "name": full_name,
            "type": name_type.lower(),
        }

        # For personal names, split into given and family names
        # RDM requires family_name to be non-empty for personal names
        if person_or_org["type"] == "personal" and full_name:
            if "," in full_name:
                # Format: "family_name, given_name"
                parts = full_name.split(",", 1)
                person_or_org["family_name"] = parts[0].strip()
                person_or_org["given_name"] = parts[1].strip()
            else:
                # No comma: treat entire name as family_name
                person_or_org["family_name"] = full_name

        # Add identifiers (ORCID, etc.)
        authority_identifiers = person.pop("authorityIdentifiers", [])
        if authority_identifiers:
            identifiers = self.parse_authority_identifiers(authority_identifiers)
            if identifiers:
                person_or_org["identifiers"] = identifiers

        return person_or_org

    @check_converted(exceptions=[])
    def parse_authority_identifiers(self, authority_identifiers):
        """Parse authority identifiers."""
        identifiers = []
        for auth_id in authority_identifiers:
            identifier = auth_id.pop("identifier", "").strip()
            # fix known malformed ORCID
            identifier = fix_malformed_identifier(identifier)
            scheme = auth_id.pop("scheme", "").lower()
            if identifier and scheme:
                if not any(
                    id_["scheme"] == scheme and id_["identifier"] == identifier
                    for id_ in identifiers
                ):
                    identifiers.append({"scheme": scheme, "identifier": identifier})
        return identifiers

    @check_converted(exceptions=["ROR", "URL", "COAR", "DOI"])
    def extract_ror_id(self, related_uri):
        """Extract ROR ID from relatedURI dict."""
        ror = related_uri.pop("ROR", None)
        related_uri.pop(
            "URL", None
        )  # not used here, used by parse_related_uri_for_url if needed
        related_uri.pop("COAR", None)  # not in RDM schema
        related_uri.pop("DOI", None)  # not in RDM schema for affiliations
        if ror and "ror.org/" in ror:
            return ror.split("ror.org/")[-1]
        return None

    @check_converted(exceptions=[])
    def extract_first_language_value(self, lang_dict):
        """Extract first value from a language dict and consume all keys."""
        result = ""
        for lang in list(lang_dict.keys()):
            value = lang_dict.pop(lang)
            if value and not result:
                result = value
        return result

    @check_converted(exceptions=[])
    def parse_related_uri_for_url(self, related_uri):
        """Extract URL from relatedURI dict."""
        url = related_uri.pop("URL", None)
        related_uri.pop("ROR", None)  # not used here, used by extract_ror_id if needed
        related_uri.pop("COAR", None)  # not in RDM schema
        related_uri.pop("DOI", None)  # not in RDM schema for rights/licenses
        return url

    @check_converted(
        exceptions=vocabulary_exceptions
        + [
            "institutionCategory",
            "nameType",
            "ico",
            "nameTranslated",
            "relatedRID",
            "aliases",
            "formerTitles",
        ]
    )
    def convert_affiliations(self, affiliations):
        """Convert affiliations from catch-all to RDM format."""
        rdm_affiliations = []
        for affiliation in affiliations:
            # Pop all vocabulary metadata fields
            full_name = affiliation.pop("fullName", "")

            aff_obj = {"name": full_name}

            # Add ROR if available
            related_uri = affiliation.pop("relatedURI", {})
            if related_uri:
                ror_id = self.extract_ror_id(related_uri)
                if ror_id:
                    aff_obj["id"] = ror_id

            # Only append if this affiliation ID hasn't been seen before
            aff_id = aff_obj.get("id")
            if aff_id:
                if not any(aff.get("id") == aff_id for aff in rdm_affiliations):
                    rdm_affiliations.append(aff_obj)
            else:
                # Always append affiliations without IDs
                rdm_affiliations.append(aff_obj)

        return rdm_affiliations

    @check_converted(
        exceptions=vocabulary_exceptions
        + [
            "institutionCategory",
            "ico",
            "nameType",
            "nameTranslated",
            "relatedRID",
            "aliases",
            "formerTitles",
        ]
    )
    def convert_publisher(self, publishers):
        """Convert publisher from catch-all to RDM format."""
        if publishers:
            publisher_obj = publishers[0]  # Take first publisher
            full_name = publisher_obj.pop("fullName", "")
            publisher_obj.pop("relatedURI", {})  # Pop relatedURI from first publisher

            # Pop fullName and relatedURI from remaining publishers to satisfy check_converted
            for i in range(1, len(publishers)):
                publishers[i].pop("fullName", "")
                publishers[i].pop("relatedURI", {})

            if full_name:
                return full_name
        return None

    @check_converted(exceptions=[])
    def convert_description(self, abstract):
        """Convert abstract to description for RDM format."""
        result = ""
        if abstract:
            # Return first available language and consume all keys
            # we need the list here because we are popping keys while iterating
            for lang in list(abstract.keys()):
                desc_text = abstract.pop(lang)
                if desc_text and not result:
                    result = sanitize_html(desc_text)
        return result

    @check_converted(exceptions=[])
    def convert_additional_descriptions(self, methods, technical_info):
        """Convert methods and technicalInfo to additional_descriptions."""
        additional_descs = []

        if methods:
            # we need the list here because we are popping keys while iterating
            for lang in list(methods.keys()):
                method_text = methods.pop(lang)
                if method_text:
                    additional_descs.append(
                        {
                            "description": sanitize_html(method_text),
                            "type": {"id": "methods"},
                            "lang": {"id": self.convert_lang2_to_lang3(lang)},
                        }
                    )

        if technical_info:
            for lang in list(technical_info.keys()):
                tech_text = technical_info.pop(lang)
                if tech_text:
                    additional_descs.append(
                        {
                            "description": sanitize_html(tech_text),
                            "type": {"id": "technical-info"},
                            "lang": {"id": self.convert_lang2_to_lang3(lang)},
                        }
                    )

        return additional_descs if additional_descs else None

    def convert_note(self, note):
        """Convert a note string to internal_notes format.

        Note: we do not know the language of the note, so we default to 'en'.
        """
        return {
            "description": sanitize_html(note),
            "type": {"id": "other"},
            "lang": {"id": "eng"},
        }

    @check_converted(exceptions=[])
    def parse_keywords(self, keywords):
        """Parse keywords field."""
        parsed_keywords = []
        for keyword in keywords:
            if isinstance(keyword, dict):
                # Keywords are structured as {lang: text}, e.g., {"en": "keyword"}
                # Get the first available language and consume all keys
                keyword_added = False
                for lang in list(keyword.keys()):
                    keyword_text = keyword.pop(lang)
                    if keyword_text and not keyword_added:
                        parsed_keywords.append(keyword_text)
                        keyword_added = True
            elif isinstance(keyword, str):
                parsed_keywords.append(keyword)
        return parsed_keywords

    @check_converted(exceptions=vocabulary_exceptions)
    def parse_subject_categories(self, subject_categories):
        """Parse subjectCategories field."""
        parsed_categories = []
        for subject_cat in subject_categories:
            # Skip ancestor categories (is_ancestor=True means it's a parent category, not a leaf)
            if subject_cat.pop("is_ancestor", False):
                continue
            title = subject_cat.pop("title", {})
            # Consume all language keys from title
            subject_added = False
            for lang in list(title.keys()):
                subject_text = title.pop(lang)
                if subject_text and not subject_added:
                    parsed_categories.append(subject_text)
                    subject_added = True
        return parsed_categories

    def convert_subjects(self, parsed_keywords, parsed_subject_categories):
        """Convert keywords and subject categories to subjects."""
        subjects = []

        # Convert keywords
        for keyword_text in parsed_keywords:
            subjects.append({"subject": keyword_text})

        # Convert subject categories
        for subject_text in parsed_subject_categories:
            subjects.append({"subject": subject_text})

        return subjects if subjects else None

    @check_converted(exceptions=vocabulary_exceptions + ["aliases"])
    def convert_languages(self, language_list):
        """Convert languages from catch-all to RDM format."""
        languages = []
        for lang in language_list:
            if isinstance(lang, dict):
                lang_id = lang.pop("id", None)
                if lang_id:
                    languages.append({"id": self.convert_lang2_to_lang3(lang_id)})
            elif isinstance(lang, str):
                languages.append({"id": self.convert_lang2_to_lang3(lang)})
        return languages if languages else None

    @check_converted(exceptions=vocabulary_exceptions)
    def convert_rights(self, rights):
        """Convert rights/licenses from catch-all to RDM format.

        Creates separate rights entries for each locale since RDM only accepts
        one locale per title.
        """
        rights_list = []

        for right in rights:
            # Skip ancestor entries (is_ancestor=True means it's a parent license, not a leaf)
            if right.pop("is_ancestor", False):
                continue

            # Pop all vocabulary metadata fields
            title = right.pop("title", {})
            related_uri = right.pop("relatedURI", {})

            # Get link from relatedURI
            link = None
            if related_uri:
                link = self.parse_related_uri_for_url(related_uri)

            # Create separate rights entry for each locale in title
            # since RDM only accepts one locale per title
            if title:
                for locale, title_text in title.items():
                    if title_text:
                        right_obj = {"title": {locale: title_text}}
                        if link:
                            right_obj["link"] = link
                        rights_list.append(right_obj)
            elif link:
                # If no title but there's a link, create entry with just the link
                rights_list.append({"link": link})

        return rights_list if rights_list else None

    @check_converted(exceptions=[])
    def parse_date_collected(self, date_collected):
        """Parse dateCollected field."""
        return self.parse_edtf_date(date_collected)

    def convert_dates(self, parsed_date_created, parsed_date_collected):
        """Convert various dates from catch-all to RDM format."""
        dates = []

        if parsed_date_created:
            dates.append(
                {
                    "date": parsed_date_created,
                    "type": {"id": "created"},
                }
            )

        if parsed_date_collected:
            dates.append(
                {
                    "date": parsed_date_collected,
                    "type": {"id": "collected"},
                }
            )

        return dates if dates else None

    @check_converted(exceptions=vocabulary_exceptions + ["CEA", "aliases", "fullName"])
    def parse_funder_info(self, funder_info):
        """Parse funder information from funder dict."""
        funder_name = funder_info.pop("fullName", None)
        if not funder_name:
            title_dict = funder_info.pop("title", {})
            if title_dict:
                funder_name = self.extract_first_language_value(title_dict)

        ror_id = None
        related_uri = funder_info.pop("relatedURI", {})
        if related_uri:
            ror_id = self.extract_ror_id(related_uri)

        return funder_name, ror_id

    @check_converted(
        exceptions=["funder", "projectID", "projectName", "fundingProgram"]
    )
    def convert_funding(self, funding_refs):
        """Convert funding references from catch-all to RDM format."""
        funding_list = []
        # TODO: we lose findingProgram as it's not in RDM schema, is that ok?
        for funding_ref in funding_refs:
            funders = funding_ref.pop("funder", [])
            if funders:
                funder_info = funders[0]  # Take first funder

                funding_obj = {}

                # Extract funder information
                funder_name, ror_id = self.parse_funder_info(funder_info)
                if funder_name:
                    funding_obj["funder"] = {"name": funder_name}
                    if ror_id:
                        funding_obj["funder"]["id"] = ror_id

                # Extract award information
                project_id = funding_ref.pop("projectID", None)
                project_name = funding_ref.pop("projectName", None)
                funding_ref.pop("fundingProgram", None)  # not in RDM schema

                if project_id or project_name:
                    award = {}
                    if project_id:
                        award["number"] = project_id
                    if project_name:
                        award["title"] = {"en": project_name}
                    funding_obj["award"] = award

                if funding_obj:
                    # Only add if this funder hasn't been seen before (when it has an ID)
                    funder_id = funding_obj.get("funder", {}).get("id")
                    if funder_id:
                        if not any(
                            f.get("funder", {}).get("id") == funder_id
                            for f in funding_list
                        ):
                            funding_list.append(funding_obj)
                    else:
                        # Always append funding without funder IDs
                        funding_list.append(funding_obj)

        return funding_list if funding_list else None

    @check_converted(
        exceptions=[
            "itemURL",
            "itemTitle",
            "itemYear",
            "itemResourceType",
            "itemPIDs",
            "itemRelationType",
            "itemCreators",
        ]
    )
    def convert_related_identifiers(self, related_items):
        """Convert related items to related identifiers."""
        related_ids = []

        for item in related_items:
            item_url = item.pop("itemURL", None)
            if item_url:
                related_id = {
                    "identifier": item_url,
                    "scheme": "url",
                    "relation_type": {"id": "iscitedby"},
                }

                # Try to identify DOI
                if is_doi(item_url):
                    doi = normalize_doi(item_url)
                    related_id["identifier"] = doi
                    related_id["scheme"] = "doi"

                related_ids.append(related_id)

        return related_ids if related_ids else None

    @check_converted(exceptions=vocabulary_exceptions)
    def convert_access_rights(self, access_rights_list):
        """Convert accessRights from catch-all to RDM access format.

        Maps catch-all accessRights vocabulary to RDM's access.record and access.files.
        """
        if not access_rights_list:
            return None

        # Take the first access rights entry
        access_right = access_rights_list[0]

        # Get the title to determine access level
        title = access_right.pop("title", {})
        access_level = None

        # Check for access level in any language
        for lang, value in title.items():
            if value:
                value_lower = value.lower()
                if "open" in value_lower:
                    access_level = "public"
                    break
                elif "restrict" in value_lower:
                    access_level = "restricted"
                    break
                elif "embargo" in value_lower:
                    # Embargoed access - treat as restricted for now
                    # TODO: Add embargo.until and embargo.reason if available
                    access_level = "restricted"
                    break

        # Raise exception if we can't determine access level
        if not access_level:
            raise ValueError(
                f"Could not determine access level from accessRights title: {title}"
            )

        # Pop relatedURI to consume all fields
        access_right.pop("relatedURI", {})

        return {"record": access_level, "files": access_level}

    def convert_files(self, files_data):
        """Convert files from catch-all to RDM format."""
        return {"enabled": False}
