from typing import Iterator, Sequence
import csv
import logging

from src.domain.models import CountryData
from src.domain.interfaces import BaseRepository
from src.infrastructure.schemas import CsvCountryDataSchema


logger = logging.getLogger(__name__)


class CsvSourceError(Exception):
    pass


class EmptyCsvError(CsvSourceError):
    pass


class MissingFieldsException(CsvSourceError):
    pass


class CsvRepository(BaseRepository[CountryData]):
    
    def __init__(self, 
                 file_paths: list[str], 
                 schema: CsvCountryDataSchema) -> None:
        self.file_paths = file_paths
        self.schema = schema
        self.valid_headers = schema.columns.values()
    
    def stream_data(self, year_range: range) -> Iterator[CountryData]:
        schema = self.schema
        for path in self.file_paths:
            try:
                with open(file=path, mode="r", 
                          encoding="UTF-8", newline="") as f:
                    reader = csv.DictReader(f, restval=None)
                    self._validate_headers(reader.fieldnames, path)
                    for i, row in enumerate(reader, start=2):
                        try:
                            country_data: CountryData = schema.to_domain(row)
                            if country_data.year in year_range:
                                yield country_data
                        except (ValueError, TypeError) as e:
                            raise CsvSourceError(
                                f"{path}, invalid data in row {i}"
                                ) from e
            except UnicodeDecodeError as e:
                raise CsvSourceError(f"{e}. Could not decode {path}") from e
    
    def _validate_headers(self, 
                          cur_headers: Sequence[str] | None, 
                          path: str) -> None:
        # current file headers validation with schema
        missing_fields = []
        if cur_headers is None:
            raise EmptyCsvError(f"{path} is empty")
        for h in self.valid_headers:
            if h not in cur_headers:
                missing_fields.append(h)
        if missing_fields:
            raise MissingFieldsException(
                f"{path} has missing fields: {missing_fields}."
                )