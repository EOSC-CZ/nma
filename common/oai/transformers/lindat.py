from oarepo_runtime.datastreams import (
    BaseReader,
    BaseTransformer,
    StreamBatch,
    StreamEntry,
)
from oarepo_runtime.datastreams.readers.json import JSONReader
from oarepo_runtime.datastreams.types import StreamEntryError

from oarepo_oaipmh_harvester.transformers.rule import (
    OAIRuleTransformer,
    matches,
    deduplicate,
    ignore,
    make_dict,
    make_array,
)

class LinDatTransformer(OAIRuleTransformer):
    def transform(self, entry: StreamEntry):
        metadata = entry.context["oai"]["metadata"]
        md = entry.transformed.setdefault("metadata", {})
        entry.entry = metadata
        transform_title(md, entry)
        print(md)

@matches("title")
def transform_title(md, entry, value):
    md.setdefault("title", value)