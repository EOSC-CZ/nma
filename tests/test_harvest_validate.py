# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
# SPDX-License-Identifier: MIT
"""Tests of the validation page; no services or app context are needed."""

# The stub classes below are deliberately small.
# ruff: noqa: D102, D105, D107

from types import SimpleNamespace

import pytest
from flask import Flask
from markupsafe import Markup, escape
from pygments.lexers import JsonLexer, XmlLexer
from invenio_records.systemfields.relations import RelationError
from lxml import etree
from wtforms.validators import ValidationError as WTFormsValidationError

from ui import harvest_validate
from ui.harvest_validate import (
    MAX_XML_BYTES,
    check_public_url,
    colored,
    not_converted,
    read_xml,
    relation_values,
    source_texts,
    validate,
)

OAI = "http://www.openarchives.org/OAI/2.0/"
HEADER = "<header><identifier>x:1</identifier><datestamp>2026-01-01</datestamp></header>"
RECORD = f'<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x"/></metadata></record>'
DELETED = (
    f'<record xmlns="{OAI}"><header status="deleted">'
    f"<identifier>x:1</identifier><datestamp>2026-01-01</datestamp></header></record>"
)


def bad_record(header):
    """Build a record with the given header and trivial metadata."""
    return f'<record xmlns="{OAI}">{header}<metadata><a xmlns="urn:x"/></metadata></record>'


MODEL = "datasets"


class StubTransformer:
    """Transformer that replaces the entry with fixed data."""

    def __init__(self, data):
        self.data = data

    def apply(self, stream_entry):
        stream_entry.entry = {"record": self.data}
        return stream_entry


class StubEntryTransformer:
    """Transformer that replaces the whole entry with a non-dict value."""

    def apply(self, stream_entry):
        stream_entry.entry = "not a dict"
        return stream_entry


class StubWriter:
    """Writer whose preparation steps do nothing."""

    def __init__(self, model):
        self.model = model

    def _pop_communities(self, data):
        return []

    def _add_files_defaults(self, data):
        return None


class StubField:
    """Relation field knowing which ids are missing."""

    _value_key_suffix = "id"
    _cache_key = "affiliations"

    def __init__(self, bad_ids=()):
        self.bad_ids = set(bad_ids)

    def exists(self, id_):
        return id_ not in self.bad_ids

    def validate(self):
        if self.bad_ids:
            raise RelationError(f"Invalid value {next(iter(self.bad_ids))}.")


class StubRelations:
    """Relation mapping exposing the stub fields by name."""

    def __init__(self, fields):
        self._fields = fields

    def __iter__(self):
        return iter(self._fields)

    def __getattr__(self, name):
        if name in self._fields:
            return self._fields[name]
        raise AttributeError(name)


class StubDraft(dict):
    """Draft built from the schema data, with stub relations."""

    def __init__(self, data, fields):
        super().__init__(data)
        self.relations = StubRelations(fields)


class StubSchema:
    """Schema that returns the data unchanged, or raises the given error."""

    def __init__(self, error=None):
        self.error = error

    def load(self, data, **kwargs):
        if self.error is not None:
            raise self.error
        return data, {}


class StubService:
    """Service whose schema and draft class are stubs."""

    def __init__(self, fields=None, schema_error=None):
        self.schema = StubSchema(schema_error)
        self.fields = fields or {}

    def draft_cls(self, data):
        return StubDraft(data, self.fields)


def stub_validation(monkeypatch, data, *, fields=None, schema_error=None, resolve=None, transformer=None):
    """Replace the transformer, writer, service and identifier resolution."""
    built = transformer or StubTransformer(data)

    def create(config):
        return built

    monkeypatch.setattr(harvest_validate, "TransformerFactory", SimpleNamespace(create=create))
    monkeypatch.setattr(harvest_validate, "OAIServiceWriter", StubWriter)
    service = StubService(fields=fields, schema_error=schema_error)
    monkeypatch.setattr(
        harvest_validate,
        "current_runtime",
        SimpleNamespace(models={MODEL: SimpleNamespace(service=service)}),
    )

    resolved = []

    def resolve_identifiers(valid, session=None):
        resolved.append(valid)
        if resolve is not None:
            resolve(valid)

    monkeypatch.setattr(harvest_validate, "resolve_identifiers", resolve_identifiers)
    return resolved


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1:5432/",
        "http://10.0.0.1/",
        "http://192.168.1.1/",
        "http://169.254.169.254/latest/meta-data",
        "http://224.0.0.1/",
        "http://[::1]/",
        "http://[::ffff:127.0.0.1]/",
        "http://[64:ff9b::7f00:1]/",
        "http://2130706433/",
        "file:///etc/passwd",
        "ftp://1.1.1.1/",
        "http:///x",
    ],
)
def test_internal_urls_are_refused(url):
    with pytest.raises(ValueError, match=r"Only http|public address"):
        check_public_url(url)


