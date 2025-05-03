import time

import requests

requests_session = requests.Session()


def url_get(url, **kwargs):
    """
    Get the content of a URL using requests.

    Handles 429 status code with exponential backoff.
    """
    for retry in range(10):
        params = dict(
            timeout=(2, 5),
            **kwargs,  # Connect timeout, read timeout
        )
        params["headers"] = {
            "User-Agent": "NMA Lindat Harvester",
            **(kwargs.get("headers") or {}),
        }
        response = requests_session.get(url, **params)
        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying in {2**retry:.2f} seconds...")
            time.sleep(2**retry)  # Exponential backoff
        else:
            break
    return response
