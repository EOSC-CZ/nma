from invenio_communities.records.records.systemfields import CommunitiesField
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from invenio_drafts_resources.services.records.components.media_files import (
    MediaFilesAttrConfig,
)
from invenio_rdm_records.records.api import (
    RDMDraft,
    RDMMediaFileDraft,
    RDMMediaFileRecord,
    RDMParent,
    RDMRecord,
)
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.systemfields import FilesField, IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from oarepo_communities.records.systemfields.communities import (
    OARepoCommunitiesFieldContext,
)
from oarepo_runtime.records.pid_providers import UniversalPIDMixin
from oarepo_runtime.records.relations import PIDRelation, RelationsField
from oarepo_runtime.records.systemfields.has_draftcheck import HasDraftCheckField
from oarepo_runtime.records.systemfields.icu import FulltextIndexField, TermIndexField
from oarepo_runtime.records.systemfields.record_status import RecordStatusSystemField
from oarepo_vocabularies.records.api import Vocabulary
from oarepo_workflows.records.systemfields.state import (
    RecordStateField,
    RecordStateTimestampField,
)
from oarepo_workflows.records.systemfields.workflow import WorkflowField

from datasets.files.api import DatasetsFile, DatasetsFileDraft
from datasets.records.dumpers.dumper import DatasetsDraftDumper, DatasetsDumper
from datasets.records.models import (
    DatasetsCommunitiesMetadata,
    DatasetsDraftMetadata,
    DatasetsMetadata,
    DatasetsParentMetadata,
    DatasetsParentState,
)


class DatasetsParentRecord(RDMParent):
    model_cls = DatasetsParentMetadata

    workflow = WorkflowField()

    communities = CommunitiesField(
        DatasetsCommunitiesMetadata, context_cls=OARepoCommunitiesFieldContext
    )


class DatasetsIdProvider(UniversalPIDMixin, DraftRecordIdProviderV2):
    pid_type = "dtsts"


