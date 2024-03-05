from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from invenio_records_resources.services.records.components import DataComponent
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from test_datacite.records.api import TestDataciteRecord
from test_datacite.services.records.permissions import TestDatacitePermissionPolicy
from test_datacite.services.records.results import (
    TestDataciteRecordItem,
    TestDataciteRecordList,
)
from test_datacite.services.records.schema import DataCiteRecordSchema
from test_datacite.services.records.search import TestDataciteSearchOptions


class TestDataciteServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordServiceConfig
):
    """TestDataciteRecord service config."""

    result_item_cls = TestDataciteRecordItem

    result_list_cls = TestDataciteRecordList

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/test-datacite/"

    base_permission_policy_cls = TestDatacitePermissionPolicy

    schema = DataCiteRecordSchema

    search = TestDataciteSearchOptions

    record_cls = TestDataciteRecord

    service_id = "test_datacite"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
        DataComponent,
    ]

    model = "test_datacite"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{+api}/test-datacite/{id}"),
            "self_html": RecordLink("{+ui}/test-datacite/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/test-datacite/{?args*}"),
        }
