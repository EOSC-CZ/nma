#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Views."""

from invenio_i18n import lazy_gettext as _

from flask_wtf import FlaskForm
from riv.resolvers.utils import normalize_identifier_into_resolution_url
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, URL


class StrippedStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip()


class RegisterForm(FlaskForm):
    """Form for registering a dataset by PID."""

    pid = StrippedStringField(
        label=_("Persistent Identifier"),
        filters=[normalize_identifier_into_resolution_url],
        validators=[
            DataRequired(message=_("Please enter a persistent identifier")),
            URL(
                message=_(
                    "Please enter a valid DOI (e.g., 10.xxxx/... or doi:10.xxxx/...) or full URL (e.g., https://doi.org/... or https://hdl.handle.net/...)"
                )
            ),
        ],
        render_kw={
            "autofocus": "true",
            "data-testid": "deposit-create-register-doi-input",
        },
    )
