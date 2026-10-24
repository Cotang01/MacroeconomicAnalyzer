from typing import Iterator, Sequence
import csv
import logging
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from src.domain.models import CountryData, DomainError
from src.domain.interfaces import BaseRepository
from src.infrastructure.db.models import CountryDataModel
from src.infrastructure.schemas import (
    CsvCountryDataSchema, InvalidDataError, SqlCountryDataSchema
    )


logger = logging.getLogger()


class CsvSourceError(Exception):
    pass


class EmptyCsvError(CsvSourceError):
    pass


class MissingFieldsError(CsvSourceError):
    pass


class CsvRepository(BaseRepository[CountryData]):
    """Class for reading .csv files and validating data for further processing
            file_paths: list of absolute paths of each file
        schema: schema class used for validation logic
    """
    def __init__(self,
                 file_paths: list[Path], 
                 schema: type[CsvCountryDataSchema]) -> None:
        self.file_paths = file_paths
        self.schema = schema
        self.valid_headers = schema.columns.values()
    
    def stream_data(self, year_range: range) -> Iterator[CountryData]:
        """Iterates through .csv files and yields objects consisting
        data about country statistics"""
        schema = self.schema
        for path in self.file_paths:
            try:
                with open(file=path, mode="r", 
                          encoding="UTF-8", newline="") as f:
                    # restval=None is required to catch corrupted
                    reader = csv.DictReader(f, restval=None)
                    valid_headers_exist = self._validate_headers(reader.fieldnames, path)
                    if not valid_headers_exist:
                        logger.warning(f"{path} has no data")
                        continue
                    has_data = False
                    for i, row in enumerate(reader, start=2):
                        has_data = True
                        try:
                            country_data: CountryData = schema.to_domain(row)
                            if country_data.year in year_range:
                                yield country_data
                        except InvalidDataError as e:
                            raise CsvSourceError(
                                f"{path} has invalid data in row {i}: {e}"
                                ) from e
                        except DomainError as e:
                            raise CsvSourceError(
                                f"{path} domain rule violation in row {i}: {e}"
                            )
                    if not has_data:
                        logger.warning(f"{path} has headers, but no data")
            except UnicodeDecodeError as e:
                raise CsvSourceError(f"{e}. Could not decode {path}") from e
    
    def _validate_headers(self, 
                          cur_headers: Sequence[str] | None, 
                          path: Path) -> bool:
        # current file headers validation with schema
        missing_fields = []
        if cur_headers is None:
            return False
        for h in self.valid_headers:
            if h not in cur_headers:
                missing_fields.append(h)
        if missing_fields:
            raise MissingFieldsError(
                f"{path} has missing fields: {missing_fields}."
                )
        return True


class SqlRepository(BaseRepository[CountryData]):
    def __init__(self, 
                 sessionmaker: sessionmaker, 
                 schema: type[SqlCountryDataSchema]) -> None:
        self.sessionmaker = sessionmaker
        self.schema = schema
        
    def stream_data(self, year_range: range) -> Iterator[CountryData]:
        schema = self.schema
        query = select(CountryDataModel).where(
            CountryDataModel.year.between(year_range.start, year_range.stop - 1)
        )
        with self.sessionmaker() as session:
            for row in session.scalars(query).yield_per(1000):
                yield schema.to_domain(row)