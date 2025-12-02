from ..resolvers import MetadataResolver


class CrossrefResolver(MetadataResolver):
    def resolve(self, identifier: str) -> (dict | None, str):
        return None, "Not implemented yet."