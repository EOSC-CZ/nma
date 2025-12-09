import copy
import json
from functools import wraps
from typing import Any, Callable
from urllib.error import HTTPError

from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.readers import BaseReader
from invenio_vocabularies.datastreams.transformers import BaseTransformer

from riv.utils import create_session_with_retries


class CatchAllReader(BaseReader):

    def __init__(self, origin=None, mode="r", *args, **kwargs):
        super().__init__(
            origin=origin or "https://datarepo.eosc.cz/datasets/all/",
            mode=mode,
            *args,
            **kwargs,
        )

    def _iter(self, fp, *args, **kwargs):
        session = create_session_with_retries()
        for seq, record in enumerate(self.fetch_records(session)):
            if record is None:
                yield None
            else:
                files_link = record["links"]["self"] + "/files/"
                files = session.get(files_link, headers={"Accept": "application/json"})
                files.raise_for_status()
                record["files"] = files.json()
                yield StreamEntry(
                    entry=record,
                )

    def read(self, item=None, *args, **kwargs):
        yield from self._iter(fp=None, *args, **kwargs)

    def fetch_records(self, session):
        url = self._origin
        retry_count = 5
        count = 0

        while True:
            try:
                response = session.get(url, headers={"Accept": "application/json"})
                response.raise_for_status()
                payload = response.json()
                for hit in payload["hits"]["hits"]:
                    # need to re-get as we do not have all fields in the hit
                    yield session.get(
                        hit["links"]["self"], headers={"Accept": "application/json"}
                    ).json()
                if "next" in payload["links"]:
                    url = payload["links"]["next"]
                    count = 0
                else:
                    break
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                if count >= retry_count:
                    raise
                count += 1
            except Exception as err:
                print(f"Other error occurred: {err}")
                if count >= retry_count:
                    raise
                count += 1


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
]


