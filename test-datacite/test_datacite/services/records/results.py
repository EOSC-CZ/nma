from oarepo_runtime.services.results import RecordItem, RecordList


class TestDataciteRecordItem(RecordItem):
    """TestDataciteRecord record item."""

    components = [*RecordItem.components]


class TestDataciteRecordList(RecordList):
    """TestDataciteRecord record list."""

    components = [*RecordList.components]
