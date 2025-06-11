#!/bin/bash

#
# Imports data from Zenodo UPOL repository
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
    invenio oarepo communities create upol "UPOL" || true

    invenio oarepo oai harvester add zenodo-upol \
            --name "UPOL harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("upol" OR "Univerzita Palackého v Olomouci" OR "Palacký University Olomouc" OR "Palacky University Olomouc") AND resource_type.type:dataset' \
            --prefix "" \
            --loader 'zenodo' \
            --transformer zenodo \
            --transformer add_community{community=upol} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run zenodo-upol --batch-size 10 --all-records --overwrite-all-records
fi