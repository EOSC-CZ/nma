# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""CSL based Schema for Invenio RDM Records."""

from edtf import parse_edtf
from edtf.parser.edtf_exceptions import EDTFParseException
from edtf.parser.parser_classes import Date, Interval
from invenio_access.permissions import system_identity
from invenio_vocabularies.proxies import current_service as vocabulary_service
from marshmallow import Schema, fields, missing
from marshmallow_utils.fields import SanitizedUnicode
from oarepo_runtime.services.schema.i18n_ui import (
    I18nStrUIField,
    MultilingualLocalizedUIField,
)
from gettext import gettext as _


class CSLCreatorSchema(Schema):
    """Creator/contributor common schema."""

    literal = fields.Str(attribute="name")


def add_if_not_none(year, month, day):
    """Adds year, month a day to a list if each are not None."""
    _list = []
    _list.append(year) if year else None
    _list.append(month) if month else None
    _list.append(day) if day else None
    return _list


class CSLJSONSchema(Schema):
    """CSL Marshmallow Schema."""

    id_ = SanitizedUnicode(data_key="id", attribute="id")
    type_ = fields.Constant("dataset", data_key="type", attribute="type")
    title = fields.Method("get_title")
    abstract = MultilingualLocalizedUIField(I18nStrUIField(value_name="description"))
    author = fields.List(fields.Nested(CSLCreatorSchema()), attribute="metadata.creators")
    issued = fields.Method("get_issued")
    language = fields.Method("get_language")
    version = SanitizedUnicode(attribute="metadata.version")
    publisher = SanitizedUnicode(attribute="metadata.publisher.name")
    
    def get_title(self, obj):
        """Get title."""
        sanitized = SanitizedUnicode()._deserialize(obj["metadata"].get("titles", [])[0]["title"], None, None)
        return sanitized

    def _read_resource_type(self, id_):
        """Retrieve resource type record using service."""
        rec = vocabulary_service.read(system_identity, ("resource-types", id_))
        return rec._record

    def get_issued(self, obj):
        """Get issued dates."""
        try:
            filtered = next(o for o in obj["metadata"].get("dates", []) if o.get("dateType").lower() == "issued")
            parsed = parse_edtf(filtered.get("date"))
        except EDTFParseException:
            return missing
        except StopIteration:
            return missing

        if isinstance(parsed, Date):
            parts = add_if_not_none(parsed.year, parsed.month, parsed.day)
            return {"date-parts": [parts]}
        elif isinstance(parsed, Interval):
            d1 = parsed.lower
            d2 = parsed.upper
            return {
                "date-parts": [
                    add_if_not_none(d1.year, d1.month, d1.day),
                    add_if_not_none(d2.year, d2.month, d2.day),
                ]
            }
        else:
            return missing

    def get_language(self, obj):
        """Get language."""
        metadata = obj["metadata"]
        language = metadata.get("language")

        return language if language else missing
