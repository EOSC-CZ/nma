
from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from invenio_access.permissions import system_identity

def get_ok_records():
    from test_datacite.proxies import current_service as model_service

    ok_records = list(model_service.scan(system_identity).hits)
    # ok_records = {x["oai"]["harvest"]["identifier"]: x for x in ok_records}
    return ok_records

def test_harvest_lindat(app, db, search_clear):

    batch_size = 50

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
        title="Test harvest",
    )
    run = run_service.read(system_identity, run_id).data
    from time import sleep
    sleep(5)
    data = get_ok_records()
    print(data)
    print(run["errors"])
    print(run["total_batches"])
