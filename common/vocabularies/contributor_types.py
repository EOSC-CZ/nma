import logging
from typing import Iterator

import requests
from lxml import etree
from oarepo_runtime.datastreams.readers import BaseReader, StreamEntry

log = logging.getLogger("datastreams.vocabularies.languages")

nsmap = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "europa": "http://publications.europa.eu/ontology/authority/",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xs": "http://www.w3.org/2001/XMLSchema",
}


class ContributorTypeReader(BaseReader):
    def __init__(
        self,
        *,
        source=None,
        base_path=None,
        base_url="https://schema.datacite.org/meta/kernel-4.6/include/datacite-contributorType-v4.xsd",
        languages=["cs", "en"],
        **kwargs,
    ):
        """Constructor.
        :param source: Data source (e.g. filepath, stream, ...)
        """
        super().__init__(source=source, base_path=base_path)
        self._base_url = base_url
        self._languages = languages

    def __iter__(self) -> Iterator[StreamEntry]:
        resp = requests.get(self._base_url)
        if resp.status_code != 200:
            raise ValueError(
                f"Unable to fetch languages {self._base_url}: {resp.status_code}"
            )
        root_node = etree.fromstring(resp.content)
        language_descriptions = root_node.findall(
            ".//xs:enumeration",
            namespaces=nsmap,
        )
        for desc in language_descriptions:
            value = desc.attrib.get("value")
            yield StreamEntry(
                id=value,
                entry={
                    "id": value,
                    "props": {
                        "definitionURL": f"https://schema.datacite.org/meta/kernel-4.6/include/datacite-contributorType-v4.xsd#{value}"
                    },
                    "title": {"en": value, "cs": value},
                },
            )


if __name__ == "__main__":
    reader = ContributorTypeReader()
    for entry in reader:
        print(entry)
