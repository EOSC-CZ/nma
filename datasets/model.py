"""
Structured collections of research data, identified with a persistent identifier
"""

from __future__ import annotations

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
    PrependMixin,
    ReplaceBaseClass,
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

from .deserializers import DataCiteJSONDeserializer, DataCiteXMLDeserializer
from .permissions import DatasetsPermissionPolicyMixin
from .serializers import DataCiteJSONSerializer
from .services.components import (
    ExternalPIDComponent,
    FetchIdentifiersComponent,
    UpdateEditorsComponent,
    UpdateMetadataComponent,
)


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
                normalized_rights.append({"title": {"en": title}})
                continue

            if isinstance(title, dict) and title:
                normalized_rights.append({"title": title})
                continue

            if isinstance(title, list) and title and isinstance(title[0], str):
                normalized_rights.append({"title": {"en": title[0]}})
                continue

            # If we get here, the right is invalid → drop it
        data["metadata"]["rights"] = normalized_rights
        print(normalized_rights, flush=True)

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


datasets_model = model(
    "datasets",
    version="1.0.0",
    presets=[rdm_complete_preset],
    types=[from_yaml("metadata.yaml", __file__), from_yaml("record.yaml", __file__)],
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
            name=_("DataCite JSON"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer(),
        ),
        # datacite xml import
        AddMetadataImport(
            code="datacite",
            name=_("DataCite XML"),
            description=_("Import metadata from DataCite XML format"),
            mimetype="application/vnd.datacite.datacite+xml",
            deserializer=DataCiteXMLDeserializer(),
            oai_name=("http://datacite.org/schema/kernel-4e", "resource"),
        ),
        # datacite json import
        AddMetadataImport(
            code="datacite",
            name=_("DataCite JSON"),
            description=_("Import metadata from DataCite JSON format"),
            mimetype="application/vnd.datacite.datacite+json",
            deserializer=DataCiteJSONDeserializer(),
        ),
        # support for non-generated persistent identifiers (always taken from the id field)
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
            ],
        ),
    ],
    configuration={"ui_blueprint_name": "datasets_ui"},
)
