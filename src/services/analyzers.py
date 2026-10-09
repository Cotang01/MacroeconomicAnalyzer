from typing import Callable
from collections import defaultdict

from src.domain.interfaces import BaseRepository

class MacroeconomicAnalyzer:
    def __init__(self, 
                 repository: BaseRepository, 
                 aggregation_operations: dict[str, Callable]) -> None:
        self._repository = repository
        self._aggregation_operations = aggregation_operations
        
    def form_data(self,
                  report_type: str,
                  report_field: str, 
                  year_range: range = range(1970, 2030)) -> list[tuple[str, float]]:
        data = defaultdict(list)
        aggr_oper = self._aggregation_operations
        for d in self._repository.stream_data(year_range=year_range):
            data[getattr(d, "country")].append(getattr(d, report_field))
        result = []
        for k, v in data.items():
            result.append((k, aggr_oper[report_type](v)))
        return result
    