from dataclasses import dataclass
from enum import StrEnum


class DomainError(Exception): 
    pass


@dataclass(frozen=True)
class CountryData:
    country: str
    year: int
    gdp: int
    gdp_growth: float
    inflation: float
    unemployment: float
    population: int
    continent: str
    
    def __post_init__(self):
        if not self.country:
            raise DomainError("Country cannot be empty")
        elif not self.continent:
            raise DomainError("Continent cannot be empty")
        elif self.gdp < 0:
            raise DomainError(f"GDP can't be a negative number: {self.gdp}")
        elif self.population < 0:
            raise DomainError(
                f"Population can't be a negative number: {self.population}"
                )
        

@dataclass(frozen=True)
class ReportData:
    group_by_field: str
    report_field: str
    data: list[tuple[str, int | float]]


# Enums are added to lessen the chances of a typo when using field names
class CountryDataField(StrEnum):
    COUNTRY = "country"
    YEAR = "year"
    GDP = "gdp"
    GDP_GROWTH = "gdp_growth"
    INFLATION = "inflation"
    UNEMPLOYMENT = "unemployment"
    POPULATION = "population"
    CONTINENT = "continent"
