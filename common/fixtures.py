# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o
# SPDX-License-Identifier: MIT

"""Communities fixture that can be re-run after the initial setup.

Registered as the ``communities`` entry of the ``oarepo.fixtures`` entry-point group, so

    invenio rdm-records add-to-fixture communities

creates the communities of ``app_data/communities.yaml`` that do not exist yet (plain RDM
``add-to-fixture`` reloads vocabularies only). Existing communities are left untouched.
The communities are created right away, no celery worker is needed. Logos are uploaded
from ``app_data/img``; a failed upload is logged and the community is kept without it.

``invenio rdm-records fixtures`` runs it too, after RDM's own communities fixture.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities
from invenio_db import db
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_rdm_records.fixtures.fixture import FixtureMixin

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


class CommunitiesFixture(FixtureMixin):
    """Create the communities of ``communities.yaml`` that do not exist yet."""

    def __init__(self, search_paths: list[Path], filename: str) -> None:
        """Initialize the fixture with the folders to look for ``filename`` in."""
        super().__init__(search_paths, filename, delay=False)

    def load(self) -> None:
        """Load the first ``filename`` found, remembering its folder for the logos."""
        self._folder = next((p for p in self._search_paths if (p / self._filename).exists()), None)
        super().load()

    def create(self, entry: dict[str, Any]) -> None:
        """Create the community unless a community with its slug exists."""
        service = current_communities.service
        slug = entry["slug"]
        try:
            service.record_cls.pid.resolve(slug)
        except PIDDoesNotExistError:
            pass
        else:
            log.info("Community %s exists, skipped.", slug)
            return

        logo = entry.pop("logo", None)
        feature = entry.pop("feature", False)
        community = service.create(system_identity, entry)
        db.session.commit()
        log.info("Community %s created.", slug)

        if feature:
            start_date = datetime.now(UTC).isoformat()
            service.featured_create(system_identity, community.id, {"start_date": start_date})
            db.session.commit()
        if logo and self._folder:
            try:
                with (self._folder / "img" / logo).open("rb") as stream:
                    service.update_logo(system_identity, community.id, stream)
                db.session.commit()
            except Exception:
                db.session.rollback()
                log.exception("Logo %s of community %s not uploaded.", logo, slug)
