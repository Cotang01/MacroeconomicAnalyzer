from argparse import ArgumentParser
import os


class BadArgumentError(Exception):
    pass

class CliParser:

    def __init__(self):
        """
        Used for parsing command line arguments.
            --files - list of .csv files to read.
            --report - report's name.
        """
        self._parser = ArgumentParser(
            prog="MacroeconomicAnalyzer",
            description="Script to analyze datasets of "
                        "countries' various statistics."
        )
        
        self._setup_arguments()
        
    
    def _setup_arguments(self) -> None:
        self._parser.add_argument("-f", "--files", nargs="+",
                                             help=".csv files to analyze.")
        self._parser.add_argument("-r", "--report",
                                               help="Report's name.")
        
        args = self._parser.parse_args()
        for arg, value in args.__dict__.items():
            if value is None:
                raise BadArgumentError(
                    f"{arg} was not provided.",
                )
        self._resolve_files(args.files)
        report_args: list[str] = args.report.split('-')
        if len(report_args) != 2:
            raise BadArgumentError(
                f"Unsupported report args {report_args}",
            )
        self.aggregate_func = report_args[0]
        self.report_field = report_args[-1]

    def _resolve_files(self, paths: list[str]) -> None:
        """
        Function that validates file paths: extension is .csv , path exists,
        is file; and then replaces paths with respective absolute versions.
        """
        abs_paths = []
        for p in paths:
            abs_path = os.path.abspath(p)
            _, cur_ext = os.path.splitext(abs_path)
            # logic to skip invalid paths can be added
            if cur_ext.lower() != ".csv":
                raise BadArgumentError(
                    f"Unsupported file extension: {cur_ext}"
                )
            elif not os.path.exists(abs_path):
                raise BadArgumentError(
                    f"Path doesn't exist: {abs_path}"
                )
            elif not os.path.isfile(abs_path):
                raise BadArgumentError(
                    f"Not a file: {abs_path}"
                )
            abs_paths.append(abs_path)
        self.csv_file_paths = abs_paths
        