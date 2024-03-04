def test_harvest_lindat(app, db, search_clear):
    data_count = 200
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
        "writer": "service{service=test_model}",

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

    print(run_id)
    print(run["errors"])
