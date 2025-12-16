from bs4 import BeautifulSoup
from dcxml import simpledc
from idutils.normalizers import normalize_handle
from idutils.validators import is_handle
from invenio_rdm_records.resources.serializers import DublinCoreXMLSerializer
from invenio_rdm_records.resources.serializers.dublincore import DublinCoreSchema
from lxml import html
from ..resolvers import MetadataResolver


def parse_creatibutor(creatibutor):
    creatibutor_obj = {}

    creatibutor_type = "personal" if "," in creatibutor else "organizational"  # best guess from looking at LINDAT data
    creatibutor_obj['name'] = creatibutor
    creatibutor_obj['type'] = creatibutor_type

    if creatibutor_type == 'personal':
        splt = [part.strip() for part in creatibutor.split(',', 1)]
        creatibutor_obj['given_name'] = splt[1]
        creatibutor_obj['family_name'] = splt[0]

    return {"person_or_org": creatibutor_obj}

class HandleResolver(MetadataResolver):
    name = "Handle"

    identifier_code = "handle"
    identifier_resolve_fn = staticmethod(is_handle)
    identifier_normalize_fn = staticmethod(normalize_handle)
    url = "https://hdl.handle.net"

    def _get_data_from_response(self, response, problems):
        # TODO: debug
        # soup = BeautifulSoup(response.content, 'lxml')
        # el = soup.find_all('meta')

        tree = html.fromstring(response.content)
        return tree.xpath("/html/head")[0]

    def _get_titles(self, data, problems):
        return data.xpath('//meta[@name="citation_title"]/@content') or \
               data.xpath('//meta[@name="title"]/@content')

    def _get_creators(self, data, problems):
        creators = data.xpath('//meta[@name="citation_author"]/@content')
        if not creators:
            return creators
        else:
            return [parse_creatibutor(creator) for creator in creators]

    def _get_resource_type(self, data, problems):
        return {"id": "dataset"}

    def _get_publication_dates(self, data, problems):
        return data.xpath('//meta[@name="citation_publication_date"]/@content') or \
               data.xpath('//meta[@name="publication_date"]/@content') or \
               data.xpath('//meta[@name="citation_date"]/@content') # TODO: valid?

    # TODO: validation - try against RDM marshamallow/search mapping .. and use only what passes instead of throwing errors for use to correct as in required fields?
    # ie. RDM DublinCoreSchema - reverse version? (if i get this correctly - it is RDM -> DC and we need DC -> RDM)
    def _process_others(self, data, problems):
        # TODO: could there be some 3rd party method for parsing/validation?
        DC = data.xpath('//meta[starts-with(@name, "DC.")]')
        dc_metadata = parse_dublincore_meta(DC)
        if "contributors" in dc_metadata:
            dc_metadata["contributors"] = [parse_creatibutor(contributor) for contributor in dc_metadata["contributors"]]
        return {}

def parse_dublincore_meta(dc_elements):


    dc_data = {}

    for meta in dc_elements:
        name = meta.get('name', '')
        content = meta.get('content', '')

        if not name or not content:
            continue

        field = f"{name.replace('DC.', '', 1).lower()}s"

        if field in dc_data:
            if not isinstance(dc_data[field], list):
                dc_data[field] = [dc_data[field]]
            dc_data[field].append(content)
        else:
            dc_data[field] = content

    return dc_data



