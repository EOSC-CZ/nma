import marshmallow as ma
from oarepo_vocabularies.services.ui_schema import VocabularyI18nStrUIField


class CCMMVocabularyUISchema(ma.Schema):
    _id = ma.fields.Str(attribute="id", data_key="id", required=True)
    _version = ma.fields.Str(data_key="@v", attribute="@v")
    title = VocabularyI18nStrUIField()
    iri = ma.fields.Str(dump_only=True)
