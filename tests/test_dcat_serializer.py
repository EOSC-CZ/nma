import json

from common.datasets.serializers.dcat import DCATAPSerializer

def serialize_metadata(input_json):
    serializer = DCATAPSerializer()
    output_data = serializer.serialize_object(input_json)
    return json.loads(output_data)

def test_publisher_name():
    input_json_str = '''
    {
        "$schema": "local://datasets-1.0.0.json",
        "created": "2024-10-09T13:17:24.228537+00:00",
        "files": {
            "enabled": true
        },
        "id": "1tcaw-ksm19",
        "links": {
            "files": "https://127.0.0.1:5000/api/datasets/1tcaw-ksm19/files",
            "self": "https://127.0.0.1:5000/api/datasets/1tcaw-ksm19",
            "self_html": "https://127.0.0.1:5000/datasets/1tcaw-ksm19"
        },
        "metadata": {
            "publisher": {
                "name": "data.narodni-repozitar.cz"
            }
        }
    }
    '''
    input_json = json.loads(input_json_str)
    
    expected_output = {
        "publisher": "data.narodni-repozitar.cz",
        "schemaVersion": "http://datacite.org/schema/kernel-4"
    }
    
    assert serialize_metadata(input_json) == expected_output

def test_url_to_identifier():
    input_json_str = '''
    {
        "$schema": "local://datasets-1.0.0.json",
        "created": "2024-10-09T13:17:24.228537+00:00",
        "files": {
            "enabled": true
        },
        "id": "1tcaw-ksm19",
        "links": {
            "files": "https://127.0.0.1:5000/api/datasets/1tcaw-ksm19/files",
            "self": "https://127.0.0.1:5000/api/datasets/1tcaw-ksm19",
            "self_html": "https://127.0.0.1:5000/datasets/1tcaw-ksm19"
        },
        "metadata": {
            "url": "https://data.narodni-repozitar.cz/general/datasets/kgb8j-r5f84"
        }
    }
    '''
    input_json = json.loads(input_json_str)

    expected_output = {
        "identifiers": [
            {
                "identifier": "https://data.narodni-repozitar.cz/general/datasets/kgb8j-r5f84",
                "identifierType": "OriginalURL"
            }
        ],
        "schemaVersion": "http://datacite.org/schema/kernel-4"
    }

    assert serialize_metadata(input_json) == expected_output

