from flask import current_app
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.resources.errors import PermissionDeniedError

from ..config import RIV_CURATORS_GROUP_ID
from ..errors import RIVRegistrationException
from ..resolvers.base import ResolverProblem, ResolverProblemLevel
from .api import generate_id
from riv.resolvers.base import TITLE_PLACEHOLDER, CREATORS_PLACEHOLDER, PUBLICATION_DATE_PLACEHOLDER, RESOURCE_TYPE_PLACEHOLDER
example_data = {
    "metadata": {
        "creators": [
            {
                "person_or_org": {
                    "family_name": "First",
                    "given_name": "Creator",
                    "name": "First, Creator",
                    "type": "personal",
                }
            },
            {
                "person_or_org": {
                    "family_name": "Second",
                    "given_name": "Creator",
                    "name": "Second, Creator",
                    "type": "personal",
                }
            },
        ],
        "publication_date": "2025-12-02",
        "resource_type": {
            "id": "dataset",
        },
        "title": "example title for riv",
        "blah": "blah",
    },
    "id": "doi:10.5281/zenodo.17801700",
}

# It will always be the same data that is beeing sent to grant service
grant_data = {
    "grants": [
        {
            "subject": {"type": "role", "id": RIV_CURATORS_GROUP_ID},
            "permission": "manage",
            "notify": True,  # TODO: Could be False?
        }
    ]
}


def create_record(record_data, persistent_url, problems):
    empty_metadata = {
        "title": TITLE_PLACEHOLDER,
        "publication_date": PUBLICATION_DATE_PLACEHOLDER,
        "creators": CREATORS_PLACEHOLDER,
        "resource_type": {"id": RESOURCE_TYPE_PLACEHOLDER},
        "persistent_url": persistent_url,
    }
    metadata = record_data["metadata"]
    for key, value in empty_metadata.items():
        metadata.setdefault(key, value)

    # disable files by default
    record_data = {**record_data, "files": {"enabled": False}}

    # create and publish
    datasets_service = current_service_registry.get("datasets")

    try:
        record = datasets_service.read(identity=system_identity, id_=record_data["id"])
        raise PIDAlreadyExists(
            pid_value=record_data["id"], pid_type=record._record.pid.pid_type
        )
    except PIDAlreadyExists:
        raise
    except Exception:
        # record does not exist, continue
        pass

    try:

        draft_record = datasets_service.create(
            identity=system_identity, data=record_data
        )

        if draft_record.errors:
            empty_metadata["persistent_url"] = draft_record.data["metadata"]["persistent_url"]
            draft_record.data["metadata"] = empty_metadata
            from invenio_i18n import lazy_gettext as _

            draft_record =  datasets_service.update_draft(system_identity, data=draft_record.data, id_ = record_data["id"])
            problems.append(
                ResolverProblem(
                    resolver="record_creation",
                    message=_("Due to an unexpected error, the data could not be loaded correctly. "
                              "Please fill in the required information and save the record. "),
                    level=ResolverProblemLevel.ERROR,
                )
            )
            current_app.logger.exception(
                "Resolver did not catch the following problems for record_id=%s: %s",
                    record_data["id"],
                        draft_record.errors,
            )

        published_record = datasets_service.publish(
            identity=system_identity, id_=record_data["id"]
        )

    except PIDAlreadyExists:
        raise

    except Exception as e:
        raise RIVRegistrationException(
            f"Error during record creation/publishing of {record_data["id"]}: {e}"
        )

    try:
        # Grant the curators group manage permission (as a support).
        _ = current_rdm_records_service.access.bulk_create_grants(
            identity=system_identity, id_=draft_record["id"], data=grant_data
        )
    except Exception:
        current_app.logger.exception(
            f"Error granting manage permission to curators group for record {draft_record['id']}"
        )

    return published_record
