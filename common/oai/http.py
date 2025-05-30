import time

import requests

requests_session = requests.Session()

sleep_times: dict[str, float] = {}


def url_get(url, **kwargs):
    """
    Get the content of a URL using requests.

    Handles 429 status code with exponential backoff.
    """
    # get host from the url
    host = url.split("/")[2]
    sleep_time = sleep_times.get(host, 0)
    # Reduce sleep time to a quarter of the last sleep time to ease in after a rate limit
    sleep_time //= 4
    if sleep_time > 0:
        if sleep_time:
            print(f"Sleeping for {sleep_time:.2f} seconds before fetching {host}")
            time.sleep(sleep_time)
            sleep_times[host] = sleep_time
    else:
        sleep_times.pop(host, None)  # Reset sleep time on success

    for retry in range(10):
        params = dict(
            timeout=(10, 20),
            **kwargs,  # Connect timeout, read timeout
        )
        params["headers"] = {
            "User-Agent": "NMA Harvester",
            **(kwargs.get("headers") or {}),
        }
        try:
            response = requests_session.get(url, **params)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(2**retry)  # Exponential backoff
            sleep_times[host] = 2**retry
            continue
        if response.status_code == 429:
            retry_after_header = response.headers.get("Retry-After", None)
            if retry_after_header:
                try:
                    retry_after = int(retry_after_header)
                except ValueError:
                    retry_after = 2**retry
            else:
                retry_after = 2**retry
            print(f"Rate limit exceeded. Retrying in {retry_after:.2f} seconds...")
            time.sleep(retry_after)  # Exponential backoff
            sleep_times[host] = retry_after
        else:
            break
    return response
