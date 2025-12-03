#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Views."""

from flask import flash, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL


class RegisterForm(FlaskForm):
    """Form for registering a dataset by PID."""

    pid = StringField(
        "Persistent Identifier",
        validators=[
            DataRequired(message="Please enter a persistent identifier"),
            URL(
                message="Please enter a valid URL (e.g., https://doi.org/... or https://hdl.handle.net/...)"
            ),
        ],
    )


def register():
    """Register a dataset by persistent identifier."""
    form = RegisterForm()

    if request.method == "GET":
        return render_template("datasets/register.html", form=form)

    if form.validate_on_submit():
        pid = form.pid.data

        try:
            # TODO: Implement actual PID resolution and record creation and redirect to deposit_edit
            # For now, just flash success and redirect
            flash(f"Successfully registered dataset with PID: {pid}", "success")
            return redirect(url_for("datasets_ui.deposit_create"))
        except Exception as e:
            flash(f"Error registering dataset: {str(e)}", "error")
            return redirect(url_for("datasets_ui.register"))

    # Form validation failed
    flash("Please correct the errors in the form", "error")
    return render_template("datasets/register.html", form=form)
