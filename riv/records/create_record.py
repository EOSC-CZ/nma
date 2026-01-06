from datetime import datetime, timedelta

from flask import current_app, url_for
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_notifications.models import Notification, Recipient
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.resources.errors import PermissionDeniedError

from ..config import EDIT_GRANT_EXPIRATION_DAYS, RIV_CURATORS_GROUP_ID
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
    if not record_data:
        record_data = {"metadata": {}}
    if not record_data.get("metadata"):
        record_data["metadata"] = {}
    metadata = record_data["metadata"]
    for key, value in empty_metadata.items():
        metadata.setdefault(key, value)

    record_data["id"] = generate_id(persistent_url)
    if current_user.is_anonymous:
        raise PermissionDeniedError("Please login first.")

    notification_backends = current_app.config.get("NOTIFICATION_BACKENDS", {})
    if not notification_backends.get("email"):
        raise RuntimeError("Email notification backend is not configured.")

    user = User.query.filter(User.id == current_user.id).one()

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
            "Due to an unexpected error, the data could not be loaded correctly. Please fill in the required information and save the record again. "
            draft_record =  datasets_service.update_draft(system_identity, data=draft_record.data, id_ = record_data["id"])
            problems.append(
                ResolverProblem(
                    resolver="record_creation",
                    message=_(f"Due to an unexpected error, the data could not be loaded correctly. "
                              f"Please fill in the required information and save the record. "),
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
    # call access service and grant

    user_grant_data = {
        "grants": [
            {
                "subject": {"type": "user", "id": str(user.id)},
                "permission": "edit",
                "notify": False,  # TODO: Could be False?
                "message": "expires in:"
                + (
                    datetime.today() + timedelta(days=EDIT_GRANT_EXPIRATION_DAYS)
                ).strftime("%Y-%m-%d"),
            }
        ]
    }
    access_service = current_rdm_records_service.access

    service_result = access_service.bulk_create_grants(
        system_identity, draft_record["id"], user_grant_data
    )

    edit_link = url_for(
        "datasets_ui.deposit_edit", pid_value=published_record["id"], _external=True
    )

    try:
        # send email to the user with an editation link
        notification = Notification(
            type="data-riv-record-created",
            context={
                "record_data": record_data,
                "expiration_time": str(EDIT_GRANT_EXPIRATION_DAYS),
                "edit_link": edit_link,
            },
        )
        recipient = Recipient(
            data={"preferences": user.preferences, "email": user.email}
        )

        email_backend_cls = notification_backends.get("email")
        email_backend = email_backend_cls()
        email_backend.send(notification, recipient)
    except Exception as ex:
        current_app.logger.exception(
            f"Error sending notification email for record {draft_record['id']}"
        )
        problems.append(
            ResolverProblem(
                "notification",
                f"Error sending notification email to {user.email}.",
                level=ResolverProblemLevel.WARNING,
                original_exception=ex,
            )
        )

    try:
        # Grant the curators group manage permission (as a support).
        _ = access_service.bulk_create_grants(
            identity=system_identity, id_=draft_record["id"], data=grant_data
        )
    except Exception:
        current_app.logger.exception(
            f"Error granting manage permission to curators group for record {draft_record['id']}"
        )

    return published_record
