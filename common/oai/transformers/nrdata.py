import re
from typing import Union
from oarepo_runtime.datastreams import BaseTransformer, StreamEntry, StreamBatch

from oarepo_runtime.datastreams.types import StreamEntryError

class NRDataTransformer(BaseTransformer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def transform_entry(self, entry: StreamEntry):
        """
        Transforms the entry.
        """
        entry.entry = convert_record_to_datacite({**entry.entry})


def convert_record_to_datacite(rec):
    links = rec.pop('links')
    link = links['self']

    id = rec['id']
    orig_md = rec['metadata']

    converted_md = {
        "url": link
    }
    converted = {
        "files": {"enabled": True},
        "metadata": converted_md
    }

    converted['$schema'] = 'local://datasets-1.0.0.json'
    convert_alternate_identifiers(converted_md.setdefault("alternateIdentifiers", []),
                                  orig_md.pop('persistentIdentifiers', []),
                                  link)
    convert_creators(converted_md.setdefault("creators", []), orig_md.pop('creators', []))
    convert_contributors(converted_md.setdefault("contributors", []), orig_md.pop('contributors', []))
    convert_abstract(converted_md.setdefault('descriptions', []), orig_md.pop('abstract', {}))
    convert_dates(converted_md.setdefault('dates', []), orig_md)
    convert_language(converted_md, orig_md.pop('language', None))
    convert_resource_types(converted_md, orig_md.pop('resourceType', None))
    convert_rights(converted_md.setdefault('rightsList', []), orig_md.pop('rights', []))
    convert_subject_categories(converted_md.setdefault('subjects', []), orig_md.pop('subjectCategories', []))
    convert_keywords(converted_md.setdefault('subjects', []), orig_md.pop('keywords', []))
    convert_titles(converted_md.setdefault('titles', []), orig_md.pop('titles'))
    convert_related_items(converted_md.setdefault("relatedItems", []), orig_md.pop('relatedItems', []))

    converted_md["publisher"] = {
        "name": "data.narodni-repozitar.cz"
    }

    ensureEmpty(orig_md, '$schema', 'InvenioID', '_files', 'accessRights',
                'oarepo:primaryCommunity', 'oarepo:recordStatus')
    return converted


vocabulary_system_fields = [
    "busy_count",
    'descendants_busy_count',
    'descendants_count',
    "label",
    "level",
    "links",
    "self",
    "slug",
    "status",
    "selectable",
    "ancestors"
]

def ensureEmpty(data, *exceptions, filter=True):
    for key in data.keys():
        if key not in exceptions:
            if filter:
                filtered_data = {k: v for k, v in data.items() if k not in exceptions}
            else:
                filtered_data = data
            raise Exception(f"Unhandled key: {key} inside data")


def convert_alternate_identifiers(alternateIdentifiers, orig_alternate_identifiers, link):
    """
          "alternateIdentifiers": [
            {"alternateIdentifier": "http://hdl.handle.net/11234/1-5423", "alternateIdentifierType": "Handle"}
      ],
    """

    for pi in orig_alternate_identifiers:
        if pi['scheme'] == 'doi':
            alternateIdentifiers.append({
                "alternateIdentifier": f"https://doi.org/{pi.pop('identifier')}",
                "alternateIdentifierType": "DOI"
            })
            ensureEmpty(pi, 'scheme')
            break
        else:
            raise Exception(f"Unknown persistent identifier scheme: {pi['scheme']}")
    else:
        # add a url as a fallback
        alternateIdentifiers.append({
            "alternateIdentifier": link,
            "alternateIdentifierType": "URL"
        })


def convert_affiliations(orig_creator, converted_creator):
    affiliations = converted_creator['affiliation'] = []
    for aff in orig_creator.pop('affiliation', []):
        if aff.get('is_ancestor'):
            continue
        related_uri = aff.pop('relatedURI', {})
        affiliation = {
            "name": aff.pop('fullName')
        }
        if 'ROR' in related_uri:
            affiliation['affiliationIdentifier'] = related_uri.pop('ROR')
            affiliation['affiliationIdentifierScheme'] = 'ROR'
        affiliations.append(affiliation)
        ensureEmpty(aff,
                    *vocabulary_system_fields,
                    "aliases",
                    "data",
                    "relatedRID",
                    "ico",
                    "institutionCategory",
                    "nameTranslated",
                    "nameType",
                    "title",
        )

def convert_creators(converted_creators, orig_creators):
    for orig_creator in orig_creators:
        converted_creator = convert_person(orig_creator)
        ensureEmpty(orig_creator)
        converted_creators.append(converted_creator)


def convert_person(orig_creator):
    converted_creator = {
        "name": orig_creator.pop('fullName'),
        "nameType": orig_creator.pop('nameType')
    }
    convert_name_identifiers(orig_creator, converted_creator)
    convert_affiliations(orig_creator, converted_creator)
    return converted_creator


def convert_contributors(converted_contributors, orig_contributors):
    for orig_contributor in orig_contributors:
        converted_contributor = convert_person(orig_contributor)
        role = orig_contributor.pop('role', None)
        contributorType = 'Other'
        if role:
            for rr in role:
                if rr.get('is_ancestor'):
                    continue
                contributorType = rr['dataCiteCode']
                break
        converted_contributor['contributorType'] = contributorType
        converted_contributors.append(converted_contributor)
        ensureEmpty(orig_contributor)

def convert_name_identifiers(orig_creator, converted_creator):
    nameIdentifiers = converted_creator['nameIdentifiers'] = []
    for ni in orig_creator.pop('authorityIdentifiers', []):
        scheme = ni['scheme']
        if scheme == 'orcid':
            identifier = ni.pop('identifier')
            nameIdentifiers.append({
                "nameIdentifier": identifier,
                "nameIdentifierScheme": "ORCID"
            })
        elif scheme == 'scopusID':
            identifier = ni.pop('identifier')
            nameIdentifiers.append({
                "nameIdentifier": identifier,
                "nameIdentifierScheme": "ScopusID"
            })
        elif scheme == 'researcherID':
            identifier = ni.pop('identifier')
            nameIdentifiers.append({
                "nameIdentifier": identifier,
                "nameIdentifierScheme": "ResearcherID"
            })
        ensureEmpty(ni, 'scheme', filter=False)


def convert_abstract(converted_descriptions, orig_abstract):
    for lang, text in orig_abstract.items():
        description = {
            "description": text,
            "descriptionType": "Abstract",
            "lang": lang
        }
        converted_descriptions.append(description)


def convert_dates(dates, orig_md):
    dateAvailable = orig_md.pop('dateAvailable', None)
    if dateAvailable:
        dates.append({
            "date": dateAvailable,
            "dateType": "Issued"
        })
    dateCreated = orig_md.pop('dateCreated', None)
    if dateCreated and re.match(r'^\d\d\d\d-\d\d-\d\d$', dateCreated):
        dates.append({
            "date": dateCreated,
            "dateType": "Created"
        })


def convert_language(converted_md, orig_language):
    if orig_language:
        converted_md['language'] = orig_language[0]['slug']


def convert_resource_types(converted_md, orig_resource_types):
    types = converted_md['types'] = []
    if not orig_resource_types:
        types.append(convert_resource_type(None))
    else:
        for rt in orig_resource_types:
            if rt.get('is_ancestor'):
                continue
            types.append(convert_resource_type(rt))


def convert_resource_type(rt):
    if not rt:
        return {
            'resourceType': 'Dataset',
            'resourceTypeGeneral': 'Dataset'
        }
    return {
        'resourceType': rt.pop('coarType', 'Dataset'),
        'resourceTypeGeneral': 'Dataset'
    }

def convert_rights(converted_rights, orig_rights):
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


def convert_subject_categories(converted_subjects, orig_subjects):
    for subject in orig_subjects:
        if subject.get('is_ancestor'):
            continue
        for lang, title in subject['title'].items():
            converted_subjects.append({
                'subject': title,
                'lang': lang
            })

def convert_keywords(created_subjects, orig_keywords):
    for keyword in orig_keywords:
        for lang, title in keyword.items():
            created_subjects.append({
                'subject': title,
                'lang': lang
            })

def convert_titles(converted_titles, orig_titles):
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


def convert_related_item_identifiers(converted_identifier, orig_identifiers):
    if len(orig_identifiers)>1:
        raise Exception("Too many identifiers")
    if not orig_identifiers:
        return
    if orig_identifiers[0]['scheme'] != 'doi':
        raise Exception(f"Unknown identifier scheme {orig_identifiers[0]['scheme']}")
    converted_identifier['relatedItemIdentifier'] = f"https://doi.org/{orig_identifiers[0]['identifier']}"
    converted_identifier['relatedItemIdentifierType'] = 'DOI'

def convert_related_items(converted_related_items, orig_related_items):
    for orig_related_item in orig_related_items:
        converted_item = {}
        convert_creators(converted_item.setdefault('creators', []), orig_related_item.pop('itemCreators', []))
        convert_contributors(converted_item.setdefault('contributors', []), orig_related_item.pop('itemContributors', []))
        convert_related_item_identifiers(
            converted_item.setdefault("relatedItemIdentifier", {}),
            orig_related_item.pop('itemPIDs', [])
        )
        item_resource_type = orig_related_item.pop('itemResourceType', [])
        converted_item['relatedItemType'] = convert_resource_type(item_resource_type[0] if item_resource_type else None)
        if 'itemTitle' in orig_related_item:
            converted_item['titles'] = [
                {
                    'title': orig_related_item.pop('itemTitle')
                }
            ]
        if 'itemYear' in orig_related_item:
            converted_item['publicationYear'] = orig_related_item.pop('itemYear')

        ensureEmpty(orig_related_item, 'itemRelationType', 'itemURL') # not present in datacite schema
