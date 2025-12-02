#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Views."""

from flask import request


def register():
    if request.method == "GET":
        return "form"
    else:
        pid = request.form.get("pid")
        return f"registered {pid}"
