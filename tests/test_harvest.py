
from oarepo_oaipmh_harvester.oai_batch.proxies import current_service as batch_service
from oarepo_oaipmh_harvester.oai_record.proxies import (
    current_service as oai_record_service,
)
from oarepo_oaipmh_harvester.cli import _add_harvester
from oarepo_oaipmh_harvester.harvester import harvest
from oarepo_oaipmh_harvester.oai_run.proxies import current_service as run_service
from invenio_access.permissions import system_identity
from test_datacite.proxies import current_service as model_service


def test_harvest_lindat(app, db, search_clear):

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
        all_records=False,
        on_background=False,
        identifiers=["oai:lindat.mff.cuni.cz:11858/00-097C-0000-0001-4872-3", "oai:lindat.mff.cuni.cz:11858/00-097C-0000-0001-B098-5"],
        title="Test harvest",
    )
    from time import sleep
    sleep(2)

    run = run_service.read(system_identity, run_id).data

    batch_records = list(batch_service.scan(system_identity).hits)
    for r in batch_records[0]["records"]:
        if "errors" in r:
            print(list(oai_record_service.scan(system_identity, params={"q": f'id:"{r["local_error_identifier"]}"'}).hits))
            print(r["errors"])

    assert run["errors"] == 0
    assert run["total_batches"] == 1
