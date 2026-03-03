import os.path

import pytest
import csv
import sys

from typing import List

from parsers import ClaParser, CfgIniParser


@pytest.fixture(scope="module")
def csv_file_path() -> str:
    return "test.csv"


@pytest.fixture
def temp_csv_path(tmp_path, csv_file_path):
    return os.path.join(tmp_path, csv_file_path)


@pytest.fixture(scope="module")
def valid_csv_data() -> List[List[str]]:
    return [
        ["country", "year", "gdp", "gdp_growth", "inflation",
         "unemployment", "population", "continent"],
        ["United States", "2022", "23315", "2.1", "8.0", "3.6",
         "338", "North America"],
        ["United States", "2021", "22994", "5.9", "4.7", "5.3",
         "337", "North America"],
        ["China", "2023", "17963", "5.2", "2.5", "5.2",
         "1425", "Asia"],
    ]


@pytest.fixture
def temp_csv_file(temp_csv_path):
    with open(file=temp_csv_path,
              mode="w+",
              encoding="UTF-8",
              newline="") as f:
        yield f


@pytest.fixture
def valid_args(temp_csv_path, temp_csv_file) -> List[str]:
    return ["", "--files", temp_csv_path, "--report", "average-gdp"]


@pytest.fixture
def invalid_args() -> List[str]:
    return ["", "--flies"]


@pytest.fixture
def valid_args_extra_arg(valid_args) -> List[str]:
    return valid_args + ["--extra", "extra"]


def test_cla_parsing_success(valid_args, monkeypatch, temp_csv_path):
    monkeypatch.setattr(sys, "argv", valid_args)
    cla_args = ClaParser()
    assert cla_args.csv_files == [os.path.abspath(temp_csv_path)]


def test_cla_parsing_bad_args(invalid_args, monkeypatch, temp_csv_file):
    monkeypatch.setattr(sys, "argv", invalid_args)
    with pytest.raises(ValueError):
        ClaParser()


def test_cla_handle_extra_arg(valid_args_extra_arg, monkeypatch,
                              temp_csv_file):
    monkeypatch.setattr(sys, "argv", valid_args_extra_arg)
    with pytest.raises(ValueError):
        ClaParser()


@pytest.fixture
def cfg_valid_data() -> str:
    return '''[DEFAULT] \n
ReportTypes = ["average", "max", "min"] \n
ReportFields = ["year", "gdp", "gdp_growth", 
                "inflation", "unemployment", "population"] \n
ReportYearRange = [2000, 2026, 1] \n 
ReportGroupBy = "country" \n
ReportSortOrder = "desc" \n
'''


@pytest.fixture
def ini_file_name() -> str:
    return "config.ini"


@pytest.fixture
def ini_file_path(tmp_path, ini_file_name) -> str:
    return os.path.join(tmp_path, ini_file_name)


@pytest.fixture
def temp_ini_file(ini_file_path, cfg_valid_data):
    with open(file=ini_file_path, mode="w+") as f:
        f.write(cfg_valid_data)
        f.seek(0)
        yield f


@pytest.fixture
def aggreg_func() -> str:
    return "average"


@pytest.fixture
def report_field() -> str:
    return "gdp"


def test_cfg_ini_parser(ini_file_path, temp_ini_file):
    config = CfgIniParser(ini_file_path=ini_file_path)
    assert config.report_types == ["average", "max", "min"]
    assert config.report_group_by == "country"
    assert config.report_year_range == range(2000, 2026, 1)
    assert config.report_sort_order == "desc"
    assert config.report_fields == [
        "year", "gdp", "gdp_growth", "inflation", "unemployment", "population"
    ]


def test_cfg_ini_parser_validate_report_args(
        ini_file_path, temp_ini_file, aggreg_func, report_field
):
    CfgIniParser(
        ini_file_path=ini_file_path
    ).validate_report_args(
        aggreg_func=aggreg_func, report_field=report_field
    )
