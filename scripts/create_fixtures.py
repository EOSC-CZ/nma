"""
This script accepts a reference to RIV csv dump and creates names.yaml,
affiliations.yaml and funders.yaml fixture files for loading into NMA.

What it does:
- Reads the RIV csv dump line by line
- Extracts DOI if present, if not skips the line
- Calls RA service to see if the DOI is datacite or crossref
- Calls the appropriate service to get metadata for the DOI
- Extracts ORCID and ROR IDs from the metadata
- Calls ROR service to get affiliation names
- Calls ORCID service to get person names and their affiliations
- Collects unique names, affiliations, and funders
- Writes the collected data into names.yaml, affiliations.yaml, and funders.yaml
"""

from csv import DictReader

import click
from idutils import normalize_doi

from riv.utils import create_session_with_retries


@click.command()
@click.argument("riv_csv_dump", type=click.Path(exists=True))
def create_fixtures(riv_csv_dump):
    """Create fixture files from RIV CSV dump."""
    # Implementation of the logic described above goes here.
    names_by_orcid = {}
    affiliations_by_ror = {}
    funders_by_ror = {}
    session = create_session_with_retries(throttle_sleep=1)

    with open(riv_csv_dump, "r") as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            doi = row.get("doi_vysledku")
            if not doi:
                continue
            process_doi(
                doi, session, names_by_orcid, affiliations_by_ror, funders_by_ror
            )


def process_doi(doi, session, names_by_orcid, affiliations_by_ror, funders_by_ror):
    doi_provides = get_doi_provider(doi, session)
    if doi_provides == "datacite":
        orcids, affiliation_rors, funder_rors = get_datacite_metadata(doi, session)
    elif doi_provides == "crossref":
        orcids, affiliation_rors, funder_rors = get_crossref_metadata(doi, session)
    else:
        return
    for orcid in orcids:
        if orcid not in names_by_orcid:
            name, affiliation_rors = get_orcid_metadata(orcid, session)
            affiliations = {
                ror: get_ror_name(ror, affiliations_by_ror, session)
                for ror in affiliation_rors
            }
            names_by_orcid[orcid] = {"name": name, "affiliations": affiliations}
    for ror in affiliation_rors:
        if ror not in affiliations_by_ror:
            name = get_ror_name(ror, affiliations_by_ror, session)
            affiliations_by_ror[ror] = name
    for ror in funder_rors:
        if ror not in funders_by_ror:
            name = get_ror_name(ror, funders_by_ror, session)
            funders_by_ror[ror] = name


def get_doi_provider(doi, session):
    ra_url = f"https://doi.org/ra/{doi}"
    response = session.get(ra_url, allow_redirects=True).json()
    return response[0]["RA"].lower()


def get_datacite_metadata(doi, session):
    # Placeholder for actual implementation
    datacite_url = "https://api.datacite.org/dois/"
    doi = normalize_doi(doi)
    url = f"{datacite_url}/{doi}"
    response = session.get(url=url).json()

    return [], [], []


if __name__ == "__main__":
    create_fixtures()
