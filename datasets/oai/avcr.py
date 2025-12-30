from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.transformers import BaseTransformer


class IdFromDOITransformer(BaseTransformer):
    def __init__(self, *args, **kwargs):
        pass

    def apply(self, stream_entry: StreamEntry, *args, **kwargs):
        """Adds an 'id' field to the entry if not present."""
        entry = stream_entry.entry
        rec = entry.get("record", {})
        if not rec:
            return stream_entry

        for identifier in rec.get("metadata", {}).get("identifiers", []):
            if identifier.get("scheme") == "doi":
                rec["id"] = "doi/" + identifier.get("identifier")
                return stream_entry

        # otherwise just suppose that it will be this one
        stream_entry.filtered = True
        stream_entry.errors.append("Missing DOI identifier for record.")
        return stream_entry
