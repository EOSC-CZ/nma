"""
Structured collections of research data, identified with a persistent identifier
"""

from __future__ import annotations

from typing import TYPE_CHECKING

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
    PatchIndexPropertyMapping,
    PatchIndexSettings,
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

from typing import TYPE_CHECKING, Any, override
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


from invenio_access.permissions import system_identity
from invenio_drafts_resources.services import RecordService as RecordServiceWithDrafts
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_rdm_records.requests.entity_resolvers import RDMRecordServiceResultProxy, RDMRecordServiceResultResolver
from invenio_records_resources.references.entity_resolvers.results import (
    ServiceResultResolver as InvenioServiceResultResolver,
)
from oarepo_model.customizations import (
    AddEntryPoint,
    AddModule,
    AddToModule,
    Customization,
)
from oarepo_model.presets import Preset
from oarepo_runtime.typing import record_from_result
from sqlalchemy.exc import NoResultFound

if TYPE_CHECKING:
    from collections.abc import Generator

    from invenio_drafts_resources.records import Draft
    from invenio_records_resources.records import Record
    from invenio_records_resources.references import RecordResolver
    from invenio_records_resources.services.records.results import RecordItem
    from oarepo_model.builder import InvenioModelBuilder
    from oarepo_model.model import InvenioModel

class RecordServiceResultProxy(RDMRecordServiceResultProxy):
    """Proxy to resolve a record service result."""

    @override
    def _resolve(self) -> dict[str, Any]:
        """Resolve the result item from the proxy's reference dict."""
        pid_value = self._parse_ref_dict_id()
        if isinstance(self.service, RecordServiceWithDrafts):
            try:
                draft = self.service.read_draft(system_identity, pid_value)
            except (PIDDoesNotExistError, NoResultFound):
                record = self._get_record(pid_value)
            else:
                record = (
                    draft if not record_from_result(draft).is_published else self._get_record(pid_value)  # type: ignore[reportAttributeAccessIssue]
                )
        else:
            record = self._get_record(pid_value)

        return record.to_dict()  # type: ignore[no-any-return]


class RecordServiceResultResolver(RDMRecordServiceResultResolver):
    """Service result resolver for draft records."""

    def __init__(
        self,
        service_id: str,
        type_key: str,
        proxy_cls: type[RecordServiceResultProxy] = RecordServiceResultProxy,
        item_cls: type[RecordItem] | None = None,
        record_cls: type[Record] | None = None,
    ):
        """Initialize the resolver."""
        super(RDMRecordServiceResultResolver, self).__init__(service_id, type_key, proxy_cls, item_cls, record_cls)

    @property
    @override
    def draft_cls(self) -> type[Draft] | None:
        """Get specified draft class or from service."""
        service = self.get_service()
        return service.draft_cls if isinstance(service, RecordServiceWithDrafts) else None

    @override
    def matches_entity(self, entity: Any) -> bool:
        """Check if the entity is a draft."""
        if self.draft_cls and isinstance(entity, self.draft_cls):
            return True

        return InvenioServiceResultResolver.matches_entity(self, entity=entity)  # type: ignore[no-any-return]

class RegisterResolversPreset(Preset):
    """Preset for registering resolvers."""

    @override
    def apply(
        self,
        builder: InvenioModelBuilder,
        model: InvenioModel,
        dependencies: dict[str, Any],
    ) -> Generator[Customization]:
        def register_entity_resolver() -> RecordResolver:
            service_id = builder.model.base_name
            runtime_dependencies = builder.get_runtime_dependencies()
            resolver = runtime_dependencies.get("RecordResolver")
            return resolver(
                record_cls=runtime_dependencies.get("Record"),
                service_id=service_id,
                type_key=service_id,
                proxy_cls=runtime_dependencies.get("RecordProxy"),
            )

        def register_notification_resolver() -> RecordServiceResultResolver:
            service_id = builder.model.base_name
            return RecordServiceResultResolver(
                service_id=service_id,
                type_key=service_id,
                proxy_cls=RecordServiceResultProxy,
            )

        # just invenio things
        register_notification_resolver.type_key = builder.model.base_name  # type: ignore[attr-defined]

        yield AddModule("resolvers", exists_ok=True)
        yield AddToModule("resolvers", "register_entity_resolver", staticmethod(register_entity_resolver))
        yield AddToModule("resolvers", "register_notification_resolver", staticmethod(register_notification_resolver))
        yield AddEntryPoint(
            group="invenio_requests.entity_resolvers",
            name=f"{model.base_name}_requests",
            value="resolvers:register_entity_resolver",
            separator=".",
        )
        yield AddEntryPoint(
            group="invenio_notifications.entity_resolvers",
            name=f"{model.base_name}_requests",
            value="resolvers:register_notification_resolver",
            separator=".",
        )

datasets_model = model(
    "datasets",
    version="1.0.0",
    presets=[rdm_complete_preset, [RegisterResolversPreset]],
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
                "metadata.resource_type",
                "metadata.languages",
            ],
        ),
        # index tweaks
        PatchIndexSettings(
            {
                "analysis": {
                    # lowercase splits on whitespaces and performs lowercasing
                    "tokenizer": {"people_tokenizer": {"type": "lowercase"}},
                    "analyzer": {
                        "people_analyzer": {
                            "type": "custom",
                            "tokenizer": "people_tokenizer",
                        },
                        "asciifolded_people_analyzer": {
                            "type": "custom",
                            "tokenizer": "people_tokenizer",
                            # additionally removes diacritics
                            "filter": ["asciifolding"],
                        },
                    },
                }
            }
        ),
        # add multi-field mappings to people names for improved searching/suggesting
        PatchIndexPropertyMapping(
            "metadata.creators.person_or_org.name",
            {
                "fields": {
                    # using both means that queries that match both ascii and non-ascii
                    # versions are ranked higher (if query is Novák, records with Novák
                    # will have better ranking than Novak and both will be found),
                    # but if user searches for Novak Novák will still match with
                    # lower ranking than Novak
                    "_search": {"type": "text", "analyzer": "people_analyzer"},
                    "_ascii_search": {
                        "type": "text",
                        "analyzer": "asciifolded_people_analyzer",
                    },
                }
            },
        ),
        PatchIndexPropertyMapping(
            "metadata.contributors.person_or_org.name",
            {
                "fields": {
                    "_search": {"type": "text", "analyzer": "people_analyzer"},
                    "_ascii_search": {
                        "type": "text",
                        "analyzer": "asciifolded_people_analyzer",
                    },
                }
            },
        ),
    ],
    configuration={"ui_blueprint_name": "datasets_ui"},
)
