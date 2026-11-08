"""What a handle whose landing page can't be read leads to."""

from types import SimpleNamespace

import pytest
from flask import Flask
from flask_babel import Babel
from oarepo_related_resources.errors import UpstreamFetchError
from oarepo_related_resources.resolvers.handle import HandleResolver

from riv.records import utils
from riv.resolvers.nma_resolvers import NMAHandleResolver

URL = "https://hdl.handle.net/1839/00-0000-0000-0009-3C7E-F"


@pytest.fixture
def resolver():
    app = Flask("test")
    Babel(app)
    app.config["RELATED_RESOURCES_HANDLE_MAPPER"] = lambda head: ({"title": head.findtext("title")}, [])
    with app.test_request_context("/"):
        yield NMAHandleResolver()


def refuse(status):
    def fetch(_identifier):
        raise UpstreamFetchError("refused", URL, status, "blocked")

    return fetch


@pytest.mark.parametrize("status", [401, 403, 404])
def test_a_refused_page_lets_the_user_fill_in_the_form(resolver, monkeypatch, status):
    monkeypatch.setattr(resolver, "fetch", refuse(status))

    metadata, problems = resolver.resolve(URL)

    assert metadata == {}
    assert len(problems) == 1


def test_a_file_lets_the_user_fill_in_the_form(resolver, monkeypatch):
    monkeypatch.setattr(resolver, "fetch", lambda _identifier: SimpleNamespace(content=b"%PDF-1.7 \x00\x01binary"))

    metadata, problems = resolver.resolve(URL)

    assert metadata == {}
    assert len(problems) == 1


def test_a_server_error_is_worth_trying_again(resolver, monkeypatch):
    monkeypatch.setattr(resolver, "fetch", refuse(503))

    with pytest.raises(UpstreamFetchError):
        resolver.resolve(URL)


def test_a_readable_page_gives_its_metadata(resolver, monkeypatch):
    page = b"<html><head><title>A dataset</title></head><body></body></html>"
    monkeypatch.setattr(resolver, "fetch", lambda _identifier: SimpleNamespace(content=page))

    metadata, problems = resolver.resolve(URL)

    assert metadata == {"title": "A dataset"}
    assert problems == []


def test_the_edit_grant_mail_is_queued_without_a_problem(monkeypatch):
    queued = []
    monkeypatch.setattr(utils.broadcast_notification, "delay", queued.append)
    problems = []

    with Flask("test").app_context():
        utils.send_user_edit_grant_notification(SimpleNamespace(id=1, email="a@b.c"), {"id": "handle/1/2"}, problems)

    assert problems == []
    assert queued[0]["type"] == "dataset-edit-grant"
    assert queued[0]["context"]["record"] == {"datasets": "handle/1/2"}
