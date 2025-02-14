#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add czu --name "CZU zenodo harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("Česká zemědělská univerzita v Praze" OR "ČZU" OR "CESKA ZEMEDELSKA UNIVERZITA V PRAZE" OR "CZU Praha" OR "The Czech University of Life Sciences Prague" OR "Czech University of Agriculture Prague")  AND resource_type.type:dataset' --prefix oai_dc \
            --loader zenodo \
            --transformer zenodo \
            --writer 'service{service=datasets,update=true}'


invenio oarepo oai harvester run czu --log-level INFO --batch-size 1 2>&1 | tee -a /tmp/harvest_czu.log