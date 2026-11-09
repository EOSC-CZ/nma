"""Harvesting datasets from the DataCite REST API (https://api.datacite.org/dois).

DataCite's OAI-PMH endpoint only supports provider / client sets, so records selected by
other criteria (e.g. affiliation country) are read from the REST API instead.

Harvester configuration:

```yaml
- id: datacite
  base-url: "https://api.datacite.org/dois"
  loader: datacite
  setspec: "affiliation-country=CZ"
  transformer:
    - "datacite"
    - "id-from-pid"
    - 'skip-if-owned{"model":"datasets"}'
```

`setspec` is the query string of the REST API (`affiliation-country=CZ`,
`query=creators.affiliation.name:Masaryk`, `client-id=...`, ...). Only datasets are
harvested - `resource-type-id=dataset` is always added. The REST API returns findable
DOIs only, so no record is ever reported as deleted.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any
from urllib import parse as urlparse

from ccmm_invenio.related_resources.datacite import map_datacite_access
from flask import current_app
from invenio_vocabularies.datastreams.readers import BaseReader
from invenio_vocabularies.datastreams.transformers import (
    BaseTransformer,
    TransformerError,
)
from oarepo_related_resources.resolvers import DataciteResolver
from oarepo_related_resources.resolvers.base import ResolverProblemLevel

from riv.utils import create_session_with_retries

from .zenodo import APIOAIHeader, APIOAIRecord

if TYPE_CHECKING:
    from collections.abc import Iterator

    from invenio_vocabularies.datastreams.datastreams import StreamEntry

DATACITE_API = "https://api.datacite.org/dois"
PAGE_SIZE = 1000
"""Maximum page size of the DataCite REST API."""


class DataciteReader(BaseReader):
    """Read datasets from the DataCite REST API, paging with a cursor."""

    def __init__(self, origin: str | None = None, mode: str = "r", *args: Any, **kwargs: Any) -> None:
        """Initialize the reader.

        Args:
            origin: REST API endpoint, defaults to the harvester's `base_url` or DataCite's API.
            set: Query string of the REST API (the harvester's `setspec`).
            from_date: Read only records updated since this date.
            identifiers: Read only these OAI identifiers (`oai:<host>:<doi>`).

        """
        self.set = kwargs.pop("set", None) or ""
        self.from_date = kwargs.pop("from_date", None)
        self.identifiers = kwargs.pop("identifiers", None)
        origin = origin or kwargs.pop("base_url", None) or DATACITE_API
        super().__init__(origin=origin, mode=mode, *args, **kwargs)  # noqa: B026
        self.oai_prefix = f"oai:{urlparse.urlparse(self._origin).hostname}:"

    def read(self, item: Any = None, *args: Any, **kwargs: Any) -> Iterator[APIOAIRecord]:
        """Yield the selected DOIs, there is no file to open."""
        yield from self._iter(fp=None)

    def _iter(self, fp: Any, *args: Any, **kwargs: Any) -> Iterator[APIOAIRecord]:
        """Yield the selected DOIs as OAI-like records with the DataCite JSON attributes."""
        session = create_session_with_retries(throttle_sleep=0.5)
        records = self._fetch_identifiers(session) if self.identifiers is not None else self._fetch_all(session)
        for record in records:
            yield APIOAIRecord(
                raw=json.dumps(record),
                json=record,
                header=APIOAIHeader(
                    identifier=self.oai_prefix + record["doi"],
                    datestamp=record["updated"],
                    deleted=False,
                ),
            )

    def params(self) -> dict[str, str]:
        """Query parameters of the first page - the set, datasets only, updated since from_date."""
        params = dict(urlparse.parse_qsl(self.set.lstrip("?")))
        params["resource-type-id"] = "dataset"
        params["affiliation"] = "true"
        params["page[size]"] = str(PAGE_SIZE)
        params["page[cursor]"] = "1"
        if self.from_date:
            updated = f"updated:[{self.from_date} TO *]"
            params["query"] = f"({params['query']}) AND {updated}" if params.get("query") else updated
        return params

    def _fetch_all(self, session: Any) -> Iterator[dict]:
        url: str | None = self._origin
        params: dict[str, str] | None = self.params()
        while url:
            current_app.logger.info("Fetching DataCite records from %s %s", url, params or "")
            response = session.get(url, params=params, headers={"Accept": "application/vnd.api+json"})
            response.raise_for_status()
            payload = response.json()
            hits = payload.get("data") or []
            current_app.logger.info("Fetched %d records", len(hits))
            for hit in hits:
                yield hit["attributes"]
            # the next link carries all the parameters
            url = (payload.get("links") or {}).get("next") if hits else None
            params = None

    def _fetch_identifiers(self, session: Any) -> Iterator[dict]:
        for identifier in self.identifiers or []:
            doi = identifier.removeprefix(self.oai_prefix)
            response = session.get(
                f"{self._origin.rstrip('/')}/{urlparse.quote(doi, safe='/')}",
                params={"affiliation": "true"},
                headers={"Accept": "application/vnd.api+json"},
            )
            response.raise_for_status()
            yield response.json()["data"]["attributes"]


class DataciteTransformer(BaseTransformer):
    """Convert DataCite JSON (REST API attributes) to the datasets model.

    The DOI is added to `metadata.identifiers` so that `id-from-pid` sets the record id
    (`doi/<doi>`) the same way as for the other harvesters.
    """

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        """Ignore the transformer options, there are none."""

    def apply(self, stream_entry: StreamEntry, *_args: Any, **_kwargs: Any) -> StreamEntry:
        """Transform the entry, fail on errors reported by the resolver."""
        oai_record = stream_entry.entry
        stream_entry.entry = {"oai_record": oai_record, "record": self.convert(oai_record.json)}
        return stream_entry

    def convert(self, data: dict) -> dict:
        """Convert DataCite JSON to the datasets record data."""
        resolver = DataciteResolver()
        resolver.metadata = data
        metadata, problems = resolver.resolve_metadata()
        errors = [problem.message for problem in problems if problem.level == ResolverProblemLevel.ERROR]
        if errors:
            raise TransformerError("; ".join(str(error) for error in errors))

        # first - id-from-pid uses the first DOI
        doi = data["doi"]
        identifiers = [
            identifier
            for identifier in metadata.get("identifiers", [])
            if not (identifier.get("scheme") == "doi" and identifier.get("identifier", "").lower() == doi.lower())
        ]
        metadata["identifiers"] = [{"identifier": doi, "scheme": "doi"}, *identifiers]
        return {
            "metadata": metadata,
            "files": {"enabled": False},
            "media_files": {"enabled": False},
            **map_datacite_access(data, metadata),
        }
