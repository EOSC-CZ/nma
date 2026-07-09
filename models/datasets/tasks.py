from __future__ import annotations

import datetime
from functools import wraps
from typing import TYPE_CHECKING, cast, Any

from celery import shared_task
from flask import current_app
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

# invenio unit_of_work decorator crashes without a positional arg
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
    return next(x for x in current_runtime.rdm_models if x.code == "datasets")

def _find_editor(editors: list[dict[str, Any]], id_: str)-> dict[str, Any] | None:
    for editor in editors:
        if editor["id"] == id_:
            return editor
    return None

def _create_editor(user: User, expiration: str, access_granted: str) -> dict:
    return {
        "id": str(user.id),
        "full_name": user.user_profile.get("full_name", ""),
        "affiliations": user.user_profile.get("affiliations", ""),
        "expiration": expiration,
        "access_granted": [access_granted],
    }

def _commit_editors(editors: list[dict[str, Any]], id: str, uow: UnitOfWork)->None:
    service = _get_model().service
    record = service.read(system_identity, id)._record
    record["editors"] = editors
    uow.register(RecordCommitOp(record, indexer=service.indexer, index_refresh=True))


@unit_of_work
def add_grant_expiration(uow: UnitOfWork=None)->None:
    now = datetime.datetime.now()
    expiration = (now + datetime.timedelta(days=EDIT_GRANT_EXPIRATION_DAYS)).isoformat()
    access_granted = now.isoformat()
    model = _get_model().record_cls.model_cls
    records = model.query.all()

    for record_data in records:
        editors = record_data.data.get("editors", [])
        edited = False

        for grant in record_data.parent.data["access"]["grants"]:
            if grant["subject"]["type"] != "user" or grant["permission"] != "edit":
                continue

            user_id = grant["subject"]["id"]
            editor = _find_editor(editors, user_id)

            # doesn't need updating
            if editor and "expiration" in editor:
                continue

            if editor:
                editor["expiration"] = expiration
                editor.setdefault("access_granted", []).append(access_granted)
            else:
                user = User.query.filter_by(id=user_id).one()
                editors.append(_create_editor(user, expiration, access_granted))

            edited = True

        if edited:
            _commit_editors(editors, record_data.data["id"], uow)


@unit_of_work
def expire_grants(uow: UnitOfWork=None)->None:
    now = datetime.datetime.now()
    service = _get_model().service
    access_service = current_rdm_records_service.access
    records_with_expired_grants = service.scan(
        identity=system_identity,
        extra_filter=dsl.Q("range", **{"editors.expiration": {"lt": now.isoformat()}}),
    )

    for record_data in records_with_expired_grants:
        record_id = record_data["id"]
        editors = record_data["editors"]

        expired_editors = [
            e
            for e in editors
            if "expiration" in e
            and datetime.datetime.fromisoformat(e["expiration"]) < now
        ]

        for editor in expired_editors:
            try:
                access_service.delete_grant_by_subject(
                    system_identity,
                    record_id,
                    editor["id"],
                    subject_type="user",
                    uow=uow,
                )
            except Exception:
                current_app.logger.exception("Failed to delete grant for editor %s", editor)
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
