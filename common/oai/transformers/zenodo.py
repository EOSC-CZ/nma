from typing import Union
from oarepo_runtime.datastreams import BaseTransformer, StreamEntry, StreamBatch

from common.oai.transformers.lindat import transform_identifier, transform_description


class ZenodoTransformer(BaseTransformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply(self, batch: StreamBatch, *args, **kwargs) -> Union[StreamBatch, None]:
        """Applies the transformation to the entry.
        :returns: A StreamEntry. The transformed entry.
                  Raises TransformerError in case of errors.
        """
        for entry in batch.entries:
            self.transform_entry(entry)

        return batch

    def ensureEmpty(self, data, *exceptions, filter=True):
        for key in data.keys():
            if key not in exceptions:
                if filter:
                    filtered_data = {k: v for k, v in data.items() if k not in exceptions}
                else:
                    filtered_data = data
                print(filtered_data)
                raise Exception(f"Unhandled key: {key} inside data")

    def transform_alt_identifiers(self, alt_identifiers, zenodo_alt_identifiers):
        for identifier in zenodo_alt_identifiers:
            alt_identifiers.append({
                'alternateIdentifier': identifier.pop('identifier'),
                'alternateIdentifierType': identifier.pop('scheme')
            })
            self.ensureEmpty(identifier)

    def transform_name_identifiers(self, name_identifiers, zenodo_name_identifiers):
        for identifier in zenodo_name_identifiers:
            name_identifiers.append({
                'nameIdentifier': identifier.pop('identifier'),
                'nameIdentifierScheme': identifier.pop('scheme')
            })
            self.ensureEmpty(identifier)

    def transform_container(self):
        pass # no container in zenodo

    def transform_contributors(self, contributors, zenodo_contributors):
        for contributor in zenodo_contributors:
            role = self.transform_role(contributor.pop('role',{}).get('id'))

            affiliations = []
            self.transform_affiliation(affiliations,contributor.pop('affiliations', []))

            person_or_org = self.transform_person(contributor.pop('person_or_org'))

            current_contributor = {
                'contributorType': role,
            }
            current_contributor.update(person_or_org)
            if len(affiliations) > 0:
                current_contributor['affiliation'] = affiliations
            contributors.append(current_contributor)


    def transform_person(self, zenodo_person):
        person = {}
        if zenodo_person.get('family_name') is not None:
            person['familyName'] = zenodo_person.pop('family_name')
        if zenodo_person.get('given_name') is not None:
            person['givenName'] = zenodo_person.pop('given_name')
        if zenodo_person.get('name') is not None:
            person['name'] = zenodo_person.pop('name')

        identifiers = []
        self.transform_name_identifiers(identifiers, zenodo_person.pop('identifiers', []))
        if len(identifiers) > 0:
            person['nameIdentifiers'] = identifiers

        if zenodo_person.pop('type') == 'personal':
            person['nameType'] = "Personal"
        else:
            person['nameType'] = "Organizational"

        return person


    def transform_role(self, role):
        zenodoRole_to_ourType = {
            'contactperson': 'ContactPerson',
            'datacollector': 'DataCollector',
            'datacurator': 'DataCurator',
            'datamanager': 'DataManager',
            'distributor': 'Distributor',
            'editor': 'Editor',
            'hostinginstitution': 'HostingInstitution',
            'producer': 'Producer',
            'projectleader': 'ProjectLeader',
            'projectmanager': 'ProjectManager',
            'projectmember': 'ProjectMember',
            'registrationagency': 'RegistrationAgency',
            'registrationauthority': 'RegistrationAuthority',
            'relatedperson': 'RelatedPerson',
            'researcher': 'Researcher',
            'researchgroup': 'ResearchGroup',
            'rightsholder': 'RightsHolder',
            'sponsor': 'Sponsor',
            'supervisor': 'Supervisor',
            'workpackageleader': 'WorkPackageLeader',
            'other': 'Other',
        }
        if role in zenodoRole_to_ourType:
            return zenodoRole_to_ourType[role]
        else:
            return "Other"

    def transform_creators(self, creators, zenodo_creators):
        for creator in zenodo_creators:
            affiliations = []
            self.transform_affiliation(affiliations, creator.pop('affiliations', []))

            person_or_org = self.transform_person(creator.pop('person_or_org'))

            current_creator = {}
            current_creator.update(person_or_org)
            if len(affiliations) > 0:
                current_creator['affiliation'] = affiliations
            creators.append(current_creator)

    def transform_affiliation(self, affiliations, zenodo_affiliations):
        for zenodo_affiliation in zenodo_affiliations:
            affiliation = {
                'name' : zenodo_affiliation['name'],
            }
            if zenodo_affiliation.get('id') is not None:
                affiliation['affiliationIdentifier'] = zenodo_affiliation.get('id')
            affiliations.append(affiliation)

    def transform_dates(self, dates, zenodo_dates):
        for date in zenodo_dates:
            schema = {
                'date': date.pop('date'),
                'dateType' : date['type']['id'].capitalize()
            }
            if date.get('description', None) is not None:
                schema['dateInformation'] = date['description']
            dates.append(schema)

    def transform_descriptions(self, descriptions, main_description, zenodo_descriptions):
        if main_description is not None:
            descriptions.append({
                'description': main_description,
                'descriptionType': 'Other'
            })

        for description in zenodo_descriptions:
            curr_description = {
                'description': description.pop('description', ''),
                'descriptionType': self.transform_descriptionType_to_our(description['type']['id']),
            }
            if description.get('lang') is not None:
                curr_description['lang'] = description['lang']['id']

            descriptions.append(curr_description)

    def transform_descriptionType_to_our(self, zenodo_type):
        if zenodo_type == 'abstract':
            return "Abstract"
        elif zenodo_type == 'methods':
            return "Methods"
        elif zenodo_type == 'series-information':
            return "SeriesInformation"
        elif zenodo_type == 'table-of-contents':
            return "TableOfContents"
        elif zenodo_type == 'technical-info':
            return "TechnicalInfo"
        else: return "Other"

    def transform_doi(self, doi, zenodo_doi):
        # TODO it is not in metadata
        pass

    def transform_format(self, _formats, zenodo_formats):
        for _format in zenodo_formats:
            _formats.append(_format)

    def transform_funding(self, fundings, zenodo_fundings):
        for funding in zenodo_fundings:
            funder = {
                'funderIdentifierType' : "ROR",
                'funderIdentifier' : funding['funder']['id'],
                'funderName' : funding.pop('funder')['name'],
            }
            if funding.get('award') is not None:
                funder['awardNumber'] = funding['award']['number']
                funder['awardTitle'] = funding['award']['title']['en']
                if funding.get('award').get('identifiers') is not None:
                    funder['awardURI'] = funding['award']['identifiers'][0]['identifier']
            fundings.append(funder)

    def transform_geo_location(self, geo_locations, zenodo_geo_locations):
        pass # didnt find on zenodo creation form

    def transform_language(self, zenodo_languages):
        if zenodo_languages is not None:
            return zenodo_languages[0]['id']

    def transform_publication_year(self, zenodo_year):
        return zenodo_year[:4]

    def transform_publisher(self, publisher, zenodo_publisher):
        if zenodo_publisher is not None:
            publisher.update({
                'name' : zenodo_publisher
            })

    def transform_related_identifiers(self, related_identifiers, zenodo_related_identifiers):
        for rel_identifier in zenodo_related_identifiers:
            if rel_identifier['scheme'] == "other":
                continue
            curr_identifier = {
                'relatedIdentifier':rel_identifier['identifier'],
                'relatedIdentifierType' : self.transform_relatedIdentifier_type(rel_identifier['scheme']),
                'relationType' : self.transform_relation_type(rel_identifier['relation_type']['id']),
                'resourceTypeGeneral' : self.transform_resourceType_to_our(rel_identifier.get('resource_type',{}).get('id',"")),
            }
            related_identifiers.append(curr_identifier)


    def transform_relatedIdentifier_type(self, zenodo_relatedIdentifier_type):
        identifier_dict = {
            "ark": "ARK",
            "arxiv": "arXiv",
            "bibcode": "bibcode",
            "doi": "DOI",
            "ean13": "EAN13",
            "eissn": "EISSN",
            "handle": "Handle",
            "igsn": "IGSN",
            "isbn": "ISBN",
            "issn": "ISSN",
            "istc": "ISTC",
            "lissn": "LISSN",
            "lsid": "LSID",
            "pmid": "PMID",
            "purl": "PURL",
            "upc": "UPC",
            "url": "URL",
            "urn": "URN",
            "w3id": "w3id"
        }
        if zenodo_relatedIdentifier_type in identifier_dict:
            return identifier_dict[zenodo_relatedIdentifier_type]

    def transform_relation_type(self, zenodo_relation_type):
        relations_dict = {
            "iscitedby": "IsCitedBy",
            "cites": "Cites",
            "iscollectedby": "IsCollectedBy",
            "collects": "Collects",
            "issupplementto": "IsSupplementTo",
            "issupplementedby": "IsSupplementedBy",
            "iscontinuedby": "IsContinuedBy",
            "continues": "Continues",
            "isdescribedby": "IsDescribedBy",
            "describes": "Describes",
            "hasmetadata": "HasMetadata",
            "ismetadatafor": "IsMetadataFor",
            "hasversion": "HasVersion",
            "isversionof": "IsVersionOf",
            "isnewversionof": "IsNewVersionOf",
            "ispartof": "IsPartOf",
            "ispreviousversionof": "IsPreviousVersionOf",
            "ispublishedin": "IsPublishedIn",
            "haspart": "HasPart",
            "isreferencedby": "IsReferencedBy",
            "references": "References",
            "isdocumentedby": "IsDocumentedBy",
            "documents": "Documents",
            "iscompiledby": "IsCompiledBy",
            "compiles": "Compiles",
            "isvariantformof": "IsVariantFormOf",
            "isoriginalformof": "IsOriginalFormOf",
            "isidenticalto": "IsIdenticalTo",
            "isreviewedby": "IsReviewedBy",
            "reviews": "Reviews",
            "isderivedfrom": "IsDerivedFrom",
            "issourceof": "IsSourceOf",
            "isrequiredby": "IsRequiredBy",
            "requires": "Requires",
            "isobsoletedby": "IsObsoletedBy",
            "obsoletes": "Obsoletes"
        }
        if zenodo_relation_type in relations_dict:
            return relations_dict[zenodo_relation_type]

    def transform_related_items(self, related_items, zenodo_related_items):
        pass # no related items in zenodo

    def transform_rights(self, rights, zenodo_rights):
        for right in zenodo_rights:
            curr_right = {}
            if right.get('id') is not None:
                curr_right['rightsIdentifier'] = right.get('id')
            if right.get('title',{}).get('en', None) is not None:
                curr_right['rights'] = right.get('title').get('en')
            if right.get('props',{}).get('url', None) is not None:
                curr_right['rightsURI'] = right.get('props').get('url')
            if right.get('props', {}).get('scheme') is not None:
                curr_right['rightsIdentifierScheme'] = right.get('props').get('scheme')
            if len(curr_right['rights']) > 0:
                rights.append(curr_right)

    def transform_schema_version(self):
        pass

    def transform_sizes(self, sizes, zenodo_sizes):
        for size in zenodo_sizes:
            sizes.append(size)

    def transform_subjects(self, subjects, zenodo_subjects):
        subjects.extend(zenodo_subjects)

    def transform_titles(self, titles, zenodo_title, zenodo_additional_titles):
        titles.append({
            'title': zenodo_title,
            'titleType': "Other"
        })
        for add_title in zenodo_additional_titles:
            title = {
                'title': add_title['title'],
                'titleType': self.transform_titleType_to_our(add_title['type']['id'])
            }
            if add_title.get('lang') is not None:
                title['lang'] = add_title['lang']['id']
            titles.append(title)

    def transform_titleType_to_our(self, zenodo_title_type):
        if zenodo_title_type == 'alternative-title':
            return "AlternativeTitle"
        elif zenodo_title_type == 'translated-title':
            return "TranslatedTitle"
        elif zenodo_title_type == 'subtitle':
            return "Subtitle"
        else: return "Other"

    def transform_types(self, types, zenodo_types):
        types.append({
            'resourceType': zenodo_types['title']['en'],
            'resourceTypeGeneral' : self.transform_resourceType_to_our(zenodo_types['id']),
        })

    def transform_resourceType_to_our(self, zenodo_type:str):
        zenodo_type_to_our = {
            'dataset' : "Dataset",
            'event' : "Event",
            'physicalobject' : "PhysicalObject",
            'publication-book' : "Book",
            'publication-section' : "BookChapter",
            'publication-conferencepaper' : "ConferencePaper",
            'publication-conferenceproceeding' : "ConferenceProceeding",
            'publication-datapaper' : "DataPaper",
            'publication-dissertation' : "Dissertation",
            'publication-journal' : "Journal",
            'publication-outputmanagementplan' : "OutputManagementPlan",
            'publication-peerreview' : "PeerReview",
            'publication-preprint' : "Preprint",
            'publication-report' : "Report",
            'publication-standard' : "Standard",
            'software' : "Software",
            'video' : "Audiovisual",
            'audio' : "Audiovisual",
            'workflow' : "Workflow",
        }
        if zenodo_type_to_our.get(zenodo_type) is not None:
            return zenodo_type_to_our[zenodo_type]
        elif zenodo_type.startswith('image-'):
            return "Image"
        else:
            return "Other"

    def transform_url(self, url, zenodo_url):
        pass # no url, could be references in zenodo

    def transform_version(self, zenodo_version):
        return zenodo_version

    def transform_entry(self, entry:StreamEntry):
        source_metadata = entry.context['oai']['metadata']
        transformed_metadata = {}

        self.transform_alt_identifiers(transformed_metadata.setdefault('alternateIdentifiers', []),
                                       source_metadata.pop('identifiers',[]))


        self.transform_contributors(transformed_metadata.setdefault('contributors', []),
                                       source_metadata.pop('contributors', []))

        self.transform_creators(transformed_metadata.setdefault('creators', []),
                                source_metadata.pop('creators', []))

        self.transform_dates(transformed_metadata.setdefault('dates', []),
                             source_metadata.pop('dates', []))

        self.transform_descriptions(transformed_metadata.setdefault('descriptions', []),
                                    source_metadata.pop('description', ""),
                                    source_metadata.pop('additional_descriptions', []))

        # TODO doi
        #self.transform_doi(transformed_metadata.setdefault('doi', []),)

        #self.transform_format(transformed_metadata.setdefault('formats', []),
        #                      source_metadata.pop('formats', []))

        self.transform_funding(transformed_metadata.setdefault('fundingReferences', []),
                               source_metadata.pop('funding', []))

        transformed_metadata['language'] = self.transform_language(source_metadata.pop('languages', []))
        transformed_metadata['publicationYear'] = self.transform_publication_year(source_metadata.pop('publication_date', ""))

        self.transform_publisher(transformed_metadata.setdefault('publisher', {}),
                                 source_metadata.pop('publisher', ""))

        self.transform_related_identifiers(transformed_metadata.setdefault('relatedIdentifiers', []),
                                           source_metadata.pop('related_identifiers', []))

        self.transform_rights(transformed_metadata.setdefault('rightsList', []),
                              source_metadata.pop('rights', []))

        self.transform_subjects(transformed_metadata.setdefault('subjects', []),
                                source_metadata.pop('subjects', []))

        self.transform_titles(transformed_metadata.setdefault('titles', []),
                              source_metadata.pop('title', ""),
                              source_metadata.pop('additional_titles', []))

        self.transform_types(transformed_metadata.setdefault('types', []),
                             source_metadata.pop('resource_type', {}))

        transformed_metadata['version'] = self.transform_version(source_metadata.pop('version', ""))
        entry.entry = transformed_metadata