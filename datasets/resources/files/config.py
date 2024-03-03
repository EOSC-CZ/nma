import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import FileResourceConfig

from datasets.resources.files.ui import DatasetsFileUIJSONSerializer


class DatasetsFileResourceConfig(FileResourceConfig):
    """DatasetsFile resource config."""

    blueprint_name = "datasets_file"
    url_prefix = "/datasets/<pid_value>"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.datasets.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                DatasetsFileUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
