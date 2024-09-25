#!/bin/bash

#
# Imports data from export inside invenio s3 bucket
#

set -e

# shellcheck disable=SC1090
#source ~/.envrc.local
source "$(dirname "$0")/../.venv/bin/activate"

invenio oarepo oai harvester add vscht --name "Vscht zenodo harvester" \
            --url 'https://zenodo.org/api/records/' \
            --set 'creators.affiliation:("vscht" OR "Vysoká škola chemicko-technologická v Praze" OR "UCT Prague" OR "University of Chemistry and Technology, Prague")' --prefix oai_dc \
            --loader zenodo \
            --transformer zenodo \
            --writer 'service{service=datasets}'


invenio oarepo oai harvester run vscht