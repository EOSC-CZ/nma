from pathlib import Path

from flask import current_app
from invenio_rdm_records.fixtures import FixturesEngine as InvenioFixturesEngine

from fixtures.harvesters import HarvestersFixture


class FixturesEngine(InvenioFixturesEngine):
    def run(self):
        """Run the fixture loading."""
        dir_ = Path(__file__).parent
        app_data_folder = Path(current_app.instance_path) / "app_data"
        data_folder = dir_ / "data"

        HarvestersFixture(
            [app_data_folder, data_folder],
            "harvesters.yaml",
        ).load()