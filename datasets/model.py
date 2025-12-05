"""
Structured collections of research data, identified with a persistent identifier
"""

from __future__ import annotations

from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from invenio_i18n import lazy_gettext as _
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.services.generators import SecretLinks
from invenio_records_permissions.generators import AuthenticatedUser
from invenio_records_resources.records.systemfields import PIDField
from oarepo_model.api import model
from oarepo_model.customizations import AddMetadataExport, PrependMixin, ReplaceBaseClass, AddServiceComponent
from oarepo_model.datatypes.registry import from_yaml
from oarepo_model.model import ModelMixin, Dependency
from oarepo_rdm.model.presets import rdm_complete_preset
from invenio_drafts_resources.services.records import RecordService as DraftRecordService

from riv.records.api import ExternalPIDProvider
from riv.records.system_fields import PIDStatusCheckField, ExternalPIDFieldContextMixin, ExternalPIDField
from riv.services.components import ExternalPIDComponent, UpdateMetadataComponent
from .serializers import DataCiteJSONSerializer


class DatasetsPermissionPolicyMixin(ModelMixin):
    """Custom permission policy for datasets."""

    can_view_deposit_page = [AuthenticatedUser()]
    can_update = [SecretLinks("edit")]

class PIDStatusCheckFieldMixin:
    """Custom PID status check field returning False when PID is not set."""

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)

class UpdatableRecordServiceMixin:
    def update(self, *args, **kwargs):
        """Do not use."""
        return super(DraftRecordService, self).update(*args, **kwargs)


class OverridenRouteResourceConfigMixin:
    @property
    def routes(self):
        """Override routes to use path instead of default converter for pid_value.

        This was causing problem when PID contained slashes (doi:1234/zenodo.12345 for example).
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
    types=[from_yaml("metadata.yaml", __file__)],
    metadata_type="Metadata",
    customizations=[
        # Add your customizations here, such as custom exports and class mixins.
        # The list of available extensions is at https://github.com/oarepo/oarepo-model.
        # If you do not find a customization that suits your needs or need a
        # help with using customizations, please contact us at support@cesnet.cz and
        # specify the keyword "Invenio repository development" inside the subject or
        # mail body of the request.
        # TODO: remove this customization if you use oarepo-communities for RDM 14
        PrependMixin("PermissionPolicy", DatasetsPermissionPolicyMixin),
        # export for datacite
        AddMetadataExport(
            code="datacite",
            name=_("Datacite export"),
            mimetype="application/vnd.datacite.datacite+json",
            serializer=DataCiteJSONSerializer(),
        ),
        AddServiceComponent(ExternalPIDComponent),
        AddServiceComponent(UpdateMetadataComponent),
        ReplaceBaseClass(
            "PIDProvider",
            DraftRecordIdProviderV2,
            ExternalPIDProvider,
        ),
        ReplaceBaseClass("PIDField", PIDField, ExternalPIDField),
        PrependMixin("PIDFieldContext", ExternalPIDFieldContextMixin),
        PrependMixin("Draft", PIDStatusCheckFieldMixin),
        PrependMixin("RecordService", UpdatableRecordServiceMixin),
        PrependMixin("RecordResourceConfig", OverridenRouteResourceConfigMixin),
    ],
    configuration={"ui_blueprint_name": "datasets_ui"},
)
