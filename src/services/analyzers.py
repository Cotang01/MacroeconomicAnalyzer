from typing import Callable, TypeVar
from collections import defaultdict

from src.domain.interfaces import BaseRepository
from src.domain.models import ReportData


T = TypeVar("T")


class MacroeconomicAnalyzer:
    def __init__(self, repository: BaseRepository[T]) -> None:
        self._repository = repository
        
    def form_data(self,
                  report_type: str,
                  report_field: str,
                  group_by_field: str,
                  year_range: range,
                  is_descending_ordering: bool,
                  aggregation_funcs: dict[str, Callable]) -> ReportData:
        data = defaultdict(list)
        for d in self._repository.stream_data(year_range=year_range):
            data[getattr(d, group_by_field)].append(getattr(d, report_field))
        result = []
        for k, v in data.items():
            result.append((k, aggregation_funcs[report_type](v)))
        result.sort(key=lambda x: x[1], reverse=is_descending_ordering)
        return ReportData(
            group_by_field=group_by_field, 
            report_field=report_field, 
            data=result
            )
    