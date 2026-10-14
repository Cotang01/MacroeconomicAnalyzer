from dataclasses import dataclass


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
        if self.year <= 0:
            raise ValueError(f"Year can't be a negative number: {self.year}")
        elif self.gdp < 0:
            raise ValueError(f"GDP can't be a negative number: {self.gdp}")
        elif self.population < 0:
            raise ValueError(
                f"Population can't be a negative number: {self.population}"
                )
        

@dataclass(frozen=True)
class ReportData:
    group_by_field: str
    report_field: str
    data: list[tuple[str, int | float]]
    