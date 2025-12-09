import dataclasses
import enum
from typing import Protocol

from flask import current_app
from flask_babel.speaklater import LazyString
from invenio_i18n import lazy_gettext as _

from riv.proxies import current_riv_extension
from riv.utils import create_session_with_retries


class ResolverProblemLevel(enum.Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclasses.dataclass
class ResolverProblem:
    resolver: str
    """Name of the resolver that produced this problem."""

    message: LazyString
    """Human-readable message describing the problem."""

    level: ResolverProblemLevel
    """Severity level of the problem."""

    original_exception: Exception | None = None
    """Original exception that caused the problem, if any."""


# TODO: if level is error -> generate glitchtip issue
# by logger.error(... resolver problem ...)


class UnresolvablePIDError(Exception):
    """Raised when a persistent identifier cannot be resolved to metadata.

    This exception means that all resolvers have failed to resolve the identifier
    - either network problems or the identifier is not supported. User should
    contact support in this case.
    """

    def __init__(self, identifier: str, problems: list[ResolverProblem]):
        self.identifier = identifier
        self.problems = problems
        super().__init__(f"Could not resolve identifier '{identifier}': {problems}.")


class UnsupportedPIDError(Exception):
    """Raised when a persistent identifier is not supported by any resolver.

    This exception means that the identifier format is not recognized by any
    of the configured resolvers. User should check the identifier or contact
    support.
    """

    def __init__(self, identifier: str):
        self.identifier = identifier
        super().__init__(f"Unsupported identifier '{identifier}'.")


class MetadataResolver(Protocol):

    name: str

    def __init__(self):
        self.session = create_session_with_retries(
            total_retries=4,
            status_forcelist=[403, 429, 500, 502],
        )

    def can_resolve(self, identifier: str) -> bool:
        """Check if this resolver can handle the given identifier.

        This call does not contact any external service, it just parses
        the identifier format.
        """
        return False

    def resolve(self, identifier: str) -> (dict | None, list[ResolverProblem]):
        """Resolve metadata by identifier.

        If the metadata can not be resolved, returns (None, list[ResolverProblem]).
        If the metadata is resolved, returns (metadata_dict, list[ResolverProblem]).
        """


def resolve_metadata(persistent_url: str) -> (dict | None, str):
    """Resolve metadata by persistent url.

    If the metadata can not be resolved, returns (None, "error_message").
    If the metadata is resolved, returns (metadata_dict, "warning message").
    Raises ValueError if all resolvers fail (for now)

        The first resolver that returns metadata wins and its problems are returned.

        If no resolver succeeds, the collected problems from all resolvers are returned.
    """

    resolvers = current_riv_extension.persistent_identifiers_resolvers
    collected_messages: list[ResolverProblem] = []
    can_be_resolved = False
    for resolver in resolvers:
        try:
            if not resolver.can_resolve(persistent_url):
                continue
            can_be_resolved = True
            metadata, problems = resolver.resolve(persistent_url)
        except Exception as e:
            current_app.logger.exception("Exception calling resolver %s", resolver)
            problems = [
                ResolverProblem(
                    resolver=resolver.name,
                    message=_(
                        "An unexpected error occurred in the resolver '%(resolver)s'.",
                        resolver=resolver.name,
                    ),
                    level=ResolverProblemLevel.ERROR,
                    original_exception=e,
                )
            ]
            metadata = None

        collected_messages.extend(problems)

        if metadata is not None:
            metadata["persistent_url"] = persistent_url
            return metadata, problems
        else:
            if not problems:
                raise ValueError(
                    f"Resolver {resolver} returned no metadata and no problems. "
                    "This is an implementation error and must be fixed."
                )

    if not can_be_resolved:
        raise UnsupportedPIDError(persistent_url)

    raise UnresolvablePIDError(persistent_url, collected_messages)
