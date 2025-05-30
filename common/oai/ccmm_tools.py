import time
from collections import defaultdict
from typing import Any

import pycountry
from invenio_access.permissions import system_identity
from invenio_search.engine import dsl
from invenio_vocabularies.proxies import current_service as vocabulary_service
from langcodes import Language


class VocabularyCache:
    def __init__(self, vocabulary_type: str):
        self.vocabulary_type = vocabulary_type
        self.caches: dict[str, Any] = {}

    @property
    def values(self):
        if not self.caches:
            print(f"Fetching {self.vocabulary_type} from the vocabulary service")
            t1 = time.time()
            self.caches["values"] = list(
                vocabulary_service.scan(
                    system_identity,
                    fields=["id", "props"],
                    extra_filter=dsl.Q("term", type__id=self.vocabulary_type),
                )
            )
            t2 = time.time()
            print(
                f"Fetched {len(self.caches['values'])} values in {t2 - t1:.2f} seconds"
            )
        return self.caches["values"]

    def clear(self):
        self.caches = {}

    def by_prop(self, prop: str):
        if prop in self.caches:
            return self.caches[prop]

        by_prop = {}
        for val in self.values:
            if prop in val["props"]:
                by_prop[val["props"][prop]] = val
        self.caches[prop] = by_prop
        return by_prop

    def by_id(self):
        if "id" in self.caches:
            return self.caches["id"]

        by_id = {}
        for val in self.values:
            by_id[val["id"]] = val

        self.caches["id"] = by_id
        return by_id


language_cache = VocabularyCache("languages")
agent_roles = VocabularyCache("agent-roles")


def get_ccmm_lang_iri(lang: str, refetch_ok=True) -> str:
    # if the lang is 2-letter, convert it to 3-letter
    if len(lang) == 2:
        lang = Language(language=lang).to_alpha3()
    by_3 = language_cache.by_prop("ISO_639_3")
    if lang in by_3:
        return by_3[lang]["props"]["iri"]
    by_2b = language_cache.by_prop("ISO_639_2B")
    if lang in by_2b:
        return by_2b[lang]["props"]["iri"]
    by_2t = language_cache.by_prop("ISO_639_2T")
    if lang in by_2t:
        return by_2t[lang]["props"]["iri"]
    if refetch_ok:
        # if not found, try to refetch the cache
        print(f"Language '{lang}' not found, refetching...")
        language_cache.clear()
        return get_ccmm_lang_iri(lang, refetch_ok=False)

    return language_cache.by_id()["UND"]["props"]["iri"]  # default to und


def get_ccmm_role(role: str, refetch=True) -> str:
    contributor_types_by_prop = agent_roles.by_prop("dataCiteCode")
    if role not in contributor_types_by_prop:
        if refetch:
            print(f"Role '{role}' not found, refetching...")
            agent_roles.clear()
            return get_ccmm_role(role, refetch=False)
    if role not in contributor_types_by_prop:
        raise ValueError(f"Role '{role}' not found in contributor types vocabulary")
    return contributor_types_by_prop[role]["props"]["iri"]


def full_name_to_person(value):
    """Convert a full name string to a person dict."""
    value = value.split(", ", maxsplit=1)
    if len(value) > 1:
        family_names = value[0].split()
        given_names = value[1].split()
    else:
        family_names = value[0].split()
        given_names = []

    person = {
        "family_names": [x for x in family_names if x],
    }
    if given_names:
        person["given_names"] = [x for x in given_names if x]

    return person


def file_formats_by_extension():
    alternatives = defaultdict(list)
    for rec in vocabulary_service.scan(
        system_identity,
        fields=["id", "props"],
        extra_filter=dsl.Q("term", type__id="file-types"),
    ):
        iri = rec["props"]["iri"]

        file_ext = None
        iana_mediatype = None
        file_ext = rec["props"].get("FILE_EXT")
        if not file_ext:
            continue

        iana_mediatype = rec["props"].get("IANA_MT")
        if not iana_mediatype:
            continue

        alternatives[file_ext].append((iri, iana_mediatype))

    ret = {}
    for file_ext, values in alternatives.items():
        if len(values) == 1:
            ret[file_ext] = values[0]
            continue

        # multiple values for the same file extension. Take the one that matches
        # the file extension in the IRI if there is one. If not, take the shortest iri
        # (in terms of the number of characters)
        shortest = None
        for iri, iana_mediatype in values:
            if iri.endswith(f"/{file_ext[1:].upper()}"):
                ret[file_ext] = (iri, iana_mediatype)
                break
            if not shortest:
                shortest = (iri, iana_mediatype)
            elif len(iri) < len(shortest[0]):
                shortest = (iri, iana_mediatype)
        else:
            # if no match found, take the shortest iri
            # with the same file extension
            ret[file_ext] = shortest

    return ret


def file_formats_by_iana():
    ret = {}
    for rec in vocabulary_service.scan(
        system_identity,
        fields=["id", "props"],
        extra_filter=dsl.Q("term", type__id="file-types"),
    ):
        iri = rec["props"]["iri"]

        file_ext = None
        iana_mediatype = None
        file_ext = rec["props"].get("FILE_EXT")
        if not file_ext:
            continue

        iana_mediatype = rec["props"].get("IANA_MT")
        if not iana_mediatype:
            continue

        iana_mediatype = iana_mediatype.lower()
        if iana_mediatype in ret:
            if len(ret[iana_mediatype]) < len(iri):
                continue
        ret[iana_mediatype] = iri

    return ret


def lang_dict_to_2(_lang):
    if isinstance(_lang, dict):
        _lang = _lang.get("id", "und")
    if len(_lang) == 3:
        # convert from 3 to 2 letter code
        try:
            _lang = pycountry.languages.get(alpha_3=_lang).alpha_2
        except AttributeError:
            # no alpha 2 code found, return the original value
            return _lang
    return _lang
