import io

from src.presenters.console_presenter import ConsolePresenter
from src.domain.models import ReportData

def test_console_presenter_returns_report_on_valid_data():
    report = ReportData(group_by_field="country", 
                        report_field="gdp",
                        data=[("United States", 26000)])
    stream = io.StringIO()
    presenter = ConsolePresenter(stream=stream)
    presenter.print_report(report)
    output = stream.getvalue()
    assert "country" in output
    assert "gdp" in output
    assert "United States" in output
    assert "26000" in output


def test_console_presenter_returns_no_on_empty_data():
    report = ReportData(group_by_field="country", 
                        report_field="gdp",
                        data=[])
    stream = io.StringIO()
    presenter = ConsolePresenter(stream=stream)
    presenter.print_report(report)
    output = stream.getvalue()
    assert "NO" in output
    assert "country" not in output
    assert "gdp" not in output
