from oarepo_runtime.records.dumpers import SearchDumper

from datasets.records.dumpers.edtf import DatasetsEDTFIntervalDumperExt
from datasets.records.dumpers.multilingual import MultilingualSearchDumperExt


class DatasetsDumper(SearchDumper):
    """DatasetsRecord opensearch dumper."""

    extensions = [DatasetsEDTFIntervalDumperExt(), MultilingualSearchDumperExt()]