class CatchAllTransformer(BaseTransformer):

    def apply(self, stream_entry: StreamEntry, *args, **kwargs) -> StreamEntry:
        """
        Transforms the entry.
        """
        stream_entry.entry = self.convert_catch_all_to_rdm(stream_entry.entry)
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

        rdm_record = {
            "id": rec.get("id"),
            "metadata": {
                "title": self.convert_title(
                    metadata.pop("titles", []), preferred_language
                ),
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
            metadata.pop("methods", {})
        )
        if additional_descriptions:
            rdm_record["metadata"]["additional_descriptions"] = additional_descriptions

        # TODO: Handle files - not now
        rdm_record["files"] = {"enabled": False}
        rec.pop("files", None)

        # check that the metadata is fully converted
        if metadata:
            raise ValueError(
                f"Unconverted metadata fields remain: {json.dumps(metadata)}"
            )

        return rdm_record

    # TODO: store other titles as translated etc.
    @check_converted(exceptions=[])
    def convert_title(self, titles, preferred_language):
        """Convert title from catch-all to RDM format."""
        title_texts = []
        if titles:
            for title_obj in titles:
                title_type = title_obj.pop("titleType", None)
                title_dict = title_obj.pop("title", {})
                if title_type == "mainTitle":
                    title_texts.append(title_dict)
        if len(title_texts) > 1:
            raise ValueError("Multiple main titles found.")
        elif title_texts:
            print(title_texts)
            print(preferred_language)
            if preferred_language in title_texts[0]:
                return title_texts[0][preferred_language]
            elif "en" in title_texts[0]:
                return title_texts[0]["en"]
            else:
                return next(iter(title_texts[0].values()))
        return "Untitled"

    @check_converted(exceptions=[])
    def parse_date_available(self, date_available):
        """Parse dateAvailable field."""
        return date_available

    @check_converted(exceptions=[])
    def parse_date_created(self, date_created):
        """Parse dateCreated field."""
        if date_created:
            # Handle date ranges like "2024-01-09/2024-01-10"
            if "/" in date_created:
                return date_created.split("/")[0]
        return date_created

    def convert_publication_date(self, parsed_date_available, parsed_date_created):
        """Convert publication date from catch-all to RDM format."""
        # Use dateAvailable as publication date
        if parsed_date_available:
            return parsed_date_available
        # Fallback to created date
        if parsed_date_created:
            return parsed_date_created
        return None

    @check_converted(
        exceptions=["altLabels", "title", "links", "is_ancestor", "level", "relatedURI"]
    )
    def convert_resource_type(self, resource_types):
        """Convert resource type from catch-all to RDM format."""
        if resource_types:
            rt = resource_types[0]
            coar_type = rt.pop("coarType", None)
            if coar_type:
                return {"id": coar_type}
        return {"id": "dataset"}

    @check_converted(exceptions=[])
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
                rdm_contributor["role"] = {"id": role}

            contributors.append(rdm_contributor)
        return contributors

    def convert_person_or_org(self, person):
        """Convert person or organization from catch-all to RDM format."""
        full_name = person.get("fullName", "")
        name_type = person.get("nameType", "Personal")

        person_or_org = {
            "name": full_name,
            "type": "personal" if name_type == "Personal" else "organizational",
        }

        # For personal names, try to split into given and family names
        if person_or_org["type"] == "personal" and ", " in full_name:
            parts = full_name.split(", ", 1)
            person_or_org["family_name"] = parts[0]
            person_or_org["given_name"] = parts[1]

        # Add identifiers (ORCID, etc.)
        authority_identifiers = person.get("authorityIdentifiers", [])
        if authority_identifiers:
            identifiers = []
            for auth_id in authority_identifiers:
                identifier = auth_id.get("identifier", "").strip()
                scheme = auth_id.get("scheme", "").lower()
                if identifier and scheme:
                    identifiers.append({"scheme": scheme, "identifier": identifier})
            if identifiers:
                person_or_org["identifiers"] = identifiers

        return person_or_org

    def convert_affiliations(self, affiliations):
        """Convert affiliations from catch-all to RDM format."""
        rdm_affiliations = []
        for affiliation in affiliations:
            aff_obj = {"name": affiliation.get("fullName", "")}

            # Add ROR if available
            related_uri = affiliation.get("relatedURI", {})
            ror = related_uri.get("ROR")
            if ror:
                # Extract ROR ID from URL
                if "ror.org/" in ror:
                    ror_id = ror.split("ror.org/")[-1]
                    aff_obj["id"] = ror_id

            rdm_affiliations.append(aff_obj)
        return rdm_affiliations

    @check_converted(exceptions=[])
    def convert_description(self, abstract):
        """Convert abstract to description for RDM format."""
        if abstract:
            # Return first available language
            for lang, desc_text in abstract.items():
                return desc_text
        return ""

    @check_converted(exceptions=[])
    def convert_additional_descriptions(self, methods):
        """Convert methods and other descriptions to additional_descriptions."""
        additional_descs = []

        if methods:
            for lang, method_text in methods.items():
                additional_descs.append(
                    {
                        "description": method_text,
                        "type": {"id": "methods"},
                        "lang": {"id": lang},
                    }
                )

        return additional_descs if additional_descs else None

    @check_converted(exceptions=[])
    def parse_keywords(self, keywords):
        """Parse keywords field."""
        parsed_keywords = []
        for keyword in keywords:
            if isinstance(keyword, dict):
                # Get the title in available language
                title = keyword.pop("title", {})
                for lang, keyword_text in title.items():
                    parsed_keywords.append(keyword_text)
                    break
            elif isinstance(keyword, str):
                parsed_keywords.append(keyword)
        return parsed_keywords

    @check_converted(exceptions=[])
    def parse_subject_categories(self, subject_categories):
        """Parse subjectCategories field."""
        parsed_categories = []
        for subject_cat in subject_categories:
            # Skip ancestor categories
            if subject_cat.pop("is_ancestor", False):
                continue
            title = subject_cat.pop("title", {})
            for lang, subject_text in title.items():
                parsed_categories.append(subject_text)
                break
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

    @check_converted(exceptions=vocabulary_exceptions)
    def convert_languages(self, language_list):
        """Convert languages from catch-all to RDM format."""
        languages = []
        for lang in language_list:
            if isinstance(lang, dict):
                lang_id = lang.pop("id", None)
                if lang_id:
                    languages.append({"id": lang_id})
            elif isinstance(lang, str):
                languages.append({"id": lang})
        return languages if languages else None

    @check_converted(exceptions=[])
    def convert_rights(self, rights):
        """Convert rights/licenses from catch-all to RDM format."""
        rights_list = []

        for right in rights:
            # Skip ancestor entries
            if right.pop("is_ancestor", False):
                continue

            right_obj = {}

            # Get title
            title = right.pop("title", {})
            if title:
                right_obj["title"] = title

            # Get link from relatedURI
            related_uri = right.pop("relatedURI", {})
            url = related_uri.get("URL")
            if url:
                right_obj["link"] = url

            if right_obj:
                rights_list.append(right_obj)

        return rights_list if rights_list else None

    @check_converted(exceptions=[])
    def parse_date_collected(self, date_collected):
        """Parse dateCollected field."""
        return date_collected

    def convert_dates(self, parsed_date_created, parsed_date_collected):
        """Convert various dates from catch-all to RDM format."""
        dates = []

        if parsed_date_created:
            dates.append(
                {
                    "date": parsed_date_created,
                    "type": {"id": "created"},
                    "description": "Date when the data was created",
                }
            )

        if parsed_date_collected:
            dates.append(
                {
                    "date": parsed_date_collected,
                    "type": {"id": "collected"},
                    "description": "Date when the data was collected",
                }
            )

        return dates if dates else None

    @check_converted(exceptions=[])
    def convert_funding(self, funding_refs):
        """Convert funding references from catch-all to RDM format."""
        funding_list = []

        for funding_ref in funding_refs:
            funders = funding_ref.pop("funder", [])
            if funders:
                funder_info = funders[0]  # Take first funder

                funding_obj = {}

                # Extract funder information
                funder_name = funder_info.get("fullName") or funder_info.get(
                    "title", {}
                ).get("en", "")
                if funder_name:
                    funding_obj["funder"] = {"name": funder_name}

                    # Add funder ID if available from relatedURI
                    related_uri = funder_info.get("relatedURI", {})
                    ror = related_uri.get("ROR")
                    if ror and "ror.org/" in ror:
                        ror_id = ror.split("ror.org/")[-1]
                        funding_obj["funder"]["id"] = ror_id

                # Extract award information
                project_id = funding_ref.pop("projectID", None)
                project_name = funding_ref.pop("projectName", None)
                if project_id or project_name:
                    award = {}
                    if project_id:
                        award["number"] = project_id
                    if project_name:
                        award["title"] = {"en": project_name}
                    funding_obj["award"] = award

                if funding_obj:
                    funding_list.append(funding_obj)

        return funding_list if funding_list else None

    @check_converted(exceptions=[])
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
                if "doi.org" in item_url:
                    doi = item_url.split("doi.org/")[-1]
                    related_id["identifier"] = doi
                    related_id["scheme"] = "doi"

                related_ids.append(related_id)

        return related_ids if related_ids else None

    def convert_files(self, files_data):
        """Convert files from catch-all to RDM format."""
        return {"enabled": False}


if __name__ == "__main__":

    def run():
        loader = CatchAllReader(
            origin="https://datarepo.eosc.cz/datasets/all/",
        )
        transformer = CatchAllTransformer()
        import json

        for idx, record in enumerate(loader.read()):
            with open(f"data/{idx:03d}_loaded.json", "w") as f:
                f.write(json.dumps(record.entry, indent=2, ensure_ascii=False))
            record = transformer.apply(record)
            with open(f"data/{idx:03d}_transformed.json", "w") as f:
                f.write(json.dumps(record.entry, indent=2, ensure_ascii=False))

            print(json.dumps(record.entry, indent=2, ensure_ascii=False))

    run()
