import json
import dataclasses
from urllib import parse as urlparse

from flask import current_app
from invenio_vocabularies.datastreams.readers import BaseReader

from riv.utils import create_session_with_retries
from invenio_vocabularies.datastreams.transformers import BaseTransformer
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from riv.resolvers import DataciteResolver

@dataclasses.dataclass
class APIOAIHeader:
    identifier: str
    datestamp: str
    deleted: bool


@dataclasses.dataclass
class APIOAIRecord:
    raw: str
    json: dict
    header: APIOAIHeader


class ZenodoReader(BaseReader):

    def __init__(self, origin=None, mode="r", *args, **kwargs):

        self.set = kwargs.get("set")

        super().__init__(
            origin=origin or "https://zenodo.org/api/records/",
            mode=mode,
            *args,
            **kwargs,
        )

    def _iter(self, fp, *args, **kwargs):
        session = create_session_with_retries()
        oai_prefix = f"oai:{urlparse.urlparse(self._origin).hostname}:"

        for record in self.fetch_records(session):
            yield APIOAIRecord(
                raw=json.dumps(record),
                json=record,
                header=APIOAIHeader(
                    identifier=oai_prefix + str(record["id"]),
                    datestamp=record["updated"],
                    deleted=False,
                ),
            )

    def read(self, item=None, *args, **kwargs):
        yield from self._iter(fp=None, *args, **kwargs)

    def fetch_records(self, session):
        url = self._origin

        while True:
            current_app.logger.info("Fetching Zenodo records from %s", url)

            response = session.get(
                url,
                headers={"Accept": "application/json"},
                params={
                        "q": self.set,
                        },
            )
            response.raise_for_status()
            payload = response.json()

            hits = payload.get("hits", {}).get("hits", [])
            current_app.logger.info("Fetched %d records", len(hits))

            for hit in hits:
                record = session.get(
                    hit["links"]["self"], headers={"Accept": "application/vnd.datacite.datacite+json"}
                ).json()
                record["id"] = hit["conceptrecid"]
                record["updated"] = hit["modified"]
                yield record


            if "next" in payload["links"]:
                url = payload["links"]["next"]
            else:
                # otherwise we are done
                break
class ZenodoTransformer(BaseTransformer):

    def __init__(self, *args, **kwargs):
        pass

    def apply(self, stream_entry: StreamEntry, *args, **kwargs) -> StreamEntry:
        """
        Transforms the entry.
        """
        stream_entry.entry = {
            "oai_record": stream_entry.entry,
            "record": self.convert_zenodo_to_rdm(stream_entry.entry.json),
        }
        return stream_entry

    def convert_zenodo_to_rdm(self, rec):
        resolver = DataciteResolver()
        metadata, _ = resolver.resolve_metadata(rec) #todo handle problems?
        rdm_record = {
            "id": rec["id"],
            "metadata": metadata,
        }
        rdm_record["files"] = {"enabled": False}
        rdm_record["media_files"] = {"enabled": False}

        return rdm_record