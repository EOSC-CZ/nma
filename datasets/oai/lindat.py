from __future__ import annotations

from typing import Any, override
from uuid import uuid4

import bleach
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.transformers import BaseTransformer
from invenio_vocabularies.proxies import current_service as vocabulary_service
from langcodes import Language
from lxml import etree

RDM_MINIMAL_DESCRIPTION_LENGTH = 3  # Minimum length for description field


class LindatTransformer(BaseTransformer):
    """LINDAT/CLARIN OAI-PMH Transformer."""

    # Namespace constants
    NS_OAI = "http://www.openarchives.org/OAI/2.0/"
    NS_CMD = "http://www.clarin.eu/cmd/"

    def __init__(self, *args, **kwargs):
        self.warnings: list[str] = []

    def _validate_vocabulary_item(
        self, vocabulary_id: str, item_id: str, field_name: str = ""
    ) -> bool:
        """Check if an item exists in a vocabulary.

        Args:
            vocabulary_id: The vocabulary to check (e.g., 'resourcetypes', 'languages')
            item_id: The ID of the item to validate
            field_name: Optional field name for better error messages

        Returns:
            True if the item exists, False otherwise
        """
        try:
            vocabulary_service.read(system_identity, (vocabulary_id, item_id))
            return True
        except Exception:
            warning_msg = f"Item '{item_id}' not found in '{vocabulary_id}' vocabulary"
            if field_name:
                warning_msg += f" (field: {field_name})"
            self.warnings.append(warning_msg)

            # Try to log if current_app is available
            try:
                current_app.logger.warning(warning_msg)
            except RuntimeError:
                # No app context, just skip logging
                pass

            return False

    def _strip_time(self, date_string: str) -> str:
        """Strip time information from a date string.

        Handles ISO datetime formats and EDTF intervals:
        - "2014-03-19T18:02:38.963+01:00" -> "2014-03-19"
        - "2014-07-30T21:22:41Z" -> "2014-07-30"
        - "2014-07-30" -> "2014-07-30" (unchanged)
        - "2020/2021" -> "2020" (EDTF interval, returns start date)
        - "2020-01-15/2021-12-31" -> "2020-01-15" (EDTF interval, returns start date)

        Args:
            date_string: Date or datetime string, or EDTF interval

        Returns:
            Date string without time information
        """
        if not date_string:
            return date_string

        # Handle EDTF intervals (e.g., "2020/2021" or "2020-01-15/2021-12-31")
        # Return the start date of the interval
        if "/" in date_string:
            date_string = date_string.split("/")[0]

        # Split on 'T' to remove time part
        return date_string.split("T")[0]

    @override
    def apply(self, stream_entry: StreamEntry, *args, **kwargs) -> StreamEntry:
        # Reset warnings for each record
        self.warnings = []

        xml_root = etree.fromstring(stream_entry.entry["record"].raw)

        rdm_record = self._convert_lindat_to_rdm(xml_root)

        stream_entry = StreamEntry(
            entry={
                "oai_record": stream_entry.entry["record"],
                "record": rdm_record,
            }
        )
        stream_entry.errors.extend(self.warnings)
        return stream_entry

    def _convert_lindat_to_rdm(self, xml_root: etree._Element) -> dict:
        """Convert LINDAT/CLARIN OAI-PMH record to RDM format.

        Supports both LINDAT_CLARIN and OLAC-DcmiTerms formats.
        """

        # Extract the <metadata> element
        metadata_elem = self.find_element(xml_root, self.NS_OAI, "metadata")
        # get the first element of metadata (which should be cmdi)
        cmdi_elem = self.find_element(metadata_elem, self.NS_CMD, "CMD")

        cmdi_components = self.find_element(cmdi_elem, self.NS_CMD, "Components")

        # Try to detect which format we have
        lindat_component = self.find_element_optional(
            cmdi_components, self.NS_CMD, "LINDAT_CLARIN"
        )

        if lindat_component is not None:
            return self._convert_lindat_metadata_to_rdm(lindat_component)

        # Try OLAC format
        data_component = self.find_element_optional(
            cmdi_components, self.NS_CMD, "data"
        )
        if data_component is not None:
            olac_component = self.find_element_optional(
                data_component, self.NS_CMD, "OLAC-DcmiTerms"
            )
            if olac_component is not None:
                return self._convert_olac_dcmi_to_rdm(olac_component)

        # Try WebLichtWebService format
        weblicht_component = self.find_element_optional(
            cmdi_components, self.NS_CMD, "WebLichtWebService"
        )
        if weblicht_component is not None:
            return self._convert_weblicht_to_rdm(weblicht_component)

        # Check for other unsupported formats
        # Get all child elements of Components to see what we have
        children = list(cmdi_components)
        if children:
            child_names = [etree.QName(child).localname for child in children]
            raise ValueError(
                f"Unsupported metadata format in Components element. "
                f"Found: {', '.join(child_names)}. "
                f"Supported formats: LINDAT_CLARIN, OLAC-DcmiTerms, WebLichtWebService"
            )

        # If neither format is found, raise an exception
        raise ValueError(
            "Unknown metadata format: expected LINDAT_CLARIN, OLAC-DcmiTerms, or WebLichtWebService, "
            "but found neither in Components element"
        )

    def _convert_lindat_metadata_to_rdm(self, lindat_component: etree._Element) -> dict:
        """Convert LINDAT_CLARIN metadata to RDM format."""

        bibliographic_info = self.find_element(
            lindat_component, self.NS_CMD, "bibliographicInfo"
        )
        data_info = self.find_element(lindat_component, self.NS_CMD, "dataInfo")
        license_info = self.find_element(lindat_component, self.NS_CMD, "licenseInfo")

        # Extract basic metadata
        titles = self._extract_titles(bibliographic_info)
        main_title = titles[0] if titles else "Untitled"
        additional_titles = titles[1:] if len(titles) > 1 else None

        creators = self._extract_creators(bibliographic_info)
        publication_date = self._extract_publication_date(bibliographic_info)
        resource_type = self._extract_resource_type(data_info)
        description = self._extract_description(data_info)

        # Extract identifier for record ID
        record_id = self._extract_identifier(bibliographic_info)
        persistent_url = self._extract_handle_url(bibliographic_info)

        # Build RDM record
        rdm_record: dict[str, Any] = {
            "id": record_id,
            "metadata": {
                "title": main_title,
                "publication_date": publication_date,
                "resource_type": resource_type,
                "creators": creators,
                "description": description,
            },
        }

        # Add persistent URL if available
        if persistent_url:
            rdm_record["metadata"]["persistent_url"] = persistent_url

        # Add additional titles if present
        if additional_titles:
            rdm_record["metadata"]["additional_titles"] = additional_titles

        # Optional fields
        publishers = self._extract_publishers(bibliographic_info)
        if publishers:
            rdm_record["metadata"]["publisher"] = publishers

        languages = self._extract_languages(data_info)
        if languages:
            rdm_record["metadata"]["languages"] = languages

        subjects = self._extract_subjects(data_info)
        if subjects:
            rdm_record["metadata"]["subjects"] = subjects

        rights = self._extract_rights(license_info)
        if rights:
            rdm_record["metadata"]["rights"] = rights

        funding = self._extract_funding(bibliographic_info)
        if funding:
            rdm_record["metadata"]["funding"] = funding

        related_identifiers = self._extract_related_identifiers(bibliographic_info)
        if related_identifiers:
            rdm_record["metadata"]["related_identifiers"] = related_identifiers

        # Files disabled for now
        rdm_record["files"] = {"enabled": False}
        rdm_record["media_files"] = {"enabled": False}

        self._remove_empty_fields(rdm_record)

        return rdm_record

    def _convert_olac_dcmi_to_rdm(self, olac_component: etree._Element) -> dict:
        """Convert OLAC-DcmiTerms metadata to RDM format.

        Strict parsing: raises exception if any unknown elements are found.
        """

        # Validate all elements are known (strict parsing)
        self._validate_olac_elements(olac_component)

        # Extract basic metadata
        title = self._extract_olac_title(olac_component)
        description = self._extract_olac_description(olac_component)
        record_id, persistent_url = self._extract_olac_identifier(olac_component)
        publication_date = self._extract_olac_publication_date(olac_component)
        resource_type = self._extract_olac_resource_type(olac_component)
        creators = self._extract_olac_creators(olac_component)

        # Build RDM record
        rdm_record: dict[str, Any] = {
            "id": record_id,
            "metadata": {
                "title": title,
                "publication_date": publication_date,
                "resource_type": resource_type,
                "creators": creators,
                "description": description,
            },
        }

        # Add persistent URL if available
        if persistent_url:
            rdm_record["metadata"]["persistent_url"] = persistent_url

        # Optional fields
        publisher = self.get_element_text(olac_component, self.NS_CMD, "publisher")
        if publisher:
            rdm_record["metadata"]["publisher"] = publisher

        languages = self._extract_olac_languages(olac_component)
        if languages:
            rdm_record["metadata"]["languages"] = languages

        contributors = self._extract_olac_contributors(olac_component)
        if contributors:
            rdm_record["metadata"]["contributors"] = contributors

        subjects = self._extract_olac_subjects(olac_component)
        if subjects:
            rdm_record["metadata"]["subjects"] = subjects

        rights = self._extract_olac_rights(olac_component)
        if rights:
            rdm_record["metadata"]["rights"] = rights

        formats = self._extract_olac_formats(olac_component)
        if formats:
            rdm_record["metadata"]["formats"] = formats

        alternative_titles = self._extract_olac_alternative_titles(olac_component)
        if alternative_titles:
            rdm_record["metadata"]["additional_titles"] = alternative_titles

        related_identifiers = self._extract_olac_related_identifiers(olac_component)
        if related_identifiers:
            rdm_record["metadata"]["related_identifiers"] = related_identifiers

        # Files disabled for now
        rdm_record["files"] = {"enabled": False}
        rdm_record["media_files"] = {"enabled": False}

        self._remove_empty_fields(rdm_record)

        return rdm_record

    def _convert_weblicht_to_rdm(self, weblicht_component: etree._Element) -> dict:
        """Convert WebLichtWebService metadata to RDM format.

        Strict parsing: raises exception if any unknown elements are found.
        """

        # Validate structure (strict parsing)
        self._validate_weblicht_elements(weblicht_component)

        # Find the Service element
        service_elem = self.find_element(weblicht_component, self.NS_CMD, "Service")

        # Extract basic metadata
        title = (
            self.get_element_text(service_elem, self.NS_CMD, "Name")
            or "Untitled Web Service"
        )

        # Extract descriptions - prefer the non-short one
        descriptions = self.find_all_elements(service_elem, self.NS_CMD, "Description")
        description = ""
        for desc_elem in descriptions:
            if desc_elem.get("type") != "short" and desc_elem.text:
                description = desc_elem.text.strip()
                break

        # If no long description, use short one
        if not description:
            for desc_elem in descriptions:
                if desc_elem.text:
                    description = desc_elem.text.strip()
                    break

        # Ensure minimum description length
        if len(description.strip()) < RDM_MINIMAL_DESCRIPTION_LENGTH:
            description = "No description available."

        # Extract publication date
        publication_date_text = self.get_element_text(
            service_elem, self.NS_CMD, "PublicationDate"
        )
        if publication_date_text:
            # Parse ISO datetime and extract date part
            publication_date = self._strip_time(publication_date_text)
        else:
            # Fallback to current date if not available
            from datetime import date

            publication_date = date.today().isoformat()

        # Extract URL as identifier
        url = self.get_element_text(service_elem, self.NS_CMD, "url")
        record_id = None
        persistent_url = None

        if url:
            # Use URL as both ID and persistent URL
            # Extract a simple ID from the URL
            url_parts = url.rstrip("/").split("/")
            record_id = url_parts[-1] if url_parts else "webservice"
            persistent_url = url

        # Extract creator from Creation/Creators/Creator/Contact/Organisation
        creators = []
        creation_elem = self.find_element_optional(
            service_elem, self.NS_CMD, "Creation"
        )
        if creation_elem is not None:
            creators_elem = self.find_element_optional(
                creation_elem, self.NS_CMD, "Creators"
            )
            if creators_elem is None:
                raise ValueError(
                    "WebLichtWebService Creation element found but missing required Creators child element"
                )

            for creator_elem in self.find_all_elements(
                creators_elem, self.NS_CMD, "Creator"
            ):
                contact_elem = self.find_element_optional(
                    creator_elem, self.NS_CMD, "Contact"
                )
                if contact_elem is None:
                    raise ValueError(
                        "WebLichtWebService Creator element found but missing required Contact child element"
                    )

                org_name = self.get_element_text(
                    contact_elem, self.NS_CMD, "Organisation"
                )
                if not org_name:
                    raise ValueError(
                        "WebLichtWebService Contact element found but missing required Organisation. "
                        "Only organizational creators are supported for web services."
                    )

                creators.append(
                    {
                        "person_or_org": {
                            "type": "organizational",
                            "name": org_name,
                        }
                    }
                )

        # If no creators found, raise error (strict validation)
        if not creators:
            raise ValueError(
                "WebLichtWebService must have at least one organizational creator in Creation/Creators/Creator/Contact/Organisation"
            )

        # Resource type is software/webservice
        resource_type = {"id": "software"}

        # Build RDM record
        rdm_record: dict[str, Any] = {
            "id": record_id,
            "metadata": {
                "title": title,
                "publication_date": publication_date,
                "resource_type": resource_type,
                "creators": creators,
                "description": description,
            },
        }

        # Add persistent URL if available
        if persistent_url:
            rdm_record["metadata"]["persistent_url"] = persistent_url

        # Files disabled for now
        rdm_record["files"] = {"enabled": False}
        rdm_record["media_files"] = {"enabled": False}

        self._remove_empty_fields(rdm_record)

        return rdm_record

    def _validate_olac_elements(self, olac_component: etree._Element) -> None:
        """Validate that all OLAC elements are known (strict parsing)."""
        known_elements = {
            "alternative",
            "available",
            "contributor",
            "creator",
            "date",
            "description",
            "format",
            "identifier",
            "isReferencedBy",
            "isReplacedBy",
            "issued",
            "language",
            "publisher",
            "relation",
            "replaces",
            "rights",
            "source",
            "subject",
            "title",
            "type",
        }

        for child in olac_component:
            local_name = etree.QName(child).localname
            if local_name not in known_elements:
                current_app.logger.error(
                    "Unknown OLAC-DcmiTerms element: %s. Known elements: %s", 
                    local_name, ', '.join(sorted(known_elements))
                )

    def _validate_weblicht_elements(self, weblicht_component: etree._Element) -> None:
        """Validate that WebLichtWebService structure is correct (strict parsing)."""

        # Check that Service element exists
        service_elem = self.find_element_optional(
            weblicht_component, self.NS_CMD, "Service"
        )
        if service_elem is None:
            raise ValueError(
                "WebLichtWebService component must have a Service child element"
            )

        # Known Service child elements
        known_service_elements = {
            "Name",
            "Description",
            "ApplicationType",
            "TypeOfWebservice",
            "url",
            "LifeCycleStatus",
            "PublicationDate",
            "LastUpdate",
            "ServiceDescriptionLocation",
            "Contact",
            "Creation",
            "Operations",
            "Licence",  # Alternative spelling
            "License",
        }

        # Validate all Service child elements are known
        for child in service_elem:
            local_name = etree.QName(child).localname
            if local_name not in known_service_elements:
                raise ValueError(
                    f"Unknown WebLichtWebService Service element: {local_name}. "
                    f"Known elements: {', '.join(sorted(known_service_elements))}"
                )

    def _extract_olac_title(self, olac_component: etree._Element) -> str:
        """Extract title from OLAC metadata."""
        return self.get_element_text(olac_component, self.NS_CMD, "title") or "Untitled"

    def _extract_olac_description(self, olac_component: etree._Element) -> str:
        """Extract description from OLAC metadata."""
        description = (
            self.get_element_text(olac_component, self.NS_CMD, "description") or ""
        )
        # Ensure minimum length of 3 characters for validation
        if len(description.strip()) < RDM_MINIMAL_DESCRIPTION_LENGTH:
            return f"Bad description, was too short: '{description}'"
        return description

    def _extract_olac_identifier(
        self, olac_component: etree._Element
    ) -> tuple[str | None, str | None]:
        """Extract identifier for record ID and persistent URL from OLAC metadata.

        Returns:
            Tuple of (record_id, persistent_url)
        """
        identifier_text = self.get_element_text(
            olac_component, self.NS_CMD, "identifier"
        )
        record_id = None
        persistent_url = None

        if identifier_text:
            # Extract handle ID from URL
            if "hdl.handle.net/" in identifier_text or "handle.net/" in identifier_text:
                # e.g., "http://hdl.handle.net/11372/LRT-1028" -> "handle/11372/LRT-1028"
                handle_part = identifier_text.split("handle.net/")[-1]
                record_id = f"handle/{handle_part}"
                persistent_url = identifier_text
            else:
                # Use identifier as-is
                record_id = identifier_text

        return record_id, persistent_url

    def _extract_olac_publication_date(self, olac_component: etree._Element) -> str:
        """Extract publication date from OLAC metadata."""
        publication_date = self.get_element_text(
            olac_component, self.NS_CMD, "issued"
        ) or self.get_element_text(olac_component, self.NS_CMD, "date")
        if not publication_date:
            raise ValueError(
                "Missing required publication date (issued or date) in OLAC-DcmiTerms"
            )
        return self._strip_time(publication_date)

    def _extract_olac_resource_type(self, olac_component: etree._Element) -> dict:
        """Extract resource type from OLAC metadata."""
        type_value = self.get_element_text(olac_component, self.NS_CMD, "type")
        return (
            self._extract_resource_type_from_value(type_value)
            if type_value
            else {"id": "other"}
        )

    def _extract_olac_languages(self, olac_component: etree._Element) -> list:
        """Extract languages from OLAC metadata."""
        languages = []
        lang_elem = self.find_element_optional(olac_component, self.NS_CMD, "language")
        if lang_elem is not None:
            # Try olac-language attribute first
            lang_code = lang_elem.get("olac-language")
            if not lang_code and lang_elem.text:
                lang_code = lang_elem.text.strip()

            if lang_code:
                lang_code_3 = self._convert_lang_code(lang_code)
                if self._validate_vocabulary_item(
                    "languages", lang_code_3, "languages"
                ):
                    languages.append({"id": lang_code_3})
                else:
                    # Language not in vocabulary, use 'und' (undetermined)
                    self.warnings.append(
                        f"Language code '{lang_code_3}' not in vocabulary, using 'und' (undetermined)"
                    )
                    languages.append({"id": "und"})
        return languages

    def _extract_olac_creators(self, olac_component: etree._Element) -> list:
        """Extract creators from OLAC metadata."""
        creators = []

        for creator_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "creator"
        ):
            if creator_elem.text:
                name = creator_elem.text.strip()
                if name:
                    person_or_org = {"type": "personal"}

                    # Try to parse name (often in "Last, First" format)
                    if "," in name:
                        parts = name.split(",", 1)
                        family_name = parts[0].strip()
                        given_name = parts[1].strip() if len(parts) > 1 else ""

                        if family_name:
                            person_or_org["family_name"] = family_name
                        if given_name:
                            person_or_org["given_name"] = given_name
                        person_or_org["name"] = name
                    else:
                        # Single name - use as is but also set family_name as it is required
                        person_or_org["name"] = name
                        person_or_org["family_name"] = name

                    creators.append({"person_or_org": person_or_org})

        # If no creators found, use placeholder
        if not creators:
            creators = [
                {
                    "person_or_org": {
                        "type": "organizational",
                        "name": "Unknown",
                    }
                }
            ]

        return creators

    def _extract_olac_contributors(self, olac_component: etree._Element) -> list:
        """Extract contributors from OLAC metadata."""
        contributors = []

        for contrib_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "contributor"
        ):
            if contrib_elem.text:
                name = contrib_elem.text.strip()
                if name:
                    person_or_org = {"type": "personal"}

                    # Try to parse name (often in "Last, First" format)
                    if "," in name:
                        parts = name.split(",", 1)
                        family_name = parts[0].strip()
                        given_name = parts[1].strip() if len(parts) > 1 else ""

                        if family_name:
                            person_or_org["family_name"] = family_name
                        if given_name:
                            person_or_org["given_name"] = given_name
                        person_or_org["name"] = name
                    else:
                        # Single name - use as is but also set family_name as it is required for personal type
                        person_or_org["name"] = name
                        person_or_org["family_name"] = name

                    contributors.append(
                        {
                            "person_or_org": person_or_org,
                            "role": {
                                "id": "other"
                            },  # Required field - default to 'other' role
                        }
                    )

        return contributors

    def _extract_olac_subjects(self, olac_component: etree._Element) -> list:
        """Extract subjects from OLAC metadata."""
        subjects = []
        for subject_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "subject"
        ):
            if subject_elem.text:
                subject_text = subject_elem.text.strip()
                if subject_text:
                    subjects.append({"subject": subject_text})
        return subjects

    def _extract_olac_rights(self, olac_component: etree._Element) -> list:
        """Extract rights/licenses from OLAC metadata."""
        rights = []
        for rights_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "rights"
        ):
            if rights_elem.text:
                rights_text = rights_elem.text.strip()
                if rights_text:
                    # Try to extract license ID from text
                    license_id = None
                    if "/" in rights_text:
                        license_id = rights_text.split("/")[-1].lower()

                    if license_id and self._validate_vocabulary_item(
                        "licenses", license_id, "rights"
                    ):
                        rights.append({"id": license_id})
                    else:
                        # Use title/link format if not in vocabulary
                        rights.append(
                            {
                                "title": {"en": rights_text},
                            }
                        )
        return rights

    def _extract_olac_formats(self, olac_component: etree._Element) -> list:
        """Extract formats from OLAC metadata."""
        formats = []
        for format_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "format"
        ):
            if format_elem.text:
                format_text = format_elem.text.strip()
                if format_text:
                    formats.append(format_text)
        return formats

    def _extract_olac_alternative_titles(self, olac_component: etree._Element) -> list:
        """Extract alternative titles from OLAC metadata."""
        alternative_titles = []
        for alt_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "alternative"
        ):
            if alt_elem.text:
                alt_text = alt_elem.text.strip()
                if alt_text:
                    alternative_titles.append(
                        {
                            "title": alt_text,
                            "type": {"id": "alternative-title"},
                            "lang": {
                                "id": "eng"
                            },  # Default to English, no lang info in OLAC
                        }
                    )
        return alternative_titles

    def _extract_olac_related_identifiers(self, olac_component: etree._Element) -> list:
        """Extract related identifiers from OLAC metadata."""
        related_identifiers = []

        # Add source as related identifier
        source = self.get_element_text(olac_component, self.NS_CMD, "source")
        if source:
            if self._validate_vocabulary_item(
                "relationtypes", "isderivedfrom", "relation_type"
            ):
                related_identifiers.append(
                    {
                        "identifier": source,
                        "scheme": "url",
                        "relation_type": {"id": "isderivedfrom"},
                    }
                )

        # Add replaces relationship
        for replaces_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "replaces"
        ):
            if replaces_elem.text:
                identifier_text = replaces_elem.text.strip()
                if identifier_text and self._validate_vocabulary_item(
                    "relationtypes", "isnewversionof", "relation_type"
                ):
                    related_identifiers.append(
                        {
                            "identifier": identifier_text,
                            "scheme": (
                                "url" if identifier_text.startswith("http") else "other"
                            ),
                            "relation_type": {"id": "isnewversionof"},
                        }
                    )

        # Add isReplacedBy relationship
        for replaced_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "isReplacedBy"
        ):
            if replaced_elem.text:
                identifier_text = replaced_elem.text.strip()
                if identifier_text and self._validate_vocabulary_item(
                    "relationtypes", "ispreviousversionof", "relation_type"
                ):
                    related_identifiers.append(
                        {
                            "identifier": identifier_text,
                            "scheme": (
                                "url" if identifier_text.startswith("http") else "other"
                            ),
                            "relation_type": {"id": "ispreviousversionof"},
                        }
                    )

        # Add isReferencedBy relationship
        for referenced_elem in self.find_all_elements(
            olac_component, self.NS_CMD, "isReferencedBy"
        ):
            if referenced_elem.text:
                identifier_text = referenced_elem.text.strip()
                if identifier_text and self._validate_vocabulary_item(
                    "relationtypes", "iscitedby", "relation_type"
                ):
                    related_identifiers.append(
                        {
                            "identifier": identifier_text,
                            "scheme": (
                                "url" if identifier_text.startswith("http") else "other"
                            ),
                            "relation_type": {"id": "iscitedby"},
                        }
                    )

        return related_identifiers

    def _remove_empty_fields(self, data: Any) -> Any:
        # recursively and in-place remove None, empty lists, and empty dicts from the data dict
        if isinstance(data, dict):
            keys_to_delete = []
            for key, value in data.items():
                cleaned_value = self._remove_empty_fields(value)
                if cleaned_value in (None, {}, []):
                    keys_to_delete.append(key)
                else:
                    data[key] = cleaned_value
            for key in keys_to_delete:
                del data[key]
            return data
        elif isinstance(data, list):
            indices_to_delete = []
            for index, item in enumerate(data):
                cleaned_item = self._remove_empty_fields(item)
                if cleaned_item in (None, {}, []):
                    indices_to_delete.append(index)
                else:
                    data[index] = cleaned_item
            for index in reversed(indices_to_delete):
                del data[index]
            return data
        else:
            return data

    def _extract_titles(self, bibliographic_info: etree._Element) -> list:
        """Extract titles from bibliographicInfo."""
        titles: list[str | dict] = []
        titles_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "titles"
        )
        if titles_elem is not None:
            for title_elem in self.find_all_elements(titles_elem, self.NS_CMD, "title"):
                lang = title_elem.get(
                    "{http://www.w3.org/XML/1998/namespace}lang", "en"
                )
                title_text = title_elem.text.strip() if title_elem.text else ""
                if title_text:
                    if len(titles) == 0:
                        # Main title is without a language
                        titles.append(title_text)
                    else:
                        # Additional titles
                        titles.append(
                            {
                                "title": title_text,
                                "type": {"id": "alternative-title"},
                                "lang": {"id": self._convert_lang_code(lang)},
                            }
                        )
        return titles

    def _extract_creators(self, bibliographic_info: etree._Element) -> list:
        """Extract creators/authors from bibliographicInfo."""
        creators = []
        authors_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "authors"
        )
        if authors_elem is not None:
            for author_elem in self.find_all_elements(
                authors_elem, self.NS_CMD, "author"
            ):
                first_name = (
                    self.get_element_text(author_elem, self.NS_CMD, "firstName") or ""
                )
                last_name = (
                    self.get_element_text(author_elem, self.NS_CMD, "lastName") or ""
                )

                # Build person_or_org
                person_or_org = {
                    "type": "personal",
                }

                if first_name and last_name:
                    person_or_org["given_name"] = first_name
                    person_or_org["family_name"] = last_name
                    person_or_org["name"] = f"{last_name}, {first_name}"
                elif last_name:
                    person_or_org["name"] = last_name
                elif first_name:
                    person_or_org["name"] = first_name
                else:
                    continue  # Skip if no name

                creators.append({"person_or_org": person_or_org})

        if not creators:
            creators = [
                {
                    "person_or_org": {
                        "type": "organizational",
                        "name": "Unknown",
                    }
                }
            ]

        return creators

    def _extract_publication_date(self, bibliographic_info: etree._Element) -> str:
        """Extract publication date from bibliographicInfo."""
        dates_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "dates"
        )
        if dates_elem is not None:
            ret = self.get_element_text(dates_elem, self.NS_CMD, "dateIssued")
            if ret is None:
                raise ValueError("No <dateIssued> found in <dates>.")
            return ret
        raise ValueError("No <dates> element found in bibliographicInfo.")

    def _extract_resource_type(self, data_info: etree._Element) -> dict:
        """Extract resource type from dataInfo.

        Maps LINDAT resource types to RDM resource types based on
        ccmm_resource_types.yaml zenodo mappings.
        """
        type_value = self.get_element_text(data_info, self.NS_CMD, "type")
        return self._extract_resource_type_from_value(type_value)

    def _extract_resource_type_from_value(self, type_value: str | None) -> dict:
        """Map resource type value to RDM resource type.

        Used by both LINDAT and OLAC converters.
        """
        if type_value:
            # Map LINDAT types to first zenodo term from ccmm_resource_types.yaml
            # Based on props.lindat -> first value in props.zenodo
            # https://github.com/NRP-CZ/ccmm-invenio/blob/main/src/ccmm_invenio/fixtures/ccmm_resource_types.yaml
            type_mapping = {
                "corpus": "publication",  # text type, first zenodo term
                "languageDescription": "publication",  # text type, first zenodo term
                "toolService": "software",  # software type, first zenodo term
                "Spreadsheet": "dataset",  # dataset type
                "OBRAZ": "image-figure",  # still image type, first zenodo term
                "clip": "video",  # video type
                "bibliography": "other",  # no zenodo mapping, fallback
                "lexicalConceptualResource": "other",  # knowledge org system, no zenodo mapping
                "onlineCourse": "other",  # learning object, no zenodo mapping
            }
            rdm_type = type_mapping.get(type_value, "other")

            # Validate the resource type exists in vocabulary
            if self._validate_vocabulary_item(
                "resourcetypes", rdm_type, "resource_type"
            ):
                return {"id": rdm_type}
            else:
                # Fallback to 'other' if validation fails
                if self._validate_vocabulary_item(
                    "resourcetypes", "other", "resource_type"
                ):
                    return {"id": "other"}

        # Default fallback
        return {"id": "other"}

    def _extract_description(self, data_info: etree._Element) -> str:
        """Extract description from dataInfo."""
        desc_text = self.get_element_text(data_info, self.NS_CMD, "description")
        if desc_text:
            return self._sanitize_html(desc_text)
        return ""

    def _extract_identifier(self, bibliographic_info: etree._Element) -> str | None:
        """Extract identifier from bibliographicInfo."""
        identifiers_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "identifiers"
        )
        if identifiers_elem is not None:
            identifier_elem = self.find_element_optional(
                identifiers_elem, self.NS_CMD, "identifier"
            )
            if identifier_elem is not None and identifier_elem.text:
                identifier_type = identifier_elem.get("type", "").strip()
                if (
                    identifier_type.lower() == "handle"
                    and "https://hdl.handle.net/" in identifier_elem.text
                ):
                    # the identifier is handle/<whatever comes after hdl.handle.net/>
                    handle_url = identifier_elem.text.strip()
                    handle_url = handle_url.split("hdl.handle.net/")[-1]

                    return "handle/" + handle_url
        return None

    def _extract_handle_url(self, bibliographic_info: etree._Element) -> str | None:
        """Extract Handle URL from bibliographicInfo."""
        identifiers_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "identifiers"
        )
        if identifiers_elem is not None:
            identifier_elem = self.find_element_optional(
                identifiers_elem, self.NS_CMD, "identifier"
            )
            if identifier_elem is not None and identifier_elem.text:
                identifier_type = identifier_elem.get("type", "").strip()
                if (
                    identifier_type.lower() == "handle"
                    and "https://hdl.handle.net/" in identifier_elem.text
                ):
                    return identifier_elem.text.strip()
        return None

    def _extract_publishers(self, bibliographic_info: etree._Element) -> str | None:
        """Extract publisher from bibliographicInfo."""
        publishers_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "publishers"
        )
        if publishers_elem is not None:
            return self.get_element_text(publishers_elem, self.NS_CMD, "publisher")
        return None

    def _extract_languages(self, data_info: etree._Element) -> list:
        """Extract languages from dataInfo."""
        languages = []
        languages_elem = self.find_element_optional(data_info, self.NS_CMD, "languages")
        if languages_elem is not None:
            for lang_elem in self.find_all_elements(
                languages_elem, self.NS_CMD, "language"
            ):
                lang_code = self.get_element_text(lang_elem, self.NS_CMD, "code")
                if lang_code:
                    # Convert to 3-letter code if needed
                    lang_code_3 = self._convert_lang_code(lang_code)
                    if self._validate_vocabulary_item(
                        "languages", lang_code_3, "languages"
                    ):
                        languages.append({"id": lang_code_3})
                    else:
                        # Language not in vocabulary, use 'und' (undetermined)
                        self.warnings.append(
                            f"Language code '{lang_code_3}' not in vocabulary, using 'und' (undetermined)"
                        )
                        languages.append({"id": "und"})
        return languages if languages else []

    def _extract_subjects(self, data_info: etree._Element) -> list:
        """Extract subjects/keywords from dataInfo."""
        subjects = []
        keywords_elem = self.find_element_optional(data_info, self.NS_CMD, "keywords")
        if keywords_elem is not None:
            for keyword_elem in self.find_all_elements(
                keywords_elem, self.NS_CMD, "keyword"
            ):
                if keyword_elem.text:
                    keyword_text = keyword_elem.text.strip()
                    if keyword_text:
                        subjects.append({"subject": keyword_text})
        return subjects if subjects else []

    def _extract_rights(self, license_info: etree._Element) -> list:
        """Extract rights/license from licenseInfo."""
        rights = []
        license_elem = self.find_element_optional(license_info, self.NS_CMD, "license")
        if license_elem is not None:
            license_uri = self.get_element_text(license_elem, self.NS_CMD, "uri")
            if license_uri:
                # Try to extract license ID from URI
                # e.g., "http://opensource.org/licenses/LGPL-3.0" -> "lgpl-3.0"
                license_id = None
                if "/" in license_uri:
                    license_id = license_uri.split("/")[-1].lower()

                if license_id:
                    # Validate the license exists in vocabulary
                    if self._validate_vocabulary_item("licenses", license_id, "rights"):
                        rights.append({"id": license_id})
                    else:
                        # If not in vocabulary, use title and link instead
                        rights.append(
                            {
                                "title": {"en": license_uri},
                            }
                        )
                else:
                    rights.append(
                        {
                            "title": {"en": license_uri},
                        }
                    )
        return rights if rights else []

    def _extract_funding(self, bibliographic_info: etree._Element) -> list:
        """Extract funding information from bibliographicInfo."""
        funding_list = []
        funds_elem = self.find_element_optional(
            bibliographic_info, self.NS_CMD, "funds"
        )
        if funds_elem is not None:
            for funding_elem in self.find_all_elements(
                funds_elem, self.NS_CMD, "funding"
            ):
                org_name = self.get_element_text(
                    funding_elem, self.NS_CMD, "organization"
                )
                code = self.get_element_text(funding_elem, self.NS_CMD, "code")
                project_name = self.get_element_text(
                    funding_elem, self.NS_CMD, "projectName"
                )

                funding_entry = {}

                # Funder
                if org_name:
                    funding_entry["funder"] = {"name": org_name}

                # Award
                award_data = {}
                if code:
                    award_data["number"] = code
                if project_name:
                    award_data["title"] = {"en": project_name}

                if award_data:
                    funding_entry["award"] = award_data

                if funding_entry:
                    funding_list.append(funding_entry)

        return funding_list if funding_list else []

    def _extract_related_identifiers(self, bibliographic_info: etree._Element) -> list:
        """Extract related identifiers (e.g., project URL) from bibliographicInfo."""
        related_ids = []
        project_url = self.get_element_text(
            bibliographic_info, self.NS_CMD, "projectUrl"
        )
        if project_url:
            # Validate the relation type exists in vocabulary
            relation_type = "issupplementedby"
            if self._validate_vocabulary_item(
                "relationtypes", relation_type, "relation_type"
            ):
                related_ids.append(
                    {
                        "identifier": project_url,
                        "scheme": "url",
                        "relation_type": {"id": relation_type},
                    }
                )
        return related_ids if related_ids else []

    def _convert_lang_code(self, lang_code: str) -> str:
        """Convert language code to 3-letter ISO 639-3 format."""
        try:
            lang = Language.get(lang_code)
            # Try to get ISO 639-3 code, fallback to ISO 639-2 or original
            return lang.to_alpha3() if hasattr(lang, "to_alpha3") else lang_code.lower()
        except Exception:
            # If conversion fails, return lowercase original
            return lang_code.lower()

    def _sanitize_html(self, text: str) -> str:
        """Sanitize HTML content."""
        if not text:
            return text

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

    def find_element(self, parent: etree._Element, namespace: str, local_name: str):
        """Find required element in XML."""
        ret = parent.find(f"{{{namespace}}}{local_name}")
        if ret is None:
            raise ValueError(f"No <{local_name}> element found in the parent.")
        return ret

    def find_element_optional(
        self, parent: etree._Element, namespace: str, local_name: str
    ):
        """Find optional element in XML, return None if not found."""
        return parent.find(f"{{{namespace}}}{local_name}")

    def get_element_text(
        self, parent: etree._Element, namespace: str, local_name: str
    ) -> str | None:
        """Get text content from an optional element, return None if not found or empty."""
        elem = self.find_element_optional(parent, namespace, local_name)
        if elem is not None and elem.text:
            return elem.text.strip()
        return None

    def find_all_elements(
        self, parent: etree._Element, namespace: str, local_name: str
    ):
        """Find all elements with the given name in XML."""
        return parent.findall(f"{{{namespace}}}{local_name}")


