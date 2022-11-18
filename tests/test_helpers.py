import pytest

from pinrex.db_models import helpers


@pytest.fixture
def names():
    """Define what names should look like after cleaning"""
    names = {
        "colon:remove": "colonremove",
        "Upper_Case": "upper_case",
        "{bracket}": "bracket",
        "space exists": "spaceexists",
        "(parenthesis)": "parenthesis",
        "[brackets]": "brackets",
        "comma,": "comma",
        "dash-": "dash",
        "'single quote": "singlequote",
        '"doublequote"': "doublequote",
        "Ma{n}y_di[]fferent -'iss:\"(u)e-s": "many_differentissues",
    }
    return names


def test_make_name_searchable(names):
    for k, v in names.items():
        assert helpers.make_name_searchable(k) == v
