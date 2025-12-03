from ..resolvers import DataciteResolver


def test_doi():
    resolver = DataciteResolver()

    data = resolver.resolve("https://doi.org/10.5281/zenodo.17801829")
    assert data == ({'title': 'Zum FAIRen Umgang mit qualitativen, sensiblen Forschungsdaten beim Forschungsdatenzentrum Qualiservice', 'creators': [{'person_or_org': {'type': 'personal', 'given_name': 'Paula', 'family_name': 'Lein', 'name': 'Lein, Paula'}}, {'person_or_org': {'type': 'personal', 'given_name': 'Viola', 'family_name': 'Logemann', 'name': 'Logemann, Viola'}}]}, 'OK')

    data = resolver.resolve("10.5281/zenodo.17801829")
    assert data == (None, 'Incorrect URL for datacite identifier.')

    data = resolver.resolve("https://doi.org/10.5281/nonexisting")
    assert data == (None, 'Could not retrieve data, code 404.')

    data = resolver.resolve("doi.org/10.5281/zenodo.17801829")
    assert data == ({'title': 'Zum FAIRen Umgang mit qualitativen, sensiblen Forschungsdaten beim Forschungsdatenzentrum Qualiservice', 'creators': [{'person_or_org': {'type': 'personal', 'given_name': 'Paula', 'family_name': 'Lein', 'name': 'Lein, Paula'}}, {'person_or_org': {'type': 'personal', 'given_name': 'Viola', 'family_name': 'Logemann', 'name': 'Logemann, Viola'}}]}, 'OK')

    data = resolver.resolve("https://doii.org/10.5281/nonexisting")
    assert data == (None, 'Incorrect URL for datacite identifier.')

    data = resolver.resolve("https://doi.org")
    assert data == (None, 'The URL is missing information about the DOI.')


    data = resolver.resolve("https://doi.org/10.64000/wadve-3tj60") # crossref (doi correct, but not datacite)
    assert data == (None, 'Could not retrieve data, code 404.')