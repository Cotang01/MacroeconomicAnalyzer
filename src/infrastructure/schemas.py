from dataclasses import dataclass
from enum import StrEnum

from src.domain.models import CountryData

# Enums are added to lessen the chances of a typo when accessing keys
class CountryDataField(StrEnum):
    COUNTRY = "country"
    YEAR = "year"
    GDP = "gdp"
    GDP_GROWTH = "gdp_growth"
    INFLATION = "inflation"
    UNEMPLOYMENT = "unemployment"
    POPULATION = "population"
    CONTINENT = "continent"


@dataclass(frozen=True)
class CsvCountryDataSchema:
    columns = {
        CountryDataField.COUNTRY: "country",
        CountryDataField.YEAR: "year",
        CountryDataField.GDP: "gdp",
        CountryDataField.GDP_GROWTH: "gdp_growth",
        CountryDataField.INFLATION: "inflation",
        CountryDataField.UNEMPLOYMENT: "unemployment",
        CountryDataField.POPULATION: "population",
        CountryDataField.CONTINENT: "continent"
    }
    
    @classmethod
    def to_domain(cls, row: dict[str, str]) -> CountryData:
        col = cls.columns
        return CountryData(
            country=row[col[CountryDataField.COUNTRY]].strip(),
            year=int(row[col[CountryDataField.YEAR]].strip()),
            gdp=int(row[col[CountryDataField.GDP]].strip()),
            gdp_growth=float(row[col[CountryDataField.GDP_GROWTH]].strip()),
            inflation=float(row[col[CountryDataField.INFLATION]].strip()),
            unemployment=float(row[col[CountryDataField.UNEPLOYMENT]].strip()),
            population=int(row[col[CountryDataField.POPULATION]].strip()),
            continent=row[col[CountryDataField.CONTINENT]].strip()
        )