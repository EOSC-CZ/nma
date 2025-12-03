from ..resolvers import MetadataResolver


class HandleResolver(MetadataResolver):
    name = "Handle"
    def resolve(self, identifier: str) -> (dict | None, str):
        return None, "Not implemented yet."