"""
A generic dataset model
"""
from __future__ import annotations

from invenio_i18n import lazy_gettext as _
from oarepo_model.api import model
from oarepo_model.customizations import AddMetadataExport
from oarepo_model.datatypes.registry import from_yaml
from ccmm_invenio.models import ccmm_production_preset_1_1_0

from .serializers import DataCiteJSONSerializer
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from invenio_drafts_resources.services.records import (
    RecordService as DraftRecordService,
)
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.resources.serializers.ui.schema import UIRecordSchema
from invenio_records_resources.records.systemfields import PIDField
from invenio_records_resources.services import RecordEndpointLink
from oarepo_model.api import model
from oarepo_model.customizations import (
    AddFacetGroup,
    AddMetadataExport,
    AddMetadataImport,
    AddServiceComponent,
    AddToList,
    PatchIndexPropertyMapping,
    PatchIndexSettings,
    PrependMixin,
    ReplaceBaseClass, PatchIndexMapping, SetDefaultSearchFields,
)
from oarepo_model.customizations.high_level.add_link import AddLink
from oarepo_model.datatypes.registry import from_yaml
from oarepo_rdm.model.presets import rdm_complete_preset
from oarepo_runtime.services.config import (
    has_permission,
)

from riv.records.api import ExternalPIDProvider
from riv.records.system_fields import (
    ExternalPIDField,
    ExternalPIDFieldContextMixin,
    PIDStatusCheckField,
)
from .records.is_harvested_dumper import IsHarvestedDumperExt
from .deserializers import DataCiteJSONDeserializer, DataCiteXMLDeserializer
from .permissions import DatasetsPermissionPolicyMixin
from .serializers import DataCiteJSONSerializer
from .services.components import (
    ExternalPIDComponent,
    FetchIdentifiersComponent,
    UpdateEditorsComponent,
    UpdateMetadataComponent,
)
from common.oai.aire_provenance import aire_about_etree
from models.datasets.oai.openaire.openaire_serializer import OpenAIREXMLSerializer

class PIDStatusCheckFieldMixin:
    """Custom PID status check field returning False when PID is not set."""

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)


class UpdatableRecordServiceMixin:
    EDITABLE_FIELDS = [
        "title",
        "creators",
        "resource_type",
        "publication_date",
        # for checks
        "check_status",
        "last_checked",
        "check_message",
    ]
    """Invenio forms based editor modifies even fields that are not in the editor,
    such as removing title from rights. To workaround this, we override update
    method to only propagate changes from editor fields. If you add a new field to
    the UI editor, please add it also to the EDITABLE_FIELDS list here.
    """

    def update(self, identity, id_, data, *args, revision_id=None, **kwargs):
        """Override update to allow updating published records.
        """

        # metadata.rights: invenio rdm can not upload record that has rights that contain both id and title
        # so we remove all other props if there is an id
        rights = data["metadata"].get("rights", [])
        normalized_rights = []

        for right in rights:
            if "id" in right and isinstance(right["id"], str):
                normalized_rights.append({"id": right["id"]})
                continue

            title = right.get("title")

            if isinstance(title, str):
                normalized_rights.append({**right, "title": {"en": title}})
                continue

            if isinstance(title, dict) and title:
                normalized_rights.append(right)
                continue

            if isinstance(title, list) and title and isinstance(title[0], str):
                normalized_rights.append({**right, "title": {"en": title[0]}})

        data["metadata"]["rights"] = normalized_rights

        # metadata/creators/person_or_org/affiliations - can not have identifiers
        for creator in data["metadata"].get("creators", []):
            for aff in creator.get("affiliations", []):
                aff.pop("identifiers", None)
        for contributor in data["metadata"].get("contributors", []):
            for aff in contributor.get("affiliations", []):
                aff.pop("identifiers", None)

        # we need to call super directly on the base record service, because draft
        # service disables the update on published records completely, regardless
        # of permission policy
        return super(DraftRecordService, self).update(
            identity, id_, data, *args, revision_id=revision_id, **kwargs
        )
class OverriddenRouteResourceConfigMixin:
    @property
    def routes(self):
        """Override routes to use path instead of default converter for pid_value.

        This was causing a problem when PID contained slashes (doi:1234/zenodo.12345 for example).
        It would parse only first part before the slash.
        """
        routes = super().routes

        updated_routes = {}
        for (
            key,
            route,
        ) in routes.items():
            updated_route = route.replace("<pid_value>", "<path:pid_value>")
            updated_routes[key] = updated_route

        return updated_routes

COPY_TO_MAPPINGS = [
    # boost_10 - Primary identifiers (highest weight)
    ("metadata.title", 10),
    ("metadata.persistent_url", 10),
    ("id", 10),

    # boost_5 - Important searchable content
    ("metadata.additional_titles.title", 5),
    ("metadata.description", 5),

    ("metadata.creators.person_or_org.name", 5),
    # Author names
    # boost_1 - Supplementary content
    ("metadata.additional_descriptions.description", 1),
    ("metadata.contributors.person_or_org.name", 1),
    # Contributor names
    ("metadata.publisher", 1),
    # Publisher
    ("metadata.funding.funder.name", 1),
    # Funder names
    ("metadata.locations.features.place", 1),
    # Place names
    ("metadata.related_resources.title", 1),
    ("metadata.related_resources.identifiers.identifier", 1),

]

