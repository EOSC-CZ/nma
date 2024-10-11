from common.oai.transformers.zenodo import ZenodoTransformer
from nr_metadata.datacite.services.records.schema_datatypes import CreatorSchema, ResourceTypeSchema, TitleSchema, \
    SubjectSchema, RightsSchema, PublisherSchema, DescriptionSchema, DateSchema, AlternateIdentifierSchema, \
    ContributorSchema, FundingReferenceSchema
from nr_metadata.datacite.services.records.schema import NRDataCiteMetadataSchema
import json
from oarepo_runtime.datastreams import BaseReader, StreamEntry

def test_transform_types():
    transformer = ZenodoTransformer()
    converted = {}
    transformer.transform_resource_type(converted, {
      "id": "publication-conferencepaper",
      "title": {
        "de": "Konferenzbeitrag",
        "en": "Conference paper"
      }
    })
    assert converted['resourceType'] == {
        'resourceType' : 'Conference paper',
        'resourceTypeGeneral' : 'ConferencePaper'
    }

    ResourceTypeSchema().load(converted['resourceType'])

def test_transform_sizes():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_sizes(converted, ['1321321','12313','123135'])
    assert converted == ['1321321','12313','123135']

def test_transform_titles():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_titles(converted, "Main title", [
        {
            "lang": {
                "id": "rus",
                "title": {
                    "en": "Russian"
                }
            },
            "title": "addtitle",
            "type": {
                "id": "alternative-title",
                "title": {
                    "de": "Alternativer Titel",
                    "en": "Alternative title"
                }
            }
        },
      {
        "title": "test2",
        "type": {
          "id": "translated-title",
          "title": {
            "de": "\u00dcbersetzter Titel",
            "en": "Translated title"
          }
        }
      },
      {
        "title": "test3",
        "type": {
          "id": "subtitle",
          "title": {
            "de": "Untertitel",
            "en": "Subtitle"
          }
        }
      },
      {
        "title": "test4",
        "type": {
          "id": "other",
          "title": {
            "de": "Sonstiger Titel",
            "en": "Other"
          }
        }
      }
    ])
    assert converted == [
        {'title' : "Main title", 'titleType':"Other"},
        {'title' : "addtitle", 'titleType':"AlternativeTitle", 'lang': "rus"},
        {'title' : "test2", 'titleType':"TranslatedTitle"},
        {'title' : "test3", 'titleType':"Subtitle"},
        {'title' : "test4", 'titleType':"Other"}
    ]
    for i, title in enumerate(converted):
        TitleSchema().load(title)

def test_transform_subjects():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_subjects(converted, [
      {
        "subject": "subject1",
      },
      {
        "subject": "t"
      },
      {
        "subject": "q"
      },
    ])
    assert converted == [
        {'subject' : 'subject1'},
        {'subject' : "t"},
        {'subject' : 'q'},
    ]

    for subject in converted:
        SubjectSchema().load(subject)

def test_transform_rights():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_rights(converted, [
      {
        "description": {
          "en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."
        },
        "icon": "cc-by-icon",
        "id": "cc-by-4.0",
        "props": {
          "scheme": "spdx",
          "url": "https://creativecommons.org/licenses/by/4.0/legalcode"
        },
        "title": {
          "en": "Creative Commons Attribution 4.0 International"
        }
      },
      {
        "description": {
          "en": ""
        },
        "id": "antlr-pd",
        "props": {
          "scheme": "spdx",
          "url": "http://www.antlr2.org/license.html"
        },
        "title": {
          "en": "ANTLR Software Rights Notice"
        }
      }
    ])
    assert converted == [
        {
            'rightsIdentifier': 'cc-by-4.0',
            'rights' : 'Creative Commons Attribution 4.0 International',
            'rightsURI': 'https://creativecommons.org/licenses/by/4.0/legalcode',
            'rightsIdentifierScheme' : 'spdx'
        },
        {
            'rightsIdentifier': 'antlr-pd',
            'rights': 'ANTLR Software Rights Notice',
            'rightsURI': 'http://www.antlr2.org/license.html',
            'rightsIdentifierScheme': 'spdx'
        }
    ]
    for right in converted:
        RightsSchema().load(right)

