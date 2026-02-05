import click

from riv.utils import create_session_with_retries


class NMAChecker:
    """Class to check NMA records and their various export formats."""

    def __init__(self, session, token=None):
        self.session = session
        self.token = token

    def _get_headers(self, accept_header):
        """Build headers including Authorization if token is provided."""
        headers = {"Accept": accept_header}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def check_all_records(self, server_url):
        """Check all records from the server."""
        listing_url = f"{server_url}/api/datasets"
        page_number = 1
        while listing_url:
            click.secho(f"Fetching page {page_number} of records...", fg="cyan")
            page = self.session.get(
                listing_url, headers=self._get_headers("application/json")
            )
            page.raise_for_status()
            ui_page = self.session.get(
                listing_url,
                headers=self._get_headers("application/vnd.inveniordm.v1+json"),
            )
            ui_page.raise_for_status()

            data = page.json()
            records = data["hits"]["hits"]
            for record in records:
                self.check_record(record)

            listing_url = data["links"].get("next")
            page_number += 1

    def check_record(self, record):
        """Check a single record."""
        html_url = record["links"]["self_html"]
        api_url = record["links"]["self"]

        click.secho(f"    Checking record {html_url}...", nl=False, fg="yellow")
        failures = []
        try:
            # get html view
            headers = {}
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
            self.session.get(html_url, headers=headers).raise_for_status()
        except Exception:
            failures.append("HTML view")

        try:
            # export in datacite json format, links[self] with accept
            datacite_response = self.session.get(
                api_url,
                headers=self._get_headers("application/vnd.datacite.datacite+json"),
            )
            datacite_response.raise_for_status()
        except Exception:
            failures.append("DataCite JSON export")

        try:
            # export in datacite xml format, links[self] with accept
            datacite_response = self.session.get(
                api_url,
                headers=self._get_headers("application/vnd.datacite.datacite+xml"),
            )
            datacite_response.raise_for_status()
        except Exception:
            failures.append("DataCite XML export")

        try:
            # get citation view
            citation_query = {"locale": "en-GB", "style": "iso690-author-date-cs"}
            citation_url = html_url.replace("/datasets/records/", "/api/datasets/")
            citation_response = self.session.get(
                citation_url,
                params=citation_query,
                headers=self._get_headers("text/x-bibliography"),
            )
            citation_response.raise_for_status()
        except Exception:
            failures.append("Citation view")
        if failures:
            click.secho(f" FAILED {', '.join(failures)}", fg="red")
        else:
            click.secho(" OK", fg="green")


@click.command("test-all-records")
@click.argument("server_url", default="https://nma.eosc.cz")
@click.option("--token", default=None, help="Bearer token for authentication")
def run(server_url, token):
    """Run all tests."""
    session = create_session_with_retries()
    checker = NMAChecker(session, token=token)
    checker.check_all_records(server_url)


if __name__ == "__main__":
    run()
