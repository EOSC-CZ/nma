# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o
# SPDX-License-Identifier: MIT

"""Temporary fixes of the CCMM XML served by https://herbarium.biodiversity.cz/oai-pmh.

The herbarium sends vocabulary values the CCMM import can not resolve. This transformer
rewrites them in the harvested XML, so it must run before ``oai-import``:

* ``date_type`` - Skosmos page URLs ``https://vocabs.ccmm.cz/TimeReference/en/page/<X>``
  instead of ``https://vocabs.ccmm.cz/registry/codelist/TimeReference/<X>``
* creator ``role`` - ``.../AgentRole/Contributor/Creator`` instead of ``.../AgentRole/Creator``
* ``format`` - EU vocabularies viewer URLs wrapping the file-type IRI
* ``media_type`` - the EU file-type IRI instead of an IANA media type
* ``description`` - with an empty ``description_text`` (removed)

Remove the transformer from the harvester once the herbarium fixes its data.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from invenio_vocabularies.datastreams.transformers import BaseTransformer
from lxml import etree

if TYPE_CHECKING:
    from invenio_vocabularies.datastreams.datastreams import StreamEntry

OAI_METADATA = "{http://www.openarchives.org/OAI/2.0/}metadata"

EU_VIEWER_PREFIX = "https://op.europa.eu/en/web/eu-vocabularies/concept/-/resource?uri="
EU_FILE_TYPE = "http://publications.europa.eu/resource/authority/file-type/"
IANA_MEDIA_TYPE = "http://www.iana.org/assignments/media-types/"

# EU file type -> IANA media type, for the file types the herbarium uses
FILE_TYPE_MEDIA_TYPES = {
    "TIFF": "image/tiff",
    "JPEG2000": "image/jp2",
    "PNG": "image/png",
    "JPEG": "image/jpeg",
}

# wrong IRI prefix -> correct IRI prefix
IRI_PREFIXES = {
    "https://vocabs.ccmm.cz/TimeReference/en/page/": "https://vocabs.ccmm.cz/registry/codelist/TimeReference/",
    "https://vocabs.ccmm.cz/registry/codelist/AgentRole/Contributor/Creator": (
        "https://vocabs.ccmm.cz/registry/codelist/AgentRole/Creator"
    ),
    EU_VIEWER_PREFIX: "",
}


class HerbariumFixTransformer(BaseTransformer):
    """Fixes the vocabulary values of herbarium.biodiversity.cz records in the OAI XML."""

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        """Ignore the transformer options, there are none."""

    @override
    def apply(self, stream_entry: StreamEntry, *_args: Any, **_kwargs: Any) -> StreamEntry:
        """Fix the dataset element of the OAI record in place."""
        oai_record = stream_entry.entry["record"]
        if oai_record.header.deleted:
            return stream_entry
        metadata = oai_record.xml.find(OAI_METADATA)
        if metadata is None:
            return stream_entry
        for dataset in metadata:
            if isinstance(dataset.tag, str):
                self.fix_dataset(dataset)
        return stream_entry

    def fix_dataset(self, dataset: etree._Element) -> None:
        """Fix the vocabulary IRIs and empty descriptions of a CCMM dataset element."""
        ns = etree.QName(dataset).namespace

        def q(name: str) -> str:
            return f"{{{ns}}}{name}"

        for iri in dataset.iter(q("iri")):
            text = (iri.text or "").strip()
            for wrong, correct in IRI_PREFIXES.items():
                if text.startswith(wrong):
                    text = correct + text[len(wrong) :]
            iri.text = text

        for iri in dataset.iterfind(f".//{q('media_type')}/{q('iri')}"):
            if iri.text.startswith(EU_FILE_TYPE):
                media_type = FILE_TYPE_MEDIA_TYPES.get(iri.text[len(EU_FILE_TYPE) :])
                if media_type:
                    iri.text = IANA_MEDIA_TYPE + media_type

        for description in dataset.findall(q("description")):
            if not "".join(t.text or "" for t in description.iter(q("description_text"))).strip():
                dataset.remove(description)
