#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add lindat_dc --name "LINDAT oai_dc harvester" \
            --url 'http://lindat.mff.cuni.cz/repository/oai/request?' \
            --set "" \
            --prefix oai_dc \
            --loader 'sickle' \
            --transformer lindat_transformer \
            --writer 'service{service=datasets,update=true}'


invenio oarepo oai harvester run lindat_dc