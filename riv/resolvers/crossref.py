#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# nma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
import re

from flask import current_app
from idutils.normalizers import normalize_doi
from idutils.validators import is_doi
from invenio_access.permissions import system_identity
from invenio_i18n import lazy_gettext as _
from invenio_vocabularies.proxies import current_service as vocabulary_service
from marshmallow import ValidationError
from marshmallow_utils.fields import EDTFDateString

from .base import ResolverProblem, ResolverProblemLevel, CREATORS_PLACEHOLDER, PUBLICATION_DATE_PLACEHOLDER
from .utils import handle_errors
from ..resolvers import MetadataResolver

"""Crossref resolver to retrieve RDM-like metadata based on PID.

Article with announcement of changes to REST API rate limits
https://doi.org/10.64000/wadve-3tj60

public pool rate limit: 5 requests per second

example: https://api.crossref.org/works/doi/10.64000/wadve-3tj60

polite pool rate limit: 10 requests per second
available by adding query parameter mailto to API URL
But currently returns "Resource not found."

example: https://api.crossref.org/works/doi/10.64000/wadve-3tj60&mailto=info@eosc.cz
"""

class CrossrefResolver(MetadataResolver):
    """Crossref resolver."""

    name = "Crossref"

    identifier_code = "doi"
    identifier_resolve_fn = staticmethod(lambda x: re.match(r"https?://api.crossref.org/works/doi/.+$", x)) # TODO: correct version
    identifier_normalize_fn = staticmethod(lambda x: re.match(r"https?://api.crossref.org/works/doi/(.+)$", x).group(1) )
    url = "https://api.crossref.org/works/doi"

    def _get_data_from_response(self, response, problems):
        data = response.json()
        return data.get("message", {})

    def _get_titles(self, data, problems):
        return data.get("title", [])

    def _get_creators(self, data, problems):
        authors = data.get("author", [])
        creator_list = []
        for crossref_author in authors:
            creator_obj = {
                "name": crossref_author.get("family", ""),
                "family_name": crossref_author.get("family", ""),
                "type": "personal"
            }
            if crossref_author.get("given"):
                creator_obj["given_name"] = crossref_author.get("given", "")
                creator_obj["name"] += ", " + crossref_author.get("given", "")
            if crossref_author.get("ORCID"):
                orcid_id = crossref_author.get("ORCID", "").removeprefix("https://orcid.org/")
                creator_obj["identifiers"] = {
                    "identifier": orcid_id,
                    "scheme": "orcid"
                }
            creator_list.append({"person_or_org": creator_obj})
        return creator_list

    def _get_publication_dates(self, data, problems):
        return data.get("deposited", {}).get("date-time")

    def _get_resource_type(self, data, problems):
        types = data.get("types", {})
        return types.get("resourceTypeGeneral", "dataset").lower()







