import re

from ..resolvers import MetadataResolver
"""Crossref resolver to retrieve RDM-like metadata based on PID.

Article with announcement of changes to REST API rate limits
https://doi.org/10.64000/wadve-3tj60

public pool rate limit: 5 requests per second

example: https://api.crossref.org/works/doi/10.64000/wadve-3tj60

polite pool rate limit: 10 requests per second
available by adding query parameter mailto to API URL

example: https://api.crossref.org/works/doi/10.64000/wadve-3tj60&mailto=info@eosc.cz
"""


HOST_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org(?:\/.*)?$', re.IGNORECASE)
DOI_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org\/(.+)$', re.IGNORECASE)
CROSSREF_URL="https://api.crossref.org/works/doi"

class CrossrefResolver(MetadataResolver):
    """Crossref resolver."""

    name = "Crossref"

    def resolve(self, persistent_url: str) -> (dict | None, str):
        """
        Resolves metadata associated with a given identifier using the Crossref API.

        This method retrieves data related to a specified identifier by making a request to
        the Crossref API. Depending on the response status code, it processes the result
        accordingly. Data regarding the title of the work and author details such as names
        and ORCID identifiers (if available) are extracted and returned in a structured format.
        The function also handles scenarios like rate-limiting, blocked requests, and errors.

        Parameters:
            identifier (str): The identifier of the resource to retrieve metadata for.

        Returns:
            tuple[dict | None, str]: A tuple where the first element is a dictionary containing
            retrieved metadata (if successful) or None (on failure), and the second element
            is a string message reflecting the status or any error message.

        Raises:
            None
        """
        # public pool
        if not HOST_REGEX.match(persistent_url.strip()):
            return None, "Incorrect URL for crossref identifier."

        match = DOI_REGEX.match(persistent_url.strip())
        if not match:
            return None, "The URL is missing information about the DOI."

        doi = match.group(1)
        url = f"{CROSSREF_URL}/{doi}"
        response = self.session.get(
            url=url,
        )
        # polite pool
        # resp_with_mailto = self.session.get(f"https://api.crossref.org/works/{identifier}&mailto={POLITE_POOL_MAILTO}}")

        # not found
        if response.status_code == 404:
            return None, "Could not retrieve data, code 404."

        # other errors
        if response.status_code != 200:
            return None, f"Crossref API returned {response.status_code}"

        metadata = {}

        # successful request
        data = response.json()
        crossref_metadata = data.get("message", {})
        metadata["title"] = self.resolve_title(crossref_metadata.get("title", []))
        metadata["creators"] = self.resolve_authors(crossref_metadata.get("author", []))

        return metadata, "OK"

    def resolve_title(self, titles):
        for title in titles:
            return title
        return ''

    def resolve_authors(self, authors):
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