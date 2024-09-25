from oarepo_runtime.datastreams import StreamEntry
from common.oai.loaders.zenodo import ZenodoLoader
import requests_mock

def test_charles_uni():
    # basic test
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={'setspecs':'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from=None,
                          oai_harvester_id=1,
                          manual=False,)
    entry:StreamEntry = next(iter(loader))
    assert entry.context['oai']['identifier'] ==f'oai:zenodo.org:18590'

def test_start_from():
    # test with start from date
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )
    entry: StreamEntry = next(iter(loader))
    # (creators.affiliation:("Univerzita Karlova" OR "Charles University")) AND updated:[2024-08-04 TO *]
    assert entry.context['oai']['identifier'] == f'oai:zenodo.org:17065'

def test_invalid_start_from():
    # test with incorrect start from date
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-15-15',
                          oai_harvester_id=1,
                          manual=False, )
    entry = next(iter(loader))
    assert entry is None


def test_search_zenodo_success(requests_mock):
    # Simulate a successful API response
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    requests_mock.get(loader.source, json={"hits": {"hits": []}}, status_code=200)
    result = loader.search_zenodo(params={'q': 'test'})
    assert result == {"hits": {"hits": []}}


def test_search_zenodo_http_error(requests_mock):
    # Simulate an HTTP error (e.g., 404 Not Found)
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    requests_mock.get(loader.source, status_code=404)
    result = loader.search_zenodo(params={'q': 'test'})
    assert result is None


def test_search_zenodo_server_error(requests_mock):
    # Simulate a server error (e.g., 500 Internal Server Error)
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    requests_mock.get(loader.source, status_code=500)
    result = loader.search_zenodo(params={'q': 'test'})
    assert result is None


def test_iter_http_404_error(requests_mock):
    # Simulate an HTTP 404 error from Zenodo API
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    # Mock to return a 404 error
    requests_mock.get(loader.source, status_code=404)

    result = next(iter(loader))
    assert result is None


def test_iter_http_500_error(requests_mock):
    # Simulate an HTTP 500 error from Zenodo API
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    # Mock to return a 500 error
    requests_mock.get(loader.source, status_code=500)

    result = next(iter(loader))
    assert result is None


def test_iter_success_after_error(requests_mock):
    loader = ZenodoLoader(source="https://zenodo.org/api/records/", all_records=True,
                          identifiers=[],
                          oai_config={
                              'setspecs': 'creators.affiliation:("Univerzita Karlova" OR "Charles University")'},
                          oai_run=1,
                          start_from='2024-08-04',
                          oai_harvester_id=1,
                          manual=False, )

    # First error mock
    requests_mock.get(loader.source, status_code=500)
    result = next(iter(loader))
    assert result is None

    # Second request is success
    requests_mock.get(loader.source, json={
        'hits': {'hits': [{'id': '12345', 'metadata': {'title': 'Sample Record'}, 'updated': '2024-08-04'}]}
    }, status_code=200)

    result = next(iter(loader))
    assert result.context['oai']['identifier'] == 'oai:zenodo.org:12345'
