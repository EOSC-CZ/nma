from invenio_notifications.services.generators import ContextGenerator
from invenio_rdm_records.notifications.builders import GrantUserAccessNotificationBuilder as InvenioGrantUserAccessNotificationBuilder
from invenio_records.dictutils import dict_set
from riv.config import EDIT_GRANT_EXPIRATION_DAYS


class ExpirationContextGenerator(ContextGenerator):
    """Payload generator for a notification using the entity resolvers."""

    def __call__(self, notification):
        """Update required recipient information and add backend id."""
        dict_set(notification.context, "expiration", str(EDIT_GRANT_EXPIRATION_DAYS))
        return notification

class GrantUserAccessNotificationBuilder(InvenioGrantUserAccessNotificationBuilder):
    """Notification builder for user access grant."""

    context = InvenioGrantUserAccessNotificationBuilder.context + [ExpirationContextGenerator()]