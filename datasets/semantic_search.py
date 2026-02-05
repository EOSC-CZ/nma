from typing import Any

from invenio_records.dictutils import dict_lookup
from invenio_records.dumpers import SearchDumperExt
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from invenio_records_resources.services.records.params import ParamInterpreter
from marshmallow import fields
from opensearch_dsl.query import Query


class SemanticSearchDumperExtension(SearchDumperExt):
    """Semantic search dumper extension."""

    def __init__(self, *fields):
        """Initialize the dumper.

        :param fields: The fields to include in semantic search.
        """
        self._fields = fields

    def dump(self, record: dict, data: dict) -> None:
        """Dump semantic search fields."""

        fields_texts = []
        for field in self._fields:
            txt = dict_lookup(record, field)
            if txt:
                fields_texts.append(str(txt))

        # TODO: transform the texts into embeddings
        embedding = [0] * 256
        data["embedding"] = embedding

    def load(self, data: dict, record_cls: type) -> None:
        """Load semantic search fields."""
        data.pop("embedding", None)


class KNNQuery(Query):
    """KNN Query for semantic search.

    Note: opensearch natively does not have a KNN query class, so we define a custom one.
    """

    name = "knn"


class SemanticSearchParamsInterpreter(ParamInterpreter):
    """Apply the semantic search parameters."""

    def apply(self, identity, search, params):
        """Apply the parameters."""
        q_str = params.get("sq")
        if not q_str:
            return search

        # TODO: transform the query string into an embedding
        embedding = [0] * 256  # Example placeholder for embedding vector

        search = search.query(
            KNNQuery(
                embedding={
                    "vector": embedding,
                    "k": min(10000, params.get("size", 10) * params.get("page", 1)),
                }
            )
        )
        return search


class SemanticSearchOptionsMixin:
    @property
    def params_interpreters_cls(self) -> Any:
        return [
            *super().params_interpreters_cls,
            SemanticSearchParamsInterpreter,
        ]


class SemanticSearchRequestArgsSchema(SearchRequestArgsSchema):
    sq = fields.String()


class SemanticSearchResourceConfigMixin:
    request_search_args = SemanticSearchRequestArgsSchema
