from typing import Iterator
from csv import reader as CsvReader
from dataclasses import fields
import logging

from src.domain.models import CountryData
from src.domain.interfaces import BaseRepository
from src.infrastructure.schemas import CountryDataSchema

logger = logging.getLogger(__name__)
    
class CsvRepository(BaseRepository[CountryData]):
    
    def __init__(self, file_paths: list[str], schema: CountryDataSchema) -> None:
        self.file_paths = file_paths
        self.schema = schema
        self.valid_headers = [getattr(schema, field.name) for field in fields(schema)]
    
    def stream_data(self, year_range: range) -> Iterator[CountryData]:
        schema = self.schema
        valid_headers = self.valid_headers
        for path in self.file_paths:
            fields_idx = {}
            missing_fields = []
            with open(file=path, mode="r", encoding="UTF-8") as f:
                reader = CsvReader(f)
                cur_headers = next(reader)    
                # current headers validation with schema
                for v_h in valid_headers:
                    if v_h not in cur_headers:
                        missing_fields.append(v_h)
                    else:
                        fields_idx[v_h] = cur_headers.index(v_h)
                if missing_fields:
                    logging.warning(f"{path} has missing fields: {missing_fields}")
                    continue
                for row in reader:
                    if int(row[fields_idx[schema.year]]) in year_range:
                        kwargs_ = {}
                        for field, cast_func in CountryData.__annotations__.items():
                            csv_header_name = getattr(schema, field)
                            idx = fields_idx[csv_header_name]
                            kwargs_[field] = cast_func(row[idx].strip())
                        yield CountryData(**kwargs_)
