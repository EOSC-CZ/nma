import re
from typing import Union, List, Dict, Any
import json

class DataCiteTransformer:
    
    def __init__(self):
        pass

    def convert(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transforms the input data into DataCite format."""
        links = input_data.pop('links', {})
        link = links.get('self', '')

        orig_md = input_data.pop('metadata', {})
        converted_md = {
            "url": link,
            "$schema": 'local://datasets-1.0.0.json',
            "creators": [],
            "contributors": [],
            "descriptions": [],
            "dates": [],
            "rightsList": [],
            "subjects": [],
            "titles": [],
            "relatedItems": []
        }

        # Convert various sections
        self.convert_alternate_identifiers(converted_md.setdefault("alternateIdentifiers", []),
                                            orig_md.pop('persistentIdentifiers', []),
                                            link)
        self.convert_creators(converted_md.setdefault("creators", []), orig_md.pop('creators', []))
        self.convert_contributors(converted_md.setdefault("contributors", []), orig_md.pop('contributors', []))
        self.convert_abstract(converted_md.setdefault('descriptions', []), orig_md.pop('abstract', {}))
        self.convert_dates(converted_md.setdefault('dates', []), orig_md)
        self.convert_language(converted_md, orig_md.pop('language', None))
        self.convert_resource_types(converted_md, orig_md.pop('resourceType', None))
        self.convert_rights(converted_md.setdefault('rightsList', []), orig_md.pop('rights', []))
        self.convert_subject_categories(converted_md.setdefault('subjects', []), orig_md.pop('subjectCategories', []))
        self.convert_keywords(converted_md.setdefault('subjects', []), orig_md.pop('keywords', []))
        self.convert_titles(converted_md.setdefault('titles', []), orig_md.pop('titles'))
        self.convert_related_items(converted_md.setdefault("relatedItems", []), orig_md.pop('relatedItems', []))

        converted_md["publisher"] = {
            "name": "data.narodni-repozitar.cz"
        }

        # Ensure no unhandled keys remain
        self.ensure_empty(orig_md, '$schema', 'InvenioID', '_files', 'accessRights',
                          'oarepo:primaryCommunity', 'oarepo:recordStatus')
        
        return {
            "files": {"enabled": True},
            "metadata": converted_md
        }

    def convert_alternate_identifiers(self, alternateIdentifiers: List[Dict[str, str]], 
                                       orig_alternate_identifiers: List[Dict[str, str]], 
                                       link: str):
        for pi in orig_alternate_identifiers:
            if pi['scheme'] == 'doi':
                alternateIdentifiers.append({
                    "alternateIdentifier": f"https://doi.org/{pi.pop('identifier')}",
                    "alternateIdentifierType": "DOI"
                })
                self.ensure_empty(pi, 'scheme')
                break
        else:
            # Add a URL as a fallback
            alternateIdentifiers.append({
                "alternateIdentifier": link,
                "alternateIdentifierType": "URL"
            })

    def convert_creators(self, converted_creators: List[Dict[str, Any]], orig_creators: List[Dict[str, Any]]):
        for orig_creator in orig_creators:
            converted_creator = self.convert_person(orig_creator)
            self.ensure_empty(orig_creator)
            converted_creators.append(converted_creator)

    def convert_person(self, orig_creator: Dict[str, Any]) -> Dict[str, Any]:
        converted_creator = {
            "name": orig_creator.pop('fullName'),
            "nameType": orig_creator.pop('nameType')
        }
        self.convert_name_identifiers(orig_creator, converted_creator)
        self.convert_affiliations(orig_creator, converted_creator)
        return converted_creator

    def convert_affiliations(self, orig_creator: Dict[str, Any], converted_creator: Dict[str, Any]):
        affiliations = converted_creator['affiliation'] = []
        for aff in orig_creator.pop('affiliation', []):
            if aff.get('is_ancestor'):
                continue
            affiliation = {
                "name": aff.pop('fullName')
            }
            if 'relatedURI' in aff and 'ROR' in aff['relatedURI']:
                affiliation['affiliationIdentifier'] = aff['relatedURI'].pop('ROR')
                affiliation['affiliationIdentifierScheme'] = 'ROR'
            affiliations.append(affiliation)
            self.ensure_empty(aff, *vocabulary_system_fields)

    def convert_dates(self, dates: List[Dict[str, str]], orig_md: Dict[str, Any]):
        date_available = orig_md.pop('dateAvailable', None)
        if date_available:
            dates.append({
                "date": date_available,
                "dateType": "Issued"
            })
        date_created = orig_md.pop('dateCreated', None)
        if date_created and re.match(r'^\d\d\d\d-\d\d-\d\d$', date_created):
            dates.append({
                "date": date_created,
                "dateType": "Created"
            })

    def convert_abstract(self, converted_descriptions: List[Dict[str, str]], orig_abstract: Dict[str, str]):
        for lang, text in orig_abstract.items():
            description = {
                "description": text,
                "descriptionType": "Abstract",
                "lang": lang
            }
            converted_descriptions.append(description)

    def convert_language(self, converted_md: Dict[str, Any], orig_language: Any):
        if orig_language:
            converted_md['language'] = orig_language[0]['slug']

    def convert_resource_types(self, converted_md: Dict[str, Any], orig_resource_types: Any):
        types = converted_md['types'] = []
        if not orig_resource_types:
            types.append(self.convert_resource_type(None))
        else:
            for rt in orig_resource_types:
                if rt.get('is_ancestor'):
                    continue
                types.append(self.convert_resource_type(rt))

    def convert_resource_type(self, rt: Any) -> Dict[str, str]:
        if not rt:
            return {
                'resourceType': 'Dataset',
                'resourceTypeGeneral': 'Dataset'
            }
        return {
            'resourceType': rt.pop('coarType', 'Dataset'),
            'resourceTypeGeneral': 'Dataset'
        }

    def convert_rights(self, converted_rights: List[Dict[str, str]], orig_rights: List[Dict[str, str]]):
        for r in orig_rights:
            if r.get('is_ancestor'):
                continue
            base_attrs = {}
            if 'relatedURI' in r:
                base_attrs['rightsURI'] = r['relatedURI']['URL']
            converted_rights.append({
                **base_attrs,
                'rights': r['title']['cs'],
                'lang': 'cs'
            })
            converted_rights.append({
                **base_attrs,
                'rights': r['title']['en'],
                'lang': 'en'
            })

    def convert_subject_categories(self, converted_subjects: List[Dict[str, str]], orig_subjects: List[Dict[str, Any]]):
        for subject in orig_subjects:
            if subject.get('is_ancestor'):
                continue
            for lang, title in subject['title'].items():
                converted_subjects.append({
                    'subject': title,
                    'lang': lang
                })

    def convert_keywords(self, created_subjects: List[Dict[str, str]], orig_keywords: List[Dict[str, str]]):
        for keyword in orig_keywords:
            for lang, title in keyword.items():
                created_subjects.append({
                    'subject': title,
                    'lang': lang
                })

    def convert_titles(self, converted_titles: List[Dict[str, str]], orig_titles: List[Dict[str, Any]]):
        for title in orig_titles:
            for lang, text in title['title'].items():
                converted = {
                    'title': text,
                    'lang': lang
                }
                if title.get('titleType') == 'subtitle':
                    converted['titleType'] = 'Subtitle'
                elif title.get('titleType') != 'mainTitle':
                    raise Exception(f"Unknown title type: {title['titleType']}")
                converted_titles.append(converted)

    def convert_related_items(self, converted_related_items: List[Dict[str, Any]], orig_related_items: List[Dict[str, Any]]):
        for orig_related_item in orig_related_items:
            converted_item = {}
            self.convert_creators(converted_item.setdefault('creators', []), orig_related_item.pop('itemCreators', []))
            self.convert_contributors(converted_item.setdefault('contributors', []), orig_related_item.pop('itemContributors', []))
            self.convert_related_item_identifiers(
                converted_item.setdefault("relatedItemIdentifier", {}),
                orig_related_item.pop('itemPIDs', [])
            )
            item_resource_type = orig_related_item.pop('itemResourceType', [])
            converted_item['relatedItemType'] = self.convert_resource_type(item_resource_type[0] if item_resource_type else None)
            if 'itemTitle' in orig_related_item:
                converted_item['titles'] = [
                    {
                        'title': orig_related_item.pop('itemTitle')
                    }
                ]
            if 'itemYear' in orig_related_item:
                converted_item['publicationYear'] = orig_related_item.pop('itemYear')

            self.ensure_empty(orig_related_item, 'itemRelationType', 'itemURL')  # Not present in DataCite schema
            converted_related_items.append(converted_item)

    def convert_related_item_identifiers(self, converted_identifier: Dict[str, str], orig_identifiers: List[Dict[str, str]]):
        if len(orig_identifiers) > 1:
            raise Exception("Too many identifiers")
        if not orig_identifiers:
            return
        if orig_identifiers[0]['scheme'] != 'doi':
            raise Exception(f"Unknown identifier scheme {orig_identifiers[0]['scheme']}")
        converted_identifier['relatedItemIdentifier'] = f"https://doi.org/{orig_identifiers[0]['identifier']}"
        converted_identifier['relatedItemIdentifierType'] = 'DOI'

    def ensure_empty(self, data: Dict[str, Any], *exceptions):
        for key in data.keys():
            if key not in exceptions:
                raise Exception(f"Unhandled key: {key} inside data")

def main():
    input_file = "ours.json"
    
    # Load input data from JSON file
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    # Create transformer instance and convert data
    transformer = DataCiteTransformer()
    converted_data = transformer.convert(input_data)
    
    # Print the converted data
    print(converted_data)
    
    return converted_data

if __name__ == "__main__":
    main()

