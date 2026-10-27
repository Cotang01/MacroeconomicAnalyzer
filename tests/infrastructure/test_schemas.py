import pytest
from dataclasses import fields

from src.domain.models import CountryData
from src.infrastructure.schemas import (
    CountryDataField, CsvCountryDataSchema, InvalidDataError
    )

@pytest.fixture
def valid_raw_data_kwargs() -> dict[str, str]:
    return {
        "country": "USA",
        "year": "2021",
        "gdp": "21000",
        "gdp_growth": "5.7",
        "inflation": "4.7",
        "unemployment": "5.4",
        "population": "331",
        "continent": "North America",
    }


def test_enum_values_are_model_fields():
    assert {f.value for f in CountryDataField} == {f.name for f in fields(CountryData)}
    
    
def test_to_domain_success_on_valid_raw_data(valid_raw_data_kwargs):
    CsvCountryDataSchema().to_domain(valid_raw_data_kwargs)
    
    
@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("year", "year"),
        ("gdp", "bad_gdp"),
        ("gdp_growth", ""),
        ("inflation", None),
        ("unemployment", "abc"),
        ("population", None),
    ]
)
def test_to_domain_error_on_invalid_data(valid_raw_data_kwargs, field, invalid_value):
    valid_raw_data_kwargs[field] = invalid_value
    with pytest.raises(InvalidDataError) as e:
        CsvCountryDataSchema().to_domain(valid_raw_data_kwargs)
    e_values = e.value
    assert e_values.name == field
    assert e_values.value == invalid_value