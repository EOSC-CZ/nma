#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""RIV resolver config."""

PERSISTENT_IDENTIFIER_RESOLVERS = [
    "riv.resolvers.DataciteResolver",
    "riv.resolvers.CrossrefResolver",
    "riv.resolvers.HandleResolver",
]

PERSISTENT_IDENTIFIER_PATTERNS = {
    r"https://doi.org/(.*)": "doi",
    r"https://hdl.handle.net/(.*)": "handle",
}


SECRET_LINK_EXPIRATION_DAYS = 7
RIV_CURATORS_GROUP_ID = "riv_curators"

# Revalidate the persistent URL if it was last checked more than this number of days ago
LAST_CHECKED_THRESHOLD_DAYS = 2

DATACITE_URL="https://api.datacite.org/dois"
