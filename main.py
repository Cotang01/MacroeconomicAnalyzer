import logging
import sys

from src.app.cli.parser import CliParser, BadArgumentError
from src.presenters.console_presenter import ConsolePresenter
from src.infrastructure.repositories import CsvRepository, CsvSourceError
from src.infrastructure.schemas import CsvCountryDataSchema
from src.services.analyzers import MacroeconomicAnalyzer
from src.domain.analysis_rules import OPERATIONS


logging.basicConfig()
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None):
    try:
        args = CliParser().parse_args(argv)
        
        repo = CsvRepository(file_paths=args.file_paths, 
                            schema=CsvCountryDataSchema)
        analyzer = MacroeconomicAnalyzer(repository=repo)
        # group_by_field and year_range can be moved to src/app/cli/parser.py
        report = analyzer.form_data(report_type=args.aggregate_operation, 
                                    report_field=args.report_field,
                                    group_by_field="country",
                                    year_range=range(1970, 2030),
                                    is_descending_ordering=True,
                                    aggregation_funcs=OPERATIONS)
        ConsolePresenter().print_report(report=report)
        return 0
    except BadArgumentError as e:
        logger.error(f"Error occured on validating user inputs: {e}")
        return 1
    except CsvSourceError as e:
        logger.error(f"Error when reading source: {e}")
        return 2
    
if __name__ == "__main__":
    sys.exit(main())
