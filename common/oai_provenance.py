"""Inject OAI-PMH provenance <about> blocks into OAI record responses."""
from __future__ import annotations

from datetime import UTC, datetime
from functools import wraps

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


def _append_about_block(app, e_record, harvested: OAIHarvestedRecord) -> None:
    base_url = getattr(harvested.harvester, "base_url", None)
    identifier = harvested.oai_identifier
    datestamp = _to_utc_z(harvested.datestamp)
    harvest_date = _to_utc_z(harvested.harvested_at)
    metadata_namespace = DEFAULT_METADATA_NAMESPACE

    if not (base_url and identifier and datestamp and harvest_date and metadata_namespace):
        return

    e_about = etree.SubElement(e_record, etree.QName(NS_OAIPMH, "about"))
    e_provenance = etree.SubElement(
        e_about,
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


def _extract_and_remove_pid(e_record) -> str | None:
    pid_nodes = e_record.xpath(
        "./oai:metadata//*[local-name()='pid']",
        namespaces={"oai": NS_OAIPMH},
    )
    if not pid_nodes:
        return None

    pid_node = pid_nodes[0]
    pid_value = pid_node.text
    parent = pid_node.getparent()
    if parent is not None:
        parent.remove(pid_node)

    return pid_value or None


def _inject_provenance_into_tree(app, e_tree) -> None:
    records = e_tree.xpath("//oai:record", namespaces={"oai": NS_OAIPMH})
    if not records:
        return

    for e_record in records:
        pid = _extract_and_remove_pid(e_record)
        if not pid:
            continue

        harvested = (
            db.session.query(OAIHarvestedRecord)
            .filter(OAIHarvestedRecord.record_pid == pid)
            .order_by(OAIHarvestedRecord.harvested_at.desc())
            .first()
        )
        if not harvested:
            continue
        _append_about_block(app, e_record, harvested)


def _patch_oaiserver_response(app) -> None:
    import invenio_oaiserver.response as oai_response

    original_getrecord = oai_response.getrecord
    original_listrecords = oai_response.listrecords

    @wraps(original_getrecord)
    def patched_getrecord(**kwargs):
        e_tree = original_getrecord(**kwargs)
        _inject_provenance_into_tree(app, e_tree)
        return e_tree

    @wraps(original_listrecords)
    def patched_listrecords(**kwargs):
        e_tree = original_listrecords(**kwargs)
        _inject_provenance_into_tree(app, e_tree)
        return e_tree

    oai_response.getrecord = patched_getrecord
    oai_response.listrecords = patched_listrecords



class OAIProvenanceExt:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        _patch_oaiserver_response(app)
        app.extensions["oai-provenance"] = self
