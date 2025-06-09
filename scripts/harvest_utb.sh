#!/bin/bash

#
# Imports data from Zenodo UTB repository
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
    invenio oarepo communities create utb "UTB" || true

    invenio oarepo oai harvester add zenodo-utb \
            --name "UTB harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("utb" OR "Univerzita Tomáše Bati ve Zlíně" OR "Tomas Bata University in Zlin") AND resource_type.type:dataset' \
            --prefix "" \
            --loader 'zenodo' \
            --transformer zenodo \
            --transformer add_community{community=utb} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run zenodo-utb --batch-size 10 --all-records --overwrite-all-records
fi