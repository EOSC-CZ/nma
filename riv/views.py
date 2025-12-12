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
from wtforms import StringField
from wtforms.validators import DataRequired, URL

class StrippedStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip()


class RegisterForm(FlaskForm):
    """Form for registering a dataset by PID."""

    pid = StrippedStringField(
        "Persistent Identifier",
        validators=[
            DataRequired(message=_("Please enter a persistent identifier")),
            URL(
                message=_("Please enter a valid URL (e.g., https://doi.org/... or https://hdl.handle.net/...)")
            ),
        ],
        render_kw={"autofocus": True},
    )
