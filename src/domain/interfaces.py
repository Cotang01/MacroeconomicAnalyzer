from abc import ABC, abstractmethod
from typing import Iterator

from src.domain.models import Data

class BaseRepository(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def stream_data(self, 
                    year_range: range = range(1970, 2030)) -> Iterator[Data]:
        pass
    