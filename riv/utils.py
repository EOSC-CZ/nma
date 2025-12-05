#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of nma (see https://github.com/EOSC-CZ/nma).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Utility functions for RIV module."""

from typing import Any

import click
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def create_session_with_retries(
    total_retries: int = 4,
    status_forcelist: list[int] | None = None,
    backoff_factor: float = 0.3,
    **kwargs: Any,
):
    """Create a requests session with retry strategy.

    :param total_retries: Maximum number of retry attempts
    :param status_forcelist: List of HTTP status codes to retry on
    :param backoff_factor: Backoff factor for retries (delay between retries)

    :return: Configured requests session with automatic retries
    """
    if status_forcelist is None:
        status_forcelist = [403, 429, 500, 502]

    retry_strategy = Retry(
        total=total_retries,
        status_forcelist=status_forcelist,
        backoff_factor=backoff_factor,
        **kwargs,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    return session


def extract_text_from_html(html_content: str) -> str:
    """Extract plain text from HTML content.

    :param html_content: HTML content as string

    :return: Extracted plain text
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text and clean it up
        text = soup.get_text()
        # Break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = " ".join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        return f"[Could not extract text: {str(e)}]"


def is_title_in_content(
    title: str, content: str, token_threshold: int = 75, partial_threshold: int = 85
) -> tuple[bool, str, int]:
    """
    Check if title appears in content using hybrid matching approach.

    Uses three methods in order of speed:
    1. Exact substring match python built-in
    2. Token-based fuzzy matching
        - split string by words, sort words, and compare with Levenshtein
        - handles word reordering and extra/missing words
    3. Partial substring fuzzy matching (handles typos)
        - takes title and compares using Levenshtein

    :param title: The title to search for
    :param content: The content to search in
    :param token_threshold: Minimum score for token matching (0-100).
    Typically lower than partial_threshold. Score could be diluted by extra words.
    :param partial_threshold: Minimum score for partial matching (0-100)

    :return: tuple: (found, method, score) where:
            - found: True if title was found
            - method: 'exact', 'token', 'partial', or 'none'
            - score: Matching score (0-100)
    """
    if not title or not content:
        return False, "none", 0

    title_clean = title.lower().strip()
    content_clean = content.lower()

    # Method 1: Fast exact match (covers ~60% of cases)
    if title_clean in content_clean:
        return True, "exact", 100

    # Method 2: Token-based matching (handles word reordering and extra words)
    token_score = fuzz.token_sort_ratio(title_clean, content_clean)
    if token_score >= token_threshold:
        return True, "token", token_score

    # Method 3: Partial matching (handles typos in substring)
    partial_score = fuzz.partial_ratio(title_clean, content_clean)
    if partial_score >= partial_threshold:
        return True, "partial", partial_score

    # Not found - return best score for logging
    best_score = max(token_score, partial_score)
    return False, "none", best_score


def check_url_availability(
    url: str, timeout: int = 15, title: str = ""
) -> tuple[int | None, str, str]:
    """Check if a URL is available and return its status.

    :param url: The URL to check
    :param timeout: Request timeout in seconds
    :param title: Optional title to verify in content (for tombstone detection)

    :return: tuple: (status_code, status_string, message) where:
            - status_code: HTTP status code or None if request failed
            - status_string is one of: 'success', 'warning', 'not_accessible', 'not_found' or 'error'
            - message is a human-readable description of the result
    """
    session = create_session_with_retries()
    status = "error"
    status_code = None
    message = ""

    # Clean title for matching (extract text if it contains HTML entities)
    title_clean = (
        extract_text_from_html(f"<html><body>{title}</body></html>") if title else ""
    )

    try:
        resp = session.get(url, allow_redirects=True, timeout=timeout)
        status_code = resp.status_code

        if status_code == 200:
            # Check if response is HTML
            content_type = resp.headers.get("Content-Type", "").lower()

            # Some tombstone pages may return 200. Provide an additional check to see if title is present.
            if "text/html" in content_type:
                # Extract text from HTML
                text_content = extract_text_from_html(resp.text)

                # Check if title appears in content (tombstone detection)
                if title_clean:
                    found, method, score = is_title_in_content(
                        title_clean, text_content
                    )

                    if found:
                        status = "success"
                        message = f"URL is accessible. Title found in content ({method} match, score: {score})"
                    else:
                        # Title NOT found - potential tombstone!
                        status = "warning"
                        message = f"URL accessible but title not found in content. Possible tombstone/deleted record (best score: {score}). Manual verification recommended"
                else:
                    # No title provided to check
                    status = "success"
                    message = "URL is accessible (no tombstone verification)"
            else:
                # Non-HTML content (PDF, JSON, etc.)
                status = "success"
                message = f"URL is accessible ({content_type})"
        elif status_code == 403:
            status = "not_accessible"
            message = "Access forbidden (HTTP 403)"
        elif status_code == 404:
            status = "not_found"
            message = "Resource not found (HTTP 404)"
        elif status_code == 410:
            status = "not_accessible"
            message = "Resource gone (HTTP 410)"
    except requests.exceptions.Timeout as e:
        status = "error"
        message = f"Request timeout after {timeout}s: {str(e)}"
        click.secho(f"Timeout checking {url}: {e}", fg="red")
    except requests.exceptions.ConnectionError as e:
        status = "error"
        message = f"Connection error: {str(e)}"
        click.secho(f"Connection error checking {url}: {e}", fg="red")
    except requests.exceptions.RequestException as e:
        status = "error"
        message = f"Request error: {str(e)}"
        click.secho(f"Error checking {url}: {e}", fg="red")
    except Exception as e:
        status = "error"
        message = f"Unexpected error: {str(e)}"
        click.secho(f"Unexpected error checking {url}: {e}", fg="red")

    return status_code, status, message
