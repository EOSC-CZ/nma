from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.files import FilesComponent

from datasets.records.api import DatasetsRecord
from datasets.services.records.permissions import DatasetsPermissionPolicy
from datasets.services.records.results import DatasetsRecordItem, DatasetsRecordList
from datasets.services.records.schema import DatasetsSchema
from datasets.services.records.search import DatasetsSearchOptions


class DatasetsServiceConfig(PermissionsPresetsConfigMixin, InvenioRecordServiceConfig):
    """DatasetsRecord service config."""

    result_item_cls = DatasetsRecordItem

    result_list_cls = DatasetsRecordList

    PERMISSIONS_PRESETS = ["read_only"]

    url_prefix = "/datasets/"

    base_permission_policy_cls = DatasetsPermissionPolicy

    schema = DatasetsSchema

    search = DatasetsSearchOptions

    record_cls = DatasetsRecord

    service_id = "datasets"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        DataComponent,
        FilesComponent,
    ]

    model = "datasets"

    @property
    def links_item(self):
        return {
            "files": RecordLink("{+api}/datasets/{id}/files"),
            "self": RecordLink("{+api}/datasets/{id}"),
            "self_html": RecordLink("{+ui}/datasets/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/datasets/{?args*}"),
        }
