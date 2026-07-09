"""
Structured collections of research data, identified with a persistent identifier
"""

from __future__ import annotations

from flask_principal import RoleNeed
from invenio_access import action_factory
from invenio_administration.generators import Administration
from invenio_rdm_records.services.generators import AccessGrant
from invenio_records_permissions.generators import (
    AuthenticatedUser,
    Disable,
    Generator,
    SystemProcess,
)
from oarepo_model.model import ModelMixin

manage_record_action = action_factory("manage-record")


# TODO: manage-record seems not to work if assigned to role and not to user
# not sure why, the current workaround is to require riv_curators role
# directly, without the action
class RecordManagement(Generator):
    """Allows record management access."""

    def __init__(self):
        """Constructor."""
        super(RecordManagement, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [manage_record_action]


class RIVCurators(Generator):
    """Allows access to users with riv_curators role."""

    def __init__(self):
        """Constructor."""
        super(RIVCurators, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("riv_curators")]


class DatasetsPermissionPolicyMixin(ModelMixin):
    """Custom permission policy for datasets."""

    can_view_deposit_page = [AuthenticatedUser()]
    can_update = [
        AccessGrant("edit"),
        SystemProcess(),
        Administration(),
    ]  # system process can update records (in tasks etc)

    can_create = [
        SystemProcess(),
        Administration(),
    ]  # only system process and admin can create records
    can_publish = [
        SystemProcess(),
        Administration(),
    ]  # only system process and admin can publish records

    can_manage = [
        SystemProcess(),
        Administration(),
        AccessGrant("manage"),
        RecordManagement(),
        RIVCurators(),
    ]

    can_draft_create_files = [Disable()]  # disable files by default
    can_update_draft = [SystemProcess(), Administration()]
