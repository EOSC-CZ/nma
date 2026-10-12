from datetime import datetime, timedelta
from typing import Any

from flask import current_app
from flask_login import current_user
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_notifications.proxies import current_notifications_manager
from invenio_rdm_records.proxies import current_rdm_records_service
from oarepo_related_resources.resolvers.base import ResolverProblem, ResolverProblemLevel

from riv.config import EDIT_GRANT_EXPIRATION_DAYS
from riv.notifications.builders import DatasetEditGrantNotificationBuilder

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
    try:
        notification = DatasetEditGrantNotificationBuilder.build(
            record_id=record_data["id"],
            user=user,
            expiration_time=EDIT_GRANT_EXPIRATION_DAYS,
        )
        current_notifications_manager.broadcast(notification)
    except Exception as ex:
        current_app.logger.exception(
            "Error sending notification email for record %s.", record_data["id"]
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
