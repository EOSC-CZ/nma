#!/bin/bash

#
# Imports data from LINDAT repository
#

cd "$(dirname $0)/.."

set -e
set -x

CREATE=true
HARVEST=true

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-create) CREATE=false ;;
        --skip-harvest) HARVEST=false ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# shellcheck disable=SC1090
#source ~/.envrc.local
source .venv/bin/activate

if [ $CREATE == "true" ] ; then
    invenio oarepo communities create lindat "LINDAT CLARIAH CZ" || true

    invenio oarepo oai harvester add lindat \
            --name "LINDAT oai_dc harvester" \
            --url 'http://lindat.mff.cuni.cz/repository/oai/request?' \
            --set "" \
            --prefix oai_dc \
            --loader 'sickle' \
            --transformer lindat \
            --transformer add_community{community=lindat} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run lindat --all-records --overwrite-all-records
fi