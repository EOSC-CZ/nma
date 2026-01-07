from datetime import datetime, timedelta
from typing import Any

from flask import current_app, url_for
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_notifications.models import Notification, Recipient
from invenio_rdm_records.proxies import current_rdm_records_service

from riv.config import EDIT_GRANT_EXPIRATION_DAYS
from riv.resolvers.base import ResolverProblem, ResolverProblemLevel

# moving riv/records as the only other module that isn't in riv/resolvers with ResolverProblem dependency is there

def create_user_edit_grant(user: User, record_id: str) -> None:
    expiration_date = (datetime.today() + timedelta(days=EDIT_GRANT_EXPIRATION_DAYS)).strftime("%Y-%m-%d")
    user_grant_data = {
        "grants": [
            {
                "subject": {"type": "user", "id": str(user.id)},
                "permission": "edit",
                "notify": False,
                "message": f"expires in: {expiration_date}",
            }
        ]
    }

    current_rdm_records_service.access.bulk_create_grants(
        system_identity, record_id, user_grant_data
    )



def send_user_edit_grant_notification(user: User, record_data: dict[str, Any], problems: list[ResolverProblem]) -> None:
    notification_backends = current_app.config.get("NOTIFICATION_BACKENDS", {})
    if not notification_backends.get("email"):
        raise RuntimeError("Email notification backend is not configured.")
    edit_link = url_for(
        "datasets_ui.deposit_edit", pid_value=record_data["id"], _external=True
    )
    try:
        # send email to the user with an edit link
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
            f"Error sending notification email for record %s.", record_data['id']
        )
        problems.append(
            ResolverProblem(
                "notification",
                f"Error sending notification email to {user.email}.",
                level=ResolverProblemLevel.WARNING,
                original_exception=ex,
            )
        )


def user_edit_grant_and_notification(record_data: dict[str, Any], problems: list[ResolverProblem])->None:
    user = User.query.filter(User.id == current_user.id).one()
    create_user_edit_grant(user, record_data["id"])
    send_user_edit_grant_notification(user, record_data, problems)