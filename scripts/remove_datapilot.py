#
# To run this file, do
#
# invenio shell
# %load 'scripts/remove_datapilot.py'
# remove_ids()
#

from datasets.proxies import current_service
from invenio_access.permissions import system_identity

def remove_ids():
    ids = []
    # scan all records
    for record in current_service.scan(system_identity):
        url = record['metadata'].get('url')
        if url.startswith('https://data.narodni-repozitar.cz/'):
            ids.append(record['id'])
            print(record['id'])

    print(f"Found {len(ids)} records to remove")
    # remove all records
    for id in ids:
        current_service.delete(system_identity, id)