def test_transform_related_identifiers():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_related_identifiers(converted, [
      {
        "identifier": "00xh22n12",
        "relation_type": {
          "id": "continues",
          "title": {
            "de": "Setzt fort",
            "en": "Continues"
          }
        },
        "resource_type": {
          "id": "model",
          "title": {
            "de": "Modell",
            "en": "Model"
          }
        },
        "scheme": "other"
      },
      {
        "identifier": "arXiv:2309.12345",
        "relation_type": {
          "id": "cites",
          "title": {
            "de": "Zitiert",
            "en": "Cites"
          }
        },
        "resource_type": {
          "id": "physicalobject",
          "title": {
            "de": "Physikalisches Objekt",
            "en": "Physical object"
          }
        },
        "scheme": "w3id"
      },
      {
        "identifier": "4006381333931",
        "relation_type": {
          "id": "isdescribedby",
          "title": {
            "de": "Wird beschrieben von",
            "en": "Is described by"
          }
        },
        "scheme": "ean13"
      }])
    assert converted == [
        {
            'relatedIdentifier' : "arXiv:2309.12345",
            'relatedIdentifierType' : 'w3id',
            'relationType' : "Cites",
            'resourceTypeGeneral' : "PhysicalObject"
        },
        {
            'relatedIdentifier' : "4006381333931",
            'relatedIdentifierType' : 'EAN13',
            'relationType' : "IsDescribedBy",
            'resourceTypeGeneral' : "Other"
        }
    ]

def test_transform_publisher():
    transformer = ZenodoTransformer()
    converted = {}
    transformer.transform_publisher(converted, 'Some publisher')
    assert converted == {'name': 'Some publisher'}
    PublisherSchema().load(converted)

def test_transform_publication_year():
    transformer = ZenodoTransformer()
    converted = transformer.transform_publication_year("2024-06-01")
    assert converted == "2024"

def test_transform_language():
    transformer = ZenodoTransformer()
    converted = transformer.transform_language([
      {
        "id": "en",
        "title": {
          "en": "English"
        }
      },
      {
        "id": "jam",
        "title": {
          "en": "Jamaican Creole English"
        }
      }
    ])
    assert converted == 'en'

def test_transform_geo_locations():
    pass #TODO

def test_transform_formats():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_format(converted, ['format1','format2'])
    assert converted == ['format1','format2']

def test_transform_descriptions():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_descriptions(converted, '<p>some description idk</p>',[
      {
        "description": "<p>abstract description</p>",
        "lang": {
          "id": "eng",
          "title": {
            "en": "English"
          }
        },
        "type": {
          "id": "abstract",
          "title": {
            "de": "Abstract",
            "en": "Abstract"
          }
        }
      },
      {
        "description": "<p>methods des</p>",
        "type": {
          "id": "methods",
          "title": {
            "de": "Methoden",
            "en": "Methods"
          }
        }
      },
      {
        "description": "<p>note des</p>",
        "type": {
          "id": "notes",
          "title": {
            "de": "Anmerkungen",
            "en": "Notes"
          }
        }
      },
      {
        "description": "<p>series info</p>",
        "type": {
          "id": "series-information",
          "title": {
            "de": "Informationen zur Reihe",
            "en": "Series information"
          }
        }
      },
      {
        "description": "<p>table of content</p>",
        "type": {
          "id": "table-of-contents",
          "title": {
            "de": "Inhaltsverzeichnis",
            "en": "Table of contents"
          }
        }
      },
      {
        "description": "<p>tech info</p>",
        "type": {
          "id": "technical-info",
          "title": {
            "de": "Technische Informationen",
            "en": "Technical info"
          }
        }
      }
    ])
    assert converted == [
        {'description': '<p>some description idk</p>',
         'descriptionType' : 'Abstract'},

        {'description': '<p>abstract description</p>',
         'descriptionType': 'Abstract',
         'lang':'eng'},

        {'description': '<p>methods des</p>',
         'descriptionType': 'Methods',
         },

        {'description': '<p>note des</p>',
         'descriptionType': 'Other',
         },

        {'description': '<p>series info</p>',
         'descriptionType': 'SeriesInformation',
         },

        {'description': '<p>table of content</p>',
         'descriptionType': 'TableOfContents',
         },

        {'description': '<p>tech info</p>',
         'descriptionType': 'TechnicalInfo',
         },
    ]
    for description in converted:
        DescriptionSchema().load(description)

