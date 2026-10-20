#!/usr/bin/env bash

# This script prepares a new alpha release.
#

set -exo pipefail

cd "$(dirname "$0")/.."

if [ -d .venv ]; then
    source .venv/bin/activate
fi

if [ -z "$INVENIO_S3_BUCKET" ] ; then
    echo "INVENIO_S3_BUCKET is not set"
    exit 1
fi

if [ -z "$KUBERNETES_SERVICE_HOST" ] ; then
    ./run.sh services setup
else
    # RPC server socket lives in the instance dir, which is read-only in the pod
    sed -i 's/^use_rpc *= *true/use_rpc = false/' .invenio
    ./run.sh services setup --no-services -N
fi

invenio files location create --default s3 s3://${INVENIO_S3_BUCKET};

invenio roles create administration
invenio access allow administration-access role administration
invenio access allow administration-moderation role administration
invenio roles create riv_curators
