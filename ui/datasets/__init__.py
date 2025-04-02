from oarepo_ui.resources import BabelComponent
from oarepo_ui.resources.components import (
    AllowedCommunitiesComponent,
    AllowedHtmlTagsComponent,
    EmptyRecordAccessComponent,
    FilesComponent,
    FilesLockedComponent,
    RecordRestrictionComponent,
    PermissionsComponent,
)
from oarepo_ui.resources.components.custom_fields import CustomFieldsComponent
from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources.resource import RecordsUIResource
from oarepo_ui.utils import can_view_deposit_page
from oarepo_ui.ui.components import UIComponent
from flask_menu import current_menu
from oarepo_runtime.i18n import lazy_gettext as _


class DatasetsUIResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/datasets"
    blueprint_name = "datasets"
    ui_serializer_class = "datasets.resources.records.ui.DatasetsUIJSONSerializer"
    api_service = "datasets"

    search_component = UIComponent(
        "DatasetsResultsListItem", "@js/datasets/search/ResultsListItem", "default"
    )

    routes = {
        "search": "",
        "detail": "/<pid_value>",
        "export": "/<pid_value>/export/<export_format>",
        "published_file_preview": "/<pid_value>/files/<path:filepath>/preview",
    }

    components = [
        AllowedHtmlTagsComponent,
        BabelComponent,
        PermissionsComponent,
        FilesComponent,
        AllowedCommunitiesComponent,
        CustomFieldsComponent,
        RecordRestrictionComponent,
        EmptyRecordAccessComponent,
        FilesLockedComponent,
    ]

    try:
        from oarepo_vocabularies.ui.resources.components import (
            DepositVocabularyOptionsComponent,
        )

        components.append(DepositVocabularyOptionsComponent)
    except ImportError:
        pass

    application_id = "datasets"

    templates = {
        "detail": "datasets.Detail",
        "search": "datasets.Search",
    }


class DatasetsUIResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    blueprint = DatasetsUIResource(DatasetsUIResourceConfig()).as_blueprint()
    return blueprint
