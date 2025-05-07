from oarepo_runtime.datastreams import StreamBatch
from oarepo_runtime.datastreams.transformers import BaseTransformer


class CommunityTransformer(BaseTransformer):
    def __init__(self, community: str, **kwargs) -> None:
        """Community transformer.
        :param community: The community to set.
        """
        super().__init__(**kwargs)
        self.community = community

    def apply(self, batch: StreamBatch, *args, **kwargs) -> StreamBatch | None:
        """Applies the transformation to the entry.
        :returns: A StreamEntry. The transformed entry.
                  Raises TransformerError in case of errors.
        """
        for entry in batch.entries:
            entry.entry.setdefault("parent", {}).setdefault(
                "communities", {}
            ).setdefault("default", self.community)
        return batch