copy_to_mappings = [PatchIndexPropertyMapping(c[0], {"copy_to": f"boost_{c[1]}"}) for c in COPY_TO_MAPPINGS]
analyzer_fields = {"fields": {
    # using both means that queries that match both ascii and non-ascii
    # versions are ranked higher (if query is Novák, records with Novák
    # will have better ranking than Novak and both will be found),
    # but if user searches for Novak Novák will still match with
    # lower ranking than Novak
    "_search": {"type": "text", "analyzer": "lowercase_analyzer"},
    "_ascii_search": {
        "type": "text",
        "analyzer": "asciifolded_lowercase_analyzer",
    },
}
}

# TODO: Consider letting users add an image/icon for the model,
# so that the deposit model selection page is more visually appealing.
datasets_model = model(
    "datasets",
    version="1.0.0",
    description="A generic dataset model",
    presets=[

        ccmm_production_preset_1_1_0

    ],
    types=[
        from_yaml("metadata.yaml", __file__), from_yaml("record.yaml", __file__)
    ],
    metadata_type="Metadata",
    record_type="Record",

    customizations=[
        # Add your customizations here, such as custom exports and class mixins. 
        # The list of available extensions is at https://github.com/oarepo/oarepo-model.
        # If you do not find a customization that suits your needs or need a
        # help with using customizations, please contact us at support@cesnet.cz and
        # specify the keyword "Invenio repository development" inside the subject or
        # mail body of the request.
        # TODO: remove this customization if you use oarepo-communities for RDM 14
        PrependMixin("PermissionPolicy", DatasetsPermissionPolicyMixin),
        # TODO: move this to oarepo-rdm
        PrependMixin("RecordUISchema", UIRecordSchema),
        # export for datacite
        AddMetadataExport(
            code="datacite",
            name=_("Datacite export"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer()
        ),
        AddMetadataExport(
            code="aire",
            name=_("OpenAIRE"),
            mimetype="application/vnd.datacite.datacite+xml",
            serializer=OpenAIREXMLSerializer(),
            about_serializer=aire_about_etree,
            oai_metadata_prefix="oai_datacite",
            oai_schema="http://schema.datacite.org/oai/oai-1.1/oai.xsd",
            oai_namespace="http://schema.datacite.org/oai/oai-1.1/",
        ),
        AddMetadataImport(
            code="datacite-xml",
            name=_("DataCite XML"),
            description=_("Import metadata from DataCite XML format"),
            mimetype="application/vnd.datacite.datacite+xml",
            deserializer=DataCiteXMLDeserializer(),
            oai_name=(
                "http://datacite.org/schema/kernel-4e",
                "resource",
        ),
        ),


        AddServiceComponent(ExternalPIDComponent),
        ReplaceBaseClass(
            "PIDProvider",
            DraftRecordIdProviderV2,
            ExternalPIDProvider,
        ),
ReplaceBaseClass("PIDField", PIDField, ExternalPIDField),
        #
        AddServiceComponent(UpdateMetadataComponent),
        AddServiceComponent(UpdateEditorsComponent),
        AddServiceComponent(FetchIdentifiersComponent),
        AddLink("self_persistent_html", RecordEndpointLink("pidresolver.redirect")),
        AddLink(
            "edit_html",
            RecordEndpointLink(
                "datasets_ui.deposit_edit",
                when=has_permission("update"),
            ),
        ),
        PrependMixin("PIDFieldContext", ExternalPIDFieldContextMixin),
        PrependMixin("Draft", PIDStatusCheckFieldMixin),
        PrependMixin("RecordService", UpdatableRecordServiceMixin),
        PrependMixin("RecordResourceConfig", OverriddenRouteResourceConfigMixin),
        AddFacetGroup(
            "default",
            [
                "metadata.publisher",
                "metadata.resource_type",
                "metadata.languages",
            ],
        ),
        AddToList("record_dumper_extensions", IsHarvestedDumperExt()),
        # index tweaks
        PatchIndexSettings(
            {
                "analysis": {
                    # lowercase splits on whitespaces and performs lowercasing
                    "tokenizer": {"lowercase_tokenizer": {"type": "lowercase"}},
                    "analyzer": {
                        "lowercase_analyzer": {
                            "type": "custom",
                            "tokenizer": "lowercase_tokenizer",
                        },
                        "asciifolded_lowercase_analyzer": {
                            "type": "custom",
                            "tokenizer": "lowercase_tokenizer",
                            # additionally removes diacritics
                            "filter": ["asciifolding"],
                        },
                    },
                }
            }
        ),
        PatchIndexMapping(
            {
                "properties": {
                    "boost_10": {"type": "text", "boost": 10, **analyzer_fields},
                    "boost_5": {"type": "text", "boost": 5, **analyzer_fields},
                    "boost_1": {"type": "text", "boost": 1, **analyzer_fields},
                    "parent.is_harvested": {"type": "boolean"},
                }
            }
        ),
        *copy_to_mappings,
        SetDefaultSearchFields("boost_10", "boost_5", "boost_1", "boost_10._search",
                               "boost_5._search", "boost_1._search", "boost_10._ascii_search",
                               "boost_5._ascii_search", "boost_1._ascii_search")

    ],
    configuration={
        "ui_blueprint_name": "datasets_ui"
    }
)
