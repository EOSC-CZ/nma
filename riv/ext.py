#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""RIV resolver extension."""

from typing import TYPE_CHECKING, List
from functools import cached_property
from . import config

from invenio_base.utils import obj_or_import_string
from flask import Flask
from .resolvers.base import MetadataResolver
from .resolvers.registry import ResolverRegistry
if TYPE_CHECKING:  # pragma: no cover
    from flask import Flask

class RIVResolverExtension:
    def __init__(self, app: Flask | None = None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.app = app
        self.init_config(app)
        self.resolver_registry =ResolverRegistry()

        app.extensions["riv-extension"] = self

    def init_config(self, app: Flask) -> None:
        """Initialize the configuration for the extension."""
        app.config.setdefault("PERSISTENT_IDENTIFIER_RESOLVERS", config.PERSISTENT_IDENTIFIER_RESOLVERS)
        app.config.setdefault("PERSISTENT_IDENTIFIER_PATTERNS", config.PERSISTENT_IDENTIFIER_PATTERNS)
        app.config.setdefault("DATACITE_URL", config.DATACITE_URL)
        app.config.setdefault("HANDLE_URL", config.HANDLE_URL)
        app.config.setdefault("CROSSREF_URL", config.CROSSREF_URL)

    @cached_property
    def persistent_identifiers_resolvers(self)-> List[MetadataResolver]:
        """Return resolvers for persistent identifiers."""
        return [obj_or_import_string(res)() for res in self.app.config["PERSISTENT_IDENTIFIER_RESOLVERS"]]

