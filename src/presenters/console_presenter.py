from tabulate import tabulate
import sys

from src.domain.models import ReportData


class ConsolePresenter:
    """Presenter class for reports' formatting"""
    def __init__(self, stream=sys.stdout) -> None:
        self.stream = stream
    
    def print_report(self, report: ReportData) -> None:
        """ Converts report into tabulate table if the report.data is not 
        empty and prints it using self.stream"""
        if not report.data:
            print("NO", file=self.stream)
            return
        print(tabulate(
            report.data,
            headers=["", report.group_by_field, report.report_field],
            colalign=("right", "left", "right"),
            tablefmt="pipe",
            showindex=range(1, len(report.data) + 1),
            floatfmt=".2f"
        ), file=self.stream)
        