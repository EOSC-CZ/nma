from __future__ import annotations

import time
from csv import DictReader
from itertools import chain
from typing import TYPE_CHECKING

from celery import shared_task
from flask import current_app
from idutils import normalize_doi
from invenio_jobs.jobs import JobType, PredefinedArgsSchema
from marshmallow import fields

from datasets.services.idutils import (
    resolve_orcid,
    resolve_ror,
)

from ..utils import create_session_with_retries

if TYPE_CHECKING:
    pass


DOIS_BATCH_SIZE = 100


def seconds_to_hms(seconds: float) -> str:
    """Convert seconds to hours, minutes, seconds string."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


@shared_task(ignore_result=True)
def load_identifiers_from_riv_dump(
    riv_csv_url: str = "https://www.isvavai.cz/dokumenty/opendata/RIV-2024.csv",
):
    session = create_session_with_retries(throttle_sleep=0.1)
    dois_to_process: set[str] = set()
    current_app.logger.info(f"Fetching RIV dump from {riv_csv_url}")
    with session.get(riv_csv_url, stream=True) as response:
        response.raise_for_status()
        reader = DictReader(response.iter_lines(decode_unicode=True))
        for row in reader:
            doi = row.get("doi_vysledku")
            if not doi:
                continue
            # the doi might be malformed:
            if doi.startswith("http://") or doi.startswith("https://"):
                doi = doi.split("doi.org/")[-1]
            if doi.startswith("doi:"):
                doi = doi.replace("doi:", "")
            if doi.startswith("DOI:"):
                doi = doi.replace("DOI:", "")
            if doi.startswith("dx.doi.org/"):
                doi = doi.replace("dx.doi.org/", "")
            if doi.startswith("https://"):
                doi = doi.replace("https://", "")
            if doi.startswith("http://"):
                doi = doi.replace("http://", "")
            dois_to_process.add(doi)
    total_dois = len(dois_to_process)
    current_app.logger.info(f"Total DOIs to process from RIV dump: {total_dois}")

    start_time = time.time()
    seen: set[str] = set()
    for idx, doi in enumerate(dois_to_process, 1):
        try:
            load_identifiers_from_doi(doi, session, seen)
        except Exception:
            current_app.logger.exception("Error processing DOI %s: ", doi)

        elapsed = time.time() - start_time
        rate = idx / elapsed if elapsed > 0 else 0
        remaining = (total_dois - idx) / rate if rate > 0 else 0

        current_app.logger.info(
            f"Identifiers import: {idx}/{total_dois} ({idx*100//total_dois}%) {seconds_to_hms(elapsed)}, ETA {seconds_to_hms(remaining)}"
        )
        current_app.logger.info(f"    - DOI: {doi}")


def load_identifiers_from_doi(doi: str, session, seen: set[str] | None = None):
    if seen is None:
        seen = set()
    doi_provider = get_doi_provider(doi, session)
    if doi_provider == "datacite":
        orcids, affiliation_rors, funder_rors = get_datacite_metadata(doi, session)
    elif doi_provider == "crossref":
        orcids, affiliation_rors, funder_rors = get_crossref_metadata(doi, session)
    else:
        current_app.logger.info(
            f"DOI provider for {doi} not recognized: {doi_provider}"
        )
        return
    current_app.logger.info(
        f"DOI {doi} provided by {doi_provider}: "
        f"{len(orcids)} ORCIDs, "
        f"{len(affiliation_rors)} affiliation RORs, "
        f"{len(funder_rors)} funder RORs"
    )
    # limit to first 30 ORCIDs to not harvest articles with hundreds/thousands of authors
    # for example: 10.1016/j.physletb.2024.139007 has 2800+ authors with ORCID
    for orcid_value in list(orcids)[:30]:
        if f"orcid:{orcid_value}" in seen:
            continue
        seen.add(f"orcid:{orcid_value}")
        try:
            current_app.logger.info(f"Resolving ORCID: {orcid_value}")
            resolve_orcid(orcid_value, "names", session=session)
        except Exception as e:
            current_app.logger.error(f"Error resolving ORCID: {orcid_value}: {str(e)}")
    for ror in list(affiliation_rors)[:30]:
        if f"affiliation:{ror}" in seen:
            continue
        seen.add(f"affiliation:{ror}")
        try:
            current_app.logger.info(f"Resolving ROR in affiliation: {ror}")
            resolve_ror(ror, "affiliations", session=session)
        except Exception as e:
            current_app.logger.error(
                f"Error resolving ROR in affiliation: {ror}: {str(e)}"
            )
    for ror in list(funder_rors)[:30]:
        if f"funder:{ror}" in seen:
            continue
        seen.add(f"funder:{ror}")
        try:
            current_app.logger.info(f"Resolving ROR in funder: {ror}")
            resolve_ror(ror, "funders", session=session)
        except Exception as e:
            current_app.logger.error(f"Error resolving ROR in funder: {ror}: {str(e)}")


def get_doi_provider(doi, session):
    ra_url = f"https://doi.org/ra/{doi}"
    response = session.get(ra_url, allow_redirects=True).json()
    if "RA" not in response[0]:
        current_app.logger.warning(
            "Could not determine DOI provider for %s: %s", doi, response
        )
        return "Invalid"
    return response[0]["RA"].lower()


def get_datacite_metadata(doi, session):
    # Placeholder for actual implementation
    datacite_url = "https://api.datacite.org/dois/"
    doi = normalize_doi(doi)
    url = f"{datacite_url}/{doi}"
    response = session.get(url=url).json()
    attrs = response.get("data", {}).get("attributes", {})
    return (
        set(parse_orcids_from_datacite(attrs)),
        set(parse_affiliation_rors_from_datacite(attrs)),
        set(parse_funder_rors_from_datacite(attrs)),
    )


def parse_orcids_from_datacite(attrs):
    for c in chain(attrs.get("creators", []), attrs.get("contributors", [])):
        for identifier in c.get("nameIdentifiers", []):
            if identifier.get("nameIdentifierScheme") == "ORCID":
                orcid_identifier = identifier.get("nameIdentifier")
                yield orcid_identifier


def parse_affiliation_rors_from_datacite(attrs):
    for c in chain(attrs.get("creators", []), attrs.get("contributors", [])):
        for affiliation in c.get("affiliations", []):
            if not isinstance(affiliation, dict):
                continue
            ror = affiliation.get("affiliationIdentifier")
            if affiliation.get("affiliationIdentifierScheme") == "ROR" and ror:
                yield ror


def parse_funder_rors_from_datacite(attrs):
    for f in attrs.get("fundingReferences", []):
        ror = f.get("funderIdentifier")
        if f.get("funderIdentifierType") == "ROR" and ror:
            yield ror


def get_crossref_metadata(doi, session):
    # Placeholder for actual implementation
    crossref_url = "https://api.crossref.org/works/"
    doi = normalize_doi(doi)
    url = f"{crossref_url}{doi}"
    response = session.get(url=url).json()
    message = response.get("message", {})
    return (
        set(parse_orcids_from_crossref(message)),
        set(parse_affiliation_rors_from_crossref(message)),
        set(parse_funder_rors_from_crossref(message)),
    )


def parse_orcids_from_crossref(message):
    """
    Parse ORCID identifiers from Crossref metadata.

    Crossref structure for contributors (author, editor, chair, translator):
    - ORCID: URL-form of an ORCID identifier (e.g., "https://orcid.org/0000-0001-2345-6789")
    - authenticated-orcid: Boolean indicating if ORCID was authenticated
    """
    for contributor_type in ["author", "editor", "chair", "translator"]:
        for contributor in message.get(contributor_type, []):
            orcid = contributor.get("ORCID")
            if orcid:
                # ORCID is provided as a URL, extract just the identifier
                # Format: https://orcid.org/0000-0001-2345-6789
                if orcid.startswith("https://orcid.org/"):
                    yield orcid.replace("https://orcid.org/", "")
                elif orcid.startswith("http://orcid.org/"):
                    yield orcid.replace("http://orcid.org/", "")
                else:
                    # If it's already just the ID, yield as-is
                    yield orcid


def parse_affiliation_rors_from_crossref(message):
    """
    Parse ROR identifiers from affiliation data in Crossref metadata.

    Crossref structure for affiliations (nested under contributors):
    - affiliation: Array of affiliation objects
      - name: String (affiliation name)
      - id: Array of identifier objects (optional, added in recent schema updates)
        - id: String (the identifier value, e.g., ROR URL)
        - id-type: String (e.g., "ROR", "ISNI")
        - asserted-by: String (who provided the ID)

    Note: ROR support in Crossref affiliations is relatively new and not all
    records have structured ROR identifiers yet.
    """
    for contributor_type in ["author", "editor", "chair", "translator"]:
        for contributor in message.get(contributor_type, []):
            for affiliation in contributor.get("affiliation", []):
                # Check for structured identifiers (newer format)
                for identifier in affiliation.get("id", []):
                    if identifier.get("id-type", "").upper() == "ROR":
                        ror = identifier.get("id", "")
                        if ror:
                            # ROR IDs may be URLs (https://ror.org/abc123) or just IDs
                            if ror.startswith("https://ror.org/"):
                                yield ror.replace("https://ror.org/", "")
                            elif ror.startswith("http://ror.org/"):
                                yield ror.replace("http://ror.org/", "")
                            else:
                                yield ror


def parse_funder_rors_from_crossref(message):
    """
    Parse ROR identifiers from funder data in Crossref metadata.

    Crossref structure for funders:
    - funder: Array of funder objects
      - name: String (funder name)
      - DOI: String (Crossref Funder Registry DOI, format: 10.13039/...)
      - award: Array of strings (award numbers)
      - doi-asserted-by: String (who provided the DOI)
      - id: Array of identifier objects (newer schema)
        - id: String (identifier value)
        - id-type: String (e.g., "DOI", "ROR")
        - asserted-by: String

    Note: Most funders use Crossref Funder Registry DOIs (10.13039/...).
    ROR identifiers for funders are less common but may appear in the 'id' array.
    """
    for funder in message.get("funder", []):
        # Check for structured identifiers with ROR
        for identifier in funder.get("id", []):
            if identifier.get("id-type", "").upper() == "ROR":
                ror = identifier.get("id", "")
                if ror:
                    # ROR IDs may be URLs (https://ror.org/abc123) or just IDs
                    if ror.startswith("https://ror.org/"):
                        yield ror.replace("https://ror.org/", "")
                    elif ror.startswith("http://ror.org/"):
                        yield ror.replace("http://ror.org/", "")
                    else:
                        yield ror


class LoadIdentifiersFromRIVDumpJobSchema(PredefinedArgsSchema):
    job_arg_schema = fields.String(
        metadata={"type": "hidden"},
        dump_default="LoadIdentifiersFromRIVDumpJobSchema",
        load_default="LoadIdentifiersFromRIVDumpJobSchema",
    )

    riv_csv_url = fields.String(
        required=True,
        metadata={
            "description": "URL of the RIV CSV dump (https://www.isvavai.cz/opendata, file RIV-year.csv)."
        },
    )


class LoadIdentifiersFromRIVDumpJob(JobType):
    """A job type to run invenio CLI commands as Celery tasks."""

    id = "load_identifiers_from_riv_dump"
    title = "Import RIV identifiers"
    description = "Import names, affiliations and funders from RIV CSV dump."

    task = load_identifiers_from_riv_dump

    arguments_schema = LoadIdentifiersFromRIVDumpJobSchema

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, riv_csv_url=None, **kwargs):
        """Override to define extra arguments to be injected on task execution.

        :param job_obj (Job): the Job object.
        :param since (datetime): last time the job was executed, or None if never
            executed.
        :return: a dict of arguments to be injected on task execution.
        """
        return {"riv_csv_url": riv_csv_url}
