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
invenio access allow manage-record role riv_curators

$(dirname "$0")/create_oai_harvesters.sh
