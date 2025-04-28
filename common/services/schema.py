import marshmallow as ma
from invenio_i18n import gettext as _
from invenio_vocabularies.services.schema import i18n_strings


class CCMMVocabularySchema(ma.Schema):
    _id = ma.fields.Str(attribute="id", data_key="id", required=True)
    _version = ma.fields.Str(data_key="@v", attribute="@v")
    title = i18n_strings

    @ma.pre_load
    def load_from_iri(self, data):
        if not data:
            return data
        if not isinstance(data, dict):
            raise ma.ValidationError(
                _("Invalid data format for dictionary. Expected an object.")
            )
        if "iri" not in data:
            return data

        iri = data.pop("iri")
        # crude implementation
        if "#" in iri:
            _id = iri.rsplit("#")[-1]
        else:
            _id = iri.strip("/").rsplit["/"][-1]
        data["id"] = _id
        return data
