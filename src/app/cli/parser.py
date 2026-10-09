from argparse import ArgumentParser
import os


class BadArgumentError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

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
                    message=f"{arg} was not provided.",
                )
        self._resolve_files(args.files)
        report_args: list[str] = args.report.split('-')
        if len(report_args) != 2:
            raise BadArgumentError(
                message=f"Unsupported report args {report_args}",
            )
        self.aggregate_func = report_args[0]
        self.report_field = report_args[-1]

    def _resolve_files(self, paths: list[str]) -> None:
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
                raise BadArgumentError(
                    message=f"Unsupported file extension: {cur_ext}"
                )
            elif not os.path.exists(abs_path):
                raise BadArgumentError(
                    message=f"Path doesn't exist: {abs_path}"
                )
            elif not os.path.isfile(abs_path):
                raise BadArgumentError(
                    message=f"Not a file: {abs_path}"
                )
            paths[i] = abs_path
        self.csv_file_paths = paths