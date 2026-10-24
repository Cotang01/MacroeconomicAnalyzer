from typing import TypeVar, ClassVar, Callable

from src.domain.models import CountryData, CountryDataField


T = TypeVar("T")


class InvalidDataError(Exception):
    def __init__(self, msg: str, name: str, value: str | None) -> None:
        self.msg = msg
        self.name = name
        self.value = value


class CsvCountryDataSchema:
    columns: ClassVar[dict[CountryDataField, str]] = {
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
        return CountryData(
            country=cls._parse(row, str, CountryDataField.COUNTRY),
            year=cls._parse(row, int, CountryDataField.YEAR),
            gdp=cls._parse(row, int, CountryDataField.GDP),
            gdp_growth=cls._parse(row, float, CountryDataField.GDP_GROWTH),
            inflation=cls._parse(row, float, CountryDataField.INFLATION),
            unemployment=cls._parse(row, float, CountryDataField.UNEMPLOYMENT),
            population=cls._parse(row, int, CountryDataField.POPULATION),
            continent=cls._parse(row, str, CountryDataField.CONTINENT)
        )

    @classmethod
    def _parse(cls, 
               row: dict[str, str], 
               cast_func: Callable[[str], T], 
               field: CountryDataField) -> T:
        csv_col_name = cls.columns[field]
        raw_value = row[csv_col_name]
        return cls._convert_to(cast_func, field.value, raw_value)
        
    @staticmethod
    def _convert_to(cast_func: Callable[[str], T], col: str, value: str | None) -> T:
        if value is None:
            raise InvalidDataError("Got bad value", col, value)
        try:
            return cast_func(value.strip())
        except ValueError as e:
            raise InvalidDataError(
                f"Could not convert into {cast_func}", col, value
                ) from e
    