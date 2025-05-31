import copy
import logging
import sys
import traceback
from functools import cached_property
from typing import Union

import bleach
import tqdm
import yaml
from invenio_access.permissions import system_identity
from oarepo_runtime.datastreams import BaseTransformer, StreamBatch, StreamEntry
from oarepo_runtime.datastreams.types import StreamEntryError

from common.oai.ccmm_tools import (
    file_formats_by_extension,
    file_formats_by_iana,
    get_ccmm_lang_iri,
    get_ccmm_role,
    lang_dict_to_2,
    relation_types_cache,
)

log = logging.getLogger("oai.zenodo")

UNKNOWN_LANGUAGE_IRI = "https://publications.europa.eu/resource/authority/language/UND"

allowed_tags = set(
    [
        *bleach.ALLOWED_TAGS,
        "span",
        "p",
        "br",
        "pre",
        "code",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
    ]
)


class ZenodoTransformer(BaseTransformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, batch: StreamBatch, *args, **kwargs) -> Union[StreamBatch, None]:
        """Applies the transformation to the entry.
        :returns: A StreamEntry. The transformed entry.
                  Raises TransformerError in case of errors.
        """
        for entry in batch.entries:
            try:
                self.transform_entry(entry)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                entry.errors.append(StreamEntryError.from_exception(e))
        return batch

    def transform_entry(self, entry: StreamEntry):
        """
        Transforms the entry.
        """
        entry.entry = self.convert_record_to_ccmm({**entry.entry})

    """
    Example zenodo record:
{
  "id": "14646925",
  "created": "2025-01-14T17:04:17.696221+00:00",
  "updated": "2025-01-14T17:04:17.860579+00:00",
  "links": {
    "self": "https://zenodo.org/api/records/14646925",
    "self_html": "https://zenodo.org/records/14646925",
    "preview_html": "https://zenodo.org/records/14646925?preview=1",
    "doi": "https://doi.org/10.5281/zenodo.14646925",
    "self_doi": "https://doi.org/10.5281/zenodo.14646925",
    "self_doi_html": "https://zenodo.org/doi/10.5281/zenodo.14646925",
    "parent": "https://zenodo.org/api/records/14646924",
    "parent_html": "https://zenodo.org/records/14646924",
    "parent_doi": "https://doi.org/10.5281/zenodo.14646924",
    "parent_doi_html": "https://zenodo.org/doi/10.5281/zenodo.14646924",
    "self_iiif_manifest": "https://zenodo.org/api/iiif/record:14646925/manifest",
    "self_iiif_sequence": "https://zenodo.org/api/iiif/record:14646925/sequence/default",
    "files": "https://zenodo.org/api/records/14646925/files",
    "media_files": "https://zenodo.org/api/records/14646925/media-files",
    "thumbnails": {
      "10": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^10,/0/default.jpg",
      "50": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^50,/0/default.jpg",
      "100": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^100,/0/default.jpg",
      "250": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^250,/0/default.jpg",
      "750": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^750,/0/default.jpg",
      "1200": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/^1200,/0/default.jpg"
    },
    "archive": "https://zenodo.org/api/records/14646925/files-archive",
    "archive_media": "https://zenodo.org/api/records/14646925/media-files-archive",
    "latest": "https://zenodo.org/api/records/14646925/versions/latest",
    "latest_html": "https://zenodo.org/records/14646925/latest",
    "versions": "https://zenodo.org/api/records/14646925/versions",
    "draft": "https://zenodo.org/api/records/14646925/draft",
    "reserve_doi": "https://zenodo.org/api/records/14646925/draft/pids/doi",
    "access_links": "https://zenodo.org/api/records/14646925/access/links",
    "access_grants": "https://zenodo.org/api/records/14646925/access/grants",
    "access_users": "https://zenodo.org/api/records/14646925/access/users",
    "access_request": "https://zenodo.org/api/records/14646925/access/request",
    "access": "https://zenodo.org/api/records/14646925/access",
    "communities": "https://zenodo.org/api/records/14646925/communities",
    "communities-suggestions": "https://zenodo.org/api/records/14646925/communities-suggestions",
    "requests": "https://zenodo.org/api/records/14646925/requests"
  },
  "revision_id": 4,
  "parent": {
    "id": "14646924",
    "access": {
      "owned_by": {
        "user": "219147"
      },
      "settings": {
        "allow_user_requests": false,
        "allow_guest_requests": false,
        "accept_conditions_text": null,
        "secret_link_expiration": 0
      }
    },
    "communities": {
      "ids": [
        "e567b3f5-5b02-4da7-9ff3-54123b882a71"
      ],
      "default": "e567b3f5-5b02-4da7-9ff3-54123b882a71",
      "entries": [
        {
          "id": "e567b3f5-5b02-4da7-9ff3-54123b882a71",
          "created": "2021-05-14T11:23:29.667982+00:00",
          "updated": "2024-06-25T14:13:08.018579+00:00",
          "links": {},
          "revision_id": 3,
          "slug": "labdiagn",
          "metadata": {
            "title": "Laboratórna Diagnostika",
            "description": "recenzovaný časopis pre pracovníkov diagnostických laboratórií",
            "curation_policy": "<p>pr&iacute;spevky akceptovan&eacute; redakčnou radou odborn&eacute;ho časopisu Laborat&oacute;rna Diagnostika</p>",
            "website": "https://www.sskb.sk/2022/",
            "organizations": [
              {
                "name": "SLOVENSKÁ SPOLOČNOSŤ KLINICKEJ BIOCHÉMIE SLS"
              }
            ]
          },
          "access": {
            "visibility": "public",
            "members_visibility": "public",
            "member_policy": "open",
            "record_submission_policy": "open",
            "review_policy": "open"
          },
          "custom_fields": {},
          "deletion_status": {
            "is_deleted": false,
            "status": "P"
          },
          "children": {
            "allow": false
          }
        }
      ]
    },
    "pids": {
      "doi": {
        "identifier": "10.5281/zenodo.14646924",
        "provider": "datacite",
        "client": "datacite"
      }
    }
  },
  "versions": {
    "is_latest": true,
    "index": 1
  },
  "is_published": true,
  "is_draft": false,
  "pids": {
    "doi": {
      "identifier": "10.5281/zenodo.14646925",
      "provider": "datacite",
      "client": "datacite"
    },
    "oai": {
      "identifier": "oai:zenodo.org:14646925",
      "provider": "oai"
    }
  },
  "metadata": {
    "resource_type": {
      "id": "publication-article",
      "title": {
        "de": "Zeitschriftenartikel",
        "en": "Journal article"
      }
    },
    "creators": [
      {
        "person_or_org": {
          "type": "personal",
          "name": "Jabor, Antonín",
          "given_name": "Antonín",
          "family_name": "Jabor"
        },
        "affiliations": [
          {
            "name": "Pracoviště laboratorních metod, Institut klinické a experimentální medicíny, Praha, Česká republika"
          },
          {
            "name": "3. lékařská fakulta Univerzity Karlovy, Praha, Česká republika"
          }
        ]
      },
      {
        "person_or_org": {
          "type": "personal",
          "name": "Franeková, Janka",
          "given_name": "Janka",
          "family_name": "Franeková"
        },
        "affiliations": [
          {
            "name": "Pracoviště laboratorních metod, Institut klinické a experimentální medicíny, Praha, Česká republika"
          },
          {
            "name": "3. lékařská fakulta Univerzity Karlovy, Praha, Česká republika"
          }
        ]
      }
    ],
    "title": "Vnitřní prostředí, tekutinová strategie a sepse / \"Milieu interieur\", fluid stewardship, and sepsis",
    "publisher": "Zenodo",
    "publication_date": "2024-11-17",
    "languages": [
      {
        "id": "ces",
        "title": {
          "en": "Czech"
        }
      }
    ],
    "rights": [
      {
        "id": "cc-by-4.0",
        "title": {
          "en": "Creative Commons Attribution 4.0 International"
        },
        "description": {
          "en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."
        },
        "icon": "cc-by-icon",
        "props": {
          "url": "https://creativecommons.org/licenses/by/4.0/legalcode",
          "scheme": "spdx"
        }
      }
    ],
    "description": "<p><strong><span>Souhrn</span></strong></p>\n<p><span>Formou narativn&iacute;ho přehledu se autoři zab&yacute;vaj&iacute; problematikou sepse a septick&eacute;ho &scaron;oku se zvl&aacute;&scaron;tn&iacute;m zaměřen&iacute;m na glykokalyx, revidovanou Starlingovu rovnici, tekutinovou strategii, vztah mezi klinick&yacute;mi projevy org&aacute;nov&eacute; dysfunkce a laboratorn&iacute;mi ukazateli, možnosti infuzn&iacute; terapie a vztah mezi iontov&yacute;m složen&iacute;m infuzn&iacute;ch roztoků a acidobazickou rovnov&aacute;hou. </span></p>\n<p><strong><span>Abstract</span></strong></p>\n<p><span>In the form of a narrative overview, the authors deal with the issue of sepsis and septic shock with a special focus on the glycocalyx, the revised Starling equation, fluid stewardship, the relationship between clinical manifestations of organ dysfunction and laboratory indicators, the possibilities of infusion therapy and the relationship between the electrolyte composition of infusion solutions and acid-base balance.</span></p>"
  },
  "custom_fields": {
    "journal:journal": {
      "title": "Laboratórna Diagnostika",
      "issue": "2/2024",
      "volume": "XXIX",
      "pages": "159-166"
    }
  },
  "access": {
    "record": "public",
    "files": "public",
    "embargo": {
      "active": false,
      "reason": null
    },
    "status": "open"
  },
  "files": {
    "enabled": true,
    "default_preview": "Laboratórna Diagnostika XXIX_2_2024_159-166.pdf.pdf",
    "order": [],
    "count": 1,
    "total_bytes": 363181,
    "entries": {
      "Laboratórna Diagnostika XXIX_2_2024_159-166.pdf.pdf": {
        "id": "4484d3af-2c2d-47b8-8836-973c8a671f6a",
        "checksum": "md5:84d6bba940df0daa7888411deb3b71e8",
        "ext": "pdf",
        "size": 363181,
        "mimetype": "application/pdf",
        "storage_class": "L",
        "key": "Laboratórna Diagnostika XXIX_2_2024_159-166.pdf.pdf",
        "metadata": {},
        "access": {
          "hidden": false
        },
        "links": {
          "self": "https://zenodo.org/api/records/14646925/files/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
          "content": "https://zenodo.org/api/records/14646925/files/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/content",
          "iiif_canvas": "https://zenodo.org/api/iiif/record:14646925/canvas/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
          "iiif_base": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
          "iiif_info": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/info.json",
          "iiif_api": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/full/0/default.png"
        }
      }
    }
  },
  "media_files": { ... },
  "status": "published",
  "deletion_status": {
    "is_deleted": false,
    "status": "P"
  },
  "stats": { ... }
  "swh": {},
  "ui": { ... }
}


    """

    def convert_record_to_ccmm(self, rec):
        rec = copy.deepcopy(rec)

        links = rec.pop("links")
        link = links["self"]
        files = rec.pop("files", {})

        id = rec.pop("id")
        orig_md = rec.pop("metadata")

        languages = orig_md.pop("languages", [])
        if not languages:
            language = "und"
        else:
            language = languages[0]["id"]

        transformed = {
            "files": {
                "enabled": False,
            },
            "metadata": {
                "is_described_by": [
                    {
                        "iri": link,
                        "dates_updated": [],
                        "languages": [{"iri": get_ccmm_lang_iri(language)}],
                        "original_repositories": [
                            {
                                "iri": "https://zenodo.org",
                                "labels": [
                                    {"lang": "en", "value": "Zenodo repository"},
                                ],
                            }
                        ],
                    }
                ],
            },
        }
        md = transformed["metadata"]
        md["primary_language"] = {
            "iri": get_ccmm_lang_iri(language),
        }

        md["identifiers"] = [
            self.convert_doi(pid)
            for pid_type, pid in rec.pop("pids", {}).items()
            if pid_type == "doi"
        ]
        md["identifiers"] += [
            self.convert_identifier(i) for i in orig_md.pop("identifiers", [])
        ]

        for orig_creator in orig_md.pop("creators", []):
            if "role" in orig_creator:
                self.convert_contributor(md, orig_creator)
            else:
                self.convert_creator(md, orig_creator)

        for orig_contributor in orig_md.pop("contributors", []):
            self.convert_contributor(md, orig_contributor)

        md["descriptions"] = self.convert_description(orig_md.pop("description", None))
        md["descriptions"] += [
            self.convert_additional_description(x)
            for x in orig_md.pop("additional_descriptions", [])
        ]

        md["time_references"] = self.convert_dates(orig_md)

        md["resource_type"] = self.convert_resource_type(
            orig_md.pop("resource_type", None)
        )

        md["title"] = orig_md.pop("title")

        md["alternate_titles"] = [
            self.convert_additional_title(x)
            for x in orig_md.pop("additional_titles", [])
        ]

        md["version"] = orig_md.pop("version", None)

        md.setdefault("qualified_relations", []).append(
            {
                "role": {
                    "iri": "https://vocabs.ccmm.cz/registry/codelist/AgentRole/Publisher",
                },
                "organization": {
                    "name": orig_md.pop("publisher", "Zenodo"),
                },
            }
        )

        md["terms_of_use"] = self.convert_rights(orig_md.pop("rights", []))

        md["terms_of_use"]["access_rights"] = self.convert_access_rights(
            rec.pop("access", {}), bool(files)
        )

        md["subjects"] = self.convert_subjects(orig_md.pop("subjects", []))

        md["related_resources"] = self.convert_related_items(
            orig_md.pop("related_identifiers", [])
        )

        md["funding_references"] = [
            self.convert_funding(f) for f in orig_md.pop("funding", [])
        ]

        md["locations"] = [
            self.convert_location(l)
            for l in orig_md.pop("locations", {}).get("features", [])
        ]

        orig_md.pop(
            "references", None
        )  # text-only references, no place for those in ccmm

        orig_md.pop("dates", None)  # TODO: not translated now

        md["distributions"] = [
            self.convert_file(f, link) for f in files.get("entries", {}).values()
        ]

        transformed["metadata"] = {
            k: v for k, v in md.items() if v is not None and v != []
        }
        transformed = {
            k: v for k, v in transformed.items() if v is not None and v != []
        }
        for k, v in list(transformed.items()):
            if isinstance(v, list):
                transformed[k] = [vv for vv in v if vv]

        self.ensureEmpty(
            orig_md,
        )
        self.ensureEmpty(
            rec,
            "created",
            "updated",
            "revision_id",
            "parent",
            "versions",
            "is_published",
            "is_draft",
            "custom_fields",
            "media_files",
            "status",
            "deletion_status",
            "stats",
            "swh",
            "ui",
        )
        return transformed

        @cached_property
        def file_formats_by_extension(self):
            """Cache the file formats by extension."""
            return file_formats_by_extension()

        @cached_property
        def file_formats_by_iana(self):
            """Cache the file formats by IANA type."""
            return file_formats_by_iana()

    def ensureEmpty(self, data, *exceptions, filter=True):
        for key in data.keys():
            if key not in exceptions:
                if filter:
                    filtered_data = {
                        k: v for k, v in data.items() if k not in exceptions
                    }
                else:
                    filtered_data = data
                raise Exception(f"Unhandled key: {key} inside data: {filtered_data}")

    def convert_doi(self, doi):
        return {
            "identifier_scheme": {"iri": "https://doi.org/"},
            "value": doi["identifier"],
            "iri": "https://doi.org/" + doi["identifier"],
        }

    #
    # not checked follow
    #

    def convert_creator(self, md, orig_creator):
        self.convert_creator_contributor(
            md,
            orig_creator,
            "https://vocabs.ccmm.cz/registry/codelist/AgentRole/Creator",
        )

    def convert_contributor(self, md, orig_contributor):
        def capitalize(x):
            if not x:
                return x
            return x[0].upper() + x[1:]

        data_cite_code = "".join(
            capitalize(x) for x in orig_contributor.pop("role")["title"]["en"].split()
        )
        self.convert_creator_contributor(
            md,
            orig_contributor,
            get_ccmm_role(data_cite_code),
        )

    def convert_creator_contributor(self, md, orig_creator, role_iri):
        """
        Convert creator or contributor to CCMM format.

        orig_creator looks like this:
        {
            "person_or_org": {
                "type": "personal",
                "name": "Zahradník, Jiří",
                "given_name": "Jiří",
                "family_name": "Zahradník"
            },
            "affiliations": [
                [
                    1,
                    "Institute of Biotechnology, CAS, v.v.i., BIOCEV"
                ]
            ]
        }
        """
        person_or_org = orig_creator.pop("person_or_org")
        affiliations = orig_creator.pop("affiliations", [])
        name_type = person_or_org.pop("type")
        if name_type == "personal":
            creator = {"person": self.convert_person(person_or_org, affiliations)}
        elif name_type == "organizational":
            creator = {"organization": self.convert_organization(person_or_org)}
        else:
            raise Exception(f"Unknown name type: {name_type}")

        self.ensureEmpty(orig_creator)

        md.setdefault("qualified_relations", []).append(
            {
                "role": {
                    "iri": role_iri,
                },
                **creator,
            }
        )

    def convert_person(self, orig_creator, affiliations):

        converted_person = {
            "family_names": [orig_creator.pop("family_name")],
            "given_names": (
                [orig_creator.pop("given_name", None)]
                if orig_creator.get("given_name")
                else []
            ),
        }
        if converted_person["given_names"] and converted_person["family_names"]:
            converted_person["name"] = (
                f"{converted_person['family_names'][0]}, {converted_person['given_names'][0]}"
            )
        elif converted_person["given_names"]:
            converted_person["name"] = converted_person["given_names"][0]
        else:
            converted_person["name"] = converted_person["family_names"][0]

        converted_person["identifiers"] = [
            self.convert_identifier(i) for i in orig_creator.pop("identifiers", [])
        ]
        converted_person["identifiers"] = [
            x for x in converted_person["identifiers"] if x
        ]
        converted_person["affiliations"] = self.convert_affiliations(affiliations)
        return converted_person

    def convert_organization(self, orig_creator):
        converted_organization = {
            "name": orig_creator.pop("name"),
        }
        converted_organization["identifiers"] = [
            self.convert_identifier(i) for i in orig_creator.pop("identifiers", [])
        ]
        converted_organization["identifiers"] = [
            x for x in converted_organization["identifiers"] if x
        ]
        return converted_organization

    def convert_identifier(self, orig_identifier):
        """
        Example: {'identifier': 'https://gitlab.com/JaraSit/dynamic-newmark', 'scheme': 'url'}
        """
        identifier = orig_identifier.pop("identifier")
        scheme = orig_identifier.pop("scheme")

        if scheme == "doi":
            iri = f"https://doi.org/{identifier}"
            identifier = {
                "identifier_scheme": {"iri": "https://doi.org/"},
                "value": identifier,
                "iri": iri,
            }
        elif scheme == "url":
            iri = identifier
            identifier = {
                "identifier_scheme": {"iri": "urn:iri"},
                "value": identifier,
                "iri": iri,
            }
        elif scheme == "arxiv":
            iri = f"https://arxiv.org/abs/{identifier}"
            identifier = {
                "identifier_scheme": {"iri": "https://arxiv.org/"},
                "value": identifier,
                "iri": iri,
            }
        elif scheme == "ror":
            iri = f"https://ror.org/{identifier}"
            identifier = {
                "identifier_scheme": {"iri": "https://ror.org/"},
                "value": identifier,
                "iri": iri,
            }
        elif scheme == "orcid":
            iri = f"https://orcid.org/{identifier}"
            identifier = {
                "identifier_scheme": {"iri": "https://orcid.org/"},
                "value": identifier,
                "iri": iri,
            }
        else:
            log.error(
                f"Unknown related item scheme: {scheme} for identifier: {identifier}"
            )
            return None
        self.ensureEmpty(orig_identifier)
        return identifier

    def convert_affiliations(self, affiliations):
        affiliations = []
        for aff in affiliations:
            affiliation = {
                "name": {"lang": "und", "value": aff.pop("name")},
                "identifiers": [],
            }
            affiliations.append(affiliation)

            self.ensureEmpty(
                aff,
            )
        return affiliations

    def convert_description(self, orig_description):
        if not orig_description:
            return []
        if isinstance(orig_description, str):
            return [
                {
                    "lang": "und",
                    "value": bleach.clean(
                        orig_description, tags=allowed_tags, strip=True
                    ),
                }
            ]
        raise NotImplementedError(
            f"Description type {type(orig_description)} not supported"
        )

    def convert_additional_description(self, orig_description):
        """
        Format:
        {'description': 'The corresponding dataset...', 'type': {'id': 'notes', 'title': {'de': 'Anmerkungen', 'en': 'Notes'}}}
        """
        description = orig_description.pop("description")
        _type = orig_description.pop("type", None)
        _lang = lang_dict_to_2(orig_description.pop("lang", None) or "und")
        self.ensureEmpty(orig_description)
        return {"lang": _lang, "value": description}

    def convert_additional_title(self, orig_title):
        """
        Format:
        {'title': 'Supplementary...',
          'type': {'id': 'subtitle',
          'title': {'de': 'Untertitel', 'en': 'Subtitle'}},
          'lang': {'id': 'eng', 'title': {'en': 'English'}}}
        """
        title = orig_title.pop("title")
        _lang = lang_dict_to_2(orig_title.pop("lang", "und"))
        zenodo_title_types = {
            "alternative-title": "https://vocabs.ccmm.cz/registry/codelist/AlternateTitle/AlternativeTitle",
            "subtitle": "https://vocabs.ccmm.cz/registry/codelist/AlternateTitle/Subtitle",
            "translated-title": "https://vocabs.ccmm.cz/registry/codelist/AlternateTitle/TranslatedTitle",
            "other": "https://vocabs.ccmm.cz/registry/codelist/AlternateTitle/Other",
        }
        _type = zenodo_title_types[orig_title.pop("type", {})["id"]]
        self.ensureEmpty(orig_title)
        return {
            "title": [
                {
                    "lang": _lang,
                    "value": title,
                }
            ],
            "type": {"iri": _type},
        }

    def convert_dates(self, orig_md):
        dates = []
        dateAvailable = orig_md.pop("publication_date", None)
        if dateAvailable:
            if "/" in dateAvailable:
                # the date is edtf-interval, which is currently not supported
                # we'll take the last part of the date
                dateAvailable = dateAvailable.split("/")[-1]
            dates.append(
                {
                    "date": dateAvailable,
                    "date_type": {
                        "iri": "https://vocabs.ccmm.cz/registry/codelist/TimeReference/Issued"
                    },
                }
            )
        return dates

    def convert_resource_type(self, rt):
        if not rt:
            return {
                # generic dataset
                "iri": "http://purl.org/coar/resource_type/c_ddb1"
            }
        # return just id that should match, not an iri
        return {
            "iri": "http://purl.org/coar/resource_type/" + rdm_to_coar_mapping[rt["id"]]
        }

    def convert_rights(self, orig_rights):
        converted_rights = {
            "description": [],
        }

        for r in orig_rights:
            if "props" in r and r["props"].get("url"):
                if converted_rights.get("iri") is None:
                    converted_rights["iri"] = r["props"]["url"]
                else:
                    log.warning(
                        f"Multiple rights with URL found: "
                        f"{converted_rights.get('iri')}, ignoring {r['props']['url']}."
                    )

            converted_rights["description"] += [
                {
                    "lang": lang,
                    "value": text.strip(),
                }
                for lang, text in r["description"].items()
                if text and text.strip()
            ]

        return converted_rights

    def convert_access_rights(self, orig_access, has_files):
        record_access = orig_access.get("record")
        files_access = orig_access.get("files")

        if record_access == "public" and files_access == "public":
            if has_files:
                # open access
                return {"iri": "http://purl.org/coar/access_right/c_abf2"}
            else:
                # metadata only
                return {"iri": "http://purl.org/coar/access_right/c_14cb"}
        else:
            if orig_access.get("embargo", {}).get("active"):
                return {
                    # embargoed
                    "iri": "http://purl.org/coar/access_right/c_f1cf",
                }
            else:
                return {
                    # restricted
                    "iri": "http://purl.org/coar/access_right/c_16ec"
                }

    def convert_subjects(self, orig_subjects):
        created_subjects = []
        for subject in orig_subjects:
            subj = subject.pop("subject")
            """
            Sample data:
            {'title': {...}, 
             'id': 'euroscivoc:933', 
             'scheme': 'EuroSciVoc', 
             'props': {
                'parents': 'euroscivoc:23,euroscivoc:47,euroscivoc:297'
              }, 
              'identifiers': [
                  {'identifier': 'http://data.europa.eu/...', 'scheme': 'url'}
            ]}
            """
            classification_code = subject.pop("id", None)
            scheme = subject.pop("scheme", None)
            _props = subject.pop("props", None)
            _identifiers = subject.pop("identifiers", None)
            created_subject = {"title": [{"value": subj, "lang": "und"}]}
            if classification_code and scheme:
                created_subject["classification_code"] = classification_code
                created_subject["scheme"] = {"id": scheme}
            # TODO: what about subject identifiers?
            created_subjects.append(created_subject)
            self.ensureEmpty(subject)
        return created_subjects

    def convert_related_items(self, orig_related_items):
        converted_related_items = []

        for orig_related_item in orig_related_items:
            relation_type = orig_related_item.pop("relation_type")
            title = orig_related_item.pop("title", {})
            resource_type_dict = orig_related_item.pop("resource_type", None)
            if resource_type_dict:
                resource_type = self.convert_resource_type(resource_type_dict)
            else:
                resource_type = None

            identifier = self.convert_identifier(orig_related_item)
            if not identifier:
                return None

            converted_relation_type = {
                "id": relation_types_cache.by_prop("zenodo")[relation_type["id"]]["id"]
            }

            converted_item = {
                "iri": identifier["iri"],
                "relation_type": converted_relation_type,
                "type": resource_type,
                "title": title.get("en") or next(iter(title.values()), None),
                "identifiers": [identifier],
            }
            converted_related_items.append(
                {k: v for k, v in converted_item.items() if v is not None}
            )
            self.ensureEmpty(orig_related_item)  # not present in datacite schema
        return converted_related_items

    def convert_related_item_identifiers(self, orig_identifiers):
        converted = []
        for orig_identifier in orig_identifiers:
            identifier = orig_identifier.pop("identifier")
            scheme = orig_identifier.pop("scheme")
            if scheme == "doi":
                converted.append(
                    {
                        "identifier_scheme": {"iri": "https://doi.org/"},
                        "value": identifier,
                        "iri": "https://doi.org/" + identifier,
                    }
                )
            else:
                raise Exception(
                    f"Unknown identifier scheme: {scheme} for identifier: {identifier}"
                )
        if len(converted) > 1:
            raise Exception(
                f"More than one identifier found for related item: {orig_identifiers}"
            )
        if len(converted) == 0:
            return None
        return converted[0]

    def convert_location(self, orig_location):
        place = orig_location.pop("place", None)
        if place:
            ret = {"names": [place]}
        else:
            ret = None
        self.ensureEmpty(orig_location)
        return ret

    @cached_property
    def file_formats_by_extension(self):
        """Cache the file formats by extension."""
        return file_formats_by_extension()

    @cached_property
    def file_formats_by_iana(self):
        """Cache the file formats by IANA type."""
        return file_formats_by_iana()

    def convert_funding(self, orig_funding):
        ret = {}

        funder = orig_funding.pop("funder", None)
        award = orig_funding.pop("award", None)
        self.ensureEmpty(orig_funding)

        if award:
            _award_id = award.pop("id", None)
            award_number = award.pop("number", None)
            award_title = award.pop("title", None)
            _award_identifiers = award.pop("identifiers", [])
            _award_acronym = award.pop("acronym", None)
            award_program = award.pop("program", None)
            ret = {
                "funding_program": award_program,
                "award_title": (
                    award_title.get("en") or next(iter(award_title.values()), None)
                    if award_title
                    else None
                ),
                "local_identifier": award_number,
            }
            self.ensureEmpty(award)

        if funder:
            funder_id = funder.pop("id")
            _funder_name = funder.pop("name")
            self.ensureEmpty(funder)
            ret["funders"] = [
                {
                    "organization": {
                        # TODO: what to do with funder id?
                        "name": _funder_name,
                    }
                }
            ]
        return {k: v for k, v in ret.items() if v}

    def convert_file(self, f, record_url):
        """Convert file to CCMM format.

        f looks like this: {
        {
            "id": "4484d3af-2c2d-47b8-8836-973c8a671f6a",
            "checksum": "md5:84d6bba940df0daa7888411deb3b71e8",
            "ext": "pdf",
            "size": 363181,
            "mimetype": "application/pdf",
            "storage_class": "L",
            "key": "Laboratórna Diagnostika XXIX_2_2024_159-166.pdf.pdf",
            "metadata": {},
            "access": {
            "hidden": false
            },
            "links": {
            "self": "https://zenodo.org/api/records/14646925/files/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
            "content": "https://zenodo.org/api/records/14646925/files/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/content",
            "iiif_canvas": "https://zenodo.org/api/iiif/record:14646925/canvas/Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
            "iiif_base": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf",
            "iiif_info": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/info.json",
            "iiif_api": "https://zenodo.org/api/iiif/record:14646925:Laborat%C3%B3rna%20Diagnostika%20XXIX_2_2024_159-166.pdf.pdf/full/full/0/default.png"
            }
        }
        """

        ret = {
            "byte_size": f.get("size"),
            "access_urls": [record_url],
            "title": f.get("key"),
        }
        checksum = f.get("checksum")
        if checksum:
            # invenio always uses md5 for checksums, so we can assume that
            ret["checksum"] = {
                "value": checksum.split(":")[-1] if ":" in checksum else checksum,
                "algorithm": {"id": "md5"},
            }
        return {k: v for k, v in ret.items() if v}


