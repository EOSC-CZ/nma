# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
# SPDX-License-Identifier: MIT
"""Page validating one harvested OAI-PMH record: /harvest/validate. See validation.md.

The page runs one transformer, the schema and the relation checks on a single record and
creates no dataset. Resolving ORCID and ROR identifiers may create their vocabulary records.
"""

from __future__ import annotations

import ipaddress
import json
import re
import socket
import time
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit

import httpx
import requests
from flask import Blueprint, Flask, Response, current_app, redirect, render_template, request, session, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from invenio_access.permissions import system_identity
from invenio_i18n import lazy_gettext as _
from invenio_records.systemfields.relations import RelationError
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.factories import TransformerFactory
from lxml import etree
from markupsafe import Markup
from marshmallow import ValidationError
from oaipmh_scythe.models import Record
from oarepo_oaipmh_harvester.datastream import CatchingTransformer
from oarepo_oaipmh_harvester.writers.oai_service import OAIServiceWriter, _flatten_messages
from oarepo_runtime import current_runtime
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer, XmlLexer
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import ValidationError as WTFormsValidationError

from ccmm_invenio.services.components.fetch_identifiers import resolve_identifiers

if TYPE_CHECKING:
    from collections.abc import Iterator

OAI = "{http://www.openarchives.org/OAI/2.0/}"
MODEL = "datasets"
MAX_XML_BYTES = 1_000_000
FETCH_SECONDS = 15
SESSION_KEY = "harvest_validate_form"
VOCABULARY_ELEMENTS = {"iri", "label"}  # vocabulary references become ids, so their values are expected to go
SOURCE_COPY_KEYS = {"ccmm_xml"}  # holds the source XML itself, so everything would seem converted

# Addresses that are_global() still calls public, but that a server must not contact.
NAT64_PREFIXES = (
    ipaddress.IPv6Network("64:ff9b::/96"),
    ipaddress.IPv6Network("64:ff9b:1::/48"),
)

Raw = tuple[dict[str, Record], list[str]]


class TimedSession(requests.Session):
    """Session with a short timeout, so an unresponsive ROR cannot hold a web worker."""

    def request(self, *args: Any, **kwargs: Any) -> requests.Response:
        """Use the page's timeout, not the longer ROR_TIMEOUT that harvests use."""
        kwargs["timeout"] = FETCH_SECONDS
        return super().request(*args, **kwargs)


def is_public_address(address: str) -> bool:
    """Return whether an address is a public unicast one (not private, multicast or NAT64)."""
    ip = ipaddress.ip_address(address)
    if ip.is_multicast or not ip.is_global:
        return False
    return not (isinstance(ip, ipaddress.IPv6Address) and any(ip in net for net in NAT64_PREFIXES))


def check_public_url(url: str) -> None:
    """Refuse URLs that would make the server call an internal address."""
    # ponytail: DNS can change between this check and the request (rebinding). Pin the resolved IP
    # in the HTTP client if that becomes a real concern.
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("Only http(s) URLs are allowed")
    for *_rest, addr in socket.getaddrinfo(parts.hostname, parts.port or 443):
        if not is_public_address(addr[0]):
            raise ValueError("The URL must point to a public address")


def wrap_metadata(root: etree._Element) -> etree._Element | None:
    """Put pasted <metadata> content into a record with a placeholder header; None if it is not metadata."""
    name = etree.QName(root)
    is_oai = root.tag.startswith(OAI)
    if (is_oai and name.localname != "metadata") or (
        name.namespace is None and name.localname in {"record", "OAI-PMH", "metadata"}  # a forgotten xmlns
    ):
        return None
    record = etree.Element(f"{OAI}record", nsmap={None: OAI[1:-1]})
    header = etree.SubElement(record, f"{OAI}header")
    etree.SubElement(header, f"{OAI}identifier").text = "pasted-metadata"
    etree.SubElement(header, f"{OAI}datestamp").text = "1970-01-01"
    if is_oai:
        record.append(root)
    else:
        etree.SubElement(record, f"{OAI}metadata").append(root)
    return record


