from typing import Protocol

from riv.proxies import current_riv_extension
from riv.utils import create_session_with_retries


class MetadataResolver(Protocol):

    name: str

    def __init__(self):
        self.session = create_session_with_retries(
            total_retries=4,
            status_forcelist=[403, 429, 500, 502],
        )

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

