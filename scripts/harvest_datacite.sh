#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add datacite --name "datacite oai_dc harvester" \
            --url 'https://oai.datacite.org/oai' \
            --set '' --prefix datacite \
            --loader 'sickle' \
            --transformer datacite\
            --writer 'service{service=datasets}'


invenio oarepo oai harvester run datacite