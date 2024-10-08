from invenio_records_resources.services import FileLink, FileServiceConfig, RecordLink
from oarepo_runtime.services.components import CustomFieldsComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin

from datasets.records.api import DatasetsRecord
from datasets.services.files.schema import DatasetsFileSchema
from datasets.services.records.permissions import DatasetsPermissionPolicy


class DatasetsFileServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DatasetsRecord service config."""

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/datasets/<pid_value>"

    base_permission_policy_cls = DatasetsPermissionPolicy

    schema = DatasetsFileSchema

    record_cls = DatasetsRecord

    service_id = "datasets_file"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *FileServiceConfig.components,
        CustomFieldsComponent,
    ]

    model = "datasets"
    allowed_mimetypes = []
    allowed_extensions = []

    @property
    def file_links_list(self):
        return {
            "self": RecordLink("{+api}/datasets/{id}/files"),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink("{+api}/datasets/{id}/files/{key}/commit"),
            "content": FileLink("{+api}/datasets/{id}/files/{key}/content"),
            "preview": FileLink("{+ui}/datasets/{id}/files/{key}/preview"),
            "self": FileLink("{+api}/datasets/{id}/files/{key}"),
        }