SAMPLE_OAI_RECORD = """
<record xmlns="http://www.openarchives.org/OAI/2.0/"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <header>
    <identifier>oai:lindat.mff.cuni.cz:11234/1-3068</identifier>
    <datestamp>2025-06-24T19:42:29Z</datestamp>
    <setSpec>com_11858_00-097C-0000-0001-486F-D</setSpec>
    <setSpec>com_11234_3430</setSpec>
    <setSpec>col_11858_00-097C-0000-0001-4877-A</setSpec>
    </header>
    <metadata>
    <cmd:CMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:cmd="http://www.clarin.eu/cmd/"
        xmlns:lindat="http://lindat.mff.cuni.cz/ns/experimental/cmdi" CMDVersion="1.1" xsi:schemaLocation="http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1403526079380/xsd">
        <cmd:Header>
            <cmd:MdCreationDate>2025-06-24 21:42:29.284</cmd:MdCreationDate>
            <cmd:MdSelfLink>https://hdl.handle.net/11234/1-3068@format=cmdi</cmd:MdSelfLink>
            <cmd:MdProfile>clarin.eu:cr1:p_1403526079380</cmd:MdProfile>
            <cmd:MdCollectionDisplayName>LINDAT / CLARIAH-CZ Data &amp; Tools</cmd:MdCollectionDisplayName>
        </cmd:Header>
        <cmd:Resources>
            <cmd:ResourceProxyList>
                <cmd:ResourceProxy id="lp_009148f9-ac95-4283-aff4-c07dc775a1cf">
                <cmd:ResourceType>LandingPage</cmd:ResourceType>
                <cmd:ResourceRef>https://hdl.handle.net/11234/1-3068</cmd:ResourceRef>
                </cmd:ResourceProxy>
                <cmd:ResourceProxy id="uri_1">
                <cmd:ResourceType mimetype="text/html">Resource</cmd:ResourceType>
                <cmd:ResourceRef>https://www.muni.cz/vyzkum/projekty/40205</cmd:ResourceRef>
                </cmd:ResourceProxy>
                <cmd:ResourceProxy id="_be69be86-1edc-4bf4-8ba4-2102a91b4262">
                <cmd:ResourceType mimetype="application/x-xz">Resource</cmd:ResourceType>
                <cmd:ResourceRef lindat:md5_checksum="85d3ca4e908692dd5a9cfe7c100318a8">https://lindat.mff.cuni.cz/repository//bitstream/handle/11234/1-3068/sqad_v2.1.tar.xz?sequence=3</cmd:ResourceRef>
                </cmd:ResourceProxy>
            </cmd:ResourceProxyList>
            <cmd:JournalFileProxyList/>
            <cmd:ResourceRelationList/>
        </cmd:Resources>
        <cmd:Components>
            <cmd:LINDAT_CLARIN>
                <cmd:bibliographicInfo>
                <cmd:projectUrl>https://www.muni.cz/vyzkum/projekty/40205</cmd:projectUrl>
                <cmd:titles>
                    <cmd:title xml:lang="en">sqad 2.1</cmd:title>
                </cmd:titles>
                <cmd:authors>
                    <author xmlns="http://www.clarin.eu/cmd/">
                        <lastName>Medveď</lastName>
                        <firstName> Marek</firstName>
                    </author>
                    <author xmlns="http://www.clarin.eu/cmd/">
                        <lastName>Horák</lastName>
                        <firstName> Aleš</firstName>
                    </author>
                    <author xmlns="http://www.clarin.eu/cmd/">
                        <lastName>Kušniráková</lastName>
                        <firstName> Dáša</firstName>
                    </author>
                </cmd:authors>
                <cmd:dates>
                    <cmd:dateIssued>2019-10-14</cmd:dateIssued>
                </cmd:dates>
                <cmd:identifiers>
                    <cmd:identifier type="Handle">https://hdl.handle.net/11234/1-3068</cmd:identifier>
                </cmd:identifiers>
                <cmd:funds>
                    <funding xmlns="http://www.clarin.eu/cmd/">
                        <organization>Czech Science Foundation</organization>
                        <code>GA18-23891S</code>
                        <projectName>Hyperintensionální usuzování nad texty přirozeného jazyka</projectName>
                        <fundsType>nationalFunds</fundsType>
                    </funding>
                    <funding xmlns="http://www.clarin.eu/cmd/">
                        <organization>Ministerstvo školství, mládeže a tělovýchovy České republiky</organization>
                        <code>LM2015071</code>
                        <projectName>LINDAT/CLARIN: Institut pro analýzu, zpracování a distribuci lingvistických dat</projectName>
                        <fundsType>nationalFunds</fundsType>
                    </funding>
                </cmd:funds>
                <contactPerson xmlns="http://www.clarin.eu/cmd/">
                    <firstName>Marek</firstName>
                    <lastName>Medveď</lastName>
                    <email>xmedved1@fi.muni.cz</email>
                    <affiliation>Masaryk University, NLP Centre</affiliation>
                </contactPerson>
                <cmd:publishers>
                    <cmd:publisher>Natural Language Processing Centre, Faculty of Informatics, Masaryk University</cmd:publisher>
                </cmd:publishers>
                </cmd:bibliographicInfo>
                <cmd:dataInfo>
                <cmd:type>corpus</cmd:type>
                <cmd:description>Simple question answering database version 2.1 (SQAD_v2.1) created from Czech Wikipedia. Each record of SQAD consist of four files (in vertical form provided with lemmatization and POS tagging) and two metadata files.</cmd:description>
                <cmd:languages>
                    <cmd:language>
                        <cmd:code>ces</cmd:code>
                        <cmd:name>Czech</cmd:name>
                    </cmd:language>
                </cmd:languages>
                <cmd:keywords>
                    <cmd:keyword>Czech</cmd:keyword>
                    <cmd:keyword>Simple Question Answering Database</cmd:keyword>
                    <cmd:keyword>question answering</cmd:keyword>
                </cmd:keywords>
                <cmd:sizeInfo>
                    <size xmlns="http://www.clarin.eu/cmd/">
                        <size>8566</size>
                        <unit>other</unit>
                    </size>
                </cmd:sizeInfo>
                </cmd:dataInfo>
                <cmd:licenseInfo>
                <cmd:license>
                    <cmd:uri>http://opensource.org/licenses/LGPL-3.0</cmd:uri>
                </cmd:license>
                </cmd:licenseInfo>
            </cmd:LINDAT_CLARIN>
        </cmd:Components>
    </cmd:CMD>
    </metadata>
</record>
""".strip()

