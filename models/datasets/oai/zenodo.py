import dataclasses
import json
from urllib import parse as urlparse

from flask import current_app
from invenio_vocabularies.datastreams.datastreams import StreamEntry
from invenio_vocabularies.datastreams.readers import BaseReader
from invenio_vocabularies.datastreams.transformers import BaseTransformer

from oarepo_related_resources.resolvers import DataciteResolver
from riv.utils import create_session_with_retries


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
        # sleep 2 seconds between requests to be kind to Zenodo servers
        session = create_session_with_retries(throttle_sleep=2.0)
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
                    hit["links"]["self"],
                    headers={"Accept": "application/vnd.datacite.datacite+json"},
                ).json()
                record["id"] = hit["conceptrecid"] #todo: why??
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
            "record": self.convert_zenodo_to_ccmm(stream_entry.entry.json),
        }
        return stream_entry

    def convert_zenodo_to_ccmm(self, rec):

        resolver = DataciteResolver()
        resolver.metadata = rec
        metadata, problems = resolver.resolve_metadata()


        doi = rec["doi"]

        record_id = f"doi/{doi}"
        metadata["persistent_url"] = f"https://doi.org/{doi}"


        ccmm_record = {
            "id": record_id,
            "metadata": metadata,
        }
        ccmm_record["files"] = {"enabled": False}
        ccmm_record["media_files"] = {"enabled": False}

        return ccmm_record
