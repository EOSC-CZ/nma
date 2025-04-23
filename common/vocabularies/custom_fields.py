import marshmallow as ma
from invenio_records_resources.services.custom_fields import BaseCF
from invenio_vocabularies.services.schema import i18n_strings


class RelatedURICF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""

        return ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Str())


class NonPreferredLabelsCF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""
        return ma.fields.List(i18n_strings)


class HintCF(BaseCF):
    @property
    def mapping(self):
        """Return the mapping."""
        return {"type": "object", "dynamic": True}

    @property
    def field(self):
        """Marshmallow field for custom fields."""
        return i18n_strings