def read_xml(xml: bytes, encoding: str | None = None, allow_metadata: bool = False) -> Raw:
    """Parse an OAI-PMH response or a single <record>; return (reader-like entry, warnings).

    `encoding` overrides the XML declaration, which a paste may state wrongly. With
    `allow_metadata`, the <metadata> element or just its content is accepted as well.
    """
    parser = etree.XMLParser(
        remove_blank_text=True, recover=True, resolve_entities=False, encoding=encoding
    )  # as scythe
    root = etree.XML(xml, parser=parser)
    warnings = [e.message for e in parser.error_log]  # truncated XML recovers silently!
    if root is not None and (error := root.find(f"{OAI}error")) is not None:
        raise ValueError(f"{error.get('code')}: {error.text}")
    records = [] if root is None else [root] if root.tag == f"{OAI}record" else list(root.iter(f"{OAI}record"))
    if not records and root is not None and allow_metadata and (wrapped := wrap_metadata(root)) is not None:
        records = [wrapped]
        warnings.append("Only metadata was pasted: a placeholder OAI header was added and the real one wasn't checked")
    if len(records) != 1:
        raise ValueError(f"Expected one <record> in the OAI-PMH namespace, found {len(records)}: {warnings}")
    try:
        record = Record(records[0], strip_ns=True)
    except (AttributeError, IndexError) as e:  # scythe's error for a missing or empty <metadata>
        raise ValueError("The record has no <metadata> content") from e
    if not record.header.identifier or not record.header.datestamp:
        raise ValueError("The record has no identifier or datestamp")
    return {"record": record}, warnings


def download(base_url: str, params: dict[str, str]) -> bytes:
    """Call an OAI-PMH source; the oai-pmh reader has a fixed 60 s timeout and no size limit."""
    check_public_url(base_url)
    deadline = time.monotonic() + FETCH_SECONDS
    body = bytearray()
    with httpx.stream("GET", base_url, params=params, timeout=5) as response:
        response.raise_for_status()  # also rejects redirects, httpx doesn't follow them
        for chunk in response.iter_bytes():
            body += chunk
            if len(body) > MAX_XML_BYTES:
                raise ValueError(f"Response is larger than {MAX_XML_BYTES} bytes")
            if time.monotonic() > deadline:
                raise ValueError(f"Response took longer than {FETCH_SECONDS} s")
    return bytes(body)


def read_fetch(base_url: str, metadata_prefix: str, identifier: str) -> Raw:
    """Download one record."""
    params = {"verb": "GetRecord", "metadataPrefix": metadata_prefix, "identifier": identifier}
    return read_xml(download(base_url, params))


def oai_verb(base_url: str, verb: str) -> etree._Element:
    """Return the element with the answer of an OAI-PMH verb; an OAI error becomes a ValueError."""
    parser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)
    root = etree.XML(download(base_url, {"verb": verb}), parser=parser)
    if root is None:
        raise ValueError("The response is not XML")
    if (error := root.find(f"{OAI}error")) is not None:
        raise ValueError(f"{error.get('code')}: {error.text}")
    if (answer := root.find(f"{OAI}{verb}")) is None:
        raise ValueError(f"The response has no {verb} element")
    return answer


def child_texts(element: etree._Element) -> dict[str, str]:
    """Return the text of the direct child elements by their name without namespace."""
    return {etree.QName(child).localname: (child.text or "").strip() for child in element.iterchildren(etree.Element)}


