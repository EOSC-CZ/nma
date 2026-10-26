#!/usr/bin/env python3
"""Download NMA datasets into a JSONL file.

By default, datasets created by OAI harvesting are skipped. They are identified
by the record_pid of the OAI harvest records (requires a bearer token with access
to the harvest API).
"""

import json
import time
import urllib.request
from urllib.parse import urlencode

import click
from tqdm import tqdm

DEFAULT_URL = "https://nma.eosc.cz/api/datasets"
DEFAULT_HARVEST_URL = "https://nma.eosc.cz/api/oai/harvest/records"


def fetch(url, token=None, retries=3):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except Exception as e:
            if attempt == retries - 1:
                raise
            tqdm.write(f"Error fetching {url}: {e}, retrying...")
            time.sleep(2**attempt)


def paginate(url, size, desc, token=None, sort=None):
    params = {"size": size}
    if sort:
        params["sort"] = sort
    url = f"{url}?{urlencode(params)}"
    with tqdm(desc=desc, unit="rec") as bar:
        while url:
            data = fetch(url, token)
            hits = data["hits"]["hits"]
            bar.total = data["hits"]["total"]
            for hit in hits:
                yield hit
                bar.update()
            url = data["links"].get("next") if hits else None


@click.command(help=__doc__)
@click.argument("output", type=click.Path(dir_okay=False), default="nma_datasets.jsonl")
@click.option("--url", default=DEFAULT_URL, show_default=True, help="Datasets API endpoint")
@click.option(
    "--harvest-url", default=DEFAULT_HARVEST_URL, show_default=True, help="OAI harvest records API endpoint"
)
@click.option("--token", envvar="BEARER", help="Bearer token for the harvest API [env: BEARER]")
@click.option(
    "--exclude-harvested/--include-harvested",
    default=True,
    show_default=True,
    help="Skip datasets that were created by OAI harvesting",
)
@click.option("--size", default=100, show_default=True, help="Page size")
def main(output, url, harvest_url, token, exclude_harvested, size):
    harvested = set()
    if exclude_harvested:
        if not token:
            raise click.UsageError("--token (or $BEARER) is required with --exclude-harvested")
        harvested = {
            r["record_pid"] for r in paginate(harvest_url, size, "Harvest records", token) if r.get("record_pid")
        }
        click.echo(f"Found {len(harvested)} harvested record pids", err=True)

    seen = set()
    skipped = 0
    with open(output, "w", encoding="utf-8") as f:
        # sort by oldest so records created during the download do not shift pages
        for hit in paginate(url, size, "Datasets", sort="oldest"):
            if hit["id"] in seen:
                continue
            seen.add(hit["id"])
            if hit["id"] in harvested:
                skipped += 1
                continue
            f.write(json.dumps(hit, ensure_ascii=False) + "\n")

    click.echo(f"Wrote {len(seen) - skipped} records to {output} (skipped {skipped} harvested)", err=True)


if __name__ == "__main__":
    main()
