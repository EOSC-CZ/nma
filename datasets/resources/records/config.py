import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from datasets.resources.records.ui import DatasetsUIJSONSerializer


class DatasetsResourceConfig(RecordResourceConfig):
    """DatasetsRecord resource config."""

    blueprint_name = "datasets"
    url_prefix = "/datasets/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.datasets.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DatasetsUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
