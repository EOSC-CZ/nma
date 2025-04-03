#!/bin/bash

cd "$(dirname "$0")/.."



set -e
set -x

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --destroy) DESTROY=true ;;
        --harvest) HARVEST=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

export DESTROY
export HARVEST

if [ -d .venv ]; then
    source .venv/bin/activate
fi

if [ -z "$USER_PASSWORD" ] ; then
    echo "USER_PASSWORD is not set"
    exit 1
fi

if [ -z "$BUCKET_NAME" ] ; then
    echo "BUCKET_NAME is not set"
    exit 1
fi

if [ "$DESTROY" == "true" ] ; then
    invenio db destroy --yes-i-know || true
    invenio index destroy --force --yes-i-know || true
    invenio db init create 
    invenio index init
fi

invenio oarepo cf init
invenio communities custom-fields init
invenio files location create --default default s3://${BUCKET_NAME};

invenio oarepo fixtures load --verbose

invenio oarepo fixtures load --no-system-fixtures ./fixtures --verbose

invenio users create -a -c "nrdocstest+vlastnik@gmail.com" --password "${USER_PASSWORD}" --profile '{"full_name": "Vlastník - superkurátor"}'
invenio oarepo communities members add generic "nrdocstest+vlastnik@gmail.com" owner
invenio oarepo communities members add lindat "nrdocstest+vlastnik@gmail.com" owner
invenio access allow administration-access user nrdocstest+vlastnik@gmail.com
invenio access allow administration-moderation user nrdocstest+vlastnik@gmail.com


if [ "$HARVEST" == "true" ] ; then
    ./scripts/harvest_lindat.sh
fi