def test_public_address_is_allowed():
    check_public_url("https://1.1.1.1/oai")


@pytest.mark.parametrize(
    "xml",
    [RECORD, f'<OAI-PMH xmlns="{OAI}"><GetRecord>{RECORD}</GetRecord></OAI-PMH>'],
)
def test_record_is_found(xml):
    entry, warnings = read_xml(xml.encode())
    assert entry["record"].header.identifier == "x:1"
    assert warnings == []


@pytest.mark.parametrize(
    "xml",
    [
        "hello",
        f"<record>{HEADER}<metadata><a/></metadata></record>",  # no namespace
        f'<record xmlns="{OAI}"><metadata><a/></metadata></record>',  # no header
        f'<record xmlns="{OAI}">{HEADER}</record>',  # no metadata
        f'<record xmlns="{OAI}">{HEADER}<metadata/></record>',  # empty metadata
        bad_record("<header><datestamp>2026-01-01</datestamp></header>"),  # no identifier
        bad_record("<header><identifier>x:1</identifier></header>"),  # no datestamp
        f'<OAI-PMH xmlns="{OAI}">{RECORD}{RECORD}</OAI-PMH>',  # two records
        f'<OAI-PMH xmlns="{OAI}"><error code="idDoesNotExist">No</error></OAI-PMH>',
    ],
)
def test_bad_input_gives_a_value_error(xml):
    with pytest.raises(
        ValueError,
        match=r"Expected one|no <metadata> content|no identifier or datestamp|idDoesNotExist|Header element not found",
    ):
        read_xml(xml.encode())


def test_truncated_xml_gives_a_warning():
    _, warnings = read_xml(RECORD[:-20].encode())
    assert warnings


def test_external_entity_is_not_resolved(tmp_path):
    secret = tmp_path / "secret.txt"
    secret.write_text("CANARY")
    dtd = f'<!DOCTYPE record [<!ENTITY e SYSTEM "file://{secret}">]>'
    xml = f'{dtd}<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x">&e;</a></metadata></record>'
    entry, _ = read_xml(xml.encode())
    assert "CANARY" not in entry["record"].raw


def test_relation_values_gives_positions():
    data = {"metadata": {"creators": [{"role": {"id": "a"}}, {"affiliations": [{"name": "n"}, {"id": "b"}]}]}}
    assert list(relation_values(data, ["metadata", "creators", "role"])) == [("metadata.creators[0].role", {"id": "a"})]
    assert list(relation_values(data, ["metadata", "creators", "affiliations"])) == [
        ("metadata.creators[1].affiliations[0]", {"name": "n"}),
        ("metadata.creators[1].affiliations[1]", {"id": "b"}),
    ]


def test_a_wrong_encoding_declaration_is_ignored_for_pastes():
    body = f'<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x">Příliš</a></metadata></record>'
    xml = f'<?xml version="1.0" encoding="ISO-8859-2"?>{body}'
    entry, _ = read_xml(xml.encode(), encoding="utf-8")
    assert "Příliš" in entry["record"].raw


def test_fetched_bytes_keep_their_declared_encoding():
    body = f'<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x">Příliš</a></metadata></record>'
    xml = f'<?xml version="1.0" encoding="ISO-8859-2"?>{body}'
    entry, _ = read_xml(xml.encode("iso-8859-2"))
    assert "Příliš" in entry["record"].raw


