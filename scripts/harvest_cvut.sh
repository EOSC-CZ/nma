#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add cvut --name "CVUT zenodo harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("České vysoké učení technické v Praze" OR "ČVUT" OR "CESKE VYSOKE UCENI TECHNICKE V PRAZE" OR "CVUT" OR "Czech Technical University In Prague" OR "CTU in Prague" OR "CTU Prague")  AND resource_type.type:dataset' --prefix oai_dc \
            --loader zenodo \
            --transformer zenodo \
            --writer 'service{service=datasets,update=true}'


invenio oarepo oai harvester run cvut