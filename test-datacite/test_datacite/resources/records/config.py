import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig
from test_datacite.resources.records.ui import TestDataciteUIJSONSerializer


class TestDataciteResourceConfig(RecordResourceConfig):
    """TestDataciteRecord resource config."""

    blueprint_name = "test_datacite"
    url_prefix = "/test-datacite/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.test_datacite.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                TestDataciteUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
