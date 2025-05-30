#
# Initialize NMA Instance
#

cd "$(dirname $0)/.."

set -e
set -x

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --destroy) DESTROY=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

export DESTROY

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

invenio oarepo fixtures load --batch-size 1000 --verbose
# invenio oarepo fixtures load --no-system-fixtures ./fixtures --batch-size 10 --verbose

invenio oarepo communities create generic "Obecná komunita"

invenio oarepo index reindex
invenio oarepo index reindex
