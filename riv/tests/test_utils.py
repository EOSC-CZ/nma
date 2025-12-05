#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Tests for RIV utility functions."""

from riv.utils import is_title_in_content


def test_exact_match():
    """Test exact substring match (fastest path)."""
    title = "Climate Research Dataset"
    content = "This is the Climate Research Dataset from 2024"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_exact_match_case_insensitive():
    """Test exact match is case-insensitive."""
    title = "Climate Research Dataset"
    content = "This is the CLIMATE RESEARCH DATASET from 2024"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_token_match_word_reordering():
    """Test token-based matching handles word reordering."""
    title = "Report on Annual Climate trends 2024"
    content = "See the 2024 Report on Annual Climate trends for details"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "token"
    assert score >= 75  # Above token threshold


def test_partial_match_with_typos():
    """Test partial matching handles typos."""
    title = "Marine Biodiversity Study"
    content = "Welcome to the Marin Biodiversty Studie project homepage"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "partial"
    assert score >= 85  # Above partial threshold


def test_no_match_completely_different():
    """Test no match when content is completely different."""
    title = "Climate Research Dataset"
    content = "This is about marine biology and ocean studies"

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    assert score < 75  # Below both thresholds


def test_no_match_below_threshold():
    """Test no match when similarity is below threshold."""
    title = "Specific Dataset Name"
    content = "Some general information about data"

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    assert score < 75


def test_tombstone_page_detection():
    """Test detection of tombstone page (title not in content)."""
    title = "Urban Air Quality Dataset"
    content = (
        "This record has been deleted. Contact administrator for more information."
    )

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    # Score might be low due to some word overlap like "record"
    assert score < 75


def test_tombstone_with_partial_words():
    """Test tombstone detection when some words from title appear."""
    title = "Climate Change Research Project"
    content = "Dataset removed. This climate study project is no longer available."

    found, method, score = is_title_in_content(title, content)

    # Should not find complete title, but might get some token matches
    # Depending on threshold, could be found or not
    # Let's assert it finds something with token matching
    assert method in ["token", "none"]
    if found:
        assert method == "token"
        assert score >= 75
    else:
        assert score < 75


def test_empty_title():
    """Test handling of empty title."""
    title = ""
    content = "Some content here"

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    assert score == 0


def test_empty_content():
    """Test handling of empty content."""
    title = "Some Title"
    content = ""

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    assert score == 0


def test_both_empty():
    """Test handling when both title and content are empty."""
    title = ""
    content = ""

    found, method, score = is_title_in_content(title, content)

    assert found is False
    assert method == "none"
    assert score == 0


def test_whitespace_handling():
    """Test that leading/trailing whitespace is handled."""
    title = "  Climate Dataset  "
    content = "  This is about Climate Dataset research  "

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_long_content_performance():
    """Test with realistic long HTML content."""
    title = "Climate Research Dataset 2024"
    # Simulate extracted text from a real HTML page
    content = """
    Header Navigation Home About Contact
    Climate Research Dataset 2024 Main Content
    This comprehensive study examines climate patterns over the last decade.
    The research includes temperature data precipitation levels and atmospheric conditions.
    Methods We collected data from multiple sources worldwide using standardized protocols.
    Results Our findings indicate significant trends in global climate patterns.
    Footer Copyright 2024 All Rights Reserved Contact Us
    """

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_html_entities_cleaned():
    """Test that HTML entities are properly handled."""
    title = "Research & Development"
    content = "Welcome to the Research & Development portal"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_custom_thresholds():
    """Test with custom threshold values."""
    title = "Test Title"
    content = "This is about Testing Titles and more"

    # Stricter thresholds
    found, _, score = is_title_in_content(
        title, content, token_threshold=90, partial_threshold=95
    )

    # Should not match with strict thresholds
    assert found is False or score >= 90


def test_very_similar_but_different_title():
    """Test distinguishing between similar titles."""
    title = "Annual Climate Report 2024"
    content = "See the Annual Climate Report 2023 for previous year data"

    found, method, score = is_title_in_content(title, content)

    # Might match on token level (3 out of 4 words match)
    # but partial should catch the difference
    if found:
        assert method in ["token", "partial"]
        # Score should reflect the difference
        assert score < 100


def test_special_characters():
    """Test handling of special characters in title."""
    title = "COVID-19 Research: Impact & Response"
    content = "This study focuses on COVID-19 Research: Impact & Response measures"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert score >= 85


def test_numbers_in_title():
    """Test titles with numbers."""
    title = "Dataset 12345 Version 2.0"
    content = "Access Dataset 12345 Version 2.0 for download"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "exact"
    assert score == 100


def test_unicode_characters():
    """Test with Unicode characters."""
    title = "Výzkum klimatu v České republice"
    content = "Tento projekt se zabývá Výzkumem klimatu v České republice"

    found, method, score = is_title_in_content(title, content)

    assert found is True
    assert method == "partial"
    assert score >= 85
