import metsrw
import requests
from lxml import etree
from metsrw import metadata, utils

LINDAT_LANGUAGE = "en"
LINDAT_LANGUAGE_IRI = "https://publications.europa.eu/resource/authority/language/ENG"

requests_session = requests.Session()


class LindatMETSDocument(metsrw.METSDocument):

    def _parse_tree(self, tree=None):
        if tree is None:
            tree = self.tree
        # self._validate()

        self._parse_header(tree)

        # Read root attributes
        root = tree
        if isinstance(tree, etree._ElementTree):
            root = tree.getroot()
        self.objid = root.get("OBJID", None)

        # Parse structMap - dspace has its own structMap
        structMap = tree.find("mets:structMap", namespaces=utils.NAMESPACES)

        # change dspace object contents to directory to let archivematica code parse it
        # correctly
        dspace_object = structMap.find(
            "mets:div[@TYPE='DSpace Object Contents']", utils.NAMESPACES
        )
        if dspace_object is not None:
            dspace_object.attrib["TYPE"] = "Directory"

        self._root_elements = self._parse_tree_structmap(
            tree, structMap, normative_parent_elem=None
        )

        self._custom_structmaps = []

        # Associated derived files
        for entry in self.all_files():
            entry.derived_from = self.get_file(
                file_uuid=entry.derived_from, type="Item"
            )

    @staticmethod
    def _add_amdsecs_to_fs_entry(amdids, fs_entry, tree):
        if amdids:
            amdids = amdids.split()
            for amdid in amdids:
                amdsec_elem = tree.find(
                    'mets:amdSec[@ID="' + amdid + '"]', namespaces=utils.NAMESPACES
                )
                if amdsec_elem is None:  # removed parts here
                    # Workaround for https://github.com/archivematica/Issues/issues/1129.
                    # The objects directory might reference a non-existent amdSec.
                    # Ignore it to avoid parsing errors.
                    continue
                amdsec = metadata.AMDSec.parse(amdsec_elem)
                fs_entry.amdsecs.append(amdsec)

    @classmethod
    def fromtree(cls, tree):
        """Parse the METS document from an XML tree."""

        # lindat has incorrect CREATEDATE, removing it so that it is not checked
        mets_hdr = tree.find("./mets:metsHdr", utils.NAMESPACES)
        del mets_hdr.attrib["CREATEDATE"]

        return super().fromtree(tree)
