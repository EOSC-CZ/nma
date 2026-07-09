#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Prometheus Metrics exporter extension."""


from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics


class PrometheusMetricsExporterExt:
    def __init__(self, app: Flask | None = None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.app = app
        metrics = PrometheusMetrics.for_app_factory(path=None)
        metrics.init_app(app)

        app.extensions["metrics-extension"] = self
