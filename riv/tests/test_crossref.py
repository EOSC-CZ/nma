from ..resolvers import CrossrefResolver


def test_crossref():
    resolver = CrossrefResolver()

    data = resolver.resolve("https://doi.org/10.64000/wadve-3tj60")
    assert data == ({'creators': [{'person_or_org': {'family_name': 'Rittman', 'given_name': 'Martyn',
                                                     'type': 'personal',
                                                     'identifiers': {'identifier': '0000-0001-9327-3734',
                                                                     'scheme': 'orcid'}, 'name': 'Rittman, Martyn'}}, {
                                      'person_or_org': {'family_name': 'Montilla', 'given_name': 'Luis',
                                                        'type': 'personal',
                                                        'identifiers': {'identifier': '0000-0002-7079-6775',
                                                                        'scheme': 'orcid'}, 'name': 'Montilla, Luis'}}],
                     'title': 'Announcing changes to REST API rate limits',
                     'publication_date': '2025-12-03T22:03:59Z',
                     'resource_type': {'id': 'other'}, }, 'OK')

    data = resolver.resolve("10.5281/zenodo.17801829")
    assert data == (None, 'Incorrect URL for crossref identifier.')

    data = resolver.resolve("https://doi.org/10.5281/nonexisting")
    assert data == (None, 'Could not retrieve data, code 404.')

    data = resolver.resolve("doi.org/10.64000/wadve-3tj60")
    assert data == ({'creators': [{'person_or_org': {'family_name': 'Rittman', 'given_name': 'Martyn',
                                                     'type': 'personal',
                                                     'identifiers': {'identifier': '0000-0001-9327-3734',
                                                                     'scheme': 'orcid'}, 'name': 'Rittman, Martyn'}}, {
                                      'person_or_org': {'family_name': 'Montilla', 'given_name': 'Luis',
                                                        'type': 'personal',
                                                        'identifiers': {'identifier': '0000-0002-7079-6775',
                                                                        'scheme': 'orcid'}, 'name': 'Montilla, Luis'}}],
                     'title': 'Announcing changes to REST API rate limits',
                     'publication_date': '2025-12-03T22:03:59Z',
                     'resource_type': {'id': 'other'}, }, 'OK')

    data = resolver.resolve("https://doii.org/10.5281/nonexisting")
    assert data == (None, 'Incorrect URL for crossref identifier.')

    data = resolver.resolve("https://doi.org")
    assert data == (None, 'The URL is missing information about the DOI.')

    data = resolver.resolve("https://doi.org/10.5281/zenodo.17801829")  # datacite (doi correct, but not crossref)
    assert data == (None, 'Could not retrieve data, code 404.')
