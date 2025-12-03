PERSISTENT_IDENTIFIER_RESOLVERS = [
    "riv.resolvers.DataciteResolver",
    "riv.resolvers.CrossrefResolver",
    "riv.resolvers.HandleResolver",
]

PERSISTENT_IDENTIFIER_PREFIXES = {
    "https://doi.org/": "doi",
    "https://hdl.handle.net/": "handle",
}


SECRET_LINK_EXPIRATION_DAYS = 7
RIV_CURATORS_GROUP_ID = "riv_curators"