rdm_to_coar_mapping = {
    # Publication types
    "publication-article": "http://purl.org/coar/resource_type/c_6501",  # journal article
    "publication-book": "http://purl.org/coar/resource_type/c_2f33",  # book
    "publication-section": "http://purl.org/coar/resource_type/c_3248",  # book part
    "publication-conferencepaper": "http://purl.org/coar/resource_type/c_5794",  # conference paper
    "publication-datamanagementplan": "http://purl.org/coar/resource_type/c_ab79",  # data management plan
    "publication-deliverable": "http://purl.org/coar/resource_type/c_18op",  # project deliverable
    "publication-annotation": "http://purl.org/coar/resource_type/c_1162",  # annotation
    "publication-abstract": "http://purl.org/coar/resource_type/c_8544",  # abstract
    "publication-bachelorthesis": "http://purl.org/coar/resource_type/c_7a1f",  # bachelor thesis
    "publication-mastersthesis": "http://purl.org/coar/resource_type/c_bdcc",  # master thesis
    "publication-doctorthesis": "http://purl.org/coar/resource_type/c_46ec",  # doctoral thesis
    "publication-lecture": "http://purl.org/coar/resource_type/c_8544",  # lecture
    "publication-preprint": "http://purl.org/coar/resource_type/c_816b",  # preprint
    "publication-report": "http://purl.org/coar/resource_type/c_93fc",  # report
    "publication-softwaredocumentation": "http://purl.org/coar/resource_type/c_71bd",  # software documentation
    "publication-technicalnote": "http://purl.org/coar/resource_type/c_18gh",  # technical documentation
    "publication-workingpaper": "http://purl.org/coar/resource_type/c_8042",  # working paper
    "publication-other": "http://purl.org/coar/resource_type/c_1843",  # other
    # Poster types
    "poster": "http://purl.org/coar/resource_type/c_6670",  # poster
    # Presentation types
    "presentation": "http://purl.org/coar/resource_type/c_c94f",  # presentation
    # Dataset types
    "dataset": "http://purl.org/coar/resource_type/c_ddb1",  # dataset
    # Image types
    "image-figure": "http://purl.org/coar/resource_type/c_ecc8",  # figure
    "image-plot": "http://purl.org/coar/resource_type/c_ecc8",  # figure (using same as figure)
    "image-drawing": "http://purl.org/coar/resource_type/c_2cd9",  # drawing
    "image-diagram": "http://purl.org/coar/resource_type/c_5ce6",  # diagram
    "image-photo": "http://purl.org/coar/resource_type/c_e73b",  # photograph
    "image-other": "http://purl.org/coar/resource_type/c_c51a",  # still image
    # Video/Audio types
    "video": "http://purl.org/coar/resource_type/c_12ce",  # video
    "audio": "http://purl.org/coar/resource_type/c_18cc",  # sound
    # Software types
    "software": "http://purl.org/coar/resource_type/c_5ce6",  # software
    # Lesson types
    "lesson": "http://purl.org/coar/resource_type/c_9a1e",  # lesson
    # Physical object types
    "physicalobject": "http://purl.org/coar/resource_type/c_1843",  # other (closest match)
    # Other types
    "other": "http://purl.org/coar/resource_type/c_1843",  # other
    "annotationcollection": "http://purl.org/coar/resource_type/c_1162",  # annotation (using same as annotation)
    "peerreview": "http://purl.org/coar/resource_type/c_efa0",  # peer review
    "publication-peerreview": "http://purl.org/coar/resource_type/c_efa0",  # peer review
    "publication": "http://purl.org/coar/resource_type/c_18cf",  # generic text
    "publication-annotationcollection": "http://purl.org/coar/resource_type/c_18cf",
    "publication-conferenceproceeding": "http://purl.org/coar/resource_type/c_f744",
    "publication-journal": "http://purl.org/coar/resource_type/c_0640",
    "publication-patent": "http://purl.org/coar/resource_type/c_15cd",
    "publication-milestone": "http://purl.org/coar/resource_type/c_18cf",
    "publication-proposal": "http://purl.org/coar/resource_type/c_baaf",
    "publication-taxonomictreatment": "http://purl.org/coar/resource_type/c_18cf",
    "publication-thesis": "http://purl.org/coar/resource_type/c_46ec",
    "publication-datapaper": "http://purl.org/coar/resource_type/c_18cf",
    "publication-dissertation": "http://purl.org/coar/resource_type/c_46ec",
    "publication-standard": "http://purl.org/coar/resource_type/c_18cf",
    "event": "http://purl.org/coar/resource_type/c_1843",
    "image": "http://purl.org/coar/resource_type/c_c513",
    "model": "http://purl.org/coar/resource_type/c_1843",
    "software-computationalnotebook": "http://purl.org/coar/resource_type/c_5ce6",
    "workflow": "http://purl.org/coar/resource_type/c_393c",
}

