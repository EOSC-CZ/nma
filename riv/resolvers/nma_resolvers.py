import re
import unicodedata
from oarepo_related_resources.resolvers.datacite import DataciteResolver
from oarepo_related_resources.resolvers.handle import HandleResolver
from oarepo_related_resources.resolvers.crossref import CrossrefResolver
from idutils.validators import is_doi
from idutils.validators import is_handle
from flask import current_app
from idutils.normalizers import normalize_doi
from idutils.normalizers import normalize_handle
from invenio_i18n import lazy_gettext as _
from lxml import etree
from oarepo_related_resources.errors import UpstreamFetchError
from oarepo_related_resources.resolvers.base import ResolverProblem, ResolverProblemLevel

class NMADataciteResolver(DataciteResolver):
    def can_resolve(self, persistent_url: str) -> bool:
        return is_doi(persistent_url)

    def generate_id(self, identifier: str) -> str:
        pattern = r"https://doi.org/(.*)"
        m = re.match(pattern, identifier)
        if m:
            return f"doi/{m.group(1)}"
        raise ValueError(f"Could not generate pid from url: {identifier}")

    def normalize(self, identifier: str) -> str:
        """Normalize a DOI using the shared resolver normalizer."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        identifier = unicodedata.normalize("NFC", identifier.strip())
        doi = self.normalize_identifier(identifier)
        return f"https://doi.org/{doi}"

    def exists(self, persistent_url: str) -> bool:
        datacite_url = current_app.config.get("DATACITE_URL")
        doi = normalize_doi(persistent_url)
        url = f"{datacite_url}/{doi}"
        response = self.session.get(url=url, timeout=self.resolve_timeout)
        if response.status_code != 200:
            return False
        return True

class NMACrossrefResolver(CrossrefResolver):
    def can_resolve(self, persistent_url: str) -> bool:
        return is_doi(persistent_url)

    def generate_id(self, identifier: str) -> str:
        pattern = r"https://doi.org/(.*)"
        m = re.match(pattern, identifier)
        if m:
            return f"doi/{m.group(1)}"
        raise ValueError(f"Could not generate pid from url: {identifier}")

    def normalize(self, identifier: str) -> str:
        """Normalize a DOI using the shared resolver normalizer."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        identifier = unicodedata.normalize("NFC", identifier.strip())
        doi = self.normalize_identifier(identifier)
        return f"https://doi.org/{doi}"

    def exists(self, persistent_url: str) -> (dict | None, list[ResolverProblem]):
        crossref_url = current_app.config["CROSSREF_URL"]
        doi = normalize_doi(persistent_url)

        url = f"{crossref_url}/{doi}"
        response = self.session.get(url=url, timeout=self.resolve_timeout)
        if response.status_code != 200:
            return False
        return True

class NMAHandleResolver(HandleResolver):

    def resolve(self, identifier: str) -> tuple[dict, list[ResolverProblem]]:
        """Read the landing page; if the source refuses it or it is not a web page, let the user fill the form in.

        A problem makes the registration open the deposit form, see `deposit_create`. Server errors and
        timeouts are still raised, trying again later may help there.
        """
        try:
            return super().resolve(identifier)
        except UpstreamFetchError as e:
            if e.error_code >= 500:
                raise
            cause = e
        except (IndexError, etree.ParserError) as e:  # a file, without an html head
            cause = e
        current_app.logger.warning("No metadata could be read from %s: %s", identifier, cause)
        return {}, [
            ResolverProblem(
                "handle",
                _("The metadata could not be read from the source of this identifier. Please fill it in below."),
                ResolverProblemLevel.WARNING,
                original_exception=cause,
            )
        ]

    def normalize(self, identifier: str) -> str:
        """Normalize a Handle using the shared resolver normalizer."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        identifier = unicodedata.normalize("NFC", identifier.strip())
        handle = self.normalize_identifier(identifier)
        return f"https://hdl.handle.net/{handle}"

    def generate_id(self, identifier: str) -> str:
        pattern = r"https?://hdl.handle.net/(.+)"
        m = re.match(pattern, identifier)
        if m:
            return f"handle/{m.group(1)}"
        raise ValueError(f"Could not generate pid from url: {identifier}")

    def can_resolve(self, persistent_url: str) -> bool:
        persistent_url = self.normalize(persistent_url)
        return is_handle(persistent_url) and "https://hdl.handle.net" in persistent_url

    def exists(self, persistent_url: str) -> bool:
        handle_url = current_app.config.get("HANDLE_URL")
        handle = normalize_handle(persistent_url)
        url = f"{handle_url}/{handle}"
        response = self.session.get(
            url=url, timeout=self.resolve_timeout, allow_redirects=False
        )
        return 200 <= response.status_code < 400