class DatasetsRecord(RDMRecord):

    model_cls = DatasetsMetadata

    schema = ConstantField("$schema", "local://datasets-1.0.0.json")

    index = IndexField(
        "datasets-datasets-1.0.0",
    )

    pid = PIDField(
        provider=DatasetsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper = DatasetsDumper()

    search_title = FulltextIndexField(source_field="metadata.title", boost=20)

    search_person_name = FulltextIndexField(
        source_field="metadata.qualified_relations.person.name", boost=20
    )

    search_organization_name = FulltextIndexField(
        source_field="metadata.qualified_relations.organization.name", boost=20
    )

    search_person_id = TermIndexField(
        source_field="metadata.qualified_relations.person.identifiers.value", boost=20
    )

    search_organization_id = TermIndexField(
        source_field="metadata.qualified_relations.organization.identifiers.value",
        boost=20,
    )

    search_id = TermIndexField(source_field="identifiers.value", boost=20)

    search_pid = TermIndexField(source_field="id", boost=20)

    search_subjects = FulltextIndexField(
        source_field="metadata.subjects.title.value", boost=10
    )

    search_descriptions = FulltextIndexField(
        source_field="metadata.descriptions.value", boost=10
    )

    search_alternate_titles = FulltextIndexField(
        source_field="metadata.alternate_titles.title.value", boost=10
    )

    state = RecordStateField(initial="published")

    state_timestamp = RecordStateTimestampField()

    media_files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileRecord,
        create=False,
        delete=False,
    )

    relations = RelationsField(
        type=PIDRelation(
            "metadata.alternate_titles.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("title-types"),
        ),
        algorithm=PIDRelation(
            "metadata.distributions.checksum.algorithm",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("checksum-algorithms"),
        ),
        format=PIDRelation(
            "metadata.distributions.format",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("file-types"),
        ),
        media_type=PIDRelation(
            "metadata.distributions.media_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("media-types"),
        ),
        identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        identifiers_identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        person_identifiers_identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_identifiers_identifier_scheme=PIDRelation(
            "metadata.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        languages=PIDRelation(
            "metadata.is_described_by.languages",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        role=PIDRelation(
            "metadata.is_described_by.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_objects_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_objects_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_role=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        relation_type=PIDRelation(
            "metadata.locations.related_objects.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("relation-types"),
        ),
        date_type=PIDRelation(
            "metadata.locations.related_objects.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
        related_objects_type=PIDRelation(
            "metadata.locations.related_objects.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        locations_relation_type=PIDRelation(
            "metadata.locations.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("location-relation-types"),
        ),
        other_languages=PIDRelation(
            "metadata.other_languages",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        primary_language=PIDRelation(
            "metadata.primary_language",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        metadata_qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_qualified_relations_role=PIDRelation(
            "metadata.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_resources_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_role=PIDRelation(
            "metadata.related_resources.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_resources_relation_type=PIDRelation(
            "metadata.related_resources.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("relation-types"),
        ),
        time_references_date_type=PIDRelation(
            "metadata.related_resources.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
        related_resources_type=PIDRelation(
            "metadata.related_resources.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        resource_type=PIDRelation(
            "metadata.resource_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        scheme=PIDRelation(
            "metadata.subjects.scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("subject-schemes"),
        ),
        access_rights=PIDRelation(
            "metadata.terms_of_use.access_rights",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        contacts_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        contacts_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        contacts_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_time_references_date_type=PIDRelation(
            "metadata.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
    )

    versions_model_cls = DatasetsParentState

    parent_record_cls = DatasetsParentRecord
    record_status = RecordStatusSystemField()
    has_draft = HasDraftCheckField(
        draft_cls=lambda: DatasetsDraft, config_key="HAS_DRAFT_CUSTOM_FIELD"
    )

    files = FilesField(file_cls=DatasetsFile, store=False, create=False, delete=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


class RDMRecordMediaFiles(DatasetsRecord):
    """RDM Media file record API."""

    files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileRecord,
        # Don't create
        create=False,
        # Don't delete, we'll manage in the service
        delete=False,
    )


class DatasetsDraft(RDMDraft):

    model_cls = DatasetsDraftMetadata

    schema = ConstantField("$schema", "local://datasets-1.0.0.json")

    index = IndexField("datasets-datasets_draft-1.0.0", search_alias="datasets")

    pid = PIDField(
        provider=DatasetsIdProvider,
        context_cls=PIDFieldContext,
        create=True,
        delete=False,
    )

    dumper = DatasetsDraftDumper()

    state = RecordStateField()

    state_timestamp = RecordStateTimestampField()

    search_title = FulltextIndexField(source_field="metadata.title", boost=20)

    search_person_name = FulltextIndexField(
        source_field="metadata.qualified_relations.person.name", boost=20
    )

    search_organization_name = FulltextIndexField(
        source_field="metadata.qualified_relations.organization.name", boost=20
    )

    search_person_id = TermIndexField(
        source_field="metadata.qualified_relations.person.identifiers.value", boost=20
    )

    search_organization_id = TermIndexField(
        source_field="metadata.qualified_relations.organization.identifiers.value",
        boost=20,
    )

    search_id = TermIndexField(source_field="identifiers.value", boost=20)

    search_pid = TermIndexField(source_field="id", boost=20)

    search_subjects = FulltextIndexField(
        source_field="metadata.subjects.title.value", boost=10
    )

    search_descriptions = FulltextIndexField(
        source_field="metadata.descriptions.value", boost=10
    )

    search_alternate_titles = FulltextIndexField(
        source_field="metadata.alternate_titles.title.value", boost=10
    )

    media_files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileDraft,
        create=False,
        delete=False,
    )

    relations = RelationsField(
        type=PIDRelation(
            "metadata.alternate_titles.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("title-types"),
        ),
        algorithm=PIDRelation(
            "metadata.distributions.checksum.algorithm",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("checksum-algorithms"),
        ),
        format=PIDRelation(
            "metadata.distributions.format",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("file-types"),
        ),
        media_type=PIDRelation(
            "metadata.distributions.media_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("media-types"),
        ),
        identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        identifiers_identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        person_identifiers_identifier_scheme=PIDRelation(
            "metadata.funding_references.funders.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_identifiers_identifier_scheme=PIDRelation(
            "metadata.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        languages=PIDRelation(
            "metadata.is_described_by.languages",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.is_described_by.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        role=PIDRelation(
            "metadata.is_described_by.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_objects_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_objects_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_role=PIDRelation(
            "metadata.locations.related_objects.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        relation_type=PIDRelation(
            "metadata.locations.related_objects.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("relation-types"),
        ),
        date_type=PIDRelation(
            "metadata.locations.related_objects.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
        related_objects_type=PIDRelation(
            "metadata.locations.related_objects.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        locations_relation_type=PIDRelation(
            "metadata.locations.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("location-relation-types"),
        ),
        other_languages=PIDRelation(
            "metadata.other_languages",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        primary_language=PIDRelation(
            "metadata.primary_language",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        metadata_qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        qualified_relations_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_qualified_relations_role=PIDRelation(
            "metadata.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_resources_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.related_resources.qualified_relations.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        related_resources_qualified_relations_role=PIDRelation(
            "metadata.related_resources.qualified_relations.role",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("agent-roles"),
        ),
        related_resources_relation_type=PIDRelation(
            "metadata.related_resources.relation_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("relation-types"),
        ),
        time_references_date_type=PIDRelation(
            "metadata.related_resources.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
        related_resources_type=PIDRelation(
            "metadata.related_resources.type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        resource_type=PIDRelation(
            "metadata.resource_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        scheme=PIDRelation(
            "metadata.subjects.scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("subject-schemes"),
        ),
        access_rights=PIDRelation(
            "metadata.terms_of_use.access_rights",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        contacts_organization_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.organization.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        contacts_person_affiliations_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.person.affiliations.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        contacts_person_identifiers_identifier_scheme=PIDRelation(
            "metadata.terms_of_use.contacts.person.identifiers.identifier_scheme",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("identifier-schemes"),
        ),
        metadata_time_references_date_type=PIDRelation(
            "metadata.time_references.date_type",
            keys=["id", "title", {"key": "props.iri", "target": "iri"}],
            pid_field=Vocabulary.pid.with_type_ctx("time-reference-types"),
        ),
    )

    versions_model_cls = DatasetsParentState

    parent_record_cls = DatasetsParentRecord
    record_status = RecordStatusSystemField()

    has_draft = HasDraftCheckField(config_key="HAS_DRAFT_CUSTOM_FIELD")

    files = FilesField(file_cls=DatasetsFileDraft, store=False)

    bucket_id = ModelField(dump=False)
    bucket = ModelField(dump=False)


class RDMDraftMediaFiles(DatasetsDraft):
    """RDM Draft media file API."""

    files = FilesField(
        key=MediaFilesAttrConfig["_files_attr_key"],
        bucket_id_attr=MediaFilesAttrConfig["_files_bucket_id_attr_key"],
        bucket_attr=MediaFilesAttrConfig["_files_bucket_attr_key"],
        store=False,
        dump=False,
        file_cls=RDMMediaFileDraft,
        # Don't delete, we'll manage in the service
        delete=False,
    )


RDMMediaFileRecord.record_cls = RDMRecordMediaFiles
RDMMediaFileDraft.record_cls = RDMDraftMediaFiles

DatasetsFile.record_cls = DatasetsRecord

DatasetsFileDraft.record_cls = DatasetsDraft
