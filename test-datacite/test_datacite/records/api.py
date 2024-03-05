from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from test_datacite.records.dumpers.dumper import TestDataciteDumper
from test_datacite.records.models import TestDataciteMetadata


class TestDataciteIdProvider(RecordIdProviderV2):
    pid_type = "tsttct"


class TestDataciteRecord(InvenioRecord):

    model_cls = TestDataciteMetadata

    schema = ConstantField("$schema", "local://test_datacite-1.0.0.json")

    index = IndexField("test_datacite-test_datacite-1.0.0")

    pid = PIDField(
        provider=TestDataciteIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = TestDataciteDumper()
