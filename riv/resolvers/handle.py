from idutils.normalizers import normalize_handle
from idutils.validators import is_handle
from lxml import html
from ..resolvers import MetadataResolver


class HandleResolver(MetadataResolver):
    name = "Handle"

    identifier_code = "handle"
    identifier_resolve_fn = staticmethod(is_handle)
    identifier_normalize_fn = staticmethod(normalize_handle)
    url = "https://hdl.handle.net"

    def _get_data_from_response(self, response, problems):
        tree = html.fromstring(response.content)
        return tree.xpath("/html/head")[0]

    def _get_titles(self, data, problems):
        return data.xpath('//meta[@name="citation_title"]/@content') or \
               data.xpath('//meta[@name="title"]/@content')

    def _get_creators(self, data, problems):
        creators = data.xpath('//meta[@name="citation_author"]/@content')
        if not creators:
            return creators
        creator_list = []

        for creator in creators:
            creator_obj = {}

            creator_type = "personal" if "," in creator else "organizational" # best guess from looking at LINDAT data
            creator_obj['name'] = creator
            creator_obj['type'] = creator_type

            if creator_type == 'personal':
                splt = [part.strip() for part in creator.split(',', 1)]
                creator_obj['given_name'] = splt[1]
                creator_obj['family_name'] = splt[0]

            creator_list.append({"person_or_org": creator_obj})

        return creator_list

    def _get_resource_type(self, data, problems):
        return {"id": "other"}

    def _get_publication_dates(self, data, problems):
        return data.xpath('//meta[@name="citation_publication_date"]/@content') or \
               data.xpath('//meta[@name="publication_date"]/@content')



