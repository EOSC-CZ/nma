from ..resolvers import MetadataResolver


class CrossrefResolver(MetadataResolver):

    name = "Crossref"
    def resolve(self, identifier: str) -> (dict | None, str):
        return None, "Not implemented yet."