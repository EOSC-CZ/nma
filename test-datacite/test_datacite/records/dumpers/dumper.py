from oarepo_runtime.records.dumpers import SearchDumper
from test_datacite.records.dumpers.edtf import TestDataciteEDTFIntervalDumperExt
from test_datacite.records.dumpers.multilingual import MultilingualSearchDumperExt


class TestDataciteDumper(SearchDumper):
    """TestDataciteRecord opensearch dumper."""

    extensions = [MultilingualSearchDumperExt(), TestDataciteEDTFIntervalDumperExt()]
