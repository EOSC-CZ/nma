"""Conftest for repository tests.

Note: as the tests are run in the context of the whole Invenio instance,
they should not modify the database or opensearch indexes in a way that
would affect other tests or the running instance!
"""

import pytest


@pytest.fixture(scope="module")
def app():
    """Application fixture for tests."""
    from invenio_app.factory import create_app

    app = create_app()
    with app.app_context():
        yield app
