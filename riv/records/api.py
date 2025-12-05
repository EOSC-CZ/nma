#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# nma is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Persistent identifier provider for nma."""
import re
from typing import override, Any
from invenio_drafts_resources.records.api import DraftRecordIdProviderV2
from flask import current_app

def generate_id(record: dict[str, Any] = None) -> str:
    url = record["metadata"]["persistent_url"]
    for prefix, val in current_app.config["PERSISTENT_IDENTIFIER_PATTERNS"].items():
        m = re.match(prefix, url)
        if m:
            return f"{val}:{m.group(1)}"
    raise ValueError(f"Could not generate pid from url: {url}")


class ExternalPIDProvider(DraftRecordIdProviderV2):
    """RIV identifier provider.

    This PID provider uses record url to generate a PID.
    """
    # NEW status due to eg invenio_pidstore.resolver.Resolver.resolve crashing on resolving links

    @classmethod
    @override
    def generate_id(cls, options: dict[str, Any] = None) -> str:
        return options["record"]["id"]

    @classmethod
    @override
    def create(cls, object_type: str | None = None, object_uuid: str | None = None,
               options: dict[str, Any] | None = None, **kwargs: Any):
        options = {**(options or {})}
        options["record"] = kwargs.pop("record")
        return super().create(object_type=object_type, object_uuid=object_uuid, options=options, **kwargs)


