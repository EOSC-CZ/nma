from ..resolvers import MetadataResolver


class DataciteResolver(MetadataResolver):
    def resolve(self, identifier: str) -> (dict | None, str):
        return None, "Not implemented yet."