import marshmallow as ma
from marshmallow import fields as ma_fields
from nr_metadata.datacite.services.records.ui_schema import (
    DataCiteRecordUISchema,
    NRDataCiteMetadataUISchema,
)


class DatasetsUISchema(DataCiteRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDataCiteMetadataUISchema())
