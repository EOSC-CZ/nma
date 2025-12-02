from datetime import datetime, timedelta

from flask import current_app
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_base import invenio_url_for
from invenio_notifications.models import Notification, Recipient
from invenio_rdm_records.services.access.service import RecordAccessService
from invenio_records_resources.proxies import current_service_registry

from ..config import SECRET_LINK_EXPIRATION_DAYS

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


def create_record(record_data):
    import debugpy

    try:
        debugpy.listen(("127.0.0.1", 5678))
        debugpy.wait_for_client()
        print("🚀 Debugger attached!")

    except Exception as e:
        print(f"⚠️  Failed to start debugpy listener: {e}")

    if current_user.is_anonymous:
        raise ValueError("Please login first.")
    user = User.query.filter(User.id == current_user.id).one()

    # TODO: change to record data
    example_data["files"] = {"enabled": False}

    # create and publish
    datasets_service = current_service_registry.get("datasets")
    draft_record = datasets_service.create(identity=system_identity, data=example_data)
    published_record = datasets_service.publish(
        identity=system_identity, id_=draft_record["id"]
    )

    # call access service and secret link
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

    # grant na skupinu GrantSubject(type = role, , id = id skupina z configu), can_manage pravo
    # jedna genericka grupa (treba support)

    # return URL
    return "created_record_url"
