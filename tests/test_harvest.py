
from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from invenio_access.permissions import system_identity
from test_datacite.proxies import current_service as model_service


def get_ok_records():

    ok_records = list(model_service.scan(system_identity).hits)
    # ok_records = {x["oai"]["harvest"]["identifier"]: x for x in ok_records}
    return ok_records
# def test_indices(app, db, search_clear):
#     from invenio_search.proxies import current_search_client
#     with app.app_context():
#         for index in current_search_client.indices.get_mapping().keys():
#             print(index)
#             current_search_client.indices.delete(index=index, ignore=[400, 404])
def test_harvest_lindat(app, db, search_clear, destroy_indices):

    batch_size = 1000

    harvester_metadata = {
        "code": "lindat",
        "baseurl": "http://lindat.mff.cuni.cz/repository/oai/request?",
        "metadataprefix": "oai_dc",
        "comment": "comment",
        "name": "lindat",
        "batch_size": batch_size,
        "setspecs": "hdl_11858_00-097C-0000-0001-486F-D",
        "loader": "sickle",
        "transformers" : ["lindat_transformer"],
        "writer": "service{service=test_datacite}",

    }
    harvester = _add_harvester(harvester_metadata)
    run_id = harvest(
        harvester,
        # all_records=True,
        all_records=False,
        on_background=False,
        identifiers=["oai:lindat.mff.cuni.cz:11858/00-097C-0000-0001-B098-5"],
        # identifiers=None,
        # identifiers=["oai:lindat.mff.cuni.cz:11858/00-097C-0000-0001-4872-3"],
        title="Test harvest",
    )
    from time import sleep
    sleep(2)
    run = run_service.read(system_identity, run_id).data

    data = get_ok_records()
    batch_records = list(batch_service.scan(system_identity).hits)
    # print(batch_records)
    # print(data)
    print("errors ", run["errors"])
    for r in batch_records[0]["records"]:
        if "errors" in r:
            print(list(oai_record_service.scan(system_identity, params={"q": f'id:"{r["local_error_identifier"]}"'}).hits))
            print(r["errors"])
    print("batches", run["total_batches"])
