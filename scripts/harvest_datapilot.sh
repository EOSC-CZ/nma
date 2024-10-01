#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add nrdata --name "data.narodni-repozitar.cz harvester" \
            --url 'https://data.narodni-repozitar.cz/datasets/all/' \
            --set 'all' --prefix nr_data \
            --loader nrdata \
            --transformer nrdata \
            --writer 'service{service=datasets,update=true}'


invenio oarepo oai harvester run nrdata