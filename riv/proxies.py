#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Proxies."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from .ext import RIVResolverExtension
    current_riv_extension: RIVResolverExtension  # type: ignore[reportRedeclaration]

current_riv_extension = LocalProxy(lambda: current_app.extensions["riv-extension"])  # type: ignore[assignment]

