from abc import ABC, abstractmethod
from typing import Iterator, TypeVar, Generic

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def stream_data(self, 
                    year_range: range = range(1970, 2030)) -> Iterator[T]:
        pass
    