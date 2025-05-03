import time
from typing import Any

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


language_cache = VocabularyCache("languages")
contributor_types = VocabularyCache("contributor-types")


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

    return by_3["und"]["props"]["iri"]  # default to und


def get_ccmm_role(role: str, refetch=True) -> str:
    contributor_types_by_prop = contributor_types.by_prop("dataCiteCode")
    if role not in contributor_types_by_prop:
        if refetch:
            print(f"Role '{role}' not found, refetching...")
            contributor_types.clear()
            return get_ccmm_role(role, refetch=False)
    if role not in contributor_types_by_prop:
        raise ValueError(f"Role '{role}' not found in contributor types vocabulary")
    return contributor_types_by_prop[role]["props"]["iri"]


def full_name_to_person(value):
    """Convert a full name string to a person dict."""
    value = value.split(", ")
    if len(value) > 1:
        family_name = value[0]
        given_names = value[1:]
    else:
        family_name = value[0]
        given_names = []

    person = {
        "family_name": family_name,
    }
    if given_names:
        person["given_names"] = given_names

    return person
