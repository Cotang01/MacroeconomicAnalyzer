from argparse import ArgumentParser
from pathlib import Path
from dataclasses import dataclass

from src.domain.analysis_rules import OPERATIONS, AGGREGATABLE_FIELDS


VALID_OPERATIONS = {*OPERATIONS.keys()}
VALID_FILE_EXTENSIONS = {".csv"}


class BadArgumentError(Exception):
    pass


class BadFileExtensionError(BadArgumentError):
    pass


class BadFilePathError(BadArgumentError):
    pass


class BadAggregationFuncError(BadArgumentError):
    pass


class BadReportFieldError(BadArgumentError):
    pass


@dataclass(frozen=True)
class CliArgs:
    file_paths: list[Path]
    aggregate_operation: str
    report_field: str


class CliParser:

    def __init__(self):
        """
        Used for parsing command line arguments.
            --files - sequence of .csv files to read delimited by space.
            --report - report's parameters (f"{type}-{field}").
        """
        self._parser = ArgumentParser(
            prog="MacroeconomicAnalyzer",
            description="Script to analyze datasets of "
                        "countries' various statistics."
        )
        self._parser.add_argument("-f", "--files", nargs="+",
                                             help=".csv files to analyze.")
        self._parser.add_argument("-r", "--report",
                                               help="Report's params.")
    
    def parse_args(self, argv: list[str] | None = None) -> CliArgs:
        args = self._parser.parse_args(argv)
        if not args.files:
            raise BadArgumentError("--files is required")
        if not args.report:
            raise BadArgumentError("--report is required")
        paths = self._resolve_files(args.files)
        if not paths:
            raise BadFilePathError(f"Provided file paths are invalid: {paths}")
        aggreg_func, report_field = self._parse_report(args.report)
        return CliArgs(
            file_paths=paths,
            aggregate_operation=aggreg_func,
            report_field=report_field
        )
        

    def _resolve_files(self, paths: list[str]) -> list[Path]:
        """
        Function that validates file paths and returns absolute paths.
        """
        abs_paths = []
        for p in paths:
            abs_path = Path(p).absolute()
            if not abs_path.is_file():
                raise BadFilePathError(f"{p} is not a file")
            if abs_path.suffix.lower() not in VALID_FILE_EXTENSIONS:
                raise BadFileExtensionError(f"{p} has unsupported extension")
            abs_paths.append(abs_path)
        return abs_paths
        
    def _parse_report(self, report: str) -> tuple[str, str]:
        report_args = report.split("-")
        if len(report_args) != 2:
            raise BadArgumentError(f"{report} is not supported.")
        aggr, field = report_args
        if aggr not in VALID_OPERATIONS:
            raise BadAggregationFuncError(f"{aggr} operation is not supported")
        if field not in AGGREGATABLE_FIELDS:
            raise BadReportFieldError(
                f"You can not form a report based on {field}"
                )
        return aggr, field
    