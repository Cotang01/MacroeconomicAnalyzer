from dataclasses import dataclass


@dataclass(frozen=True)
class CountryDataSchema:
    country: str = "country"
    year: str = "year"
    gdp: str = "gdp"
    gdp_growth: str = "gdp_growth"
    inflation: str = "inflation"
    unemployment: str = "unemployment"
    population: str = "population"
    continent: str = "continent"

