from dataclasses import dataclass


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
    