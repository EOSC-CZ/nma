"""Mapping of LINDAT/CLARIN license URIs and names to licenses vocabulary ids.

The licenses vocabulary uses lowercased SPDX ids (e.g. ``cc-by-sa-4.0``,
``gpl-3.0-only``). LINDAT's own licenses (published under
``https://lindat.mff.cuni.cz/repository/static/``) are mapped to ``lindat-<slug>``
ids, see ``app_data/vocabularies/licenses.yaml``.
"""

from __future__ import annotations

import re

# opensource.org license names that differ from the SPDX id
OPENSOURCE_ALIASES = {
    "mit-license": ["mit"],
    "artistic-perl-1.0": ["artistic-1.0-perl"],
    # LINDAT labels this uri as "GNU General Public License 2 or later (GPL-2.0)"
    "gpl-2.0": ["gpl-2.0-or-later", "gpl-2.0-only"],
}

# license names used in LINDAT records (OLAC dc:rights and dc.rights), lowercased
LICENSE_NAMES = {
    "apache license 2.0": "apache-2.0",
    "artistic license 2.0": "artistic-2.0",
    "artistic license (perl) 1.0": "artistic-1.0-perl",
    'bsd 2-clause "simplified" or "freebsd" license': "bsd-2-clause",
    'bsd 3-clause "new" or "revised" license': "bsd-3-clause",
    "gnu general public license, version 2": "gpl-2.0-only",
    "gnu general public licence, version 3": "gpl-3.0-only",
    "gnu general public license 2 or later (gpl-2.0)": "gpl-2.0-or-later",
    'gnu library or "lesser" general public license 3.0 (lgpl-3.0)': "lgpl-3.0-only",
    "affero general public license 3 (agpl-3.0)": "agpl-3.0-only",
    "the mit license (mit)": "mit",
    "open data commons open database license (odbl)": "odbl-1.0",
    "public domain dedication (cc zero)": "cc0-1.0",
    "public domain mark (pd)": "cc-pdm-1.0",
    # LINDAT's own licenses referenced by name only
    "czech national corpus (shuffled corpus data)": "lindat-cnc",
    "pdt 2.0 license": "lindat-pdt2",
    "hamledt 2.0 licence agreement": "lindat-hamledt-2.0",
    "pdtsl": "lindat-pdtsl",
    "cc-by-nc-sa + ldc99t42": "lindat-pcedt2",
}

CC_URL = re.compile(r"creativecommons\.org/licenses/([a-z-]+)/(\d\.\d)", re.IGNORECASE)
CC_PUBLIC_DOMAIN_URL = re.compile(r"creativecommons\.org/publicdomain/(zero|mark)/(\d\.\d)", re.IGNORECASE)
# e.g. "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)", "Creative Commons BY-NC-SA 3.0 NL license"
CC_NAME = re.compile(r"\b(?:CC|Creative Commons)[ -](BY(?:-N[CD])*(?:-SA|-ND)?)[ -](\d\.\d)\b", re.IGNORECASE)
OPENSOURCE_URL = re.compile(r"opensource\.org/licenses?/([\w.-]+?)(?:\.php|\.html)?/?$", re.IGNORECASE)
GNU_URL = re.compile(r"gnu\.org/licenses/((?:a|l)?gpl)-?(\d\.\d)", re.IGNORECASE)
ODBL_URL = re.compile(r"opendatacommons\.org/licenses/odbl", re.IGNORECASE)
LINDAT_URL = re.compile(r"lindat\.mff\.cuni\.cz/repository/static/([^/?#]+?)\.html?$", re.IGNORECASE)
WORDNET_URL = re.compile(r"wordnet\.princeton\.edu/license", re.IGNORECASE)


def lindat_license_id(filename: str) -> str:
    """Return vocabulary id for a LINDAT static license page name.

    "licence-UD-2.5" -> "lindat-ud-2.5", "Qwant_LongEval_BY-NC-SA_License" ->
    "lindat-qwant-longeval-by-nc-sa", "LINDAT-Web-Crawl-Licence" -> "lindat-web-crawl"
    """
    slug = filename.lower().replace("_", "-")
    slug = re.sub(r"^licen[cs]e-|-licen[cs]e$", "", slug)
    slug = re.sub(r"^lindat-", "", slug)
    return f"lindat-{slug}"


def license_candidates(value: str) -> list[str]:
    """Return vocabulary ids that may correspond to a license URI or name, best first."""
    value = value.strip()
    candidates = []

    if name_id := LICENSE_NAMES.get(value.lower()):
        candidates.append(name_id)

    # country versions of creative commons licenses are mapped to the generic ones
    if match := CC_URL.search(value):
        candidates.append(f"cc-{match.group(1).lower()}-{match.group(2)}")
    if match := CC_PUBLIC_DOMAIN_URL.search(value):
        kind, version = match.group(1).lower(), match.group(2)
        candidates.append(f"cc0-{version}" if kind == "zero" else f"cc-pdm-{version}")
    if not candidates and (match := CC_NAME.search(value)):
        candidates.append(f"cc-{match.group(1).lower()}-{match.group(2)}")

    if match := OPENSOURCE_URL.search(value):
        name = match.group(1).lower()
        candidates += OPENSOURCE_ALIASES.get(name, [name, f"{name}-only"])
    if match := GNU_URL.search(value):
        candidates.append(f"{match.group(1).lower()}-{match.group(2)}-only")
    if ODBL_URL.search(value):
        candidates.append("odbl-1.0")
    if match := LINDAT_URL.search(value):
        candidates.append(lindat_license_id(match.group(1)))
    if WORDNET_URL.search(value):
        candidates.append("wordnet")

    # the last path segment, as used before (e.g. ".../licenses/Apache-2.0")
    if "/" in value:
        candidates.append(value.rstrip("/").split("/")[-1].lower())

    return list(dict.fromkeys(c for c in candidates if c))
