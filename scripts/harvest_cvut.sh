#!/bin/bash

#
# Imports data from Zenodo CVUT repository
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
    invenio oarepo communities create cvut "ČVUT"

    invenio oarepo oai harvester add zenodo-cvut \
            --name "CVUT harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("České vysoké učení technické v Praze" OR "ČVUT" OR "CESKE VYSOKE UCENI TECHNICKE V PRAZE" OR "CVUT" OR "Czech Technical University In Prague" OR "CTU in Prague" OR "CTU Prague")  AND resource_type.type:dataset' \
            --prefix "" \
            --loader 'zenodo' \
            --transformer zenodo \
            --transformer add_community{community=cvut} \
            --writer 'service{service=datasets,update=true}' \
            --writer 'publish{service=datasets}'
fi

if [ $HARVEST == "true" ] ; then
    invenio oarepo oai harvester run zenodo-cvut --batch-size 10 --all-records --overwrite-all-records
fi