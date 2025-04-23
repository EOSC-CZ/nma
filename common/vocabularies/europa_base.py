import logging
import time
from typing import Iterator

import requests
from lxml import etree
from oarepo_runtime.datastreams.readers import BaseReader, StreamEntry

log = logging.getLogger("datastreams.vocabularies.europa")

nsmap = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "europa": "http://publications.europa.eu/ontology/authority/",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "owl": "http://www.w3.org/2002/07/owl#",
}


class EuropaBaseTypeReader(BaseReader):
    def __init__(
        self,
        *,
        source=None,
        base_path=None,
        base_url=None,
        languages=["cs", "en"],
        **kwargs,
    ):
        """Constructor.
        :param source: Data source (e.g. filepath, stream, ...)
        """
        super().__init__(source=source, base_path=base_path)
        assert base_url, "Base URL is required"
        self._base_url = base_url
        self._languages = languages

    def __iter__(self) -> Iterator[StreamEntry]:
        resp = requests.get(self._base_url)
        if resp.status_code != 200:
            raise ValueError(
                f"Unable to fetch entities {self._base_url}: {resp.status_code}"
            )
        root_node = etree.fromstring(resp.content)
        entity_descriptions = root_node.findall(
            "./rdf:Description",
            namespaces=nsmap,
        )
        entity_urls = []
        for desc in entity_descriptions:
            skos_inscheme = desc.findall(
                f'./skos:inScheme[@rdf:resource="{self._base_url}"]',
                namespaces=nsmap,
            )
            if not skos_inscheme:
                continue
            about = desc.attrib.get(
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
            )

            entity_urls.append(about)

        unprocessed_entities = set(entity_urls)
        for url in entity_urls:
            loaded, url = self.load_entity(url)
            if True:
                # with Pool(30) as pool:
                #     for loaded, url in tqdm.tqdm(
                #         pool.imap(self.load_entity, entity_urls), total=len(entity_urls)
                #     ):
                print("Got", url, flush=True)
                if url in unprocessed_entities:
                    unprocessed_entities.remove(url)
                log.warning("Unprocessed entities left: %s", len(unprocessed_entities))
                if len(unprocessed_entities) < 50:
                    log.warning("Unprocessed entities left: %s", unprocessed_entities)
                if not loaded.filtered:
                    yield loaded

    def load_entity(self, about: str) -> tuple[StreamEntry, str]:
        log.warning("Loading entity from url %s", about)
        t1 = time.time()
        resp = requests.get(about, timeout=10)
        if resp.status_code != 200:
            log.error("Unable to fetch entity %s: %s", about, resp.status_code)
            return (
                StreamEntry(
                    id=None,
                    filtered=True,
                    entry={
                        "id": None,
                        "props": {"definitionURL": about},
                        "title": {},
                    },
                ),
                about,
            )
        log.warning("Loaded entity from url %s, took %s", about, time.time() - t1)
        root_node = etree.fromstring(resp.content)
        description = root_node.find(
            "./rdf:Description[@rdf:about='{}']".format(about),
            namespaces=nsmap,
        )
        code = description.find("./europa:authority-code", namespaces=nsmap).text

        title = {}
        for label in description.findall("./skos:prefLabel", namespaces=nsmap):
            lang = label.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            if lang in self._languages:
                title[lang] = label.text

        if not title:
            log.warning("entity %s has no title in selected entities", code)
            return (
                StreamEntry(
                    id=code,
                    filtered=True,
                    entry={
                        "id": code,
                        "props": {"definitionURL": about},
                        "title": {},
                    },
                ),
                about,
            )

        notations = {}
        for notation in description.findall("./skos:notation", namespaces=nsmap):
            rdf_datatype = notation.attrib.get(
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}datatype"
            )
            if rdf_datatype:
                rdf_datatype = rdf_datatype.split("#")[-1]
                notations[rdf_datatype] = notation.text

        definitions = {}
        for definition in description.findall("./skos:definition", namespaces=nsmap):
            lang = definition.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            if lang in self._languages:
                definitions[lang] = definition.text

        version_info = description.find("./owl:versionInfo", namespaces=nsmap)
        if version_info is not None:
            notations["version"] = version_info.text

        return (
            StreamEntry(
                id=code,
                entry={
                    "id": code,
                    "props": {**notations, "definitionURL": about},
                    "title": title,
                    "description": definitions,
                },
            ),
            about,
        )


if __name__ == "__main__":
    reader = EuropaentitiesTypeReader()
    for entry in reader:
        pass
