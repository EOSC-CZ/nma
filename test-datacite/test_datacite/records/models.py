from invenio_db import db
from invenio_records.models import RecordMetadataBase


class TestDataciteMetadata(db.Model, RecordMetadataBase):
    """Model for TestDataciteRecord metadata."""

    __tablename__ = "test_datacite_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
