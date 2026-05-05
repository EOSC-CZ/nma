"""Search dumper extension for is_harvested flag."""

from __future__ import annotations

from invenio_db import db

from oarepo_oaipmh_harvester.oai_record.models import OAIHarvestedRecord

from invenio_records.dumpers import SearchDumperExt

class IsHarvestedDumperExt(SearchDumperExt):
    """Set is_harvested flag for harvested records."""

    def dump(self, record, data):
        is_harvested = False
        record_id = record.get("id")
        harvested = (
            db.session.query(OAIHarvestedRecord)
            .filter(OAIHarvestedRecord.record_pid == record_id)
            .order_by(OAIHarvestedRecord.harvested_at.desc())
            .first()
        )
        if harvested:
            is_harvested = True
        data["parent"]["is_harvested"] = is_harvested

        return data

    def load(self, record, data):
        parent = data.get("parent")
        if parent:
            parent.pop("is_harvested", None)

        return data
