from datetime import datetime, timedelta

from flask import current_app
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_base import invenio_url_for
from invenio_notifications.models import Notification, Recipient
from invenio_rdm_records.services.access.service import RecordAccessService
from invenio_records_resources.proxies import current_service_registry

from ..config import RIV_CURATORS_GROUP_ID, SECRET_LINK_EXPIRATION_DAYS

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
    }
}


grant_data = {
    "grants": [
        {
            "subject": {"type": "role", "id": RIV_CURATORS_GROUP_ID},
            "permission": "manage",
            "notify": True,  # Could be False?
        }
    ]
}


def create_record(record_data):
    if current_user.is_anonymous:
        raise ValueError("Please login first.")
    user = User.query.filter(User.id == current_user.id).one()

    # TODO: change to record data
    example_data["files"] = {"enabled": False}

    # create and publish
    datasets_service = current_service_registry.get("datasets")
    draft_record = datasets_service.create(identity=system_identity, data=example_data)
    _ = datasets_service.publish(identity=system_identity, id_=draft_record["id"])

    # call access service and secret link
    # TODO: is there a better way to get access service? Maybe from datasets_service directly?
    access_service = RecordAccessService(datasets_service.config)

    # create_secret_link
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
            "record_data": example_data,  # TODO: change to record data
            "secret_link": secret_link,
            "expiration_time": f"{SECRET_LINK_EXPIRATION_DAYS}",
        },
    )
    recipient = Recipient(data={"preferences": user.preferences, "email": user.email})

    email_backend = current_app.config["NOTIFICATION_BACKENDS"]["email"]()
    email_backend.send(notification, recipient)

    # Grant the curators group manage permission (as a support). For example to be able to create a new secret link if needed.
    _ = access_service.bulk_create_grants(
        identity=system_identity, id_=draft_record["id"], data=grant_data
    )

    return secret_link
