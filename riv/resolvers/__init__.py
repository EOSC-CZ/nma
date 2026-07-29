from .nma_resolvers import NMADataciteResolver, NMACrossrefResolver, NMAHandleResolver
from oarepo_related_resources.resolvers.base import MetadataResolver

__all__ = ["MetadataResolver",
           "DataciteResolver",
           "HandleResolver",
           "CrossrefResolver"
           ]
