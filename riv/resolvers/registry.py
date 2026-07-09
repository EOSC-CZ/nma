from flask import current_app
from requests.exceptions import RetryError
from urllib3.exceptions import MaxRetryError

from riv.proxies import current_riv_extension

from .base import (
    PIDDoesNotExistError,
    PIDProcessingError,
    ResolverProblem,
    UnsupportedPIDError,
)


class ResolverRegistry:

    def can_resolve(self, persistent_url):
        resolvers = current_riv_extension.persistent_identifiers_resolvers
        can_be_resolved = False
        for resolver in resolvers:

            if not resolver.can_resolve(persistent_url):
                continue
            can_be_resolved = True

        return can_be_resolved

    def find_resolver(self, persistent_url):
        resolvers = current_riv_extension.persistent_identifiers_resolvers
        resolver_seen = False
        for resolver in resolvers:
            if not resolver.can_resolve(persistent_url):
                continue
            resolver_seen = True
            if resolver.exists(persistent_url):
                return resolver
        if not resolver_seen:
            raise UnsupportedPIDError(persistent_url)
        raise PIDDoesNotExistError(persistent_url)

    def resolve(self, persistent_url):
        """
        Resolve metadata with the correct resolver.
        return: The whole record
        example: {id: xy, metadata:{...}}
        """
        normalized_persistent_url = self.normalize(persistent_url)
        collected_messages: list[ResolverProblem] = []

        try:
            resolver = self.find_resolver(normalized_persistent_url)
        except UnsupportedPIDError:
            raise
        except PIDDoesNotExistError:
            raise
        except Exception as e:
            if isinstance(e, RetryError) and e.args:
                e = e.args[0]
            if isinstance(e, MaxRetryError):
                e = getattr(e, "reason", e)
            current_app.logger.exception(
                "Unexpected error while finding resolver for id: %s",
                normalized_persistent_url,
            )
            raise PIDProcessingError(str(e))
        try:
            metadata, problems = resolver.resolve(normalized_persistent_url)
        except Exception as e:
            current_app.logger.exception(
                "Exception calling resolver %s %s", resolver, normalized_persistent_url
            )
            raise PIDProcessingError(str(e))

        collected_messages.extend(problems)
        if metadata is None:
            raise Exception("Implementation error.")
        metadata["persistent_url"] = persistent_url

        return {
            "metadata": metadata,
            "id": resolver.generate_id(normalized_persistent_url),
        }, collected_messages

    def generate_id(self, persistent_url):
        resolvers = current_riv_extension.persistent_identifiers_resolvers
        for resolver in resolvers:
            if resolver.can_resolve(persistent_url):
                normalized_identifier = resolver.normalize(persistent_url)
                return resolver.generate_id(normalized_identifier)
        raise UnsupportedPIDError(persistent_url)

    def normalize(self, persistent_url) -> str:
        resolvers = current_riv_extension.persistent_identifiers_resolvers
        for resolver in resolvers:
            if resolver.can_resolve(persistent_url):
                return resolver.normalize(persistent_url)
        raise UnsupportedPIDError(persistent_url)
