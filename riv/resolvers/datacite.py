from ..resolvers import MetadataResolver
from .base import ResolverProblem, ResolverProblemLevel
from invenio_i18n import lazy_gettext as _
from idutils.validators import is_doi
from idutils.normalizers import normalize_doi
from requests.models import Response


class DataciteResolver(MetadataResolver):
    name = "Datacite"

    identifier_code = "doi"
    identifier_resolve_fn = staticmethod(is_doi)
    identifier_normalize_fn = staticmethod(normalize_doi)
    url = "https://api.datacite.org/dois"

    def _get_data_from_response(self, response: Response, problems):
        data = response.json()
        return data["data"]["attributes"]

    def _get_titles(self, data, problems):
        titles = data.get("titles", [])
        main_titles = []
        if titles:
            for title in titles:
                if 'title' in title and 'titleType' not in title:  # if titleType, it is additional title
                    main_titles.append(title['title'])

        return main_titles

    def _get_creators(self, data, problems):
        creators = data.get("creators", [])

        def split_personal_name(name):
            if ',' in name:
                family, given = [part.strip() for part in name.split(',', 1)]
            else:
                family, given = name.strip(), ""
            return family, given

        if not creators:
            return creators

        creator_list = []

        for creator in creators:
            creator_obj = {}

            creator_type = creator.get('nameType', 'personal').lower()
            creator_obj['type'] = creator_type

            given = creator.get('givenName')
            family = creator.get('familyName')
            name = creator.get('name')

            if name is None:
                name = 'Unknown Creator'  # should never happen
                problems.append(
                    ResolverProblem(resolver=self.name, message=_(f"Missing creators name: {creator}."),
                                    level=ResolverProblemLevel.WARNING))

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

    def _get_publication_dates(self, data, problems):
        return [data.get("publicationYear")]

    def _get_resource_type(self, data, problems):
        types = data.get("types", {})
        return types.get("resourceTypeGeneral", "dataset").lower()
