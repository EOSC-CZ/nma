# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o
# SPDX-License-Identifier: MIT

"""Transformer setting the record id from its persistent identifier."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

import idutils
from invenio_vocabularies.datastreams.transformers import BaseTransformer

if TYPE_CHECKING:
    from invenio_vocabularies.datastreams.datastreams import StreamEntry

# persistent identifier schemes usable as record id, in order of preference,
# with the idutils check matching the regexp that normalize_pid relies on
PID_SCHEMES = {
    "doi": idutils.is_doi,
    "handle": idutils.is_handle,
}


class IdFromPIDTransformer(BaseTransformer):
    """Sets the record id and persistent url from its DOI, falling back to its Handle.

    The id is ``<scheme>/<identifier>``, e.g. ``doi/10.1234/abc`` or
    ``handle/11104/0312345`` (the same as LINDAT records).
    """

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        """Ignore the transformer options, there are none."""

    @override
    def apply(self, stream_entry: StreamEntry, *_args: Any, **_kwargs: Any) -> StreamEntry:
        """Add the 'id' and 'persistent_url' fields, filter out records without a PID."""
        entry = stream_entry.entry
        rec = entry.get("record", {})
        if not rec:
            return stream_entry

        identifiers = rec.get("metadata", {}).get("identifiers", [])
        invalid = []
        for scheme, is_valid in PID_SCHEMES.items():
            for identifier in identifiers:
                value = (identifier.get("identifier") or "").strip()
                if identifier.get("scheme") != scheme or not value:
                    continue
                # normalize_pid raises AttributeError on values its regexp does not match,
                # so skip them and fall back to the next identifier or scheme
                if not is_valid(value):
                    invalid.append(f"{scheme}:{value}")
                    continue
                value = idutils.normalize_pid(value, scheme)
                rec["id"] = f"{scheme}/{value}"
                rec["metadata"]["persistent_url"] = idutils.to_url(value, scheme, url_scheme="https")
                return stream_entry

        stream_entry.filtered = True
        message = "Missing DOI or Handle identifier for record."
        if invalid:
            message += f" Invalid identifiers: {', '.join(invalid)}."
        stream_entry.errors.append(message)
        return stream_entry
