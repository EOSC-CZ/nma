from riv.resolvers.base import PUBLICATION_DATE_PLACEHOLDER, get_validation_failed_on_date_format_message, \
    get_invalid_publication_date_message, parse_date


def test_date_parse():
    normal = "2020-04-07"
    iso = "2009-11-02T09:36:29Z"
    zeros = "0000"
    year = "2020"
    empty = ""

    assert parse_date(normal) == ("2020-04-07", [])
    assert parse_date(iso) == ("2009-11-02", [get_validation_failed_on_date_format_message(iso)])
    assert parse_date(zeros) == (PUBLICATION_DATE_PLACEHOLDER, [get_invalid_publication_date_message(zeros)])
    assert parse_date(year) == ("2020", [])
    assert parse_date(empty) == (PUBLICATION_DATE_PLACEHOLDER, [get_invalid_publication_date_message(empty)])
