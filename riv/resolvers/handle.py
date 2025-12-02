from ..resolvers import MetadataResolver


class HandleResolver(MetadataResolver):
    def resolve(self, identifier: str) -> (dict | None, str):
        return None, "Not implemented yet."