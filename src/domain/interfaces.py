from abc import ABC, abstractmethod
from typing import Iterator, TypeVar, Generic

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    
    @abstractmethod
    def stream_data(self, year_range: range) -> Iterator[T]:
        pass
    