from typing import Iterator

import requests
import yaml
from lxml import etree
from lxml.etree import ElementBase
from oarepo_runtime.datastreams.readers import BaseReader, StreamEntry


class COARResourceTypeReader(BaseReader):
    def __init__(
        self,
        *,
        source=None,
        base_path=None,
        coar_url="https://vocabularies.coar-repositories.org/resource_types/{version}/resource_types_for_dspace_{lang}.xml",
        coar_version="3.2",
        coar_languages=["cs", "en"],
        **kwargs,
    ):
        """Constructor.
        :param source: Data source (e.g. filepath, stream, ...)
        """
        super().__init__(source=source, base_path=base_path)
        self._coar_url = coar_url
        self._coar_version = coar_version
        self._coar_languages = coar_languages

    def __iter__(self) -> Iterator[StreamEntry]:
        entries_by_key: dict[str, StreamEntry] = {}

        for lang in self._coar_languages:
            resp = requests.get(
                self._coar_url.format(version=self._coar_version, lang=lang)
            )
            if resp.status_code != 200:
                raise ValueError(
                    f"Unable to fetch COAR resource types from {url.status_code}"
                )
            # parse xml
            root_node = etree.fromstring(resp.content)
            base_url = root_node.attrib["id"]
            self._process_node(
                root_node,
                lang,
                entries_by_key,
                "http://purl.org/coar/resource_type",
                None,
            )
        entries_by_key.pop(base_url, None)
        return iter(entries_by_key.values())

    def _process_node(
        self,
        node: ElementBase,
        lang: str,
        entries_by_key: dict[str, StreamEntry],
        base_url: str,
        parent_id: str | None,
    ):
        node_id = node.attrib["id"]
        key = (
            "/".join([base_url, node_id])
            if not node_id.startswith(base_url)
            else base_url
        )

        if key not in entries_by_key:
            entry = entries_by_key[key] = StreamEntry(
                id=node_id,
                entry={
                    "id": node_id,
                    "props": {"iri": key, "coarVersion": self._coar_version},
                    "title": {},
                },
            )
        else:
            entry = entries_by_key[key]

        entry.entry["title"][lang] = node.attrib["label"]
        if parent_id and not parent_id.startswith(base_url):
            entry.entry.setdefault("hierarchy", {})["parent"] = parent_id

        for is_composed_by in node.findall("isComposedBy"):
            for child_node in is_composed_by.findall("node"):
                self._process_node(child_node, lang, entries_by_key, base_url, node_id)


"""
Sample content of the input xml document:

<node id="http://purl.org/coar/resource_type/scheme" label="Resource Types">
<isComposedBy>
<node id="F8RT-TJK0" label="artistic work">
<hasNote>
A work of visual arts and performing arts, including musical works; dramatic works; pantomimes and choreographic works; motion picture and other audiovisual works; pictorial, graphic, sculptural and architectural works. Adapted from Law Insider: https://www.lawinsider.com/dictionary/artistic-works
</hasNote>
</node>
<node id="c_12cc" label="kartografický dokument">
<hasNote>
Any material representing the whole or part of the earth or any celestial body at any scale. Cartographic materials include two- and three-dimensional maps and plans (including maps of imaginary places); aeronautical, navigational, and celestial charts; atlases; globes; block diagrams; sections; aerial photographs with a cartographic purpose; bird's-eye views (map views), etc. [Source: http://www.loc.gov/marc/cfmap.html]
</hasNote>
<isComposedBy>
<node id="c_12cd" label="mapa">
<hasNote>
Defined as a representation normally to scale and on a flat medium, of a selection of material or abstract features on, or in relation to, the surface of the earth or of another celestial body. [Source: https://www.loc.gov/marc/bibliographic/bd007a.html]
</hasNote>
</node>
</isComposedBy>
</node>

"""


if __name__ == "__main__":
    reader = COARResourceTypeReader()
    data = []
    for entry in reader:
        data.append(entry.entry)
    with open("fixtures/coar-resource-types.yaml", "w") as f:
        f.write(yaml.dump_all(data, sort_keys=True, allow_unicode=True))
