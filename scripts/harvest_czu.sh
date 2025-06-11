#!/bin/bash

#
# Imports data from Zenodo CZU repository
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
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

if [ $CREATE == "true" ] ; then
    invenio oarepo communities create czu "ČZU" || true

    invenio oarepo oai harvester add zenodo-czu \
            --name "ČZU harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("Česká zemědělská univerzita v Praze" OR "ČZU" OR "CESKA ZEMEDELSKA UNIVERZITA V PRAZE" OR "CZU Praha" OR "The Czech University of Life Sciences Prague" OR "Czech University of Agriculture Prague")  AND resource_type.type:dataset' \
            --prefix "" \
            --loader 'zenodo' \
            --transformer zenodo \
            --transformer add_community{community=czu} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run zenodo-czu --batch-size 10 --all-records --overwrite-all-records
fi