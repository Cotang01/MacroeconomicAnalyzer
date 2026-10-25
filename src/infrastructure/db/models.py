from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float

from src.infrastructure.db.database import Base


class CountryDataModel(Base):
    __tablename__ = "country_data"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column(Integer)
    gdp: Mapped[int] = mapped_column(Integer)
    gdp_growth: Mapped[float] = mapped_column(Float)
    inflation: Mapped[float] = mapped_column(Float)
    unemployment: Mapped[float] = mapped_column(Float)
    population: Mapped[int] = mapped_column(Integer)
    continent: Mapped[str] = mapped_column(String(20))
    
    def __repr__(self) -> str:
        return f"CountryData{list(self.__dict__.items())}"