if __name__ == "__main__":
    from oarepo_runtime.cli import oarepo

    from common.oai.loaders.zenodo import ZenodoLoader

    @oarepo.command("sample-harvest-to-file")
    def harvest():
        with open("zenodo_harvested.yaml", "w") as f:
            reader = ZenodoLoader(
                source="https://zenodo.org/api/records/",
                all_records=True,
                identifiers=None,
                oai_config={
                    "setspecs": 'creators.affiliation:("České vysoké učení technické v Praze" OR "ČVUT" OR "CESKE VYSOKE UCENI TECHNICKE V PRAZE" OR "CVUT" OR "Czech Technical University In Prague" OR "CTU in Prague" OR "CTU Prague")  AND resource_type.type:dataset',
                },
                oai_run=None,
                oai_harvester_id=None,
                manual=False,
            )
            transformer = ZenodoTransformer(identity=system_identity)
            first = True
            for entry in tqdm.tqdm(reader):
                if entry.deleted:
                    continue
                batch = StreamBatch(entries=[entry], context={})
                transformer.apply(batch)
                if entry.errors:
                    print(
                        "Transformation failed with errors for entry",
                        entry.context["oai"]["identifier"],
                        file=sys.stderr,
                    )
                    print(entry.errors, file=sys.stderr)
                    continue
                if not entry.entry:
                    print(
                        "Transformation failed for entry - empty entry returned",
                        entry.context["oai"]["identifier"],
                        file=sys.stderr,
                    )
                    continue
                if first:
                    first = False
                else:
                    f.write("---\n")
                yaml.safe_dump(entry.entry, f, allow_unicode=True)
                f.flush()

    # run invenio with this command
    # to test the transformer
    from invenio_app.cli import cli

    cli.main(["oarepo", "sample-harvest-to-file"])
