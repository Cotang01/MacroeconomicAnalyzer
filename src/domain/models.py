from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class Data(ABC):
    pass


@dataclass(frozen=True)
class CountryData(Data):
    country: str
    year: int
    gdp: int
    gdp_growth: float
    inflation: float
    unemployment: float
    population: int
    continent: str
