import pytest

from src.domain.models import CountryData, DomainError

@pytest.fixture
def valid_country_data_kwargs() -> dict[str, str | int | float]:
    return {
        "country": "USA",
        "year": 2021,
        "gdp": 21000,
        "gdp_growth": 5.7,
        "inflation": 4.7,
        "unemployment": 5.4,
        "population": 331,
        "continent": "North America",
    }


def test_country_data_rejects_negative_gdp(valid_country_data_kwargs):
    valid_country_data_kwargs["gdp"] = -1
    with pytest.raises(DomainError):
        CountryData(**valid_country_data_kwargs)
        

def test_country_data_rejects_negative_population(valid_country_data_kwargs):
    valid_country_data_kwargs["population"] = -1
    with pytest.raises(DomainError):
        CountryData(**valid_country_data_kwargs)


def test_country_data_rejects_empty_country(valid_country_data_kwargs):
    valid_country_data_kwargs["country"] = ""
    with pytest.raises(DomainError):
        CountryData(**valid_country_data_kwargs)


def test_country_data_rejects_empty_continent(valid_country_data_kwargs):
    valid_country_data_kwargs["continent"] = ""
    with pytest.raises(DomainError):
        CountryData(**valid_country_data_kwargs)
