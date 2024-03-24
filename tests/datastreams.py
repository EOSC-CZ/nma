import contextlib
from urllib.parse import unquote, urlparse
from langdetect import detect
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


class MockOAIReader(JSONReader):
    def __init__(
        self,
        *,
        all_records=None,
        identifiers=None,
        config=None,
        source=None,
        start_from=None,
        base_path=None,
        oai_run=None,
        oai_harvester_id=None,
        manual=False,
        **kwargs,
    ):
        super().__init__(source=source, base_path=base_path)
        self.all_records = all_records
        self.identifiers = identifiers
        self.config = config
        self.source = source
        self.start_from = start_from
        self.base_path = base_path
        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    @contextlib.contextmanager
    def _open(self, mode="r"):
        source = unquote(urlparse(self.source).path)
        with open(source, mode) as f:
            yield f

    def __iter__(self):
        for x in super().__iter__():
            x.context["oai"] = x.entry["oai"]
            x.context["oai_harvester_id"] = self.oai_harvester_id
            x.context["manual"] = self.manual
            x.context["oai_run_id"] = self.oai_run
            x.entry = x.entry["entry"]
            x.deleted = x.context["oai"].get("deleted", False)
            yield x


class TestDataOAIReader(BaseReader):
    def __init__(
        self,
        *,
        all_records=None,
        identifiers=None,
        config=None,
        source=None,
        start_from=None,
        base_path=None,
        oai_run=None,
        oai_harvester_id=None,
        manual=False,
        count=None,
        **kwargs,
    ):
        super().__init__(source=source, base_path=base_path)
        self.all_records = all_records
        self.identifiers = identifiers
        self.config = config
        self.source = source
        self.start_from = start_from
        self.base_path = base_path
        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual
        self.count = count

    @contextlib.contextmanager
    def _open(self, mode="r"):
        """Nothing to do in here"""

    def __iter__(self):
        for idx in range(self.count):
            x = StreamEntry({"metadata": {"title": f"{idx}"}})
            x.context["oai"] = {
                "identifier": f"{idx}",
                "datestamp": "2000-01-03",
                "deleted": False,
            }
            x.context["oai_harvester_id"] = self.oai_harvester_id
            x.context["manual"] = self.manual
            x.context["oai_run_id"] = self.oai_run
            yield x


class ErrorTransformer(BaseTransformer):
    def apply(self, stream_batch: StreamBatch, *args, **kwargs) -> StreamBatch:
        for entry in stream_batch.entries:
            if "transformer" in entry.entry:
                entry.errors.append(
                    StreamEntryError(
                        message="Error in transformer",
                        location="transformer",
                        code="TE",
                        info={
                            "transformer-specific-message": entry.entry["transformer"]
                        },
                    )
                )
        return stream_batch
