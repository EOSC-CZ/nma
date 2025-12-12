from datetime import datetime, timedelta

from flask import current_app
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_base import invenio_url_for
from invenio_notifications.models import Notification, Recipient
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.resources.errors import PermissionDeniedError
from invenio_pidstore.errors import PIDAlreadyExists


from ..config import RIV_CURATORS_GROUP_ID, SECRET_LINK_EXPIRATION_DAYS
from ..errors import RIVRegistrationException
from .api import generate_id

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


def create_record(record_data):
    record_data["id"] = generate_id(record_data)
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
        draft_record = datasets_service.create(
            identity=system_identity, data=record_data
        )

        if draft_record.errors:
            raise RIVRegistrationException(
                f"Error during record creation of {record_data["id"]}: {draft_record.errors}"
            )

        datasets_service.publish(identity=system_identity, id_=draft_record["id"])

    except RIVRegistrationException:
        raise
    except PIDAlreadyExists:
        raise
    except Exception as e:
        raise RIVRegistrationException(
            f"Error during record creation/publishing of {record_data["id"]}: {e}"
        )
    # call access service and secret link
    access_service = (
        current_rdm_records_service.access
    )  # another solution: RecordAccessService(datasets_service.config)

    # prepare data for secret link creation
    data = {
        "permission": "edit",
        "description": f"Secret link for editing record for {user.email}",
        "expires_at": (
            datetime.today() + timedelta(days=SECRET_LINK_EXPIRATION_DAYS)
        ).strftime("%Y-%m-%d"),
    }

    # service returns only token
    service_result = access_service.create_secret_link(
        system_identity, draft_record["id"], data
    )
    token = service_result.data["token"]

    # build secret link URL
    values = {"pid_value": draft_record["id"], "token": token}
    secret_link = invenio_url_for("datasets_ui.deposit_edit", **values)

    # send email to the user with a secret link
    notification = Notification(
        type="data-riv-record-created",
        context={
            "record_data": record_data,
            "secret_link": secret_link,
            "expiration_time": str(SECRET_LINK_EXPIRATION_DAYS),
        },
    )
    recipient = Recipient(data={"preferences": user.preferences, "email": user.email})

    email_backend_cls = notification_backends.get("email")
    email_backend = email_backend_cls()
    email_backend.send(notification, recipient)

    # Grant the curators group manage permission (as a support). For example to be able to create a new secret link if needed.
    _ = access_service.bulk_create_grants(
        identity=system_identity, id_=draft_record["id"], data=grant_data
    )

    return secret_link
