from __future__ import annotations

import datetime
from functools import wraps
from typing import TYPE_CHECKING, cast

from celery import shared_task
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_db import db
from invenio_db.uow import UnitOfWork
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import RecordCommitOp
from invenio_search.engine import dsl
from oarepo_runtime import current_runtime

from riv.config import EDIT_GRANT_EXPIRATION_DAYS

if TYPE_CHECKING:

    from invenio_records_resources.services.records import RecordService


def unit_of_work(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if "uow" not in kwargs or kwargs["uow"] is None:
            # Migration path - start a UoW and commit
            with UnitOfWork(db.session) as uow:
                kwargs["uow"] = uow
                res = f(*args, **kwargs)
                uow.commit()
                return res
        else:
            return f(*args, **kwargs)

    return inner


def _get_model():
    return current_runtime.rdm_models[0]


def _find_editor(editors, id_):
    for editor in editors:
        if editor["id"] == id_:
            return editor
    return None


def _commit_editors(editors, id, uow):
    service = _get_model().service
    record = service.read(system_identity, id)._record
    record["editors"] = editors
    uow.register(RecordCommitOp(record))


# unit_of_work decorator crashes without a positional arg
@unit_of_work
def add_grant_expiration(uow=None):
    model = _get_model().record_cls.model_cls
    records = model.query.all()
    for record_data in records:
        editors = record_data.data.get("editors", [])
        edited = False
        for grant in record_data.parent.data["access"]["grants"]:
            if grant["subject"]["type"] == "user":
                editor = _find_editor(editors, grant["subject"]["id"])
                # expiration either added or waiting to be collected; don't prolong
                if editor and "expiration" in editor:
                    continue

                time_now = datetime.datetime.now()
                expiration = (
                    time_now + datetime.timedelta(days=EDIT_GRANT_EXPIRATION_DAYS)
                ).isoformat()
                access_granted = time_now.isoformat()
                if not editor:
                    user = User.query.filter_by(id=grant["subject"]["id"]).one()
                    editor = {
                        "id": str(user.id),
                        "full_name": user.user_profile.get("full_name", ""),
                        "affiliations": user.user_profile.get("affiliations", ""),
                        "expiration": expiration,
                        "access_granted": [access_granted],
                    }
                    editors.append(editor)
                else:
                    editor["expiration"] = expiration
                    editor.setdefault("access_granted", []).append(access_granted)
                edited = True
        if edited:
            _commit_editors(editors, record_data.data["id"], uow)


@unit_of_work
def expire_grants(uow=None):
    now = datetime.datetime.now()
    service = _get_model().service
    access_service = current_rdm_records_service.access
    with_expired_grants = service.scan(
        identity=system_identity,
        extra_filter=dsl.Q("range", **{"editors.expiration": {"lt": now.isoformat()}}),
    )
    for expired_record_data in with_expired_grants:
        record_id = expired_record_data["id"]
        editors = expired_record_data["editors"]
        expired_editors = [
            e for e in editors if "expiration" in e and datetime.datetime.fromisoformat(e["expiration"]) < now
        ]
        for expired_editor in expired_editors:
            r = access_service.delete_grant_by_subject(
                system_identity,
                record_id,
                expired_editor["id"],
                subject_type="user",
                uow=uow,
            )

        expired_editor_ids = {
            expired_editor["id"] for expired_editor in expired_editors
        }
        for editor in editors:
            if editor["id"] in expired_editor_ids:
                del editor["expiration"]
        _commit_editors(editors, record_id, uow)


@shared_task
def expire_grants_task():
    expire_grants()


@shared_task
def add_grant_expiration_task():
    add_grant_expiration()


@shared_task
def create_vocabulary_item_task(vocabulary_service_id: str, data: dict) -> dict:
    """Create a vocabulary item."""
    vocab_service = cast(
        "RecordService", current_service_registry.get(vocabulary_service_id)
    )
    try:
        return vocab_service.read(system_identity, data["id"]).to_dict()
    except Exception:
        pass  # item does not exist yet
    ret = vocab_service.create(system_identity, data)
    return ret.to_dict()
