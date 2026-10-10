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


@dataclass(frozen=True)
class ReportData:
    group_by_field: str
    report_field: str
    data: list[tuple[str, float]]
    