import functools

import marshmallow as ma
from invenio_access.permissions import system_identity
from invenio_i18n import gettext as _
from invenio_vocabularies.proxies import current_service as vocabularies_service
from invenio_vocabularies.services.schema import i18n_strings

opensearch_illegal_characters = {
    "+",
    "-",
    "=",
    "&",
    "|",
    ">",
    "<",
    "!",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "^",
    '"',
    "~",
    "*",
    "?",
    ":",
    "\\",
    "/",
}


def escape_illegal_characters(query):
    """
    Escape illegal characters in the query string for OpenSearch.
    """
    return f'"{query}"'
    ret = []
    for char in query:
        if char in opensearch_illegal_characters:
            ret.append(f"\\{char}")
        else:
            ret.append(char)
    return "".join(ret)


@functools.lru_cache(maxsize=10000)
def iri_to_id(iri: str, vocabulary_type: str) -> str:
    """
    Convert an IRI to an ID for a given vocabulary type.
    """
    try:
        assert vocabulary_type, "Vocabulary type is not set."
        resp = vocabularies_service.search(
            system_identity,
            params=dict(q="props.iri.keyword:" + escape_illegal_characters(iri)),
            type=vocabulary_type,
        )
        hit = next(resp.hits)
        if hit.get("props", {}).get("iri") != iri:
            raise ma.ValidationError(
                _(
                    "Vocabulary with IRI '{iri}' not found in vocabulary {vocab}."
                ).format(iri=iri, vocab=vocabulary_type)
            )
        return hit["id"]
    except:
        raise ma.ValidationError(
            _("Vocabulary with IRI '{iri}' not found in vocabulary {vocab}.").format(
                iri=iri, vocab=vocabulary_type
            )
        )


class CCMMVocabularySchema(ma.Schema):
    vocabulary_type: str = ""

    _id = ma.fields.Str(attribute="id", data_key="id", required=True)
    _version = ma.fields.Str(data_key="@v", attribute="@v")
    title = i18n_strings
    iri = ma.fields.Str(dump_only=True)

    @ma.pre_load
    def load_from_iri(self, data, **kwargs):
        if not data:
            return data
        if not isinstance(data, dict):
            raise ma.ValidationError(
                _("Invalid data format for dictionary. Expected an object.")
            )
        if "iri" in data:
            data["id"] = iri_to_id(data.pop("iri"), self.vocabulary_type)

        return data


class CCMMLanguagesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "languages"


class CCMMResourceTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "resource-types"


class CCMMAgentTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "agent-roles"


class CCMMRelationTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "relation-types"


class CCMMTimeReferenceTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "time-reference-types"


class CCMMAccessRightsVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "access-rights"


class CCMMFileTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "file-types"


class CCMMSubjectSchemesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "subject-schemes"


class CCMMTitleTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "title-types"


class CCMMChecksumAlgorithmsVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "checksum-algorithms"


class CCMMIdentifierSchemesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "identifier-schemes"


class CCMMLocationRelationTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "location-relation-types"


class CCMMMediaTypesVocabularySchema(CCMMVocabularySchema):
    vocabulary_type = "media-types"
