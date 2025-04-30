#
# Initialize NMA Instance
#

cd "$(dirname $0)/.."

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

invenio oarepo fixtures load --batch-size 1000 --verbose
invenio oarepo fixtures load --no-system-fixtures ./fixtures --batch-size 10 --verbose

invenio oarepo communities create generic "Obecná komunita"

invenio oarepo index reindex
invenio oarepo index reindex

# invenio oarepo oai harvester add nusl-manual-submissions --name "Manual submissions NUSL harvester" \
#             --url https://invenio.nusl.cz/oai2d --set manual_submission --prefix marcxml \
#             --loader 'sickle' \
#             --transformer marcxml --transformer nusl \
#             --writer 'service{service=documents}' \
#             --writer 'attachment{service=documents_file_draft}' \
#             --writer 'publish{service=documents}' \
#             --writer 'owner{service=documents}' \
#             --writer 'timestamp_update{service=documents,date_created_csv_path="./scripts/datecreated.csv"}'

if [ "$HARVEST" == "true" ] ; then
    echo "Starting harvest ..."
    # invenio oarepo oai harvester run nusl-manual-submissions --batch-size 10
fi
