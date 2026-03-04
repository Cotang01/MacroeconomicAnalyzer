import csv
from typing import List, Dict

from tabulate import tabulate

from utils import operations


class CsvAnalyzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
            self,
            csv_files_paths: List[str],
            report_year_range: range | None = None,
            report_group_by: str = "country",
            aggregate_func: str = "average",
            report_field: str = "gdp",
            sort_order: str = "asc"
    ):
        """
        :param csv_files_paths: List of paths to csv files
        :param report_year_range: range object report's data needs to be
        collected within
        :param report_group_by: group statistic by: "country" or "continent"
        :param aggregate_func: aggregate function to process report_field with
        :param report_field: macroeconomic parameter to analyze
        :param sort_order: ordering, ascending or descending
        """
        self.csv_files_paths = csv_files_paths
        if report_year_range is None:
            self.report_year_range = range(2000, 2030, 1)  # start stop step
        else:
            self.report_year_range = report_year_range
        self._init_headers()
        self.report_group_by = report_group_by
        self.aggregate_func = aggregate_func
        self.report_field = report_field
        self.data: Dict[str, List[float]] = {}
        self.year_col_pos = 1

        # 0 for countries, -1 for continents
        self.group_by_idx = 0 - (self.report_group_by == "continent")

        # 0 for "asc", 1 for "desc"
        self.sort_order = 0 + (sort_order == "desc")

        # index of the needed field to analyze
        self.report_field_pos = self.csv_headers.index(self.report_field)

    def _init_headers(self) -> None:
        """
        Reads and initiates headers from the first csv file in
        stored csv file paths.
        """
        with open(file=self.csv_files_paths[0],
                  mode="r",
                  encoding="UTF-8") as f:
            self.csv_headers = next(csv.reader(f))

    def get_report(self) -> List[tuple[str, float]]:
        """ Main function, returns report with sorted data. """

        # Fills self.data with data from csv files
        for p in self.csv_files_paths:
            self._proceed_file(p)

        report_result = self._get_filtered_and_grouped_data()

        return sorted(
            # x[0] - str name, x[1] - float value
            report_result, key=lambda x: x[1], reverse=self.sort_order
        )

    def _get_filtered_and_grouped_data(self) -> List[tuple[str, float]]:
        """
        Uses self.data to pick and calculate only the required data using
        aggregation func. Returns list of (str name, float value) tuples.
        Example:
            If calculating average val is needed
            {"China": [2, 3, 6], ...} -> [("China", 5.5), ...]
        """
        res = []
        aggr_func = self.aggregate_func
        for group_by_field, stats in self.data.items():
            res.append(
                (group_by_field, (operations[aggr_func](stats)))
            )
        return res

    def _proceed_file(self, path: str) -> None:
        """
        Reads csv file using path and initiates data collection using chosen
        field as a grouping key.
        Example:
            If grouping data by countries and calculating gdp field
            [
                ["country", "gdp", ...],
                ["United States", "25462", ...],
                ...
            ] -> {"United States": [25462, ...], ...}
        """
        year_ranges: range = self.report_year_range
        idx = self.group_by_idx
        data = self.data
        headers = self.csv_headers
        report_field_pos = self.report_field_pos
        with open(file=path, mode="r", encoding="UTF-8") as f:
            reader = csv.reader(f)
            cur_headers = next(reader)
            if cur_headers != self.csv_headers:
                raise ValueError(
                    f"Headers in {path} doesn't match the initial ones; "
                    f"Initial headers are {headers}, "
                    f"got {cur_headers}"
                )
            for row in reader:
                if int(row[self.year_col_pos]) in year_ranges:
                    data.setdefault(row[idx], [])
                    data[row[idx]].append(float(row[report_field_pos]))

    def convert_into_table(self, report: List[tuple[str, float]]) -> str:
        """ Returns tabulated report if it has data, "[]" otherwise. """
        if not report:
            return "[]"
        return tabulate(
            report,
            headers=["", self.report_group_by, self.report_field],
            colalign=("right", "left", "right"),
            tablefmt="pipe",
            showindex=range(1, len(report) + 1),
            floatfmt=".2f"
        )
