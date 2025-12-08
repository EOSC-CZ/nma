from urllib.error import HTTPError

from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.readers import BaseReader
from invenio_vocabularies.datastreams.transformers import BaseTransformer

from riv.utils import create_session_with_retries


class CatchAllReader(BaseReader):

    def __init__(self, origin=None, mode="r", *args, **kwargs):
        super().__init__(
            origin=origin or "https://datarepo.eosc.cz/datasets/all/",
            mode=mode,
            *args,
            **kwargs,
        )

    def _iter(self, fp, *args, **kwargs):
        session = create_session_with_retries()
        for seq, record in enumerate(self.fetch_records(session)):
            if record is None:
                yield None
            else:
                files_link = record["links"]["self"] + "/files/"
                files = session.get(files_link, headers={"Accept": "application/json"})
                files.raise_for_status()
                record["files"] = files.json()
                yield StreamEntry(
                    entry=record,
                )

    def read(self, item=None, *args, **kwargs):
        yield from self._iter(fp=None, *args, **kwargs)

    def fetch_records(self, session):
        url = self._origin
        retry_count = 5
        count = 0

        while True:
            try:
                response = session.get(url, headers={"Accept": "application/json"})
                response.raise_for_status()
                payload = response.json()
                for hit in payload["hits"]["hits"]:
                    # need to re-get as we do not have all fields in the hit
                    yield session.get(
                        hit["links"]["self"], headers={"Accept": "application/json"}
                    ).json()
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


class CatchAllTransformer(BaseTransformer):
    pass


if __name__ == "__main__":

    def run():
        loader = CatchAllReader(
            origin="https://datarepo.eosc.cz/datasets/all/",
        )
        for record in loader.read():
            print(record.entry)

    run()
