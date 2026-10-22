import pytest
from pathlib import Path
import logging
from textwrap import dedent

from src.infrastructure.repositories import (
    CsvRepository, MissingFieldsError, CsvSourceError
    )
from src.infrastructure.schemas import CsvCountryDataSchema
from src.domain.models import CountryData


@pytest.fixture
def test_files_factory(tmp_path):
    def _create(file_name_data_dict: dict[str, str], 
                encoding: str = "UTF-8") -> list[Path]:
        file_paths = []
        for f_n, d in file_name_data_dict.items():
            f = Path(tmp_path / f_n).absolute()
            f.write_text(d, encoding=encoding)
            file_paths.append(f)
        return file_paths
    return _create


def test_csv_repo_success_on_valid_data(test_files_factory):
    file_paths = test_files_factory({
        "valid.csv": dedent(
            """country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
            United States,2023,25462,2.1,3.4,3.7,339,North America\n
            China,2023,17963,5.2,2.5,5.2,1425,Asia""")})
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert len(data) == 2
    for d in data:
        assert isinstance(d, CountryData)


def test_csv_repo_warn_log_on_empty_file(test_files_factory, caplog):
    file_paths = test_files_factory({"invalid.csv": ""})
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with caplog.at_level(logging.WARNING):
        data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert len(data) == 0
    assert "invalid.csv" in caplog.text


def test_csv_repo_warn_log_on_only_headers(test_files_factory, caplog):
    file_paths = test_files_factory(
        {"only_headers.csv": 
            dedent("country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n")}
        )
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with caplog.at_level(logging.WARNING):
        data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert len(data) == 0
    assert file_paths[0].name in caplog.text


def test_csv_repo_raises_on_missing_headers(test_files_factory):
    file_paths = test_files_factory(
            {"missing_headers.csv": 
                dedent("""country,year,gdp,gdp_growth\n
                       United States,2023,25462,2.1\n
                       China,2023,17963,5.2""")}
            )
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with pytest.raises(MissingFieldsError):
        list(repo.stream_data(year_range=range(2023, 2024)))


def test_csv_repo_raises_on_corrupted_row(test_files_factory):
    file_paths = test_files_factory(
            {"corrupted.csv": 
                dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
                       United States,2023,25462,2.1,3.4,3.7,339,\n
                       China,2023,17963,5.2,2.5,5.2,1425,Asia""")}
            )
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with pytest.raises(CsvSourceError):
        list(repo.stream_data(year_range=range(2023, 2024)))


def test_csv_repo_raises_on_bad_file_encoding(test_files_factory):
    file_paths = test_files_factory({
        "valid.csv": 
            dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
                   США,2023,25462,2.1,3.4,3.7,339,Северная Америка\n
                   China,2023,17963,5.2,2.5,5.2,1425,Asia""")}, encoding="CP1251")
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with pytest.raises(CsvSourceError) as e:
        list(repo.stream_data(year_range=range(2023, 2024)))
    assert file_paths[0].name in e.exconly()


def test_csv_repo_year_range_filter(test_files_factory):
    file_paths = test_files_factory({
    "valid.csv": 
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2025,25462,2.1,3.4,3.7,339,North America\n
               China,2023,17963,5.2,2.5,5.2,1425,Asia""")})
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert len(data) == 1
    assert data[0].country == "China"
    
def test_csv_repo_success_and_log_on_valid_and_empty_files(test_files_factory,
                                                           caplog):
    file_paths = test_files_factory({
    "valid.csv": 
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2023,25462,2.1,3.4,3.7,339,North America\n
               China,2023,17963,5.2,2.5,5.2,1425,Asia"""),
    "empty.csv": ""})
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with caplog.at_level(logging.WARNING):
        data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert "empty.csv" in caplog.text
    assert len(data) == 2
    assert isinstance(data[0], CountryData)


def test_csv_repo_success_and_log_on_valid_and_headers_only_files(test_files_factory,
                                                                  caplog):
    file_paths = test_files_factory({
    "valid.csv": 
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2023,25462,2.1,3.4,3.7,339,North America\n
               China,2023,17963,5.2,2.5,5.2,1425,Asia"""),
    "headers_only.csv": "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"})
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with caplog.at_level(logging.WARNING):
        data = list(repo.stream_data(year_range=range(2023, 2024)))
    assert "headers_only.csv" in caplog.text
    assert len(data) == 2
    assert isinstance(data[0], CountryData)
