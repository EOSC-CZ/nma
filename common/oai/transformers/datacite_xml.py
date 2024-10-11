from types import SimpleNamespace
from typing import Union
from oarepo_runtime.datastreams import BaseTransformer, StreamBatch, StreamEntry
from oarepo_runtime.datastreams.types import StreamEntryError
import re
from xml.etree import cElementTree as ElementTree

EMPTY = SimpleNamespace(text='', inner_html='',list=[])

class XmlNode:
    def __init__(self, node):
        self.node = node

    def __str__(self):
        return ElementTree.tostring(self.node, encoding="unicode")

    def remove_namespace(self, tag):
        return tag.split('}', 1)[-1]

    def get_all(self, item_name) -> list:
        ret = []
        for child in self.node:
            tag = self.remove_namespace(child.tag)
            if tag == item_name:
                ret.append(XmlNode(child))

        return ret

    def child_names(self):
        return [self.remove_namespace(child.tag) for child in self.node]


    def keys(self):
        return set(self.child_names())

    @property
    def text(self):
        return self.node.text

    def get_attribute(self,attrib_name):
        #return self.get_all(parent_name)[pos].node.attrib.get(attrib_name)
        if self.node.attrib.get(attrib_name):
            return self.node.attrib.get(attrib_name)
        return ""

    def get(self, item_name,default=None):
        l = self.get_all(item_name)
        if len(l) == 1:
            return l[0]
        elif len(l) > 1:
            raise ValueError('Multiple children found')
        if default is not None:
            return SimpleNamespace(text='',inner_html='', list=[])
        return default

    def pop(self, item_name, default=None):
        item = self.get(item_name,default)
        children = list(self.node)
        for child in children:
            if self.remove_namespace(child.tag) == item_name:
                self.node.remove(child)

        return item

    @property
    def inner_html(self):
        html = [self.node.text]
        for child in self.node:
            html.append(str(XmlNode(child)))
            html.append(child.tail)

        html = [x for x in html if x]
        return "".join(html)

    def remove_namespaces(self, node=None):
        if node is None:
            node = self.node

        node.tag = self.remove_namespace(node.tag)
        for child in node:
            self.remove_namespaces(child)

        for attr in list(node.attrib):
            if '{' in attr:
                node.attrib[self.remove_namespace(attr)] = node.attrib.pop(attr)



