from invenio_records_resources.services import (
    FileLink,
    FileServiceConfig,
    LinksTemplate,
    RecordLink,
)
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import (
    has_file_permission,
    has_permission_file_service,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin

from datasets.records.api import DatasetsDraft, DatasetsRecord
from datasets.services.files.schema import DatasetsFileSchema
from datasets.services.records.permissions import DatasetsPermissionPolicy


class DatasetsFileServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DatasetsRecord service config."""

    PERMISSIONS_PRESETS = ["workflow"]

    url_prefix = "/datasets/<pid_value>"

    base_permission_policy_cls = DatasetsPermissionPolicy

    schema = DatasetsFileSchema

    record_cls = DatasetsRecord

    service_id = "datasets_file"

    search_item_links_template = LinksTemplate
    allowed_mimetypes = []
    allowed_extensions = []
    allow_upload = False

    @property
    def components(self):
        return process_service_configs(self, CustomFieldsComponent)

    model = "datasets"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink(
                "{+api}/datasets/{id}/files",
                when=has_permission_file_service("list_files"),
            ),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink(
                "{+api}/datasets/{id}/files/{key}/commit",
                when=has_permission_file_service("commit_files"),
            ),
            "content": FileLink(
                "{+api}/datasets/{id}/files/{key}/content",
                when=has_permission_file_service("get_content_files"),
            ),
            "preview": FileLink("{+ui}/datasets/{id}/files/{key}/preview"),
            "self": FileLink(
                "{+api}/datasets/{id}/files/{key}",
                when=has_permission_file_service("read_files"),
            ),
        }


class DatasetsFileDraftServiceConfig(PermissionsPresetsConfigMixin, FileServiceConfig):
    """DatasetsDraft service config."""

    PERMISSIONS_PRESETS = ["workflow"]

    url_prefix = "/datasets/<pid_value>/draft"

    schema = DatasetsFileSchema

    record_cls = DatasetsDraft

    service_id = "datasets_file_draft"

    search_item_links_template = LinksTemplate

    @property
    def components(self):
        return process_service_configs(self, CustomFieldsComponent)

    model = "datasets"

    @property
    def file_links_list(self):
        return {
            "self": RecordLink(
                "{+api}/datasets/{id}/draft/files",
                when=has_file_permission("list_files"),
            ),
        }

    @property
    def file_links_item(self):
        return {
            "commit": FileLink(
                "{+api}/datasets/{id}/draft/files/{key}/commit",
                when=has_file_permission("commit_files"),
            ),
            "content": FileLink(
                "{+api}/datasets/{id}/draft/files/{key}/content",
                when=has_file_permission("get_content_files"),
            ),
            "preview": FileLink("{+ui}/datasets/{id}/preview/files/{key}/preview"),
            "self": FileLink(
                "{+api}/datasets/{id}/draft/files/{key}",
                when=has_file_permission("read_files"),
            ),
        }
