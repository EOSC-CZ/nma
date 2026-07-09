"""Helpers for OAI-PMH provenance <about> serialization."""

from __future__ import annotations

from datetime import UTC, datetime
from invenio_db import db
from lxml import etree
from oarepo_oaipmh_harvester.oai_record.models import OAIHarvestedRecord

NS_OAIPMH = "http://www.openarchives.org/OAI/2.0/"
NS_PROV = "http://www.openarchives.org/OAI/2.0/provenance"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
DEFAULT_METADATA_NAMESPACE = "http://www.openarchives.org/OAI/2.0/oai_dc/"
PROV_SCHEMA_LOCATION = (
    "http://www.openarchives.org/OAI/2.0/provenance "
    "http://www.openarchives.org/OAI/2.0/provenance.xsd"
)


def _to_utc_z(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    else:
        dt = dt.astimezone(UTC)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_provenance_element(harvested: OAIHarvestedRecord) -> etree._Element | None:
    base_url = getattr(harvested.harvester, "base_url", None)
    identifier = harvested.oai_identifier
    datestamp = _to_utc_z(harvested.datestamp)
    harvest_date = _to_utc_z(harvested.harvested_at)
    metadata_namespace = DEFAULT_METADATA_NAMESPACE

    if not (base_url and identifier and datestamp and harvest_date and metadata_namespace):
        return None

    e_provenance = etree.Element(
        etree.QName(NS_PROV, "provenance"),
        nsmap={None: NS_PROV, "xsi": NS_XSI},
    )
    e_provenance.set(etree.QName(NS_XSI, "schemaLocation"), PROV_SCHEMA_LOCATION)

    e_origin = etree.SubElement(e_provenance, etree.QName(NS_PROV, "originDescription"))
    e_origin.set("altered", "true")
    e_origin.set("harvestDate", harvest_date)

    etree.SubElement(e_origin, etree.QName(NS_PROV, "baseURL")).text = base_url
    etree.SubElement(e_origin, etree.QName(NS_PROV, "identifier")).text = identifier
    etree.SubElement(e_origin, etree.QName(NS_PROV, "datestamp")).text = datestamp
    etree.SubElement(
        e_origin,
        etree.QName(NS_PROV, "metadataNamespace"),
    ).text = metadata_namespace
    return e_provenance


def aire_about_etree(pid, record, **kwargs):  # noqa: ARG001
    """Return provenance XML element for an OAI record about block.

    The function is intended to be used as ``about_serializer`` callback.
    """
    source = record.get("_source", {}) if isinstance(record, dict) else {}
    record_id = source.get("id")
    if not record_id:
        return None

    harvested = (
        db.session.query(OAIHarvestedRecord)
        .filter(OAIHarvestedRecord.record_pid == record_id)
        .order_by(OAIHarvestedRecord.harvested_at.desc())
        .first()
    )
    if not harvested:
        return None

    return _build_provenance_element(harvested)