if __name__ == "__main__":
    import traceback

    import click
    from flask.cli import with_appcontext
    from invenio_access.permissions import system_identity
    from invenio_vocabularies.datastreams.readers import OAIPMHReader
    from oarepo_runtime import current_runtime
    from rich.console import Console

    @click.command
    @with_appcontext
    def run_sample():
        console = Console()
        console.rule("[bold blue]LINDAT/CLARIN Transformer Sample Run[/bold blue]")
        transformer = LindatTransformer()
        loader = OAIPMHReader(
            base_url="https://lindat.mff.cuni.cz/repository/server/oai/request",
            metadata_prefix="cmdi",
        )
        for stream_entry in loader.read():
            transformed_entry = None
            try:
                transformed_entry = transformer.apply(stream_entry)

                # Check if there are warnings
                has_warnings = transformed_entry.entry.get("warnings")

                if has_warnings:
                    # Print full details if there are warnings
                    console.print(
                        "[bold yellow]⚠ Transformation completed with warnings[/bold yellow]"
                    )
                    console.print("Transformed data", transformed_entry.entry["record"])
                    console.print(
                        "[bold red]Warnings:[/bold red]",
                        transformed_entry.entry.get("warnings"),
                    )

                loaded_data = current_runtime.models["datasets"].service.schema.load(
                    transformed_entry.entry["record"],
                    raise_errors=True,
                    context={"identity": system_identity},
                )[0]

                if has_warnings:
                    console.print("Loaded data", loaded_data)

                loaded_data["id"] += str(uuid4().hex)  # ensure unique ID for testing

                rec = current_runtime.models["datasets"].service.create(
                    system_identity, loaded_data
                )
                current_runtime.models["datasets"].service.publish(
                    system_identity, rec.id
                )

                if has_warnings:
                    console.print("[bold green]✓ Created record:[/bold green]", rec.id)
                else:
                    # For successful transformation without warnings, just print the ID
                    console.print(f"[bold green]✓[/bold green] {rec.id}")

            except Exception:
                # Print full details on exception
                console.print(
                    "[bold red]❌ Error during transformation or loading[/bold red]"
                )
                console.print("Original data", stream_entry["record"].raw)
                if transformed_entry:
                    console.print(
                        "Transformed data", transformed_entry.entry.get("record")
                    )
                    console.print(
                        "[bold red]Warnings:[/bold red]",
                        transformed_entry.entry.get("warnings"),
                    )
                console.print(
                    f"[bold red]Exception:[/bold red]\n{traceback.format_exc()}"
                )

    from invenio_app.cli import cli

    cli.add_command(run_sample)
    cli.main(["run-sample"])
