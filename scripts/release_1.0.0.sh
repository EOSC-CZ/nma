#!/usr/bin/env bash

#
# Note: this script should be run without the workers running!
#

set -eo pipefail

BUCKET=${BUCKET:-}
YES_I_KNOW=${YES_I_KNOW:-}
DESTROY=${DESTROY:-}

while [ $# -gt 0 ]; do
    case "$1" in
        --help|-h)
            echo "Usage: $0 [--destroy] [--yes-i-know]"
            exit 0
            ;;
        --destroy)
            DESTROY="true"
            ;;
        --yes-i-know)
            YES_I_KNOW="true"
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
    shift
done

if [ -z "$BUCKET" ]; then
    echo "Error: BUCKET environment variable is not set."
    exit 1
fi

if [ "$YES_I_KNOW" != "true" ]; then
    echo "Make sure that workers are not running when executing this script!"
    echo "If you are sure, re-run with --yes-i-know"
    exit 1
fi

if [ "$DESTROY" == "true" ]; then
    invenio db destroy --yes-i-know || true
    invenio index destroy --yes-i-know || true
fi

# generic initialization
invenio db init create
invenio files location create --default default "s3://$BUCKET"
invenio roles create admin
invenio access allow superuser-access role admin
invenio index init
invenio rdm-records custom-fields init
invenio communities custom-fields init
invenio rdm fixtures
# TODO: translations should be set up here
invenio queues declare
invenio rdm-records fixtures


invenio roles create riv_curators

# harvesters
invenio oai harvesters create --id catchall --name "Catch-all repository harvester" \
    --base-url "https://data.narodni-repozitar.cz" --metadata-prefix "catchall" --model datasets \
    --loader catch-all --transformer "catch-all"

invenio oai harvesters create --id zenodo-czu --name "Zenodo CZU harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "czu" --model datasets \
    --loader zenodo --transformer "zenodo"             --setspec 'creators.affiliation:("Česká zemědělská univerzita v Praze" OR "ČZU" OR "CESKA ZEMEDELSKA UNIVERZITA V PRAZE" OR "CZU Praha" OR "The Czech University of Life Sciences Prague" OR "Czech University of Agriculture Prague")  AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-cvut --name "Zenodo CVUT harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "cvut" --model datasets \
    --loader zenodo --transformer "zenodo"             --setspec 'creators.affiliation:("České vysoké učení technické v Praze" OR "ČVUT" OR "CESKE VYSOKE UCENI TECHNICKE V PRAZE" OR "CVUT" OR "Czech Technical University In Prague" OR "CTU in Prague" OR "CTU Prague")  AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-upol --name "Zenodo UPOL harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "upol" --model datasets \
    --loader zenodo --transformer "zenodo"             --setspec 'creators.affiliation:("upol" OR "Univerzita Palackého v Olomouci" OR "Palacký University Olomouc" OR "Palacky University Olomouc") AND resource_type.type:dataset' \

invenio oai harvesters create --id zenodo-utb --name "Zenodo UTB harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "utb" --model datasets \
    --loader zenodo --transformer "zenodo"             --setspec 'creators.affiliation:("utb" OR "Univerzita Tomáše Bati ve Zlíně" OR "Tomas Bata University in Zlin") AND resource_type.type:dataset'

invenio oai harvesters create --id zenodo-vscht --name "Zenodo VSCHT harvester" \
    --base-url "https://zenodo.org" --metadata-prefix "vscht" --model datasets \
    --loader zenodo --transformer "zenodo"             --setspec 'creators.affiliation:("vscht" OR "Vysoká škola chemicko-technologická v Praze" OR "UCT Prague" OR "University of Chemistry and Technology, Prague") AND resource_type.type:dataset'
