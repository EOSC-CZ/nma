import marshmallow as ma
from marshmallow import fields as ma_fields
from nr_metadata.datacite.services.records.ui_schema import (
    DataCiteRecordUISchema,
    NRDataCiteMetadataUISchema,
)
from oarepo_runtime.services.schema.marshmallow import DictOnlySchema


class DatasetsUISchema(DataCiteRecordUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDataCiteMetadataUISchema())

    oai = ma_fields.Nested(lambda: OaiUISchema())


class OaiUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    harvest = ma_fields.Nested(lambda: HarvestUISchema())


class HarvestUISchema(DictOnlySchema):
    class Meta:
        unknown = ma.RAISE

    datestamp = ma_fields.String()

    identifier = ma_fields.String()
