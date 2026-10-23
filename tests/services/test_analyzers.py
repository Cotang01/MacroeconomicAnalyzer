from typing import Iterator

import pytest

from src.domain.models import CountryData, ReportData
from src.domain.analysis_rules import OPERATIONS
from src.domain.interfaces import BaseRepository
from src.services.analyzers import MacroeconomicAnalyzer


class FakeRepository(BaseRepository[CountryData]):
    def __init__(self, data: list[dict]) -> None:
        self._data = [CountryData(**d) for d in data]

    def stream_data(self, year_range: range) -> Iterator[CountryData]:
        for d in self._data:
            yield d

@pytest.fixture
def fake_repo_factory():
    def _create(data: list[dict]):
        return FakeRepository(data=data)
    return _create


def test_macroeconomic_analyzer_success_on_valid_data(fake_repo_factory):
    repo = fake_repo_factory([
        {"country": "USA", "year": 2021, "gdp": 21000, "gdp_growth": 5.7,
        "inflation": 4.7, "unemployment": 5.4, "population": 331, "continent": "North America"},
        {"country": "USA", "year": 2021, "gdp": 19000, "gdp_growth": 9.7,
        "inflation": 5.7, "unemployment": 4.4, "population": 320, "continent": "North America"},
        {"country": "China", "year": 2021, "gdp": 18000, "gdp_growth": 5.7,
        "inflation": 2.7, "unemployment": 5.4, "population": 1400, "continent": "Asia"},
    ])
    analyzer = MacroeconomicAnalyzer(repository=repo)
    report = analyzer.form_data(
        report_type="average",
        report_field="gdp",
        group_by_field="country",
        year_range=range(1970, 2030),
        is_descending_ordering=True,
        aggregation_funcs=OPERATIONS
    )
    assert isinstance(report, ReportData)
    assert report.group_by_field == "country"
    assert report.report_field == "gdp"
    assert report.data == [("USA", 20000.0), ("China", 18000.0)]


def test_macroeconomic_analyzer_on_empty_data(fake_repo_factory):
    repo = fake_repo_factory([])
    analyzer = MacroeconomicAnalyzer(repository=repo)
    report = analyzer.form_data(
        report_type="average",
        report_field="gdp",
        group_by_field="country",
        year_range=range(1970, 2030),
        is_descending_ordering=True,
        aggregation_funcs=OPERATIONS
    )
    assert report.data == []
    
    
def test_macroeconomic_analyzer_on_grouping_by_continent(fake_repo_factory):
    repo = fake_repo_factory([
        {"country": "Germany", "year": 2021, "gdp": 4200, "gdp_growth": 2.6,
        "inflation": 4.7, "unemployment": 5.4, "population": 83, "continent": "Europe"},
        {"country": "France", "year": 2023, "gdp": 2800, "gdp_growth": 9.7,
        "inflation": 5.7, "unemployment": 4.4, "population": 68, "continent": "Europe"},
        {"country": "China", "year": 2021, "gdp": 18000, "gdp_growth": 5.7,
        "inflation": 2.7, "unemployment": 5.4, "population": 1400, "continent": "Asia"},
    ])
    analyzer = MacroeconomicAnalyzer(repository=repo)
    report = analyzer.form_data(
        report_type="average",
        report_field="gdp",
        group_by_field="continent",
        year_range=range(1970, 2030),
        is_descending_ordering=True,
        aggregation_funcs=OPERATIONS
    )
    assert report.group_by_field == "continent"
    assert report.data == [("Asia", 18000.0), ("Europe", 3500.0)]


def test_macroeconomic_analyzer_on_ascending_ordering(fake_repo_factory):
    repo = fake_repo_factory([
        {"country": "USA", "year": 2021, "gdp": 21000, "gdp_growth": 5.7,
        "inflation": 4.7, "unemployment": 5.4, "population": 331, "continent": "North America"},
        {"country": "USA", "year": 2021, "gdp": 19000, "gdp_growth": 9.7,
        "inflation": 5.7, "unemployment": 4.4, "population": 320, "continent": "North America"},
        {"country": "China", "year": 2021, "gdp": 18000, "gdp_growth": 5.7,
        "inflation": 2.7, "unemployment": 5.4, "population": 1400, "continent": "Asia"},
    ])
    analyzer = MacroeconomicAnalyzer(repository=repo)
    report = analyzer.form_data(
        report_type="average",
        report_field="gdp",
        group_by_field="country",
        year_range=range(1970, 2030),
        is_descending_ordering=False,
        aggregation_funcs=OPERATIONS
    )
    assert report.data == [("China", 18000.0), ("USA", 20000.0)]