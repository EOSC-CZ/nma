import importlib_metadata
from flask_resources import ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig

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

    @property
    def error_handlers(self):
        entrypoint_error_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.datasets_record.error_handlers"
        ):
            entrypoint_error_handlers.update(x.load())
        return {**super().error_handlers, **entrypoint_error_handlers}

    @property
    def request_body_parsers(self):
        entrypoint_request_bodyparsers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.datasets_record.request_bodyparsers"
        ):
            entrypoint_request_bodyparsers.update(x.load())
        return {
            **super().request_body_parsers,
            **entrypoint_request_bodyparsers,
        }
