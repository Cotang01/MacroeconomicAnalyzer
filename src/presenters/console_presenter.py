from tabulate import tabulate

from src.domain.models import ReportData


# TODO add logging
class ConsolePresenter:
    @staticmethod
    def print_report(report: ReportData) -> None:
        """ Returns tabulated report if it has data, "[]" otherwise. """
        if not report.data:
            print("NO")
            return
        print(tabulate(
            report.data,
            headers=["", report.group_by_field, report.report_field],
            colalign=("right", "left", "right"),
            tablefmt="pipe",
            showindex=range(1, len(report.data) + 1),
            floatfmt=".2f"
        ))