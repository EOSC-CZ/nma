# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""UI + REST WSGI application for Invenio flavours with /metrics."""
import os

from invenio_app.factory import create_app
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics

application = create_app()
"""Combined UI + REST Flask application.

REST API is mounted under ``/api``.
"""
# TODO: just a quick POC - find a better place for this module
metrics = UWsgiPrometheusMetrics(application)
metrics.start_http_server(int(os.getenv("METRICS_PORT")))
