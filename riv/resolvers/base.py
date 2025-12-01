from typing import Protocol


class MetadataResolver(Protocol):
    def resolve(self, identifier: str) -> (dict | None, str):
        """Resolve metadata by identifier.

        If the metadata can not be resolved, returns (None, "error_message").
        If the metadata is resolved, returns (metadata_dict, "warning message").
        """


def resolve_metadata(identifier: str) -> (dict | None, str):
    """Resolve metadata by identifier.

    If the metadata can not be resolved, returns (None, "error_message").
    If the metadata is resolved, returns (metadata_dict, "warning message").
    """
    # for cyklus
    resolver: MetadataResolver = ...
    return resolver.resolve(identifier)