def test_transform_dates():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_dates(converted, "2024-01-01",[
      {
        "date": "2022-01-01",
        "description": "accepted des",
        "type": {
          "id": "accepted",
          "title": {
            "de": "Angenommen",
            "en": "Accepted"
          }
        }
      },
      {
        "date": "2022-01-01",
        "type": {
          "id": "available",
          "title": {
            "de": "Verf\u00fcgbar",
            "en": "Available"
          }
        }
      },
      {
        "date": "2022-01-01",
        "type": {
          "id": "collected",
          "title": {
            "de": "Gesammelt",
            "en": "Collected"
          }
        }
      },
      {
        "date": "2022-01-01",
        "type": {
          "id": "copyrighted",
          "title": {
            "de": "Mit Copyright versehen",
            "en": "Copyrighted"
          }
        }
      },
      {
        "date": "2022-01-01",
        "type": {
          "id": "created",
          "title": {
            "de": "Erstellt",
            "en": "Created"
          }
        }
      }
    ])

    assert converted == [
        {
            'date': '2024-01-01',
            'dateType' : "Issued"
        },
        {'date': '2022-01-01',
         'dateInformation': 'accepted des',
         'dateType': 'Accepted',},

        {'date': '2022-01-01',
         'dateType': 'Available', },

        {'date': '2022-01-01',
         'dateType': 'Collected', },

        {'date': '2022-01-01',
         'dateType': 'Copyrighted', },

        {'date': '2022-01-01',
         'dateType': 'Created', },
    ]
    for date in converted:
        DateSchema().load(date)

def test_transform_creators():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_creators(converted, [
      {
        "affiliations": [
          {
            "id": "024d6js02",
            "name": "Charles University"
          }
        ],
        "person_or_org": {
          "family_name": "Testing name",
          "given_name": "given names",
          "name": "Testing name, given names",
          "type": "personal"
        },
        "role": {
          "id": "contactperson",
          "title": {
            "de": "Kontaktperson",
            "en": "Contact person"
          }
        }
      },
      {
        "person_or_org": {
          "family_name": "creator without role",
          "name": "creator without role",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "identifiers": [
            {
              "identifier": "004ymxd45",
              "scheme": "ror"
            }
          ],
          "name": "MIT World Peace University",
          "type": "organizational"
        }
      }
    ])
    assert converted == [
        {
            'affiliation': [
                {
                    'affiliationIdentifier': '024d6js02',
                    'name': 'Charles University',
                 }],
            "familyName": "Testing name",
            'givenName': 'given names',
            'name': 'Testing name, given names',
            'nameType': 'Personal',
        },
        {
            'familyName': 'creator without role',
            'name': 'creator without role',
            'nameType' : "Personal"
        },
        {
            'name' : "MIT World Peace University",
            'nameType' : "Organizational",
            'nameIdentifiers' : [
                {
                    'nameIdentifier' : "004ymxd45",
                    'nameIdentifierScheme': "ror"
                }
            ]
        }
    ]
    for creator in converted:
        CreatorSchema().load(creator)

