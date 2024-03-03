from oarepo_runtime.services.results import RecordItem, RecordList


class DatasetsRecordItem(RecordItem):
    """DatasetsRecord record item."""

    components = [*RecordItem.components]


class DatasetsRecordList(RecordList):
    """DatasetsRecord record list."""

    components = [*RecordList.components]
