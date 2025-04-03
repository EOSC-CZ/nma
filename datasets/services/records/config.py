from invenio_rdm_records.services.config import RDMRecordServiceConfig
from invenio_records_resources.services import (
    ConditionalLink,
    LinksTemplate,
    RecordLink,
    pagination_links,
)
from oarepo_communities.services.components.default_workflow import (
    CommunityDefaultWorkflowComponent,
)
from oarepo_communities.services.components.include import CommunityInclusionComponent
from oarepo_communities.services.links import CommunitiesLinks
from oarepo_runtime.services.components import (
    CustomFieldsComponent,
    process_service_configs,
)
from oarepo_runtime.services.config import (
    has_draft,
    has_file_permission,
    has_permission,
    has_published_record,
    is_published_record,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin
from oarepo_runtime.services.records import pagination_links_html
from oarepo_workflows.services.components.workflow import WorkflowComponent

from datasets.records.api import DatasetsDraft, DatasetsRecord
from datasets.services.records.permissions import DatasetsPermissionPolicy
from datasets.services.records.results import DatasetsRecordItem, DatasetsRecordList
from datasets.services.records.schema import DatasetsSchema
from datasets.services.records.search import (
    DatasetsDraftSearchOptions,
    DatasetsSearchOptions,
)


class DatasetsServiceConfig(PermissionsPresetsConfigMixin, RDMRecordServiceConfig):
    """DatasetsRecord service config."""

    result_item_cls = DatasetsRecordItem

    result_list_cls = DatasetsRecordList

    PERMISSIONS_PRESETS = ["community-workflow"]

    url_prefix = "/datasets/"

    base_permission_policy_cls = DatasetsPermissionPolicy

    schema = DatasetsSchema

    search = DatasetsSearchOptions

    record_cls = DatasetsRecord

    service_id = "datasets"

    search_item_links_template = LinksTemplate
    draft_cls = DatasetsDraft
    search_drafts = DatasetsDraftSearchOptions

    @property
    def components(self):
        return process_service_configs(
            self,
            CommunityDefaultWorkflowComponent,
            CommunityInclusionComponent,
            CustomFieldsComponent,
            WorkflowComponent,
        )

    model = "datasets"

    @property
    def links_item(self):
        links = {
            **super().links_item,
            "applicable-requests": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/datasets/{id}/requests/applicable"),
                else_=RecordLink("{+api}/datasets/{id}/draft/requests/applicable"),
            ),
            "communities": CommunitiesLinks(
                {
                    "self": "{+api}/communities/{id}",
                    "self_html": "{+ui}/communities/{slug}/records",
                }
            ),
            "draft": RecordLink(
                "{+api}/datasets/{id}/draft",
                when=has_draft() & has_permission("read_draft"),
            ),
            "edit_html": RecordLink(
                "{+ui}/datasets/{id}/edit", when=has_draft() & has_permission("update")
            ),
            "files": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink(
                    "{+api}/datasets/{id}/files", when=has_file_permission("list_files")
                ),
                else_=RecordLink(
                    "{+api}/datasets/{id}/draft/files",
                    when=has_file_permission("list_files"),
                ),
            ),
            "latest": RecordLink(
                "{+api}/datasets/{id}/versions/latest", when=has_permission("read")
            ),
            "latest_html": RecordLink(
                "{+ui}/datasets/{id}/latest", when=has_permission("read")
            ),
            "publish": RecordLink(
                "{+api}/datasets/{id}/draft/actions/publish",
                when=has_permission("publish"),
            ),
            "record": RecordLink(
                "{+api}/datasets/{id}",
                when=has_published_record() & has_permission("read"),
            ),
            "requests": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/datasets/{id}/requests"),
                else_=RecordLink("{+api}/datasets/{id}/draft/requests"),
            ),
            "self": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/datasets/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+api}/datasets/{id}/draft", when=has_permission("read_draft")
                ),
            ),
            "self_html": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+ui}/datasets/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+ui}/datasets/{id}/preview", when=has_permission("read_draft")
                ),
            ),
            "versions": RecordLink(
                "{+api}/datasets/{id}/versions", when=has_permission("search_versions")
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_item(self):
        links = {
            **super().links_search_item,
            "self": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+api}/datasets/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+api}/datasets/{id}/draft", when=has_permission("read_draft")
                ),
            ),
            "self_html": ConditionalLink(
                cond=is_published_record(),
                if_=RecordLink("{+ui}/datasets/{id}", when=has_permission("read")),
                else_=RecordLink(
                    "{+ui}/datasets/{id}/preview", when=has_permission("read_draft")
                ),
            ),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search(self):
        links = {
            **super().links_search,
            **pagination_links("{+api}/datasets/{?args*}"),
            **pagination_links_html("{+ui}/datasets/{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_drafts(self):
        links = {
            **super().links_search_drafts,
            **pagination_links("{+api}/user/datasets/{?args*}"),
            **pagination_links_html("{+ui}/user/datasets/{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}

    @property
    def links_search_versions(self):
        links = {
            **super().links_search_versions,
            **pagination_links("{+api}/datasets/{id}/versions{?args*}"),
        }
        return {k: v for k, v in links.items() if v is not None}
