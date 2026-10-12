from tabulate import tabulate

from src.domain.models import ReportData


class ConsolePresenter:
    @staticmethod
    def convert_into_table(report: ReportData) -> str:
        """ Converts report into str table if the report.data is not empty, 
        returns empty string otherwise. """
        if not report.data:
            return ""
        return tabulate(
            report.data,
            headers=["", report.group_by_field, report.report_field],
            colalign=("right", "left", "right"),
            tablefmt="pipe",
            showindex=range(1, len(report.data) + 1),
            floatfmt=".2f"
        )