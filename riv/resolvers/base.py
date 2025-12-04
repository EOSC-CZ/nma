from typing import Protocol
from riv.proxies import current_riv_extension

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry



class MetadataResolver(Protocol):

    name: str

    def __init__(self):
        self.session = None

        retry_strategy = Retry(
            total=4,  # maximum number of retries
            status_forcelist=[403, 429, 500, 502],  # the HTTP status codes to retry on
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)

    def resolve(self, identifier: str) -> (dict | None, str):
        """Resolve metadata by identifier.

        If the metadata can not be resolved, returns (None, "error_message").
        If the metadata is resolved, returns (metadata_dict, "warning message").
        """


def resolve_metadata(persistent_url: str) -> (dict | None, str):
    """Resolve metadata by persistent url.

    If the metadata can not be resolved, returns (None, "error_message").
    If the metadata is resolved, returns (metadata_dict, "warning message").
    Raises ValueError if all resolvers fail (for now)
    """

    resolvers = current_riv_extension.persistent_identifiers_resolvers
    collected_messages = []


    for resolver in resolvers:
        try:
            metadata, message = resolver.resolve(persistent_url)
        except Exception as e:
            message = f"Error: {e}"
            metadata = None

        tagged_message = f"[{resolver.name}] {message}"
        collected_messages.append(tagged_message)

        if metadata is not None:
            metadata["persistent_url"] = persistent_url
            return metadata, tagged_message

    raise ValueError(
        f"Could not resolve metadata for identifier '{persistent_url}'.\n" +
        "\n".join(collected_messages)
    )

