import pytest

from src.app.cli.parser import (
    CliParser, CliArgs, BadFilePathError, BadFileExtensionError, 
    BadAggregationFuncError, BadReportFieldError, BadArgumentError
    )



def test_cli_parser_on_valid_args(tmp_path):
    f = tmp_path / "some_real.csv"
    f.write_text("")
    argv = ["--report", "average-gdp", "--files", f"{f}"]
    cli_args = CliParser().parse_args(argv=argv)
    assert isinstance(cli_args, CliArgs)
    assert cli_args.aggregate_operation == "average"
    assert cli_args.report_field == "gdp"
    assert cli_args.file_paths == [f]


def test_cli_parser_on_invalid_file_path():
    argv = ["--report", "average-gdp", "--files", "unreal.csv"]
    with pytest.raises(BadFilePathError):
        CliParser().parse_args(argv=argv)
        

def test_cli_parser_on_invalid_file_extension(tmp_path):
    f = tmp_path / "invalid.txt"
    f.write_text("")
    argv = ["--report", "average-gdp", "--files", f"{f}"]
    with pytest.raises(BadFileExtensionError):
        CliParser().parse_args(argv=argv)    


def test_cli_parser_on_invalid_aggregation_func(tmp_path):
    f = tmp_path / "valid.csv"
    f.write_text("")
    argv = ["--report", "some-gdp", "--files", f"{f}"]
    with pytest.raises(BadAggregationFuncError):
        CliParser().parse_args(argv=argv)


def test_cli_parser_on_invalid_report_field(tmp_path):
    f = tmp_path / "valid.csv"
    f.write_text("")
    argv = ["--report", "average-year", "--files", f"{f}"]
    with pytest.raises(BadReportFieldError):
        CliParser().parse_args(argv=argv)


def test_cli_parser_without_report_arg(tmp_path):
    f = tmp_path / "valid.csv"
    f.write_text("")
    argv = ["--files", f"{f}"]
    with pytest.raises(BadArgumentError):
        CliParser().parse_args(argv=argv)


def test_cli_parser_without_files(tmp_path):
    argv = ["--report", "average-gdp"]
    with pytest.raises(BadArgumentError):
        CliParser().parse_args(argv=argv)