def test_size_limit_counts_bytes():
    validator = harvest_validate.MaxBytes(MAX_XML_BYTES)
    validator(None, SimpleNamespace(data="é" * (MAX_XML_BYTES // 2)))
    with pytest.raises(WTFormsValidationError):
        validator(None, SimpleNamespace(data="é" * (MAX_XML_BYTES // 2 + 1)))


@pytest.mark.parametrize(
    ("base_url", "metadata_prefix", "identifier"),
    [("https://example.org/oai", "oai_dc", "x:1"), ("", "", "x:1")],
)
def test_paste_wins_over_fetch_fields_with_a_warning(monkeypatch, base_url, metadata_prefix, identifier):
    stub_validation(monkeypatch, {"metadata": {}})
    fetched = []
    monkeypatch.setattr(harvest_validate, "read_fetch", lambda *args: fetched.append(args))
    result = validate("oai-import", RECORD, base_url, metadata_prefix, identifier)
    assert fetched == []
    assert result["status"] == "valid"
    assert "The pasted record was used" in result["warnings"][0]


def test_resolved_identifiers_are_validated_hard(monkeypatch):
    data = {"metadata": {"creators": [{"affiliations": [{"id": "bad"}]}]}}
    resolved = stub_validation(
        monkeypatch,
        data,
        fields={"metadata.creators.affiliations": StubField({"bad"})},
    )
    result = validate("oai-import", RECORD, "", "", "")
    assert resolved == [data]
    assert result["status"] == "invalid"
    assert (
        "relations",
        'metadata.creators[0].affiliations[0]: "bad" not found in affiliations',
    ) in result["errors"]
    assert result["warnings"] == []


def test_unexpected_output_is_reported(monkeypatch):
    stub_validation(monkeypatch, {"metadata": {}}, schema_error=TypeError("not a record"))
    result = validate("oai-import", RECORD, "", "", "")
    assert result["status"] == "invalid"
    assert ("validate", "not a record") in result["errors"]


def test_a_non_dict_entry_is_reported(monkeypatch):
    stub_validation(monkeypatch, None, transformer=StubEntryTransformer())
    result = validate("oai-import", RECORD, "", "", "")
    assert result["status"] == "invalid"
    assert result["errors"][0][0] == "validate"


def test_empty_output_for_a_live_record_is_an_error(monkeypatch):
    stub_validation(monkeypatch, {})
    result = validate("oai-import", RECORD, "", "", "")
    assert result["status"] == "invalid"
    assert ("transform", "oai-import produced no record") in result["errors"]


def test_deleted_record_is_deleted(monkeypatch):
    stub_validation(monkeypatch, None)
    result = validate("oai-import", DELETED, "", "", "")
    assert result["status"] == "deleted"
    assert result["errors"] == []


def test_valid_record(monkeypatch):
    stub_validation(monkeypatch, {"metadata": {"title": "x"}})
    result = validate("oai-import", RECORD, "", "", "")
    assert result["status"] == "valid"
    assert result["transformed"]


def test_leading_newline_in_a_paste_is_ignored(monkeypatch):
    stub_validation(monkeypatch, {"metadata": {"title": "x"}})
    result = validate("oai-import", "\n" + RECORD, "", "", "")
    assert result["status"] == "valid"
    assert result["warnings"] == []


@pytest.fixture
def form_app():
    """Minimal app, enough to build the form as the view does."""
    app = Flask(__name__)
    app.config.update(SECRET_KEY="test", WTF_CSRF_ENABLED=False)  # noqa: S105
    return app


@pytest.mark.parametrize("saved", [None, {"base_url": "https://x.org/oai"}])
def test_form_builds_on_a_visit(form_app, saved):
    with form_app.test_request_context("/harvest/validate"):
        form = harvest_validate.ValidateForm(data=saved)
        assert form.transformer.data == "oai-import"
        assert form.oai_xml.data == ""
        assert form.base_url.data == (saved or {}).get("base_url", "")


def test_form_strips_and_tolerates_missing_fields(form_app):
    posted = {"transformer": "oai-import", "identifier": " oai:x:1 "}
    with form_app.test_request_context("/harvest/validate", method="POST", data=posted):
        form = harvest_validate.ValidateForm()
        form.transformer.choices = ["oai-import"]
        assert form.validate_on_submit()
        assert form.identifier.data == "oai:x:1"
        assert form.oai_xml.data == ""
        assert form.base_url.data == ""


@pytest.mark.parametrize(
    ("text", "lexer"),
    [
        ("<a>&lt;script&gt;alert(1)&lt;/script&gt;</a>", XmlLexer()),
        ("<a><![CDATA[<script>alert(1)</script>]]></a>", XmlLexer()),
        ('<a b="&quot;><script>alert(1)</script>"/>', XmlLexer()),
        ("<a><!-- <script>alert(1)</script> --></a>", XmlLexer()),
        ("<script>alert(1)</script>", XmlLexer()),
        ('{"title": "</pre><script>alert(1)</script>"}', JsonLexer()),
        ("not json </pre><script>alert(1)</script>", JsonLexer()),
    ],
)
def test_colored_output_is_escaped(text, lexer):
    html = colored(text, lexer)
    assert isinstance(html, Markup)
    assert "<script" not in html
    assert "</pre" not in html
    assert escape(html) == html  # the template does not escape it again


def test_reset_clears_the_session(form_app):
    form_app.config.update(LOGIN_DISABLED=True, VOCABULARIES_DATASTREAM_TRANSFORMERS={"oai-import": object})
    form_app.register_blueprint(harvest_validate.create_blueprint(form_app))
    client = form_app.test_client()
    with client.session_transaction() as session:
        session[harvest_validate.SESSION_KEY] = {"oai_xml": "<old/>"}

    response = client.post("/harvest/validate", data={"reset": "1"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/harvest/validate")
    with client.session_transaction() as session:
        assert harvest_validate.SESSION_KEY not in session


@pytest.mark.parametrize(
    "xml",
    [
        '<a xmlns="urn:x"><b>text</b></a>',
        f'<metadata xmlns="{OAI}"><a xmlns="urn:x"><b>text</b></a></metadata>',
    ],
)
def test_pasted_metadata_gets_a_placeholder_record(xml):
    entry, warnings = read_xml(xml.encode(), allow_metadata=True)
    record = entry["record"]
    assert record.header.identifier == "pasted-metadata"
    assert record.xml.find(f"{{{OAI}}}metadata")[0].tag == "{urn:x}a"
    assert "placeholder" in warnings[0]


def test_whole_record_is_not_wrapped():
    entry, warnings = read_xml(RECORD.encode(), allow_metadata=True)
    assert entry["record"].header.identifier == "x:1"
    assert warnings == []


@pytest.mark.parametrize(
    "xml",
    [
        "hello",
        f"<record>{HEADER}<metadata><a/></metadata></record>",  # forgotten xmlns
        "<metadata><a/></metadata>",
        f'<OAI-PMH xmlns="{OAI}"></OAI-PMH>',
        f'<metadata xmlns="{OAI}"/>',
    ],
)
def test_pasted_non_metadata_is_refused(xml):
    with pytest.raises(ValueError, match=r"Expected one|no <metadata> content"):
        read_xml(xml.encode(), allow_metadata=True)


def test_fetched_response_is_never_wrapped():
    with pytest.raises(ValueError, match="Expected one"):
        read_xml(b'<a xmlns="urn:x"/>')


def texts_of(metadata):
    return source_texts(etree.fromstring(f'<record xmlns="{OAI}">{HEADER}<metadata>{metadata}</metadata></record>'))


def test_source_texts_cover_only_metadata_without_namespaces_or_indexes():
    metadata = '<a xmlns="urn:x"><b>  one\n two </b><b>three</b><c/>tail</a>'
    assert texts_of(metadata) == [("a/b", "one two"), ("a/b", "three"), ("a/c", "tail")]


def test_not_converted_groups_missing_values_by_path():
    texts = [("a/b", "kept"), ("a/b", "lost 1"), ("a/b", "lost 2"), ("a/c", "also lost")]
    assert not_converted(texts, {"metadata": {"title": "kept"}}) == [
        {"path": "a/b", "count": 2, "example": "lost 1"},
        {"path": "a/c", "count": 1, "example": "also lost"},
    ]


def test_not_converted_finds_numbers_and_parts_of_longer_values():
    texts = [("a/size", "11298"), ("a/title", "part")]
    assert not_converted(texts, {"size": 11298, "note": "a part of it", "flag": True}) == []


def test_not_converted_ignores_copies_of_the_source():
    assert not_converted([("a", "lost")], {"ccmm_xml": "<a>lost</a>"}) == [{"path": "a", "count": 1, "example": "lost"}]


def test_valid_record_warns_about_values_not_converted(monkeypatch):
    stub_validation(monkeypatch, {"metadata": {}})
    xml = f'<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x">lost</a></metadata></record>'
    result = validate("oai-import", xml, "", "", "")
    assert result["status"] == "valid"
    assert result["not_converted"] == [{"path": "a", "count": 1, "example": "lost"}]
    assert "1 text values" in result["warnings"][0]


def test_invalid_record_skips_the_comparison(monkeypatch):
    stub_validation(monkeypatch, {"metadata": {}}, schema_error=TypeError("broken"))
    xml = f'<record xmlns="{OAI}">{HEADER}<metadata><a xmlns="urn:x">lost</a></metadata></record>'
    result = validate("oai-import", xml, "", "", "")
    assert result["status"] == "invalid"
    assert result["not_converted"] == []


def test_source_texts_skip_vocabulary_iris_and_labels():
    metadata = '<a xmlns="urn:x"><role><iri>https://x.org/1</iri><label>Author</label></role><name>Jane</name></a>'
    assert texts_of(metadata) == [("a/name", "Jane")]

