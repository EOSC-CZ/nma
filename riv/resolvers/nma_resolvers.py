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
from oarepo_related_resources.resolvers.base import ResolverProblem

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
        """DOIs are case-insensitive, so we lowercase them."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        return unicodedata.normalize("NFC", identifier.strip())

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
        """DOIs are case-insensitive, so we lowercase them."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        return unicodedata.normalize("NFC", identifier.strip())

    def exists(self, persistent_url: str) -> (dict | None, list[ResolverProblem]):
        crossref_url = current_app.config["CROSSREF_URL"]
        doi = normalize_doi(persistent_url)

        url = f"{crossref_url}/{doi}"
        response = self.session.get(url=url, timeout=self.resolve_timeout)
        if response.status_code != 200:
            return False
        return True

class NMAHandleResolver(HandleResolver):

    def normalize(self, identifier: str) -> str:
        """Handles are case-insensitive, so we lowercase them."""
        if identifier.startswith("http://"):
            identifier = identifier.replace("http://", "https://", 1)
        return unicodedata.normalize("NFC", identifier.strip())

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