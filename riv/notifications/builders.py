"""Notification builders for the RIV dataset registration flow.

Standardized on the Invenio-RDM 14 ``invenio-notifications`` builder/registry
system (the same mechanism used for requests and grant-access notifications),
replacing the previous ad-hoc direct-backend send. The email template
(``dataset-edit-grant.jinja``) renders the edit link from the resolved record's
``links.edit_html``, which is permission-gated (``has_permission("update")``) so
the link is only present when the recipient may actually edit.
"""

from invenio_notifications.models import Notification
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.generators import EntityResolve, UserEmailBackend
from invenio_users_resources.notifications.filters import UserPreferencesRecipientFilter
from invenio_users_resources.notifications.generators import UserRecipient


class DatasetEditGrantNotificationBuilder(NotificationBuilder):
    """Notification builder for granting a user edit access to a dataset record."""

    type = "dataset-edit-grant"

    @classmethod
    def build(cls, record_id, user, expiration_time):
        """Build notification referencing the record and the granted user.

        :param record_id: The pid of the dataset record.
        :param user: The ``User`` (id resolvable via the ``user`` entity resolver).
        :param expiration_time: Number of days the edit grant is valid for.
        """
        return Notification(
            type=cls.type,
            context={
                "record": {"datasets": str(record_id)},
                "recipient_user": {"user": str(user.id)},
                "expiration_time": str(expiration_time),
            },
        )

    context = [
        EntityResolve(key="record"),
        EntityResolve(key="recipient_user"),
    ]

    recipients = [
        UserRecipient(key="recipient_user"),
    ]

    recipient_filters = [
        UserPreferencesRecipientFilter(),
    ]

    recipient_backends = [
        UserEmailBackend(),
    ]
