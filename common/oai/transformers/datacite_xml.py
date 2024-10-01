# etree
from collections import OrderedDict
from typing import Union
import xmltodict
from lxml import etree
from oarepo_runtime.datastreams import BaseTransformer, StreamBatch, StreamEntry
from oarepo_runtime.datastreams.types import StreamEntryError


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
            metadata = xmltodict.parse(entry.entry)
            if metadata.get('record',{}).get('metadata',{}).get('resource') is None:
                entry.entry = {'metadata' : {}}
                raise Exception("No metadata found")

            return metadata['record']['metadata']['resource']
        except Exception as e:
            entry.errors.append(StreamEntryError.from_exception(e))

    def transform_alt_identifiers(self, alt_identifiers, datacite_alt_identifiers):
        if isinstance(datacite_alt_identifiers, list):
            for alt_id in datacite_alt_identifiers:
                alt_identifiers.append({
                    'alternateIdentifier': alt_id.pop('#text'),
                    'alternateIdentifierType': alt_id.pop('@alternateIdentifierType'),
                })
                self.ensureEmpty(alt_id)
        else:
            alt_identifiers.append({
                'alternateIdentifier': datacite_alt_identifiers.pop('#text'),
                'alternateIdentifierType': datacite_alt_identifiers.pop('@alternateIdentifierType'),
            })
            self.ensureEmpty(datacite_alt_identifiers)

    def transform_container(self):
        pass  # no container

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
        affiliations = self.transform_affiliations(contributor.pop('affiliation', []))
        nameIdentifier = self.transform_nameIdentifier(contributor.pop('nameIdentifier',{}))
        curr_contributor['contributorType'] = self.transform_contributor_type(contributor.pop('@contributorType',""))
        person = self.transform_person(contributor)
        curr_contributor.update(person)

        if len(affiliations) > 0:
            curr_contributor['affiliation'] = affiliations
        if len(nameIdentifier) > 0:
            curr_contributor['nameIdentifiers'] = nameIdentifier
        return curr_contributor

    def transform_contributors(self, contributors, datacite_contributors):
        if isinstance(datacite_contributors, list):
            for contributor in datacite_contributors:
                contributors.append(self.transform_contributor(contributor))
                self.ensureEmpty(contributor)
        else:
            contributors.append(self.transform_contributor(datacite_contributors))
            self.ensureEmpty(datacite_contributors)

    def transform_creator(self, creator):
        curr_creator = {}
        affiliations = self.transform_affiliations(creator.pop('affiliation', []))
        nameIdentifier = self.transform_nameIdentifier(creator.pop('nameIdentifier',{}))
        person = self.transform_person(creator)

        self.ensureEmpty(creator)

        curr_creator.update(person)
        if len(affiliations) > 0:
            curr_creator['affiliation'] = affiliations
        if len(nameIdentifier) > 0:
            curr_creator['nameIdentifiers'] = nameIdentifier

        return curr_creator

    def transform_creators(self, creators, datacite_creators):
        if isinstance(datacite_creators, list):
            for creator in datacite_creators:
                creators.append(self.transform_creator(creator))
                self.ensureEmpty(creator)
        else:
            creators.append(self.transform_creator(datacite_creators))
            self.ensureEmpty(datacite_creators)

    def transform_person(self, datacite_person):
        person = {}
        if isinstance(datacite_person.get('creatorName'), str):
            person['name'] = datacite_person.pop('creatorName')
        if isinstance(datacite_person.get('creatorName',[]), OrderedDict) and datacite_person.get("creatorName",{}).get('@nameType') == "Personal":
            person['nameType'] = "Personal"
            person['name'] = datacite_person.get("creatorName").pop('#text')
            datacite_person.pop("creatorName")
        else:
            person['nameType'] = "Organizational"
            person['name'] = datacite_person.get("creatorName").pop('#text')
            datacite_person.pop('creatorName', "")

        if datacite_person.get('contributorName') is not None:
            person['name'] = datacite_person.pop('contributorName')
        if datacite_person.get('givenName') is not None:
            person['givenName'] = datacite_person.pop('givenName')
        if datacite_person.get('familyName') is not None:
            person['familyName'] = datacite_person.pop('familyName')

        self.ensureEmpty(datacite_person)
        return person


    def transform_nameIdentifier(self, nameIdentifier):
        if not nameIdentifier:
            return []
        identifier = {
            'nameIdentifier' : nameIdentifier.pop('#text',"")
        }
        if nameIdentifier.get("@nameIdentifierScheme"):
            identifier['nameIdentifierScheme'] = nameIdentifier.pop('@nameIdentifierScheme')
        if nameIdentifier.get("@schemeURI") is not None:
            identifier['schemeURI'] = nameIdentifier.pop('@schemeURI')
        self.ensureEmpty(nameIdentifier)
        return [identifier]

    def transform_affiliations(self, datacite_affiliations):
        if isinstance(datacite_affiliations,str):
            return [{
                'name' : datacite_affiliations
            }]
        elif isinstance(datacite_affiliations,OrderedDict):
            aff = {
                'name' : datacite_affiliations.pop('#text',"")
            }
            if datacite_affiliations.get('@affiliationIdentifier') is not None:
                aff['affiliationIdentifier'] = datacite_affiliations.pop('@affiliationIdentifier')
            if datacite_affiliations.get('@schemeURI') is not None:
                aff['schemeURI'] = datacite_affiliations.pop('@schemeURI')
            if datacite_affiliations.get('@affiliationIdentifierScheme') is not None:
                aff['affiliationIdentifierScheme'] = datacite_affiliations.pop('@affiliationIdentifierScheme')


        else:
            return []


    def transform_dates(self, dates, datacite_dates):
        if isinstance(datacite_dates, list):
            for date in datacite_dates:
                curr_date = self.transform_date(date)
                if len(curr_date) > 0:
                    dates.append(curr_date)
                    self.ensureEmpty(date)
        else:
            date = self.transform_date(datacite_dates)
            if len(date) > 0:
                dates.append(date)
                self.ensureEmpty(datacite_dates)

    def transform_date(self, date):
        if date.get('#text',"").isnumeric():
            return {
                    'date': date.pop('#text'),
                    'dateType': date.pop('@dateType',"Other"),
                    'dateInformation' : date.pop('@dateInformation',""),
                }
        else:
            return {}

    def transform_descriptions(self, descriptions, datacite_descriptions):
        if isinstance(datacite_descriptions, list):
            for description in datacite_descriptions:
                descriptions.append(self.transform_description(description))
                self.ensureEmpty(description)
        else:
            descriptions.append(self.transform_description(datacite_descriptions))
            self.ensureEmpty(datacite_descriptions)

    def transform_description(self, description):
        return {
                'description': description.pop('#text',""),
                'descriptionType' : description.pop('@descriptionType',"Other"),
                'lang' : description.pop("@xml:lang","")
                }

    def transform_doi(self, datacite_doi):
        if datacite_doi.get("@identifierType") == 'DOI':
            return datacite_doi.get('#text')

    def transform_format(self, _formats, datacite_formats):
        if isinstance(datacite_formats, list):
            _formats.extend(datacite_formats)
        else:
            _formats.append(datacite_formats)

    def transform_fundings(self, fundings, datacite_fundings):
        if isinstance(datacite_fundings, list):
            for funding in datacite_fundings:
                fundings.append(self.transform_funding(funding))
                self.ensureEmpty(funding)
        else:
            fundings.append(self.transform_funding(datacite_fundings))
            self.ensureEmpty(datacite_fundings)

    def transform_funding(self, funding):
        curr_funding = {
            'funderName' : funding.pop('funderName',""),
            'funderIdentifierType' : funding.get('funderIdentifier',{}).pop("@funderIdentifierType","Other"),
            'funderIdentifier' : funding.pop('funderIdentifier',{}).get("#text",""),
            'awardTitle' : funding.pop('awardTitle',""),
        }
        if isinstance(funding.get("awardNumber"), OrderedDict):
            curr_funding['awardNumber'] = funding.get("awardNumber").pop("#text","")
            curr_funding['awardURI'] = funding.get("awardNumber").pop("@awardURI","")
        elif isinstance(funding.get("awardNumber"), str):
            curr_funding['awardNumber'] = funding.pop("awardNumber","")

        return curr_funding

    def transform_geo_location(self, datacite_geo_locations):
        curr_location = {}
        if datacite_geo_locations.get('geoLocationPlace') is not None:
            curr_location['geoLocationPlace'] = datacite_geo_locations.pop('geoLocationPlace')

        if isinstance(datacite_geo_locations.get("geoLocationPoint",[]), str):
            point = datacite_geo_locations.pop('geoLocationPoint').split()
            curr_location['geoLocationPoint'] = {
                'pointLatitude': point[0],
                'pointLongitude': point[1]
            }
        elif isinstance(datacite_geo_locations.get("geoLocationPoint",[]), OrderedDict):
            curr_location['geoLocationPoint'] = {
                'pointLatitude': datacite_geo_locations.get('geoLocationPoint').pop('pointLatitude'),
                'pointLongitude': datacite_geo_locations.get('geoLocationPoint').pop('pointLongitude')
            }
            datacite_geo_locations.pop('geoLocationPoint')


        if isinstance(datacite_geo_locations.get("geoLocationBox",[]), OrderedDict):
            geoLocationBox = {
                'eastBoundLongitude': datacite_geo_locations.get('geoLocationBox').pop("eastBoundLongitude",""),
                'northBoundLatitude': datacite_geo_locations.get('geoLocationBox').pop("northBoundLatitude",""),
                'southBoundLatitude': datacite_geo_locations.get('geoLocationBox').pop("southBoundLatitude",""),
                'westBoundLongitude': datacite_geo_locations.get('geoLocationBox').pop("westBoundLongitude",""),
            }
            curr_location['geoLocationBox'] = geoLocationBox
            datacite_geo_locations.pop('geoLocationBox')
        elif isinstance(datacite_geo_locations.get("geoLocationBox",[]), str):
            coords = datacite_geo_locations.get("geoLocationBox","")
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

        self.ensureEmpty(datacite_geo_locations)
        return curr_location

    def transform_geo_locations(self, locations, datacite_geo_locations):
        if isinstance(datacite_geo_locations, list):
            for location in datacite_geo_locations:
                locations.append(self.transform_geo_location(location))
        else:
            locations.append(self.transform_geo_location(datacite_geo_locations))

    def transform_publisher(self, publisher, datacite_publisher):
        if isinstance(datacite_publisher,str):
            publisher.update({
                'name' : datacite_publisher
            })
        elif isinstance(datacite_publisher,OrderedDict):
            publisher.update({
                'name' : datacite_publisher.pop('#text',""),
                'lang' : datacite_publisher.pop('@xml:lang',""),
                'publisherIdentifier' : datacite_publisher.pop('@publisherIdentifier',""),
                'publisherIdentifierScheme' : datacite_publisher.pop('@publisherIdentifierScheme',""),
                'schemeURI' : datacite_publisher.pop('@schemeURI',""),
            })

    def transform_related_identifier(self, datacite_related_identifiers):
        return {
            'relatedIdentifier': datacite_related_identifiers.pop("#text",""),
            'relatedIdentifierType': datacite_related_identifiers.pop("@relatedIdentifierType"),
            'relatedMetadataScheme': datacite_related_identifiers.pop("@relatedMetadataScheme",""),
            'relationType' : datacite_related_identifiers.pop("@relationType",""),
            'resourceTypeGeneral' : datacite_related_identifiers.pop("@resourceTypeGeneral","Other"),
            'schemeType' : datacite_related_identifiers.pop("@schemeType",""),
            'schemeURI' : datacite_related_identifiers.pop("@schemeURI",""),
        }

    def transform_related_identifiers(self, related_identifiers, datacite_related_identifiers):
        if isinstance(datacite_related_identifiers, list):
            for rel_id in datacite_related_identifiers:
                related_identifiers.append(self.transform_related_identifier(rel_id))
                self.ensureEmpty(rel_id)
        else:
            related_identifiers.append(self.transform_related_identifier(datacite_related_identifiers))
            self.ensureEmpty(datacite_related_identifiers)

    def transform_related_items(self, related_items, datacite_related_items):
        if isinstance(datacite_related_items, list):
            for rel_item in datacite_related_items:
                related_items.append(self.transform_related_item(rel_item))
                self.ensureEmpty(rel_item)
        else:
            related_items.append(self.transform_related_item(datacite_related_items))
            self.ensureEmpty(datacite_related_items)

    def transform_related_item(self, related_item):
        rel_item = {}
        if related_item.get('contributors'):
            contributors = []
            self.transform_contributors(contributors, related_item.get('contributors',{}).pop('contributor',[]))
            related_item.pop('contributors',[])
            rel_item['contributors'] = contributors
        if related_item.get('creators'):
            creators = []
            self.transform_creators(creators, related_item.get('creators',{}).pop('creator',[]))
            related_item.pop('creators',[])
            rel_item['creators'] = creators
        if related_item.get('edition') is not None:
            rel_item['edition'] = related_item.pop('edition')
        if related_item.get('firstPage') is not None:
            rel_item['firstPage'] = related_item.pop('firstPage')
        if related_item.get('lastPage') is not None:
            rel_item['lastPage'] = related_item.pop('lastPage')
        if related_item.get('issue') is not None:
            rel_item['issue'] = related_item.pop('issue')
        if related_item.get('number') is not None:
            rel_item['number'] = related_item.get('number').pop("#text")
            rel_item['numberType'] = related_item.get('number').pop('@numberType',"Other")
            related_item.pop('number')
        if related_item.get('publicationYear') is not None:
            rel_item['publicationYear'] = related_item.pop('publicationYear')
        if related_item.get('publisher') is not None:
            self.transform_publisher(rel_item.setdefault('publisher',{}),related_item.pop('publisher',{}))
        rel_item['relatedItemIdentifier'] = {
            'relatedItemIdentifier' : related_item.get('relatedItemIdentifier').pop('#text',""),
            'relatedItemIdentifierType' :  related_item.get('relatedItemIdentifier').pop('@relatedIdentifierType',""),
        }
        related_item.pop('relatedItemIdentifier', None)

        rel_item['relatedItemType'] = related_item.pop("@relatedItemType","Other")
        rel_item['relatedMetadataScheme'] = related_item.pop("@relatedMetadataScheme", "")
        rel_item['relationType'] = related_item.pop("@relationType","")
        rel_item['resourceTypeGeneral'] = related_item.pop("@resourceTypeGeneral","Other")
        rel_item['schemeType'] = related_item.pop("@schemeType","")
        rel_item['schemeURI'] = related_item.pop("@schemeURI","")

        if related_item.get('titles'):
            titles = []
            self.transform_titles(titles, related_item.get('titles', {}).pop('title',[]))
            rel_item['titles'] = titles
            related_item.pop('titles',[])
        if related_item.get("volume") is not None:
            rel_item['volume'] = related_item.pop("volume","")

        return rel_item


    def transform_right(self, right):
        if isinstance(right, str):
            return {'rights' : right}

        curr_right = {
            'rights': right.pop('#text',""),
        }
        if right.get("@rightsURI") is not None:
            curr_right['rightsURI'] = right.pop("@rightsURI")
        if right.get("@xml:lang") is not None:
            curr_right['lang'] = right.pop("@xml:lang")
        if right.get('@schemeURI') is not None:
            curr_right['schemeURI'] = right.pop('@schemeURI')
        if right.get('@rightsIdentifierScheme') is not None:
            curr_right['rightsIdentifierScheme'] = right.pop('@rightsIdentifierScheme')
        if right.get("@rightsIdentifier") is not None:
            curr_right['rightsIdentifier'] = right.pop("@rightsIdentifier")
        self.ensureEmpty(right)
        return curr_right

    def transform_rights(self, rights, datacite_rights):
        if isinstance(datacite_rights, list):
            for right in datacite_rights:
                rights.append(self.transform_right(right))
        else:
            rights.append(self.transform_right(datacite_rights))

    def transform_schema_version(self):
        pass

    def transform_sizes(self, sizes, datacite_sizes):
        sizes.extend(datacite_sizes)

    def transform_subject(self, datacite_subject):
        if isinstance(datacite_subject, str):
            return {'subject': datacite_subject}

        subject = {"subject" : datacite_subject.pop('#text',"")}
        if datacite_subject.get("@subjectScheme") is not None:
            subject['subjectScheme'] = datacite_subject.pop('@subjectScheme')
        if datacite_subject.get("@schemeURI") is not None:
            subject['schemeURI'] = datacite_subject.pop('@schemeURI')
        if datacite_subject.get("@valueURI") is not None:
            subject['valueURI'] = datacite_subject.pop('@valueURI')
        if datacite_subject.get("@classificationCode") is not None:
            subject['classificationCode'] = datacite_subject.pop('@classificationCode')
        if datacite_subject.get("@xml:lang") is not None:
            subject['lang'] = datacite_subject.pop('@xml:lang')
        self.ensureEmpty(datacite_subject)
        return subject

    def transform_subjects(self, subjects, datacite_subjects):
        if isinstance(datacite_subjects, list):
            for subject in datacite_subjects:
                subjects.append(self.transform_subject(subject))
        else:
            subjects.append(self.transform_subject(datacite_subjects))

    def transform_title(self, datacite_titles):
       if isinstance(datacite_titles,OrderedDict):
           curr_title = {
               "title" : datacite_titles.pop('#text',""),
               "titleType" : "Other"
           }
           if datacite_titles.get('titleType') is not None:
               curr_title['titleType'] = datacite_titles.pop('titleType')
           if datacite_titles.get('xml:lang') is not None:
               curr_title['lang'] = datacite_titles.pop('xml:lang')
           self.ensureEmpty(datacite_titles)
           return curr_title
       elif isinstance(datacite_titles, str):
           curr_title = {
               "title": datacite_titles,
                "titleType": "Other"
           }
           return curr_title
       return {}

    def transform_titles(self, titles, datacite_titles):
        if isinstance(datacite_titles, list):
            for title in datacite_titles:
                titles.append(self.transform_title(title))
        else:
            titles.append(self.transform_title(datacite_titles))

    def transform_types(self, types, datacite_type):
        if datacite_type:
            curr_type = {
                'resourceTypeGeneral' : datacite_type.pop('@resourceTypeGeneral'),
            }
            if datacite_type.get('#text') is not None:
                curr_type['resourceType'] = datacite_type.pop('#text')

            self.ensureEmpty(datacite_type)
            types.append(curr_type)

    def transform_url(self, url, zenodo_url):
        pass  # no url

    def transform_entry(self, entry:StreamEntry):
        source_metadata = self.parse_xml(entry)
        source_metadata = OrderedDict((key, value) for key, value in source_metadata.items() if value is not None)

        transformed_metadata = {}

        self.transform_alt_identifiers(transformed_metadata.setdefault('alternateIdentifiers',[]),
                                       source_metadata.get('alternateIdentifiers',{}).pop("alternateIdentifier",[]))
        source_metadata.pop('alternateIdentifiers',{})

        self.transform_contributors(transformed_metadata.setdefault('contributors',[]),
                                    source_metadata.get('contributors',{}).pop('contributor',[]))
        source_metadata.pop('contributors', {})

        self.transform_creators(transformed_metadata.setdefault('creators',[]),
                                source_metadata.get('creators',{}).pop('creator',[]))
        source_metadata.pop('creators', {})

        self.transform_dates(transformed_metadata.setdefault('dates',[]),
                             source_metadata.get('dates',{}).pop("date",[]))
        source_metadata.pop('dates', {})

        self.transform_descriptions(transformed_metadata.setdefault('descriptions',[]),
                                    source_metadata.get('descriptions',{}).pop('description',[]))
        source_metadata.pop('descriptions', {})

        transformed_metadata['doi'] = self.transform_doi(source_metadata.pop('identifier',{}),)

        self.transform_format(transformed_metadata.setdefault('formats',[]),
                              source_metadata.get('formats',{}).pop('format',[]))
        source_metadata.pop('formats', {})

        self.transform_geo_locations(transformed_metadata.setdefault('geoLocations',[]),
                                    source_metadata.get('geoLocations',{}).pop('geoLocation',[]))
        source_metadata.pop('geoLocations', {})

        if source_metadata.get('language'):
            transformed_metadata['language'] = source_metadata.pop('language')

        if source_metadata.get('publicationYear'):
            transformed_metadata['publicationYear'] = source_metadata.pop('publicationYear')

        self.transform_publisher(transformed_metadata.setdefault('publisher',{}),
                                 source_metadata.pop('publisher',{}))

        self.transform_related_identifiers(transformed_metadata.setdefault('relatedIdentifiers',[]),
                                           source_metadata.get('relatedIdentifiers',{}).pop('relatedIdentifier',[]))
        source_metadata.pop('relatedIdentifiers', {})

        if isinstance(source_metadata.get('rights'),str):
            transformed_metadata['rights'] = {'rights' : source_metadata.pop('rights', "")}
        else:
            self.transform_rights(transformed_metadata.setdefault('rightsList',[]),
                              source_metadata.get('rightsList',{}).pop('rights',[]))
            source_metadata.pop('rightsList', {})

        self.transform_sizes(transformed_metadata.setdefault('sizes',[]),
                             source_metadata.get('sizes',{}).pop('size',[]))
        source_metadata.pop('sizes', {})

        self.transform_subjects(transformed_metadata.setdefault('subjects',[]),
                                source_metadata.get('subjects',{}).pop('subject',[]))
        source_metadata.pop('subjects', {})

        self.transform_titles(transformed_metadata.setdefault('titles',[]),
                              source_metadata.get('titles',{}).pop('title',[]))
        source_metadata.pop('titles', {})

        self.transform_types(transformed_metadata.setdefault('types',[]),
                             source_metadata.pop('resourceType',{}))

        if source_metadata.get('version') is not None:
            transformed_metadata['version'] = source_metadata.pop('version')

        entry.entry = {'metadata': transformed_metadata}

