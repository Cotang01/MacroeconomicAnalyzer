from tabulate import tabulate

class ConsolePresenter:
    @staticmethod
    def print_report(report: list[tuple[str, float]],
                     group_by: str ="country", 
                     report_field: str ="gdp") -> None:
        """ Returns tabulated report if it has data, "[]" otherwise. """
        if not report:
            print("NO")
        print(tabulate(
            report,
            headers=["", group_by, report_field],
            colalign=("right", "left", "right"),
            tablefmt="pipe",
            showindex=range(1, len(report) + 1),
            floatfmt=".2f"
        ))