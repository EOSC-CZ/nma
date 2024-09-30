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
                    'alternateIdentifier': alt_id['#text'],
                    'alternateIdentifierType': alt_id['@alternateIdentifierType'],
                })
        else:
            alt_identifiers.append({
                'alternateIdentifier': datacite_alt_identifiers['#text'],
                'alternateIdentifierType': datacite_alt_identifiers['@alternateIdentifierType'],
            })

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
        affiliations = self.transform_affiliations(contributor.get('affiliation', []))
        nameIdentifier = self.transform_nameIdentifier(contributor.get('nameIdentifier'))
        curr_contributor['contributorType'] = self.transform_contributor_type(contributor.get('@contributorType'))
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
        else:
            contributors.append(self.transform_contributor(datacite_contributors))

    def transform_creator(self, creator):
        curr_creator = {}
        affiliations = self.transform_affiliations(creator.get('affiliation', []))
        nameIdentifier = self.transform_nameIdentifier(creator.get('nameIdentifier'))
        person = self.transform_person(creator)

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
        else:
            creators.append(self.transform_creator(datacite_creators))

    def transform_person(self, datacite_person):
        person = {}
        if isinstance(datacite_person.get('creatorName'), str):
            person['name'] = datacite_person.get('creatorName')
        if isinstance(datacite_person.get('creatorName',[]), OrderedDict) and datacite_person.get("creatorName",{}).get('@nameType') == "Personal":
            person['nameType'] = "Personal"
            person['name'] = datacite_person.get("creatorName").get('#text')
        else:
            person['nameType'] = "Organizational"

        if datacite_person.get('contributorName'):
            person['name'] = datacite_person.get('contributorName')
        if datacite_person.get('givenName'):
            person['givenName'] = datacite_person.get('givenName')
        if datacite_person.get('familyName'):
            person['familyName'] = datacite_person.get('familyName')

        return person


    def transform_nameIdentifier(self, nameIdentifier):
        if not nameIdentifier:
            return []
        identifier = {
            'nameIdentifier' : nameIdentifier['#text']
        }
        if nameIdentifier.get("@nameIdentifierScheme"):
            identifier['nameIdentifierScheme'] = nameIdentifier['@nameIdentifierScheme']
        if nameIdentifier.get("@schemeURI"):
            identifier['schemeURI'] = nameIdentifier['@schemeURI']
        return [identifier]

    def transform_affiliations(self, datacite_affiliations):
        if datacite_affiliations:
            return [{
                'name' : datacite_affiliations
            }]
        else:
            return []


    def transform_dates(self, dates, datacite_dates):
        if isinstance(datacite_dates, list):
            for date in datacite_dates:
                curr_date = self.transform_date(date)
                if len(curr_date) > 0:
                    dates.append(self.transform_date(date))
        else:
            date = self.transform_date(datacite_dates)
            if len(date) > 0:
                dates.append(self.transform_date(datacite_dates))

    def transform_date(self, date):
        if date.get('#text').isnumeric():
            return {
                    'date': date['#text'],
                    'dateType': date['@dateType'],
                }
        else:
            return {}

    def transform_descriptions(self, descriptions, datacite_descriptions):
        if isinstance(datacite_descriptions, list):
            for description in datacite_descriptions:
                descriptions.append(self.transform_description(description))
        else:
            descriptions.append(self.transform_description(datacite_descriptions))

    def transform_description(self, description):
        return {
                'description': description['#text'],
                'descriptionType' : description['@descriptionType'],
                }

    def transform_doi(self, datacite_doi):
        if datacite_doi.get("@identifierType") == 'DOI':
            return datacite_doi.get('#text')

    def transform_format(self, _formats, datacite_formats):
        if isinstance(datacite_formats, list):
            _formats.extend(datacite_formats)
        else:
            _formats.append(datacite_formats)

    def transform_funding(self, fundings, zenodo_fundings):
       pass

    def transform_geo_location(self, datacite_geo_locations):
        curr_location = {}
        if datacite_geo_locations.get('geoLocationPlace'):
            curr_location['geoLocationPlace'] = datacite_geo_locations['geoLocationPlace']
        if datacite_geo_locations.get("geoLocationPoint"):
            point = datacite_geo_locations.get('geoLocationPoint').split()
            curr_location['geoLocationPoint'] = {
                'pointLatitude': point[0],
                'pointLongitude': point[1]
            }
        return curr_location

    def transform_geo_locations(self, locations, datacite_geo_locations):
        if isinstance(datacite_geo_locations, list):
            for location in datacite_geo_locations:
                locations.append(self.transform_geo_location(location))
        else:
            locations.append(self.transform_geo_location(datacite_geo_locations))

    def transform_publisher(self, publisher, datacite_publisher):
        if datacite_publisher:
            publisher.update({
                'name' : datacite_publisher
            })

    def transform_related_identifier(self, datacite_related_identifiers):
        return {
            'relatedIdentifier': datacite_related_identifiers["#text"],
            'relatedIdentifierType': datacite_related_identifiers["@relatedIdentifierType"],
            'relationType' : datacite_related_identifiers["@relationType"],
        }

    def transform_related_identifiers(self, related_identifiers, datacite_related_identifiers):
        if isinstance(datacite_related_identifiers, list):
            for rel_id in datacite_related_identifiers:
                related_identifiers.append(self.transform_related_identifier(rel_id))
        else:
            related_identifiers.append(self.transform_related_identifier(datacite_related_identifiers))

    def transform_right(self, right):
        if isinstance(right, str):
            return {'rights' : right}

        curr_right = {
            'rights': right['#text'],
        }
        if right.get("@rightsURI") is not None:
            curr_right['rightsURI'] = right.get("@rightsURI")
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

        subject = {"subject" : datacite_subject['#text']}
        if datacite_subject.get("@subjectScheme"):
            subject['subjectScheme'] = datacite_subject['@subjectScheme']
        return subject

    def transform_subjects(self, subjects, datacite_subjects):
        if isinstance(datacite_subjects, list):
            for subject in datacite_subjects:
                subjects.append(self.transform_subject(subject))
        else:
            subjects.append(self.transform_subject(datacite_subjects))

    def transform_title(self, datacite_titles):
       curr_title = {
           "title": datacite_titles,
            "titleType": "Other"
       }
       return curr_title

    def transform_titles(self, titles, datacite_titles):
        if isinstance(datacite_titles, list):
            for title in datacite_titles:
                titles.append(self.transform_title(title))
        else:
            titles.append(self.transform_title(datacite_titles))

    def transform_types(self, types, datacite_type):
        if datacite_type:
            curr_type = {
                'resourceTypeGeneral' : datacite_type['@resourceTypeGeneral'],
            }
            if datacite_type.get('#text'):
                curr_type['resourceType'] = datacite_type['#text']
            types.append(curr_type)

    def transform_url(self, url, zenodo_url):
        pass  # no url

    def transform_entry(self, entry:StreamEntry):
        source_metadata = self.parse_xml(entry)
        source_metadata = OrderedDict((key, value) for key, value in source_metadata.items() if value is not None)

        transformed_metadata = {}

        self.transform_alt_identifiers(transformed_metadata.setdefault('alternateIdentifiers',[]),
                                       source_metadata.get('alternateIdentifiers',{}).get("alternateIdentifier",[]))

        self.transform_contributors(transformed_metadata.setdefault('contributors',[]),
                                    source_metadata.get('contributors',{}).get('contributor',[]))

        self.transform_creators(transformed_metadata.setdefault('creators',[]),
                                source_metadata.get('creators',{}).get('creator',[]))

        self.transform_dates(transformed_metadata.setdefault('dates',[]),
                             source_metadata.get('dates',{}).get("date",[]))


        self.transform_descriptions(transformed_metadata.setdefault('descriptions',[]),
                                    source_metadata.get('descriptions',{}).get('description',[]))

        transformed_metadata['doi'] = self.transform_doi(source_metadata.get('identifier'),)

        self.transform_format(transformed_metadata.setdefault('formats',[]),
                              source_metadata.get('formats',{}).get('format',[]))

        self.transform_geo_locations(transformed_metadata.setdefault('geoLocations',[]),
                                    source_metadata.get('geoLocations',{}).get('geoLocation',[]))

        if source_metadata.get('language'):
            transformed_metadata['language'] = source_metadata.get('language')

        if source_metadata.get('publicationYear'):
            transformed_metadata['publicationYear'] = source_metadata.get('publicationYear')

        self.transform_publisher(transformed_metadata.setdefault('publisher',{}),
                                 source_metadata.get('publisher',{}))

        self.transform_related_identifiers(transformed_metadata.setdefault('relatedIdentifiers',[]),
                                           source_metadata.get('relatedIdentifiers',{}).get('relatedIdentifier',[]))

        self.transform_rights(transformed_metadata.setdefault('rightsList',[]),
                              source_metadata.get('rightsList',{}).get('rights',[]))

        self.transform_sizes(transformed_metadata.setdefault('sizes',[]),
                             source_metadata.get('sizes',{}).get('size',[]))

        self.transform_subjects(transformed_metadata.setdefault('subjects',[]),
                                source_metadata.get('subjects',{}).get('subject',[]))

        self.transform_titles(transformed_metadata.setdefault('titles',[]),
                              source_metadata.get('titles',{}).get('title',[]))

        self.transform_types(transformed_metadata.setdefault('types',[]),
                             source_metadata.get('resourceType'))

        if source_metadata.get('version') is not None:
            transformed_metadata['version'] = source_metadata['version']

        entry.entry = {'metadata': transformed_metadata}

