# SPDX-FileCopyrightText: 2026 CESNET z.s.p.o.
# SPDX-License-Identifier: MIT

"""Unit tests for the `normalize_identifier_into_resolution_url` function.
This function is responsible for normalizing the DOI identifiers of different form.
"""

import pytest

from riv.resolvers.utils import normalize_identifier_into_resolution_url


@pytest.mark.parametrize(
    "input_id, expected",
    [
        ("10.5281/zenodo.20434110", "https://doi.org/10.5281/zenodo.20434110"),
        ("10.1000/182", "https://doi.org/10.1000/182"),
        ("doi:10.5281/zenodo.20434110", "https://doi.org/10.5281/zenodo.20434110"),
        ("DOI:10.5281/zenodo.20434110", "https://doi.org/10.5281/zenodo.20434110"),
        ("  10.1234/test.123  ", "https://doi.org/10.1234/test.123"),
    ],
)
def test_valid_doi_normalization(input_id, expected):
    """Test that raw and prefixed DOIs are correctly normalized to full URLs."""
    assert normalize_identifier_into_resolution_url(input_id) == expected


@pytest.mark.parametrize(
    "input_id, expected",
    [
        (
            "https://doi.org/10.5281/zenodo.20434110",
            "https://doi.org/10.5281/zenodo.20434110",
        ),
        ("http://doi.org/10.1000/182", "https://doi.org/10.1000/182"),
        ("https://hdl.handle.net/11012/255869", "https://hdl.handle.net/11012/255869"),
        (
            "http://hdl.handle.net/20.500.12281/123",
            "http://hdl.handle.net/20.500.12281/123",
        ),
    ],
)
def test_full_urls_passed_through(input_id, expected):
    """Test that already valid full URLs (both DOI and Handle) are passed through unaltered."""
    assert normalize_identifier_into_resolution_url(input_id) == expected


@pytest.mark.parametrize(
    "input_id, expected",
    [
        ("11012/255869", "11012/255869"),
        ("hdl:11012/255869", "hdl:11012/255869"),
        ("climate change dataset", "climate change dataset"),
        ("10.5281", "10.5281"),
        ("doi:", "doi:"),
        ("", ""),
        (None, ""),
    ],
)
def test_unsupported_or_invalid_inputs(input_id, expected):
    """Test that inputs we don't normalize (like raw handles or normal search strings)
    pass through unaltered.
    """
    assert normalize_identifier_into_resolution_url(input_id) == expected
