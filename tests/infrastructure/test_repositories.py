import pytest
from pathlib import Path
import logging
from textwrap import dedent

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.repositories import (
    CsvRepository, MissingFieldsError, SourceError, SqlRepository
    )
from src.infrastructure.schemas import CsvCountryDataSchema, SqlCountryDataSchema
from src.infrastructure.db.database import Base
from src.infrastructure.db.models import CountryDataModel
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


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(url="sqlite+pysqlite:///:memory:", 
                           poolclass=StaticPool)
    try:
        Base.metadata.create_all(engine)
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def session_local(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    try:
        yield SessionLocal
    finally:    
        transaction.rollback()
        connection.close()


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
    with pytest.raises(SourceError):
        list(repo.stream_data(year_range=range(2023, 2024)))


def test_csv_repo_raises_on_bad_file_encoding(test_files_factory):
    file_paths = test_files_factory({
        "valid.csv": 
            dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
                   США,2023,25462,2.1,3.4,3.7,339,Северная Америка\n
                   China,2023,17963,5.2,2.5,5.2,1425,Asia""")}, encoding="CP1251")
    repo = CsvRepository(file_paths, CsvCountryDataSchema)
    with pytest.raises(SourceError) as e:
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


def test_sql_repo_success_on_valid_data(session_local):
    with session_local() as session:
        query = insert(CountryDataModel).values(
            country="USA", year=2021, gdp=21000, gdp_growth=5.7, inflation=4.7, 
            unemployment=5.4, population=331, continent="North America",
            )
        session.execute(query)
        session.commit()
    
    repo = SqlRepository(sessionmaker=session_local, schema=SqlCountryDataSchema)
    result = list(repo.stream_data(year_range=range(1970, 2030)))
    cd_1 = result[0]
    assert len(result) == 1
    assert isinstance(cd_1, CountryData)
    assert cd_1.country == "USA"


def test_sql_repo_on_empty_data(session_local):
    repo = SqlRepository(sessionmaker=session_local, schema=SqlCountryDataSchema)
    result = list(repo.stream_data(year_range=range(1970, 2030)))
    assert result == []


def test_sql_repo_raises_on_corrupted_data(session_local):
    with session_local() as session:
        query = insert(CountryDataModel).values(
            country="USA", year=2021, gdp="not_a_gdp", gdp_growth=5.7, inflation=4.7, 
            unemployment=5.4, population=331, continent="North America",
            )
        session.execute(query)
        session.commit()
    
    repo = SqlRepository(sessionmaker=session_local, schema=SqlCountryDataSchema)
    with pytest.raises(SourceError):
        list(repo.stream_data(year_range=range(1970, 2030)))