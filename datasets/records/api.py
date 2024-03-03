from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import FilesField, IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from datasets.files.api import DatasetsFile
from datasets.records.dumpers.dumper import DatasetsDumper
from datasets.records.models import DatasetsMetadata


class DatasetsIdProvider(RecordIdProviderV2):
    pid_type = "dtsts"


class DatasetsRecord(InvenioRecord):

    model_cls = DatasetsMetadata

    schema = ConstantField("$schema", "local://datasets-1.0.0.json")

    index = IndexField("datasets-datasets-1.0.0")

    pid = PIDField(
        provider=DatasetsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = DatasetsDumper()

    files = FilesField(file_cls=DatasetsFile, store=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


DatasetsFile.record_cls = DatasetsRecord
