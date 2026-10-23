from textwrap import dedent
import logging

from main import main


def test_main_happy_path(tmp_path, capsys):
    f = tmp_path / "valid.csv"
    f.write_text(
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2023,25462,2.1,3.4,3.7,339,North America\n"""),
        encoding="UTF-8")
    argv = ["--report", "average-gdp", "--files", f"{f}"]
    exit_code = main(argv=argv)
    assert exit_code == 0
    
    captured = capsys.readouterr()
    assert "United States" in captured.out


def test_main_error_log_on_invalid_report(tmp_path, caplog):
    f = tmp_path / "valid.csv"
    f.write_text(
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2023,25462,2.1,3.4,3.7,339,North America\n"""),
        encoding="UTF-8")
    argv = ["--report", "weird_operation-gdp", "--files", f"{f}"]
    with caplog.at_level(logging.ERROR):
        exit_code = main(argv=argv)
    assert exit_code == 1
    assert "weird_operation" in caplog.text


def test_main_error_log_on_invalid_files(tmp_path, caplog):
    f = tmp_path / "valid.csv"
    f.write_text(
        dedent("""country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n
               United States,2023,25462,2.1,3.4,3.7,,\n"""),
        encoding="UTF-8")
    argv = ["--report", "average-gdp", "--files", f"{f}"]
    with caplog.at_level(logging.ERROR):
        exit_code = main(argv=argv)
    assert exit_code == 2
    assert f.name in caplog.text