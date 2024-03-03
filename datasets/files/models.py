from invenio_db import db
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records import FileRecordModelMixin

from datasets.records.models import DatasetsMetadata


class DatasetsFileMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for DatasetsFile metadata."""

    __tablename__ = "datasets_file_metadata"
    __record_model_cls__ = DatasetsMetadata
