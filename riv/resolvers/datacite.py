from ..resolvers import MetadataResolver
import requests
import re

HOST_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org(?:\/.*)?$', re.IGNORECASE)
DOI_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org\/(.+)$', re.IGNORECASE)
DATACITE_URL="https://api.datacite.org/dois"

class DataciteResolver(MetadataResolver):
    def resolve(self, persistent_url: str) -> (dict | None, str):

        if not HOST_REGEX.match(persistent_url.strip()):
            return None, f"Incorrect URL for datacite identifier."

        match = DOI_REGEX.match(persistent_url.strip())
        if not match:
            return None, f"The URL is missing information about the DOI."

        doi = match.group(1)
        url = f"{DATACITE_URL}/{doi}"
        response = requests.get(
            url=url,
        )
        if response.status_code != 200:
            return None, f"Could not retrieve data, code {response.status_code}."

        metadata = {}

        data = response.json()
        datacite_metadata=data["data"]["attributes"]
        datacite_titles = datacite_metadata["titles"]
        title = self.resolve_titles(datacite_titles)
        metadata["title"] = title


        datacite_creators = datacite_metadata["creators"]
        creators = self.resolve_creators(datacite_creators)
        metadata["creators"] = creators

        return metadata, "OK"


    def resolve_titles(self, titles):
        for title in titles:
            if 'title' in title:
                return title['title']
        return ''

    def resolve_creators(self, creators):
        creator_list = []
        for creator in creators:
            creator_obj = {}
            type = creator.get('nameType', 'personal').lower()

            creator_obj['type'] = type

            given_from_data = creator.get('givenName', None)
            family_from_data = creator.get('familyName', None)
            if given_from_data:
                creator_obj['given_name'] = given_from_data
            if family_from_data:
                creator_obj['family_name'] = family_from_data
            if 'name' in creator: #always
                name = creator['name']
                creator_obj['name'] = name
                if type == 'personal':
                    if ',' in name:
                        parts = [p.strip() for p in name.split(',', 1)]
                        family = parts[0]
                        given = parts[1] if len(parts) > 1 else ""
                    else:
                        family = name.strip()
                        given = ""

                    if not family_from_data:
                        creator_obj['family_name'] = family

                    if not given_from_data and given != "":
                        creator_obj['given_name'] = given

            creator_list.append({"person_or_org": creator_obj})
        return creator_list
