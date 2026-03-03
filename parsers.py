from argparse import ArgumentParser, ArgumentError
from configparser import ConfigParser

import os
import json
from typing import List


class ClaParser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Used for parsing command line arguments.
            --files - list of .csv files to read.
            --report - report's name.
        """
        parser = ArgumentParser(
            prog="MacroeconomicAnalyzer",
            description="Script to analyze .csv datasets of "
                        "countries' various statistics."
        )
        self.csv_files = parser.add_argument("-f", "--files", nargs="+",
                                             help=".csv files to analyze.")
        self.report_args = parser.add_argument("-r", "--report",
                                               help="Report's name.")
        try:
            args = parser.parse_args()
        except SystemExit:
            raise ValueError(
                f"Invalid arguments were provided, valid ones are "
                f"-f or --files and -r or --report"
            )
        self._resolve_files(args.files)
        report_args: List[str] = args.report.split('-')
        if len(report_args) != 2:
            raise ArgumentError(
                message=f"Unsupported report args {report_args}",
                argument=self.report_args,
            )
        self.aggregate_func = report_args[0]
        self.report_field = report_args[-1]

    def _resolve_files(self, paths: List[str]) -> None:
        """
        Function that validates file paths: extension is .csv , path exists,
        is file; and then replaces paths with respective absolute versions.
        """
        for i in range(len(paths)):
            cur_path = paths[i]
            abs_path = os.path.abspath(cur_path)
            cur_ext = os.path.basename(cur_path).split(".")[-1]
            # logic to skip invalid paths can be added
            if cur_ext != "csv":
                raise ArgumentError(
                    message=f"Unsupported file extension: {cur_ext}",
                    argument=self.csv_files
                )
            elif not os.path.exists(abs_path):
                raise ArgumentError(
                    message=f"Path doesn't exist: {abs_path}",
                    argument=self.csv_files
                )
            elif not os.path.isfile(cur_path):
                raise ArgumentError(
                    message=f"Not a file: {abs_path}",
                    argument=self.csv_files
                )
            paths[i] = abs_path
        self.csv_files = paths


class CfgIniParser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ini_file_path: str):
        """ Parses config.ini """
        parser = ConfigParser()
        parser.read(os.path.abspath(ini_file_path))

        self.report_types = json.loads(
            parser.get("DEFAULT", "ReportTypes")
        )
        self.report_fields = json.loads(
            parser.get("DEFAULT", "ReportFields")
        )
        self.report_year_range = range(
            *json.loads(parser.get("DEFAULT", "ReportYearRange"))
        )
        self.report_group_by = json.loads(
            parser.get("DEFAULT", "ReportGroupBy")
        )
        self.report_sort_order = json.loads(
            parser.get("DEFAULT", "ReportSortOrder")
        )

    def validate_report_args(self,
                             aggreg_func: str,
                             report_field: str) -> None:
        if aggreg_func is not None and aggreg_func not in self.report_types:
            raise ValueError(
                f"Unsupported aggregation func {aggreg_func} for field "
                f"{report_field}, valid ones are {self.report_types}"
            )
        if report_field not in self.report_fields:
            if aggreg_func is not None:
                raise ValueError(
                    f"Unsupported report type {report_field} "
                    f"with aggregation function {aggreg_func}"
                )
            elif aggreg_func is None:
                raise ValueError(
                    f"Unsupported report type {report_field} "
                    f"with aggregation function {aggreg_func}"
                )
        if aggreg_func is None and report_field in self.report_fields:
            raise ValueError(
                f"{report_field} report requires one of the "
                f"aggregation funcs {self.report_types}, "
                f"not {aggreg_func}"
            )