def identify(base_url: str) -> dict[str, Any]:
    """Describe a source: Identify, ListMetadataFormats and the first page of ListSets; each may fail on its own."""
    result: dict[str, Any] = {"base_url": base_url, "identify": [], "formats": [], "sets": [], "errors": {}}
    try:
        check_public_url(base_url)
    except ValueError as e:
        result["error"] = str(e)
        return result

    try:
        # a list and not child_texts: adminEmail may repeat; <description> holds nested XML, not text
        result["identify"] = [
            (etree.QName(child).localname, (child.text or "").strip())
            for child in oai_verb(base_url, "Identify").iterchildren(etree.Element)
            if (child.text or "").strip()
        ]
    except Exception as e:  # noqa: BLE001  shown next to the section, the other verbs may still work
        result["errors"]["Identify"] = str(e)
    try:
        answer = oai_verb(base_url, "ListMetadataFormats")
        result["formats"] = [child_texts(item) for item in answer.findall(f"{OAI}metadataFormat")]
    except Exception as e:  # noqa: BLE001
        result["errors"]["ListMetadataFormats"] = str(e)
    try:
        answer = oai_verb(base_url, "ListSets")
        result["sets"] = [child_texts(item) for item in answer.findall(f"{OAI}set")]
        token = answer.find(f"{OAI}resumptionToken")
        if token is not None and (token.text or "").strip():
            result["sets_total"] = token.get("completeListSize") or "?"
    except Exception as e:  # noqa: BLE001
        result["errors"]["ListSets"] = str(e)
    return result


def relation_values(node: Any, keys: list[str], location: str = "") -> Iterator[tuple[str, Any]]:
    """Yield (location, value) for a dotted path, expanding lists on the way."""
    if isinstance(node, list):
        for i, item in enumerate(node):
            yield from relation_values(item, keys, f"{location}[{i}]")
    elif not keys:
        yield location, node
    elif isinstance(node, dict) and keys[0] in node:
        yield from relation_values(node[keys[0]], keys[1:], f"{location}.{keys[0]}" if location else keys[0])


def explain_relation(draft: Any, name: str, error: RelationError) -> list[str]:
    """Turn invenio's 'Invalid value x.' into one message per bad value, with its position."""
    field = draft.relations._fields[name]
    problems = []
    for location, value in relation_values(dict(draft), name.split(".")):  # field names are data paths
        id_ = value.get(field._value_key_suffix) if isinstance(value, dict) else None  # noqa: SLF001
        if id_ is not None and not field.exists(id_):
            problems.append(f'{location}: "{id_}" not found in {field._cache_key}')  # noqa: SLF001
    return problems or [f"{name}: {error}"]  # couldn't isolate the value: keep invenio's message


def colored(text: str, lexer: Any) -> Markup:
    """Highlight text as HTML; Pygments escapes it, so it can be marked safe for the template."""
    return Markup(highlight(text, lexer, HtmlFormatter(noclasses=True, nowrap=True)))  # noqa: S704


def flatten(messages: Any) -> list[str]:
    """Turn nested marshmallow or service errors into 'field: message' strings."""
    return [f"{field}: {message}" if field else message for field, message in _flatten_messages(messages)]


def exception_messages(exc: Exception) -> list[str]:
    """Readable messages of a transformer failure; imports raise nested ValidationErrors."""
    return flatten(exc.normalized_messages()) if isinstance(exc, ValidationError) else [str(exc) or repr(exc)]


def source_texts(record_xml: etree._Element) -> list[tuple[str, str]]:
    """Return (path without namespaces and indexes, whitespace-normalized text) of the <metadata> text nodes."""
    metadata = record_xml.find(f"{OAI}metadata")
    if metadata is None:
        return []
    tree = metadata.getroottree()
    prefix = tree.getelementpath(metadata) + "/"  # a full OAI-PMH response has GetRecord/record/ before it
    texts = []
    for element in metadata.iter(etree.Element):
        path = re.sub(r"\{[^}]*\}|\[\d+\]", "", tree.getelementpath(element).removeprefix(prefix))
        tail = None if element is metadata else element.tail
        own_text = None if etree.QName(element).localname in VOCABULARY_ELEMENTS else element.text
        texts.extend((path, " ".join(text.split())) for text in (own_text, tail) if text and text.strip())
    return texts


