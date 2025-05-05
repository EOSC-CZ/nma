#!/bin/bash

#
# Imports data from EOSC CZ Data Repo repository
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
    invenio oarepo communities create datarepo "EOSC CZ Data Repo"

    invenio oarepo oai harvester add datarepo.eosc.cz \
            --name "EOSC CZ Data Repo harvester" \
            --url 'https://datarepo.eosc.cz/datasets/all/' \
            --set "" \
            --prefix "" \
            --loader 'datarepo' \
            --transformer datarepo \
            --transformer add_community{community=datarepo} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run datarepo.eosc.cz
fi