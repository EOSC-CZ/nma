"""Rights of DataCite XML, read before the mapping of ccmm-invenio."""

from lxml import etree

from models.datasets.deserializers import DataCiteXMLDeserializer


def test_rights_identifier_is_kept():
    resource = etree.fromstring(
        """<resource xmlns="http://datacite.org/schema/kernel-4"><rightsList>
        <rights rightsIdentifier="cc-by-4.0" rightsIdentifierScheme="spdx"
                rightsURI="https://creativecommons.org/licenses/by/4.0/legalcode">CC BY 4.0</rights>
        <rights rightsURI="info:eu-repo/semantics/openAccess"/>
        </rightsList></resource>"""
    )

    assert DataCiteXMLDeserializer()._convert_rights_list(resource) == [
        {
            "rights": "CC BY 4.0",
            "rightsUri": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "rightsIdentifier": "cc-by-4.0",
        },
        {"rightsUri": "info:eu-repo/semantics/openAccess"},
    ]


def test_the_access_statement_reaches_the_record(monkeypatch):
    class Resolver:
        metadata = None

        def resolve_metadata(self):
            return {"title": "T"}, []

    monkeypatch.setattr("oarepo_related_resources.resolvers.DataciteResolver", Resolver)
    document = {"rightsList": [{"rightsUri": "info:eu-repo/semantics/restrictedAccess"}]}

    record = DataCiteXMLDeserializer()._deserialize_json(document)

    assert record["access"] == {"record": "public", "files": "restricted"}
    assert record["files"] == {"enabled": False}
