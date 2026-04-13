from datasets import schema_openaire
from flask_resources import BaseListSchema, MarshmallowSerializer
from flask_resources.serializers import SimpleSerializer
from invenio_rdm_records.contrib.journal.processors import JournalDataciteDumper
from invenio_rdm_records.resources.serializers.datacite.schema import (
    DataCite43Schema,
)

class OpenAIREXMLSerializer(MarshmallowSerializer):
    """JSON based DataCite XML serializer for records."""

    def __init__(self, **options):
        """Constructor."""
        encoder = options.get("encoder", schema_openaire.tostring)
        super().__init__(
            format_serializer_cls=SimpleSerializer,
            object_schema_cls=DataCite43Schema,
            list_schema_cls=BaseListSchema,
            schema_kwargs={"dumpers": [JournalDataciteDumper()]},  # Order matters
            encoder=encoder,
        )


    def dump_obj(self, obj):
        data = super().dump_obj(obj)
        metadata = self._get_metadata(obj)
        persistent_url = metadata.get("persistent_url")
        data["id"] = obj["id"]
        data["pid"] = obj["id"]

        primary_identifier = obj["id"]

        identifier = ""
        identifier_type = ""
        result = None

        if "doi/" in primary_identifier:
            identifier = primary_identifier.split("doi/")[1]
            identifier_type = "DOI"
        elif "handle/" in primary_identifier:
            identifier = primary_identifier.split("handle/")[1]
            identifier_type = "Handle"
        else: # oai is not supported type
            identifier = primary_identifier
            identifier_type = "URL"

        if result is None:
            result = {
                "identifier": identifier,
                "identifierType": identifier_type
            }

        link_to_original = {
            "relatedIdentifier": persistent_url,
            "relatedIdentifierType": result["identifierType"],
            "relationType": "References",
        }

        if "identifiers" not in data:
            data["identifiers"] = [result]
        else:
            data["identifiers"].insert(0, result)

        if "relatedIdentifiers" not in data:
            data["relatedIdentifiers"] = [link_to_original]
        else:
            data["relatedIdentifiers"].append(link_to_original)

        data["publicationYear"] = str(data["publicationYear"])[:4]


        return data

    def _get_metadata(self, obj):
        if isinstance(obj, dict):
            return obj.get("metadata", {}) or {}
        getter = getattr(obj, "get", None)
        if callable(getter):
            return getter("metadata", {}) or {}
        return getattr(obj, "metadata", {}) or {}