def test_transform_alternate_identifiers():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_alt_identifiers(converted, [
      {
        "identifier": "some alt identifier",
        "scheme": "other"
      },
      {
        "identifier": "arXiv:2309.12345",
        "scheme": "arxiv"
      }
    ])
    assert converted == [
        {'alternateIdentifier': 'some alt identifier',
         'alternateIdentifierType':'other'},
        {'alternateIdentifier': 'arXiv:2309.12345',
         'alternateIdentifierType':'arxiv'},
    ]
    for alt_id in converted:
        AlternateIdentifierSchema().load(alt_id)

def test_transform_contributors():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_contributors(converted, [
      {
        "person_or_org": {
          "family_name": "Torvalds",
          "given_name": "Linux=s",
          "name": "Torvalds, Linux=s",
          "type": "personal"
        },
        "role": {
          "id": "projectleader",
          "title": {
            "de": "ProjektleiterIn",
            "en": "Project leader"
          }
        }
      },
      {
        "person_or_org": {
          "name": "Org name",
          "type": "organizational"
        },
        "role": {
          "id": "distributor",
          "title": {
            "de": "VerteilerIn",
            "en": "Distributor"
          }
        }
      },
      {
        "person_or_org": {
          "name": "org name",
          "type": "organizational"
        },
        "role": {
          "id": "researcher",
          "title": {
            "de": "WissenschaftlerIn",
            "en": "Researcher"
          }
        }
      },
        {
            "person_or_org": {
                "family_name": "neco",
                "identifiers": [
                    {
                        "identifier": "004ymxd45",
                        "scheme": "ror"
                    }
                ],
                "name": "neco",
                "type": "personal"
            },
            "role": {
                "id": "hostinginstitution",
                "title": {
                    "de": "Bereitstellende Institution",
                    "en": "Hosting institution"
                }
            }
        }
    ])
    assert converted == [
        {
            'contributorType' : "ProjectLeader",
            'familyName' : "Torvalds",
            'givenName' : "Linux=s",
            'name' : "Torvalds, Linux=s",
            'nameType' : "Personal",
         },
        {
            'name' : "Org name",
            'nameType' : "Organizational",
            'contributorType' : "Distributor",
        },
        {
            'name': "org name",
            'nameType': "Organizational",
            'contributorType': "Researcher",
        },
        {
            'name' : "neco",
            'familyName' : "neco",
            'contributorType' : "HostingInstitution",
            'nameType' : "Personal" ,
            'nameIdentifiers' : [{
                "nameIdentifier" : "004ymxd45",
                'nameIdentifierScheme' : "ror"
            }]
        }
    ]
    for contributor in converted:
        ContributorSchema().load(contributor)