class DataciteXMLTransformer(BaseTransformer):
    def __init__(self, **kwargs) -> None:
        super().__init__()

    def apply(self, batch: StreamBatch, *args, **kwargs) -> Union[StreamBatch, None]:
        """Applies the transformation to the entry.
        :returns: A StreamEntry. The transformed entry.
                  Raises TransformerError in case of errors.
        """
        for entry in batch.entries:
            try:
                self.transform_entry(entry)
            except Exception as e:
                entry.entry = {'metadata' : entry.entry}
                entry.errors.append(StreamEntryError.from_exception(e))
        return batch

    def ensureEmpty(self, data, *exceptions, filter=True):
        for key in data.keys():
            if key not in exceptions:
                if filter:\
                    filtered_data = {k: v for k, v in data.items() if k not in exceptions}
                else:
                    filtered_data = data
                print(filtered_data)
                raise Exception(f"Unhandled key: {key} inside data")

    def parse_xml(self, entry:StreamEntry):
        try:
            root = ElementTree.XML(entry.entry)
            xmldict = XmlNode(root)
            xmldict.remove_namespaces()

            if xmldict.get('metadata') is None or xmldict.get('metadata').get('resource') is None:
                entry.entry = {'metadata': {}}
                raise Exception("No metadata found")

            return xmldict.get('metadata').get('resource')
        except Exception as e:
            entry.errors.append(StreamEntryError.from_exception(e))

    def transform_alt_identifiers(self, alt_identifiers, datacite_alt_identifiers):
        if not datacite_alt_identifiers:
            return
        datacite_alt_identifiers = datacite_alt_identifiers.get_all('alternateIdentifier')
        for pos, alt_id in enumerate(datacite_alt_identifiers):
            alt_identifiers.append({
                'alternateIdentifier': alt_id.text,
                'alternateIdentifierType': alt_id.get_attribute('alternateIdentifierType'),
            })
            alt_id.pop('alternateIdentifier')
            #self.ensureEmpty(alt_id)


    def transform_contributor_type(self, contributor_type):
        types = {
            "ContactPerson",
            "DataCollector",
            "DataCurator",
            "DataManager",
            "Distributor",
            "Editor",
            "HostingInstitution",
            "Producer",
            "ProjectLeader",
            "ProjectManager",
            "ProjectMember",
            "RegistrationAgency",
            "RegistrationAuthority",
            "RelatedPerson",
            "Researcher",
            "ResearchGroup",
            "RightsHolder",
            "Sponsor",
            "Supervisor",
            "WorkPackageLeader",
            "Other",
        }
        if contributor_type in types:
            return contributor_type
        return "Other"

    def transform_contributor(self, contributor):
        curr_contributor = {}
        affiliations = self.transform_affiliations(contributor.get_all('affiliation'))
        nameIdentifier = self.transform_nameIdentifier(contributor.get_all('nameIdentifier'))
        curr_contributor['contributorType'] = self.transform_contributor_type(contributor.get_attribute('contributorType'))
        person = self.transform_person(contributor,"contributor")
        curr_contributor.update(person)
        #self.ensureEmpty(contributor)

        if affiliations:
            curr_contributor['affiliation'] = affiliations
        if nameIdentifier:
            curr_contributor['nameIdentifiers'] = nameIdentifier
        return curr_contributor

    def transform_contributors(self, contributors, datacite_contributors):
        if not datacite_contributors:
            return
        datacite_contributors = datacite_contributors.get_all('contributor')
        for contributor in datacite_contributors:
            contributors.append(self.transform_contributor(contributor))
            #self.ensureEmpty(contributor)


    def transform_creator(self, creator):
        curr_creator = {}
        affiliations = self.transform_affiliations(creator.get_all('affiliation'))
        nameIdentifier = self.transform_nameIdentifier(creator.get_all('nameIdentifier'))
        person = self.transform_person(creator,"creator")

        #self.ensureEmpty(creator)

        curr_creator.update(person)
        if affiliations:
            curr_creator['affiliation'] = affiliations
        if nameIdentifier:
            curr_creator['nameIdentifiers'] = nameIdentifier

        return {k: v for k, v in curr_creator.items() if v not in ('', None)}

    def transform_creators(self, creators, datacite_creators):
        if not datacite_creators:
            return
        datacite_creators = datacite_creators.get_all('creator')
        for creator in datacite_creators:
            creators.append(self.transform_creator(creator))
           # self.ensureEmpty(creator)

    def transform_person(self, datacite_person, creator_or_contributor):
        person = {}

        person['name'] = datacite_person.get(f'{creator_or_contributor}Name').text
        if datacite_person.get(f'{creator_or_contributor}Name').get_attribute("nameType") == "Personal":
            person['nameType'] = "Personal"
        else:
            person['nameType'] = "Organizational"

        if datacite_person.get_attribute('lang'):
            person['lang'] = datacite_person.get_attribute("lang")
        if datacite_person.get('givenName') is not None and datacite_person.get('givenName').text:
            person['givenName'] = datacite_person.pop('givenName').text
        if datacite_person.get('familyName') is not None and datacite_person.get('familyName').text:
            person['familyName'] = datacite_person.pop('familyName').text

       # self.ensureEmpty(datacite_person)
        return {k: v for k, v in person.items() if v not in ('', None)}


    def transform_nameIdentifier(self, nameIdentifier):
        if not nameIdentifier:
            return []
        identifiers = []
        for identifier in nameIdentifier:
            current_identifier = {'nameIdentifier': identifier.text,
                      'nameIdentifierScheme': identifier.get_attribute('nameIdentifierScheme'),
                      'schemeURI': identifier.get_attribute('schemeURI')}
            identifiers.append({k: v for k, v in current_identifier.items() if v not in ('', None)})
        #self.ensureEmpty(nameIdentifier)
        return identifiers

    def transform_affiliations(self, datacite_affiliations):
        affs = []
        for affiliation in datacite_affiliations:
            aff = {
                'name' : affiliation.text,
                'affiliationIdentifier' : affiliation.get_attribute('affiliationIdentifier'),
                'schemeURI' : affiliation.get_attribute('schemeURI'),
                'affiliationIdentifierScheme' : affiliation.get_attribute('affiliationIdentifierScheme'),
            }
            affs.append({k: v for k, v in aff.items() if v not in ('', None)})
        return affs

    def transform_dates(self, dates, datacite_dates, publication_year):
        if not datacite_dates:
            dates.append({
                "date": publication_year.text,
                'dateType': "Issued"
            })
            return
        datacite_dates = datacite_dates.get_all('date')
        for date in datacite_dates:
            curr_date = self.transform_date(date)
            if len(curr_date) > 0:
                dates.append(curr_date)
                    #self.ensureEmpty(date)

        if not any(date['dateType'] == 'Issued' for date in dates) and publication_year:
            dates.append({
                "date" : publication_year.text,
                'dateType' : "Issued"
            })


    def transform_date(self, date):
        current_date = {
                'date': date.text,
                'dateType': date.get_attribute('dateType'),
                'dateInformation' : date.get_attribute('dateInformation'),
            }
        return {k: v for k, v in current_date.items() if v not in ('', None)}

    def transform_descriptions(self, descriptions, datacite_descriptions):
        if not datacite_descriptions:
            return
        datacite_descriptions = datacite_descriptions.get_all('description')
        for description in datacite_descriptions:
            if description.inner_html:
                descriptions.append(self.transform_description(description))
            #self.#Empty(description)
        descriptions = [description for description in descriptions if description.get("description","")]
        if len(descriptions) == 1 and descriptions[0].get('descriptionType') == "Other":
            descriptions[0]['descriptionType'] = 'Abstract'


    def transform_description(self, description):
        current_desc = {
            'description': description.inner_html,
            'descriptionType' : description.get_attribute('descriptionType'),
            'lang' : description.get_attribute("lang")
        }
        return {k: v for k, v in current_desc.items() if v not in ('', None)}

    def transform_doi(self, datacite_doi):
        if datacite_doi.get_attribute("identifierType") == 'DOI':
            return datacite_doi.text

    def transform_format(self, _formats, datacite_formats):
        if not datacite_formats:
            return
        datacite_formats = datacite_formats.get_all('format')
        for _format in datacite_formats:
            _formats.append(_format.text)

    def transform_fundings(self, fundings, datacite_fundings):
        if not datacite_fundings:
            return
        datacite_fundings = datacite_fundings.get_all('fundingReference')
        for funding in datacite_fundings:
            fundings.append(self.transform_funding(funding))
            #self.ensureEmpty(funding)


    def transform_funding(self, funding):
        curr_funding = {
            'funderName': funding.get('funderName').text,
            'funderIdentifierType': funding.get('funderIdentifier').get_attribute(
                "funderIdentifierType") if funding.get('funderIdentifier') else "",
            'funderIdentifier': funding.get('funderIdentifier', "").text,
            'awardTitle': funding.get('awardTitle', "").text,
            'awardNumber': funding.get('awardNumber', "").text,
            'awardURI': funding.get("awardNumber").get_attribute('awardURI') if funding.get('awardNumber') else "",
        }
        return {k: v for k, v in curr_funding.items() if v not in ('', None)}

    def transform_geo_location(self, datacite_geo_locations):
        curr_location = {}
        if datacite_geo_locations.get('geoLocationPlace'):
            curr_location['geoLocationPlace'] = datacite_geo_locations.get("geoLocationPlace").text

        #                      float      whitespace  float else it is dictionary according to new schema
        if re.match(r'^\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$',datacite_geo_locations.get("geoLocationPoint",'').inner_html):
            point = datacite_geo_locations.pop('geoLocationPoint').inner_html.split()
            curr_location['geoLocationPoint'] = {
                'pointLatitude': point[0],
                'pointLongitude': point[1]
            }
        elif datacite_geo_locations.get("geoLocationPoint"):
            curr_location['geoLocationPoint'] = {
                'pointLatitude': datacite_geo_locations.get('geoLocationPoint').get('pointLatitude').text,
                'pointLongitude': datacite_geo_locations.get('geoLocationPoint').get('pointLongitude').text
            }
            datacite_geo_locations.pop('geoLocationPoint')
        #                   float1 float2 float3 float4 else it is dictionary according to new schema
        if re.match(r'^\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$',
                    datacite_geo_locations.get('geoLocationBox','').inner_html):
            coords = datacite_geo_locations.get("geoLocationBox").inner_html
            if coords:
                coords = coords.split()
                geoLocationBox = {
                    'eastBoundLongitude': coords[0],
                    'northBoundLatitude': coords[1],
                    'southBoundLatitude': coords[2],
                    'westBoundLongitude': coords[3],
                }
                curr_location['geoLocationBox'] = geoLocationBox
                datacite_geo_locations.pop('geoLocationBox')
        elif datacite_geo_locations.get('geoLocationBox'):
            geoLocationBox = {
                'eastBoundLongitude': datacite_geo_locations.get('geoLocationBox').get("eastBoundLongitude").text,
                'northBoundLatitude': datacite_geo_locations.get('geoLocationBox').get("northBoundLatitude").text,
                'southBoundLatitude': datacite_geo_locations.get('geoLocationBox').get("southBoundLatitude").text,
                'westBoundLongitude': datacite_geo_locations.get('geoLocationBox').get("westBoundLongitude").text,
            }
            curr_location['geoLocationBox'] = geoLocationBox


       # self.ensureEmpty(datacite_geo_locations)
        return {k: v for k, v in curr_location.items() if v not in ('', None)}

    def transform_geo_locations(self, locations, datacite_geo_locations):
        if not datacite_geo_locations:
            return
        datacite_geo_locations = datacite_geo_locations.get_all('geoLocation')
        for location in datacite_geo_locations:
            locations.append(self.transform_geo_location(location))


    def transform_publisher(self, publisher, datacite_publisher):
        current_publisher = {
            'name': datacite_publisher.text,
            'lang' : datacite_publisher.get_attribute('lang'),
            'publisherIdentifier': datacite_publisher.get_attribute('publisherIdentifier'),
            'publisherIdentifierScheme': datacite_publisher.get_attribute('publisherIdentifierScheme'),
            'schemeURI': datacite_publisher.get_attribute('schemeURI'),
        }
        current_publisher = {k: v for k, v in current_publisher.items() if v not in ('', None)}
        publisher.update(current_publisher)
       # self.ensureEmpty(datacite_publisher)

    def transform_resource_type_general(self, resource_type):
        types = {"Audiovisual",
                    "Book",
                    "BookChapter",
                    "Collection",
                    "ComputationalNotebook",
                    "ConferencePaper",
                    "ConferenceProceeding",
                    "DataPaper",
                    "Dataset",
                    "Dissertation",
                    "Event",
                    "Image",
                    "Instrument",
                    "InteractiveResource",
                    "Journal",
                    "JournalArticle",
                    "Model",
                    "OutputManagementPlan",
                    "PeerReview",
                    "PhysicalObject",
                    "Preprint",
                    "Report",
                    "Service",
                    "Software",
                    "Sound",
                    "Standard",
                    "StudyRegistration",
                    "Text",
                    "Workflow",
                    }
        if resource_type not in types:
            return "Other"
        else:
            return resource_type

    def transform_related_identifier(self, datacite_related_identifiers):
        related_id = {
            'relatedIdentifier': datacite_related_identifiers.text,
            'relatedIdentifierType': datacite_related_identifiers.get_attribute("relatedIdentifierType"),
            'relatedMetadataScheme': datacite_related_identifiers.get_attribute("relatedMetadataScheme"),
            'relationType' : datacite_related_identifiers.get_attribute("relationType"),
            'resourceTypeGeneral' : self.transform_resource_type_general(datacite_related_identifiers.get_attribute("resourceTypeGeneral")),
            'schemeType' : datacite_related_identifiers.get_attribute("schemeType"),
            'schemeURI' : datacite_related_identifiers.get_attribute("schemeURI"),
        }
        return {k: v for k, v in related_id.items() if v not in ('', None)}

    def transform_related_identifiers(self, related_identifiers, datacite_related_identifiers):
        if not datacite_related_identifiers:
            return
        datacite_related_identifiers = datacite_related_identifiers.get_all("relatedIdentifier")
        for rel_id in datacite_related_identifiers:
            related_identifiers.append(self.transform_related_identifier(rel_id))
           # self.ensureEmpty(rel_id)

    def transform_related_items(self, related_items, datacite_related_items):
        if not datacite_related_items:
            return
        datacite_related_items = datacite_related_items.get_all("relatedItem")
        for rel_item in datacite_related_items:
            related_items.append(self.transform_related_item(rel_item))
            #self.ensureEmpty(rel_item)

    def transform_related_item(self, related_item):
        rel_item = {}
        if related_item.get('contributors'):
            contributors = []
            self.transform_contributors(contributors, related_item.get('contributors'))
            related_item.pop('contributors',[])
            rel_item['contributors'] = contributors
        if related_item.get('creators'):
            creators = []
            self.transform_creators(creators, related_item.get('creators'))
            related_item.pop('creators',[])
            rel_item['creators'] = creators
        if related_item.get('edition') is not None:
            rel_item['edition'] = related_item.pop('edition').text
        if related_item.get('firstPage') is not None:
            rel_item['firstPage'] = related_item.pop('firstPage').text
        if related_item.get('lastPage') is not None:
            rel_item['lastPage'] = related_item.pop('lastPage').text
        if related_item.get('issue') is not None:
            rel_item['issue'] = related_item.pop('issue').text
        if related_item.get('number') is not None:
            rel_item['number'] = related_item.get('number').text
            rel_item['numberType'] = related_item.get('number').get_attribute('numberType')
            related_item.pop('number')
        if related_item.get('publicationYear') is not None:
            rel_item['publicationYear'] = related_item.pop('publicationYear').text
        if related_item.get('publisher') is not None:
            self.transform_publisher(rel_item.setdefault('publisher',{}),related_item.get('publisher'))
        rel_item['relatedItemIdentifier'] = {
            'relatedItemIdentifier' : related_item.get("relatedItemIdentifier").text,
            'relatedItemIdentifierType' :  related_item.get("relatedItemIdentifier").get_attribute("relatedItemIdentifierType") if related_item.get("relatedItemIdentifier") else "",
        }
        related_item.pop('relatedItemIdentifier', None)

        rel_item['relatedItemType'] = related_item.get_attribute("relatedItemType")
        rel_item['relatedMetadataScheme'] = related_item.get_attribute("relatedMetadataScheme")
        rel_item['relationType'] = related_item.get_attribute("relationType")
        rel_item['resourceTypeGeneral'] = self.transform_resource_type_general(related_item.get_attribute("resourceTypeGeneral"))
        rel_item['schemeType'] = related_item.get_attribute("schemeType")
        rel_item['schemeURI'] = related_item.get_attribute("schemeURI")

        if related_item.get_all('titles'):
            titles = []
            self.transform_titles(titles, related_item.get('titles'))
            rel_item['titles'] = titles
            related_item.pop('titles',[])
        if related_item.get("volume") is not None:
            rel_item['volume'] = related_item.pop("volume").text

        return {k: v for k, v in rel_item.items() if v not in ('', None)}


    def transform_right(self, right):
        curr_right = {
            'rights': right.text,
        }
        if right.get_attribute("rightsURI") is not None:
            curr_right['rightsURI'] = right.get_attribute("rightsURI")
        if right.get_attribute("lang") is not None:
            curr_right['lang'] = right.get_attribute("lang")
        if right.get_attribute('schemeURI') is not None:
            curr_right['schemeURI'] = right.get_attribute('schemeURI')
        if right.get_attribute('rightsIdentifierScheme') is not None:
            curr_right['rightsIdentifierScheme'] = right.get_attribute('rightsIdentifierScheme')
        if right.get_attribute("rightsIdentifier") is not None:
            curr_right['rightsIdentifier'] = right.get_attribute("rightsIdentifier")
       # self.ensureEmpty(right)
        return {k: v for k, v in curr_right.items() if v not in ('', None)}

    def transform_rights(self, rights, datacite_rights):
        if not datacite_rights:
            return
        datacite_rights = datacite_rights.get_all("rights")
        for right in datacite_rights:
            rights.append(self.transform_right(right))

    def transform_schema_version(self):
        pass

    def transform_sizes(self, sizes, datacite_sizes):
        if not datacite_sizes:
            return
        datacite_sizes = datacite_sizes.get_all("size")
        for size in datacite_sizes:
            sizes.append(size.text)

    def transform_subject(self, datacite_subject):

        subject = {"subject" : datacite_subject.text}
        if datacite_subject.get_attribute("subjectScheme") is not None:
            subject['subjectScheme'] = datacite_subject.get_attribute('subjectScheme')
        if datacite_subject.get_attribute("schemeURI") is not None:
            subject['schemeURI'] = datacite_subject.get_attribute('schemeURI')
        if datacite_subject.get_attribute("valueURI") is not None:
            subject['valueURI'] = datacite_subject.get_attribute('valueURI')
        if datacite_subject.get_attribute("classificationCode") is not None:
            subject['classificationCode'] = datacite_subject.get_attribute('classificationCode')
        if datacite_subject.get_attribute("lang") is not None:
            subject['lang'] = datacite_subject.get_attribute('lang')
      #  self.ensureEmpty(datacite_subject)
        return {k: v for k, v in subject.items() if v not in ('', None)}

    def transform_subjects(self, subjects, datacite_subjects):
        if not datacite_subjects:
            return
        datacite_subjects = datacite_subjects.get_all("subject")
        for subject in datacite_subjects:
            subjects.append(self.transform_subject(subject))

    def transform_title(self, datacite_titles):

       curr_title = {
           "title" : datacite_titles.inner_html,
           "titleType" : "Other"
       }
       if datacite_titles.get_attribute('titleType'):
           curr_title['titleType'] = datacite_titles.get_attribute('titleType')
       if datacite_titles.get_attribute('lang'):
           curr_title['lang'] = datacite_titles.get_attribute('lang')
      # self.ensureEmpty(datacite_titles)

       return {k: v for k, v in curr_title.items() if v not in ('', None)}


    def transform_titles(self, titles, datacite_titles):
        if not datacite_titles:
            return
        datacite_titles = datacite_titles.get_all("title")
        for title in datacite_titles:
            titles.append(self.transform_title(title))

    def transform_resource_type(self, metadata, datacite_type):
        if datacite_type:
            curr_type = {
                'resourceTypeGeneral' :self.transform_resource_type_general(datacite_type.get_attribute('resourceTypeGeneral'))
            }
            if datacite_type.text:
                curr_type['resourceType'] = datacite_type.text

            metadata['resourceType'] = curr_type

    def transform_url(self, url, datacite_doi):
        pass  # no url

    def transform_entry(self, entry:StreamEntry):
        source_metadata = self.parse_xml(entry)
        transformed_metadata = {}

        self.transform_alt_identifiers(transformed_metadata.setdefault('alternateIdentifiers',[]),
                                       source_metadata.get('alternateIdentifiers'))
        source_metadata.pop('alternateIdentifiers',{})

        self.transform_contributors(transformed_metadata.setdefault('contributors',[]),
                                    source_metadata.get('contributors'))
        source_metadata.pop('contributors', {})

        self.transform_creators(transformed_metadata.setdefault('creators',[]),
                                source_metadata.get('creators'))
        source_metadata.pop('creators', {})

        self.transform_dates(transformed_metadata.setdefault('dates',[]),
                             source_metadata.get('dates'), source_metadata.get('publicationYear'))
        source_metadata.pop('dates', {})


        self.transform_descriptions(transformed_metadata.setdefault('descriptions',[]),
                                    source_metadata.get('descriptions',))
        source_metadata.pop('descriptions', {})

        transformed_metadata['doi'] = self.transform_doi(source_metadata.pop('identifier'),)


        self.transform_fundings(transformed_metadata.setdefault('fundingReferences',[]),
                                source_metadata.get('fundingReferences'))

        self.transform_format(transformed_metadata.setdefault('formats',[]),
                              source_metadata.get('formats',))
        source_metadata.pop('formats', {})

        self.transform_geo_locations(transformed_metadata.setdefault('geoLocations',[]),
                                    source_metadata.get('geoLocations'))
        source_metadata.pop('geoLocations', {})

        if source_metadata.get('language'):
            transformed_metadata['language'] = source_metadata.pop('language').text

        if source_metadata.get('publicationYear'):
            transformed_metadata['publicationYear'] = source_metadata.pop('publicationYear').text

        self.transform_publisher(transformed_metadata.setdefault('publisher',{}),
                                 source_metadata.pop('publisher'))

        self.transform_related_identifiers(transformed_metadata.setdefault('relatedIdentifiers',[]),
                                           source_metadata.get('relatedIdentifiers'))
        source_metadata.pop('relatedIdentifiers', {})

        self.transform_related_items(transformed_metadata.setdefault('relatedItems',[]),
                                     source_metadata.get('relatedItems'))

        self.transform_rights(transformed_metadata.setdefault('rightsList', []),
                              source_metadata.get('rightsList', ))
        source_metadata.pop('rightsList', {})

        self.transform_sizes(transformed_metadata.setdefault('sizes',[]),
                             source_metadata.get('sizes'))
        source_metadata.pop('sizes', {})

        self.transform_subjects(transformed_metadata.setdefault('subjects',[]),
                                source_metadata.get('subjects'))
        source_metadata.pop('subjects', {})

        self.transform_titles(transformed_metadata.setdefault('titles',[]),
                              source_metadata.get('titles',))
        source_metadata.pop('titles', {})

        self.transform_resource_type(transformed_metadata,
                                     source_metadata.pop('resourceType'))

        if transformed_metadata.get('doi') is not None:
            # https://oai.datacite.org/oai?verb=GetRecord&metadataPrefix=datacite&identifier=doi:
            transformed_metadata['url'] = f'https://oai.datacite.org/oai?verb=GetRecord&metadataPrefix=datacite&identifier=doi:{transformed_metadata["doi"]}'

        if source_metadata.get('version') is not None and source_metadata.get('version').text:
            transformed_metadata['version'] = source_metadata.pop('version').text
        source_metadata.pop('version', {})

        entry.entry = {'metadata': transformed_metadata}

