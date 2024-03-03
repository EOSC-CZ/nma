from invenio_records_resources.records.api import FileRecord
from invenio_records_resources.records.systemfields import IndexField

from datasets.files.models import DatasetsFileMetadata


class DatasetsFile(FileRecord):

    model_cls = DatasetsFileMetadata

    index = IndexField("datasets_file-datasets_file-1.0.0")
    record_cls = None  # is defined inside the parent record