def test_transform_funders():
    transformer = ZenodoTransformer()
    converted = []
    transformer.transform_funding(converted, [
      {
        "funder": {
          "id": "00xh22n12",
          "name": "Czech Environmental Information Agency"
        }
      },
      {
        "award": {
          "id": "04jsz6e67::406.17.533",
          "number": "406.17.533",
          "program": "Onderzoekstalent 2017 Onderzoekstalent Full Proposals",
          "title": {
            "en": "The sense of belonging in human rights law. A legal and theoretical inquiry into the notion of identity in Strasbourg case law."
          }
        },
        "funder": {
          "id": "04jsz6e67",
          "name": "Dutch Research Council"
        }
      },
      {
        "funder": {
          "id": "00qd5p471",
          "name": "National Gallery in Prague"
        }
      },
      {
        "funder": {
          "id": "02yq4v676",
          "name": "EVECO Brno (Czechia)"
        }
      },
      {
        "award": {
          "acronym": "GREENE",
          "id": "00k4n6c32::101129888",
          "identifiers": [
            {
              "identifier": "https://cordis.europa.eu/projects/101129888",
              "scheme": "url"
            }
          ],
          "number": "101129888",
          "title": {
            "en": "SINGLE-GRAIN RE-ENGINEERED ND-FE-B PERMANENT MAGNETS"
          }
        },
        "funder": {
          "id": "00k4n6c32",
          "name": "European Commission"
        }
      }
    ])

    assert converted == [
        {
            'funderIdentifierType' : 'ROR',
            'funderIdentifier' : '00xh22n12',
            'funderName' : "Czech Environmental Information Agency"
        },
        {
            'funderIdentifierType' : 'ROR',
            'funderIdentifier' : '04jsz6e67',
            'funderName' : "Dutch Research Council",
            'awardNumber' : "406.17.533",
            'awardTitle' : "The sense of belonging in human rights law. A legal and theoretical inquiry into the notion of identity in Strasbourg case law."
        },
        {
            'funderIdentifierType' : 'ROR',
            'funderIdentifier' : '00qd5p471',
            'funderName' : "National Gallery in Prague"
        },
        {
            'funderIdentifierType' : 'ROR',
            'funderIdentifier' : '02yq4v676',
            'funderName' : "EVECO Brno (Czechia)"
        },
        {
            'funderIdentifierType' : 'ROR',
            'funderIdentifier' : '00k4n6c32',
            'funderName' : "European Commission",
            'awardNumber' : "101129888",
            'awardTitle' : "SINGLE-GRAIN RE-ENGINEERED ND-FE-B PERMANENT MAGNETS",
            'awardURI' : "https://cordis.europa.eu/projects/101129888",
        }
    ]
    for funding in converted:
        FundingReferenceSchema().load(funding)

