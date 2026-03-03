import pytest

import os.path
import csv
from typing import List

from analyzers import CsvAnalyzer


@pytest.fixture
def csv_headers() -> List[List[str]]:
    return [
        ["country", "year", "gdp", "gdp_growth", "inflation",
         "unemployment", "population", "continent"]
    ]


@pytest.fixture
def csv_data() -> List[List[str]]:
    return [
        ['United States', '2022', '23315', '2.1', '8.0', '3.6', '338',
         'North America'],
        ['United States', '2021', '22994', '5.9', '4.7', '5.3', '337',
         'North America'],
        ['China', '2023', '17963', '5.2', '2.5', '5.2', '1425',
         'Asia']
    ]


@pytest.fixture
def csv_file_paths(tmp_path) -> List[str]:
    return [os.path.join(tmp_path, "continent1.csv")]


@pytest.fixture
def temp_csv_file(csv_file_paths, csv_headers, csv_data):
    with open(file=csv_file_paths[0], mode="w", newline='') as f:
        csv.writer(f).writerows(csv_headers + csv_data)
        f.seek(0)
        yield f


@pytest.fixture
def report_year_range() -> range:
    return range(2000, 2026, 1)


@pytest.fixture
def report_group_by() -> str:
    return "country"


@pytest.fixture
def aggregate_func() -> str:
    return "average"


@pytest.fixture
def report_field() -> str:
    return "gdp"


@pytest.fixture
def sort_order() -> str:
    return "desc"


@pytest.fixture
def csv_analyzer(
        csv_file_paths,
        report_year_range,
        report_group_by,
        aggregate_func,
        report_field,
        sort_order,
        temp_csv_file
) -> CsvAnalyzer:
    return CsvAnalyzer(
        csv_files_paths=csv_file_paths,
        report_year_range=report_year_range,
        report_group_by=report_group_by,
        aggregate_func=aggregate_func,
        report_field=report_field,
        sort_order=sort_order
    )


def test_csv_analyzer_creation_success(csv_analyzer):
    assert csv_analyzer


def test_csv_analyzer_get_report(csv_analyzer):
    report = csv_analyzer.get_report()
    assert report == [('United States', 23154.5), ('China', 17963.0)]