def transformed_strings(node: Any) -> Iterator[str]:
    """Yield the string and number values of the transformed data, except for copies of the source."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key not in SOURCE_COPY_KEYS:
                yield from transformed_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from transformed_strings(value)
    elif isinstance(node, str):
        yield " ".join(node.split())
    elif isinstance(node, int | float) and not isinstance(node, bool):
        yield str(node)


def not_converted(texts: list[tuple[str, str]], data: Any) -> list[dict[str, Any]]:
    """Group the source texts missing from the transformed data by their path; one example of each."""
    # ponytail: substring match, so a short value like "1" counts as found almost anywhere.
    # Ignoring case: xmlschema uppercases xs:hexBinary values such as checksums.
    haystack = "\n".join(transformed_strings(data)).casefold()
    groups: dict[str, dict[str, Any]] = {}
    for path, text in texts:
        if text.casefold() not in haystack:
            group = groups.setdefault(path, {"path": path, "count": 0, "example": text})
            group["count"] += 1
    return list(groups.values())


def validate(  # noqa: C901, PLR0911, PLR0912, PLR0915
    transformer: str,
    oai_xml: str,
    base_url: str,
    metadata_prefix: str,
    identifier: str,
) -> dict[str, Any]:
    """Run one record through a transformer, the schema and the relations.

    Creates no dataset, but resolving ORCID and ROR identifiers may create their vocabulary
    records.
    """
    errors, warnings = [], []
    result = {"status": "invalid", "errors": errors, "warnings": warnings, "original": None, "transformed": None, "not_converted": []}

    has_paste = bool(oai_xml.strip())
    has_fetch = bool(base_url and metadata_prefix and identifier)
    if has_paste and (base_url or metadata_prefix or identifier):
        warnings.append("The pasted record was used; the OAI URL, metadata format and identifier were ignored")

    try:
        if has_paste:
            paste = oai_xml.strip()
            if len(paste.encode()) > MAX_XML_BYTES:
                raise ValueError(f"Record is larger than {MAX_XML_BYTES} bytes")
            raw, xml_warnings = read_xml(paste.encode(), encoding="utf-8", allow_metadata=True)
        elif has_fetch:
            raw, xml_warnings = read_fetch(base_url, metadata_prefix, identifier)
        else:
            raise ValueError("Paste a record, or fill in the OAI URL, metadata format and identifier")
    except Exception as e:  # noqa: BLE001  bad input, unknown record, source down
        errors.append(("source", str(e)))
        return result
    warnings.extend(xml_warnings)

    # before the transformer: herbarium-fix edits this XML in place
    texts = source_texts(raw["record"].xml)
    result["original"] = colored(etree.tostring(raw["record"].xml, pretty_print=True, encoding="unicode"), XmlLexer())

    try:
        args = {"model": MODEL} if transformer == "oai-import" else {}
        built = TransformerFactory.create({"type": transformer, "args": args})
    except Exception as e:  # noqa: BLE001  e.g. xslt needs a stylesheet
        errors.append(("transform", f"{transformer} can't be used here: {e}"))
        return result

    entry = CatchingTransformer(built).apply(StreamEntry(raw))
    if entry.exc:
        errors.extend(("transform", message) for message in exception_messages(entry.exc))
        return result

    try:
        data = entry.entry.get("record")
        if not data:
            if raw["record"].deleted:
                result["status"] = "deleted"
            else:
                errors.append(("transform", f"{transformer} produced no record"))
            return result
        if not isinstance(data, dict):  # e.g. herbarium-fix only edits the XML
            errors.append(("transform", f"{transformer} produced no record"))
            return result

        # what the writer does before calling the service
        data = json.loads(json.dumps(data, default=str))
        writer = OAIServiceWriter(model=MODEL)
        writer._pop_communities(data)  # noqa: SLF001
        writer._add_files_defaults(data)  # noqa: SLF001
        result["transformed"] = colored(json.dumps(data, indent=2, ensure_ascii=False), JsonLexer())

        service = current_runtime.models[MODEL].service
        valid, schema_errors = service.schema.load(data, context={"identity": system_identity}, raise_errors=False)
        errors.extend(("schema", message) for message in flatten(schema_errors))

        # the harvest resolves ORCID and ROR ids first, which may create their vocabulary records
        resolve_identifiers(valid, session=TimedSession())

        draft = service.draft_cls(valid)  # never committed
        for name in draft.relations:
            try:
                getattr(draft.relations, name).validate()
            except RelationError as e:
                errors.extend(("relations", problem) for problem in explain_relation(draft, name, e))
    except Exception as e:  # noqa: BLE001  unexpected transformer output must not 500
        errors.append(("validate", str(e)))
        return result

    if not errors:
        result["status"] = "valid"
        # with all titles of the resolved vocabulary terms, which the record takes from the vocabulary;
        # subjects otherwise copy only the single-language `subject`
        for name, field in draft.relations._fields.items():  # noqa: SLF001
            getattr(draft.relations, name).dereference(keys=[*field.keys, "title"])
        result["not_converted"] = not_converted(texts, [data, dict(draft)])
        if count := sum(group["count"] for group in result["not_converted"]):
            warnings.append(
                f"{count} text values of the original were not found in the transformed data. "
                "This may be fine, or the data may have been lost; see below."
            )
    return result


class MaxBytes:
    """Validate that a string is at most `limit` UTF-8 bytes long."""

    def __init__(self, limit: int) -> None:
        """Store the byte limit."""
        self.limit = limit

    def __call__(self, _form: FlaskForm, field: Any) -> None:
        """Reject a value whose encoded size exceeds the limit."""
        if len((field.data or "").encode()) > self.limit:
            raise WTFormsValidationError(f"The record is larger than {self.limit} bytes")


def clean(value: str | None) -> str:
    """Strip copy-paste whitespace; a field is None on the first visit or if a POST omits it."""
    return (value or "").strip()


class ValidateForm(FlaskForm):
    """Field names match the arguments of `validate`."""

    transformer = SelectField(_("Transformer"), default="oai-import")
    oai_xml = TextAreaField(_("Pasted record or metadata"), filters=[clean], validators=[MaxBytes(MAX_XML_BYTES)])
    base_url = StringField(_("OAI URL"), filters=[clean])
    metadata_prefix = StringField(_("Metadata format"), filters=[clean])
    identifier = StringField(_("Identifier"), filters=[clean])


class IdentifyForm(FlaskForm):
    """The part of the validation form needed by the Identify button."""

    base_url = StringField(filters=[clean])


def create_blueprint(app: Flask) -> Blueprint:  # noqa: ARG001  the entry point passes the app
    """Blueprint with the validation page."""
    bp = Blueprint("harvest_validate", __name__)

    @bp.route("/harvest/validate", methods=["GET", "POST"])
    @login_required
    def harvest_validate() -> str | Response:
        form = ValidateForm(data=session.get(SESSION_KEY))
        form.transformer.choices = sorted(current_app.config["VOCABULARIES_DATASTREAM_TRANSFORMERS"])
        result = None
        if form.validate_on_submit():
            if "reset" in request.form:
                session.pop(SESSION_KEY, None)
                return redirect(url_for(".harvest_validate"))
            data = {key: value for key, value in form.data.items() if key != "csrf_token"}
            session[SESSION_KEY] = data
            result = validate(**data)
        return render_template("harvest_validate.html", form=form, result=result)

    @bp.route("/harvest/validate/identify", methods=["POST"])  # POST with CSRF: it makes the server call the URL
    @login_required
    def harvest_identify() -> str:
        form = IdentifyForm()
        if not form.validate_on_submit():
            info = {"base_url": "", "error": "; ".join(form.csrf_token.errors) or "Invalid request"}
        elif not form.base_url.data:
            info = {"base_url": "", "error": "Enter an OAI URL first"}
        else:
            info = identify(form.base_url.data)
        return render_template("harvest_identify.html", info=info)

    return bp
