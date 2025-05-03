from typing import Iterable
from urllib.error import HTTPError

from oarepo_runtime.datastreams import BaseReader, StreamEntry

from common.oai.http import url_get


class DataRepoLoader(BaseReader):
    def __init__(
        self,
        *,
        source,
        all_records=None,
        identifiers=None,
        oai_config=None,
        datestamp_from=None,
        datestamp_until=None,
        oai_run=None,
        oai_harvester_id=None,
        manual=False,
        **kwargs,
    ):

        super().__init__(source=source, **kwargs)
        self.all_records = all_records
        self.identifiers = identifiers
        self.oai_config = oai_config
        self.oai_run = oai_run
        self.oai_harvester_id = oai_harvester_id
        self.manual = manual

    def __iter__(self) -> Iterable[StreamEntry]:
        """
        Return iterable or none if there is error
        """
        # todo: filtering and double checking if affiliation is correct

        for seq, record in enumerate(self.fetch_records()):
            if record is None:
                yield None
            else:
                # files_link = record["links"]["self"] + "/files/"
                # files = url_get(files_link, headers={"Accept": "application/json"})
                # files.raise_for_status()
                # record["files"] = files.json()
                record["files"] = []  # for now, no files, just converting metadata
                yield StreamEntry(
                    entry=record,
                    seq=seq,
                    context={
                        "oai": {
                            "metadata": (
                                record["metadata"] if "metadata" in record else {}
                            ),
                            "datestamp": record["metadata"]["dateAvailable"]
                            + "T00:00:00+00:00",
                            "deleted": False,
                            "identifier": f"oai:datarepo.eosc.cz:{record['id']}",
                            "setSpecs": "all",
                            "oai_url": self.source,
                        },
                        "oai_run": self.oai_run,
                        "oai_harvester_id": self.oai_harvester_id,
                        "manual": self.manual,
                    },
                )

    def fetch_records(self):
        url = self.source
        retry_count = 5
        count = 0

        while True:
            try:
                response = url_get(url, headers={"Accept": "application/json"})
                response.raise_for_status()
                payload = response.json()
                for hit in payload["hits"]["hits"]:
                    yield hit
                if "next" in payload["links"]:
                    url = payload["links"]["next"]
                    count = 0
                else:
                    break
            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                if count >= retry_count:
                    raise
                count += 1
            except Exception as err:
                print(f"Other error occurred: {err}")
                if count >= retry_count:
                    raise
                count += 1


if __name__ == "__main__":

    def run():
        loader = DataRepoLoader(
            source="https://datarepo.eosc.cz/datasets/all/",
            all_records=True,
            identifiers=None,
            oai_config=None,
            oai_run=None,
            oai_harvester_id=None,
            manual=False,
        )
        for record in loader:
            print(record)

    run()