def test_serialize_metadata():
    input_json_str = '''
    {
        "$schema": "local://datasets-1.0.0.json",
        "created": "2024-10-09T13:33:00.601364+00:00",
        "files": {
            "enabled": true
        },
        "id": "kcbes-eh875",
        "links": {
            "files": "https://127.0.0.1:5000/api/datasets/kcbes-eh875/files",
            "self": "https://127.0.0.1:5000/api/datasets/kcbes-eh875",
            "self_html": "https://127.0.0.1:5000/datasets/kcbes-eh875"
        },
        "metadata": {
            "creators": [
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Hossein Beydaghi",
                "name": "Hossein Beydaghi",
                "nameIdentifiers": [
                {
                    "nameIdentifier": "0000-0002-7590-590X",
                    "nameIdentifierScheme": "orcid"
                }
                ],
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Sebastiano Bellani",
                "name": "Sebastiano Bellani",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Leyla Najafi",
                "name": "Leyla Najafi",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Department of Material Science and Engineering, Uppsala University, Box 534, 75103 Uppsala, Sweden"
                }
                ],
                "familyName": "Reinier Oropesa-Nuñez",
                "name": "Reinier Oropesa-Nuñez",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
                ],
                "familyName": "Gabriele Bianca",
                "name": "Gabriele Bianca",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
                ],
                "familyName": "Ahmad Bagheri",
                "name": "Ahmad Bagheri",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Irene Conticello",
                "name": "Irene Conticello",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
                ],
                "familyName": "Beatriz Martín-García",
                "name": "Beatriz Martín-García",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Department of Chemical Engineering, Semnan University, Semnan, Iran"
                }
                ],
                "familyName": "Sepideh Kashefi",
                "name": "Sepideh Kashefi",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
                ],
                "familyName": "Michele Serri",
                "name": "Michele Serri",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Department of Inorganic Chemistry, University of Chemistry and Technology Prague, Technická 5, 166 28 Prague 6, Czech Republic"
                }
                ],
                "familyName": "Liping Liao",
                "name": "Liping Liao",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "Department of Inorganic Chemistry, University of Chemistry and Technology Prague, Technická 5, 166 28 Prague 6, Czech Republic"
                }
                ],
                "familyName": "Zdeněk Sofer",
                "name": "Zdeněk Sofer",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Vittorio Pellegrini",
                "name": "Vittorio Pellegrini",
                "nameType": "Personal"
            },
            {
                "affiliation": [
                {
                    "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
                ],
                "familyName": "Francesco Bonaccorso",
                "name": "Francesco Bonaccorso",
                "nameType": "Personal"
            }
            ],
            "dates": [
            {
                "date": "2022-04-07",
                "dateType": "Issued"
            }
            ],
            "descriptions": [
            {
                "description": "<p>In this work, novel proton-exchange membranes (PEMs) based on sulfonated poly(ether ether ketone) (SPEEK) and two-dimensional (2D) sulfonated niobium disulphide (S-NbS<sub>2</sub>) nanoflakes are synthesized by a solution-casting method and used in vanadium redox flow batteries (VRFBs). The NbS<sub>2</sub>&nbsp;nanoflakes are produced by liquid-phase exfoliation of their bulk counterpart and chemically functionalized with terminal sulfonate groups to improve dimensional and chemical stabilities, proton conductivity (<em>&sigma;</em>) and fuel barrier properties of the as-produced membranes. The addition of S-NbS<sub>2</sub>&nbsp;nanoflakes to SPEEK decreases the vanadium ion permeability from 5.42 &times; 10<sup>&minus;7</sup>&nbsp;to 2.34 &times; 10<sup>&minus;7</sup>&nbsp;cm<sup>2</sup>&nbsp;min<sup>&minus;1</sup>. Meanwhile, it increases the membrane&nbsp;<em>&sigma;</em>&nbsp;and selectivity up to 94.35 mS cm<sup>&minus;2</sup>&nbsp;and 40.32 &times; 10<sup>4</sup>&nbsp;S min cm<sup>&minus;3</sup>, respectively. The cell assembled with the optimized membrane incorporating 2.5 wt% of S-NbS<sub>2</sub>&nbsp;nanoflakes (SPEEK:2.5% S-NbS<sub>2</sub>) exhibits high efficiency metrics,&nbsp;<em>i.e.</em>, coulombic efficiency between 98.7 and 99.0%, voltage efficiency between 90.2 and 73.2% and energy efficiency between 89.3 and 72.8% within the current density range of 100&ndash;300 mA cm<sup>&minus;2</sup>, delivering a maximum power density of 0.83 W cm<sup>&minus;2</sup>&nbsp;at a current density of 870 mA cm<sup>&minus;2</sup>. The SPEEK:2.5% S-NbS<sub>2</sub>&nbsp;membrane-based VRFBs show a stable behavior over 200 cycles at 200 mA cm<sup>&minus;2</sup>. This study opens up an effective avenue for the production of advanced SPEEK-based membranes for VRFBs.</p>",
                "descriptionType": "Abstract"
            }
            ],
            "fundingReferences": [
            {
                "awardNumber": "881603",
                "awardTitle": "Graphene Flagship Core Project 3",
                "awardURI": "https://cordis.europa.eu/projects/881603",
                "funderIdentifier": "00k4n6c32",
                "funderIdentifierType": "ROR",
                "funderName": "European Commission"
            },
            {
                "awardNumber": "813036",
                "awardTitle": "Bottom-Up generation of atomicalLy precise syntheTIc 2D MATerials for high performance in energy and Electronic applications – A multi-site innovative training action",
                "awardURI": "https://cordis.europa.eu/projects/813036",
                "funderIdentifier": "00k4n6c32",
                "funderIdentifierType": "ROR",
                "funderName": "European Commission"
            },
            {
                "awardNumber": "957273",
                "awardTitle": "Cell-integrated SENSIing functionalities for smart BATtery systems with improved performance and safety",
                "awardURI": "https://cordis.europa.eu/projects/957273",
                "funderIdentifier": "00k4n6c32",
                "funderIdentifierType": "ROR",
                "funderName": "European Commission"
            }
            ],
            "language": "eng",
            "publicationYear": "2022",
            "publisher": {
            "name": "Zenodo"
            },
            "resourceType": {
            "resourceType": "Journal article",
            "resourceTypeGeneral": "Other"
            },
            "rightsList": [
            {
                "rights": "Creative Commons Attribution 4.0 International",
                "rightsIdentifier": "cc-by-4.0",
                "rightsIdentifierScheme": "spdx",
                "rightsURI": "https://creativecommons.org/licenses/by/4.0/legalcode"
            }
            ],
            "titles": [
            {
                "title": "Sulfonated NbS2-based proton-exchange membranes for vanadium redox flow batteries",
                "titleType": "Other"
            }
            ],
            "url": "https://zenodo.org/records/7115649",
            "version": ""
        },
        "oai": {
            "harvest": {
            "datestamp": "2024-07-16T01:44:18.043154+00:00",
            "identifier": "oai:zenodo.org:7115649"
            }
        },
        "revision_id": 2,
        "updated": "2024-10-09T13:33:00.628192+00:00"
        }
    '''
    
    expected_output_str = '''
    {
        "creators": [
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Hossein Beydaghi",
            "name": "Hossein Beydaghi",
            "nameIdentifiers": [
                {
                "nameIdentifier": "0000-0002-7590-590X",
                "nameIdentifierScheme": "orcid"
                }
            ],
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Sebastiano Bellani",
            "name": "Sebastiano Bellani",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Leyla Najafi",
            "name": "Leyla Najafi",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Department of Material Science and Engineering, Uppsala University, Box 534, 75103 Uppsala, Sweden"
                }
            ],
            "familyName": "Reinier Oropesa-Nu\u00f1ez",
            "name": "Reinier Oropesa-Nu\u00f1ez",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
            ],
            "familyName": "Gabriele Bianca",
            "name": "Gabriele Bianca",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
            ],
            "familyName": "Ahmad Bagheri",
            "name": "Ahmad Bagheri",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Irene Conticello",
            "name": "Irene Conticello",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
            ],
            "familyName": "Beatriz Mart\u00edn-Garc\u00eda",
            "name": "Beatriz Mart\u00edn-Garc\u00eda",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Department of Chemical Engineering, Semnan University, Semnan, Iran"
                }
            ],
            "familyName": "Sepideh Kashefi",
            "name": "Sepideh Kashefi",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Graphene Labs, Istituto Italiano di Tecnologia, via Morego 30, 16163 Genova, Italy"
                }
            ],
            "familyName": "Michele Serri",
            "name": "Michele Serri",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Department of Inorganic Chemistry, University of Chemistry and Technology Prague, Technick\u00e1 5, 166 28 Prague 6, Czech Republic"
                }
            ],
            "familyName": "Liping Liao",
            "name": "Liping Liao",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "Department of Inorganic Chemistry, University of Chemistry and Technology Prague, Technick\u00e1 5, 166 28 Prague 6, Czech Republic"
                }
            ],
            "familyName": "Zden\u011bk Sofer",
            "name": "Zden\u011bk Sofer",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Vittorio Pellegrini",
            "name": "Vittorio Pellegrini",
            "nameType": "Personal"
            },
            {
            "affiliation": [
                {
                "name": "BeDimensional S.p.A, Lungotorrente Secca, 30R 16163 Genoa, Italy"
                }
            ],
            "familyName": "Francesco Bonaccorso",
            "name": "Francesco Bonaccorso",
            "nameType": "Personal"
            }
        ],
        "dates": [
            {
            "date": "2022-04-07",
            "dateType": "Issued"
            }
        ],
        "descriptions": [
            {
            "description": "<p>In this work, novel proton-exchange membranes (PEMs) based on sulfonated poly(ether ether ketone) (SPEEK) and two-dimensional (2D) sulfonated niobium disulphide (S-NbS<sub>2</sub>) nanoflakes are synthesized by a solution-casting method and used in vanadium redox flow batteries (VRFBs). The NbS<sub>2</sub>&nbsp;nanoflakes are produced by liquid-phase exfoliation of their bulk counterpart and chemically functionalized with terminal sulfonate groups to improve dimensional and chemical stabilities, proton conductivity (<em>&sigma;</em>) and fuel barrier properties of the as-produced membranes. The addition of S-NbS<sub>2</sub>&nbsp;nanoflakes to SPEEK decreases the vanadium ion permeability from 5.42 &times; 10<sup>&minus;7</sup>&nbsp;to 2.34 &times; 10<sup>&minus;7</sup>&nbsp;cm<sup>2</sup>&nbsp;min<sup>&minus;1</sup>. Meanwhile, it increases the membrane&nbsp;<em>&sigma;</em>&nbsp;and selectivity up to 94.35 mS cm<sup>&minus;2</sup>&nbsp;and 40.32 &times; 10<sup>4</sup>&nbsp;S min cm<sup>&minus;3</sup>, respectively. The cell assembled with the optimized membrane incorporating 2.5 wt% of S-NbS<sub>2</sub>&nbsp;nanoflakes (SPEEK:2.5% S-NbS<sub>2</sub>) exhibits high efficiency metrics,&nbsp;<em>i.e.</em>, coulombic efficiency between 98.7 and 99.0%, voltage efficiency between 90.2 and 73.2% and energy efficiency between 89.3 and 72.8% within the current density range of 100&ndash;300 mA cm<sup>&minus;2</sup>, delivering a maximum power density of 0.83 W cm<sup>&minus;2</sup>&nbsp;at a current density of 870 mA cm<sup>&minus;2</sup>. The SPEEK:2.5% S-NbS<sub>2</sub>&nbsp;membrane-based VRFBs show a stable behavior over 200 cycles at 200 mA cm<sup>&minus;2</sup>. This study opens up an effective avenue for the production of advanced SPEEK-based membranes for VRFBs.</p>",
            "descriptionType": "Abstract"
            }
        ],
        "fundingReferences": [
            {
            "awardNumber": "881603",
            "awardTitle": "Graphene Flagship Core Project 3",
            "awardURI": "https://cordis.europa.eu/projects/881603",
            "funderIdentifier": "00k4n6c32",
            "funderIdentifierType": "ROR",
            "funderName": "European Commission"
            },
            {
            "awardNumber": "813036",
            "awardTitle": "Bottom-Up generation of atomicalLy precise syntheTIc 2D MATerials for high performance in energy and Electronic applications \u2013 A multi-site innovative training action",
            "awardURI": "https://cordis.europa.eu/projects/813036",
            "funderIdentifier": "00k4n6c32",
            "funderIdentifierType": "ROR",
            "funderName": "European Commission"
            },
            {
            "awardNumber": "957273",
            "awardTitle": "Cell-integrated SENSIing functionalities for smart BATtery systems with improved performance and safety",
            "awardURI": "https://cordis.europa.eu/projects/957273",
            "funderIdentifier": "00k4n6c32",
            "funderIdentifierType": "ROR",
            "funderName": "European Commission"
            }
        ],
        "identifiers": [
            {
            "identifier": "https://zenodo.org/records/7115649",
            "identifierType": "OriginalURL"
            }
        ],
        "language": "eng",
        "publicationYear": "2022",
        "publisher": "Zenodo",
        "rightsList": [
            {
            "rights": "Creative Commons Attribution 4.0 International",
            "rightsIdentifier": "cc-by-4.0",
            "rightsIdentifierScheme": "spdx",
            "rightsURI": "https://creativecommons.org/licenses/by/4.0/legalcode"
            }
        ],
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "titles": [
            {
            "title": "Sulfonated NbS2-based proton-exchange membranes for vanadium redox flow batteries",
            "titleType": "Other"
            }
        ],
        "types": {
            "resourceType": "Journal article",
            "resourceTypeGeneral": "Other"
        }
        }
    '''
    input_json = json.loads(input_json_str)
    expected_output = json.loads(expected_output_str)

    serialized_data = serialize_metadata(input_json)


    assert serialized_data == expected_output

def test_serialize_missing_metadata():
    input_json = {
        "$schema": "local://datasets-1.0.0.json",
        "created": "2024-10-09T13:33:00.601364+00:00",
        "files": {
            "enabled": True
        },
        "id": "kcbes-eh875"
    }
    
    expected_output = {}
    
    assert serialize_metadata(input_json) == expected_output

def test_serialize_empty_metadata():
    input_json = {
        "$schema": "local://datasets-1.0.0.json",
        "created": "2024-10-09T13:33:00.601364+00:00",
        "files": {
            "enabled": True
        },
        "id": "kcbes-eh875",
        "metadata": {}
    }
    
    expected_output = {}
    
    assert serialize_metadata(input_json) == expected_output