def test_transform_all():
    transformer = ZenodoTransformer()
    record = None
    with open('tests/zenodo_example_metadata.json','r') as file:
        record = json.load(file)

    item = StreamEntry(entry=record,
                seq=0,
                context={
                    "oai": {
                        "metadata": (
                            record['metadata']
                            if "metadata" in record
                            else {}
                        ),
                        "datestamp": "",
                        "deleted": False,
                        "identifier": "",
                        "setSpecs": "",
                    },
                    "oai_run": "",
                    "oai_harvester_id": "",
                    "manual": ""
                })

    transformer.transform_entry(item)

    converted = {
        "alternateIdentifiers": [
            {
                'alternateIdentifier' : "arXiv:2309.12345",
                'alternateIdentifierType' : "arxiv"
            },
        ],
        'contributors' : [
            {
                'familyName' : "contributor without id/aff",
                'name' : "contributor without id/aff",
                'contributorType' : "HostingInstitution",
                'nameType' : "Personal"
             },
            {
                'familyName' : "contributor with id",
                'name' : "contributor with id",
                'nameType' : "Personal",
                'nameIdentifiers' : [
                    {'nameIdentifier' : "0000-0002-1825-0097", 'nameIdentifierScheme' : "orcid"}
                ],
                'contributorType' : "Editor",
            },
            {
                'familyName' : "creator with all",
                'name' : "creator with all",
                'nameType' : "Personal",
                'nameIdentifiers' : [
                    {'nameIdentifier' : "0000-0002-1825-0097", 'nameIdentifierScheme' : "orcid"}
                ],
                'contributorType' : "ContactPerson",
                'affiliation' : [
                    {"name" : "Academy of Performing Arts in Prague",
                     'affiliationIdentifier':"05mjwh489",
                     },
                ]
            },
            {
                'name' : "Federal Bureau of Investigation",
                'nameType' : "Organizational",
                'nameIdentifiers' : [
                    {'nameIdentifier' : "00ta5r839", 'nameIdentifierScheme' : "ror"},
                    {'nameIdentifier': "0000 0004 0481 0043", 'nameIdentifierScheme': "isni"},
                ],
                'contributorType' : "Supervisor",
            }
        ],
        'creators':[],
        'dates':[
            {'date' : "2024-09-23", 'dateType' : "Issued"},
            {'date':"2024-01-01",'dateType':'Accepted','dateInformation':"accepted"},
            {'date': "2024-01-01", 'dateType': 'Available', 'dateInformation': "available"},
            {'date': "2024-01-01", 'dateType': 'Collected', 'dateInformation': "collected"},
            {'date': "2024-01-01", 'dateType': 'Copyrighted'},
            {'date': "2024-01-01", 'dateType': 'Created'},
            {'date': "2024-01-01", 'dateType': 'Issued', },
            {'date': "2024-01-01", 'dateType': 'Other', },
            {'date': "2024-01-01", 'dateType': 'Submitted', },
            {'date': "2024-01-01", 'dateType': 'Updated', },
            {'date': "2024-01-01", 'dateType': 'Valid', },
            {'date': "2024-01-01", 'dateType': 'Withdrawn',},

        ],
        'descriptions':[
            {'description':"<p>main description</p>", 'descriptionType':"Abstract"},
            {'description': "<p>abstract</p>", 'descriptionType': "Abstract", 'lang':"spa"},
            {'description': "<p>methods</p>", 'descriptionType': "Methods"},
            {'description': "<p>notes</p>", 'descriptionType': "Other"},
            {'description': "<p>other</p>", 'descriptionType': "Other"},
            {'description': "<p>series information</p>", 'descriptionType': "SeriesInformation"},
            {'description': "<p>table of contents</p>", 'descriptionType': "TableOfContents"},
            {'description': "<p>technical info</p>", 'descriptionType': "TechnicalInfo"},
        ],
        'fundingReferences':[
            {"awardNumber":"101129888",
             'awardTitle':'SINGLE-GRAIN RE-ENGINEERED ND-FE-B PERMANENT MAGNETS',
             'awardURI':"https://cordis.europa.eu/projects/101129888",
             'funderIdentifier':'00k4n6c32',
             'funderIdentifierType':"ROR",
             'funderName':"European Commission"},
        ],
        'language':'eng',
        'publicationYear':"2024",
        'publisher':{'name':'some publisher'},
        'relatedIdentifiers':[
            {'relatedIdentifier':'arXiv:2309.12345','relatedIdentifierType':'arXiv',
             'relationType':'References','resourceTypeGeneral':'Software'},
            {'relatedIdentifier': 'arXiv:2309.12345', 'relatedIdentifierType': 'arXiv',
             'relationType': 'IsOriginalFormOf', 'resourceTypeGeneral': 'Other'},
        ],
        'rightsList':[
            {'rightsIdentifier':"cc-by-4.0",'rightsIdentifierScheme':'spdx',
             'rightsURI':"https://creativecommons.org/licenses/by/4.0/legalcode",
             'rights':"Creative Commons Attribution 4.0 International"},
            {'rightsIdentifier': "apache-2.0", 'rightsIdentifierScheme': 'spdx',
             'rightsURI': "http://www.apache.org/licenses/LICENSE-2.0",
             'rights': "Apache License 2.0"},
            {'rights':"custom licence"},
        ],
        'subjects':[{'subject':'testing'},{'subject':'transformer'}],
        'titles':[
            {'title':"testing transformer",'titleType':"Other"},
            {'title':"alternative title",'titleType':"AlternativeTitle",'lang':"jpn"},
            {'title': "translated title", 'titleType': "TranslatedTitle", 'lang': "deu"},
            {'title': "subtitle", 'titleType': "Subtitle", 'lang': "ces"},
            {'title': "other", 'titleType': "Other", 'lang': "slk"},
        ],
        'resourceType':{'resourceType':'Presentation','resourceTypeGeneral':"Other"},
        'version':"some version",
    }

    assert converted == item.entry['metadata']
    NRDataCiteMetadataSchema().load(item.entry['metadata'])

