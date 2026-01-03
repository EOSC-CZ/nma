"""
Structured collections of research data, identified with a persistent identifier
"""

from __future__ import annotations

from invenio_administration.generators import Administration
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from invenio_drafts_resources.services.records import (
    RecordService as DraftRecordService,
)
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.resources.serializers.ui.schema import UIRecordSchema
from invenio_rdm_records.services.generators import AccessGrant
from invenio_records_permissions.generators import (
    AuthenticatedUser,
    Disable,
    SystemProcess,
)
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
from oarepo_model.model import ModelMixin
from oarepo_rdm.model.presets import rdm_complete_preset

from riv.records.api import ExternalPIDProvider
from riv.records.system_fields import (
    ExternalPIDField,
    ExternalPIDFieldContextMixin,
    PIDStatusCheckField,
)

from .deserializers import DataCiteJSONDeserializer, DataCiteXMLDeserializer
from .serializers import DataCiteJSONSerializer
from .services.components import (
    ExternalPIDComponent,
    FetchIdentifiersComponent,
    UpdateEditorsComponent,
    UpdateMetadataComponent,
)


class DatasetsPermissionPolicyMixin(ModelMixin):
    """Custom permission policy for datasets."""

    can_view_deposit_page = [AuthenticatedUser()]
    can_update = [
        AccessGrant("edit"),
        SystemProcess(),
        Administration(),
    ]  # system process can update records (in tasks etc)

    can_create = [
        SystemProcess(),
        Administration(),
    ]  # only system process and admin can create records
    can_publish = [
        SystemProcess(),
        Administration(),
    ]  # only system process and admin can publish records

    can_manage = [SystemProcess(), Administration(), AccessGrant("manage")]

    can_draft_create_files = [Disable()]  # disable files by default
    can_update_draft = [SystemProcess(), Administration()]


class PIDStatusCheckFieldMixin:
    """Custom PID status check field returning False when PID is not set."""

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)


class UpdatableRecordServiceMixin:
    def update(self, *args, **kwargs):
        """Do not use."""
        return super(DraftRecordService, self).update(*args, **kwargs)


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
