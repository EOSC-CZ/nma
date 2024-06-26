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
    }
    
    def search_active_facets(self, api_config, identity):
        return [
            k
            for k in self.search_available_facets(api_config, identity).keys()
            # TODO: replace with a more generic `item.filterable` attribute check
            if not k.startswith("metadata_abstract")
        ]


class DatasetsResource(RecordsUIResource):
    pass


def create_blueprint(app):
    """Register blueprint for this resource."""
    return DatasetsResource(DatasetsResourceConfig()).as_blueprint()
