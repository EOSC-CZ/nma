import re

from ..resolvers import MetadataResolver
from invenio_vocabularies.proxies import current_service as vocabulary_service
from invenio_access.permissions import system_identity

HOST_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org(?:\/.*)?$', re.IGNORECASE)
DOI_REGEX = re.compile(r'^(?:https?:\/\/)?doi\.org\/(.+)$', re.IGNORECASE)
DATACITE_URL="https://api.datacite.org/dois"


class DataciteResolver(MetadataResolver):
    name = "Datacite"
    def resolve(self, persistent_url: str) -> (dict | None, str):

        if not HOST_REGEX.match(persistent_url.strip()):
            return None, "Incorrect URL for datacite identifier."

        match = DOI_REGEX.match(persistent_url.strip())
        if not match:
            return None, "The URL is missing information about the DOI."

        doi = match.group(1)
        url = f"{DATACITE_URL}/{doi}"
        response = self.session.get(
            url=url,
        )
        if response.status_code != 200:
            return None, f"Could not retrieve data, code {response.status_code}."

        metadata = {}

        data = response.json()
        datacite_metadata=data["data"]["attributes"]

        #titles
        #datacite required, rdm required
        datacite_titles = datacite_metadata["titles"]
        title = self.resolve_titles(datacite_titles)
        metadata["title"] = title

        #creators
        #datacite required, rdm required
        datacite_creators = datacite_metadata["creators"]
        creators = self.resolve_creators(datacite_creators)
        metadata["creators"] = creators

        #publication date
        #datacite required, rdm required
        publication_date = datacite_metadata.get("publicationYear")
        if publication_date:
            metadata["publication_date"] = str(publication_date)

        #resource type
        #datacite required, rdm required
        if "types" in datacite_metadata:
             metadata["resource_type"] = {"id": self.resolve_resource_type(datacite_metadata["types"])}

        return metadata, "OK"


    def resolve_titles(self, titles):
        for title in titles:
            if 'title' in title:
                return title['title']
        return ''

    def resolve_creators(self, creators):
        def split_personal_name(name):
            if ',' in name:
                family, given = [part.strip() for part in name.split(',', 1)]
            else:
                family, given = name.strip(), ""
            return family, given

        creator_list = []

        for creator in creators:
            creator_obj = {}

            creator_type = creator.get('nameType', 'personal').lower()
            creator_obj['type'] = creator_type

            given = creator.get('givenName')
            family = creator.get('familyName')

            name = creator.get('name')
            creator_obj['name'] = name

            if creator_type == 'personal':
                parsed_family, parsed_given = split_personal_name(name)

                family = family or parsed_family
                given = given or (parsed_given if parsed_given else None)

            if given:
                creator_obj['given_name'] = given
            if family:
                creator_obj['family_name'] = family

            creator_list.append({"person_or_org": creator_obj})

        return creator_list

    def resolve_resource_type(self, resource_type):
        type = resource_type.get("resourceTypeGeneral", "dataset").lower() #dataset as default option
        try:
            vocabulary_service.read(
                system_identity, ("resourcetypes", type)
            )
            return type
        except:
            return "dataset" #there was a type but it could not be resolved
