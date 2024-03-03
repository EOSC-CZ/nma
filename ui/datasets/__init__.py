from oarepo_ui.resources import BabelComponent
from oarepo_ui.resources.config import RecordsUIResourceConfig
from oarepo_ui.resources.resource import RecordsUIResource


class DatasetsResourceConfig(RecordsUIResourceConfig):
    template_folder = "templates"
    url_prefix = "/datasets/"
    blueprint_name = "datasets"
    ui_serializer_class = "datasets.resources.records.ui.DatasetsUIJSONSerializer"
    api_service = "datasets"

    components = [BabelComponent]
    try:
        from oarepo_vocabularies.ui.resources.components import (
            DepositVocabularyOptionsComponent,
        )
        components.append(DepositVocabularyOptionsComponent)
    except ImportError:
        pass

    application_id="datasets"

    templates = {
        "detail": "datasets.Detail",
        "search": "datasets.Search",
        "edit": "datasets.Deposit",
        "create":"datasets.Deposit",
    }


class DatasetsResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    return DatasetsResource(DatasetsResourceConfig()).as_blueprint()
