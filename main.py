import logging
import sys

from src.app.cli.parser import CliParser, BadArgumentError
from src.app.report_settings import (
    GROUP_BY_FIELD, YEAR_RANGE, IS_DESCENDING_ORDERING
    )
from src.presenters.console_presenter import ConsolePresenter
from src.infrastructure.repositories import CsvRepository, CsvSourceError
from src.infrastructure.schemas import CsvCountryDataSchema
from src.services.analyzers import MacroeconomicAnalyzer
from src.domain.analysis_rules import OPERATIONS


logging.basicConfig(level=logging.WARNING, 
                    format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None):
    try:
        args = CliParser().parse_args(argv)
        
        repo = CsvRepository(file_paths=args.file_paths, 
                            schema=CsvCountryDataSchema)
        analyzer = MacroeconomicAnalyzer(repository=repo)
        report = analyzer.form_data(report_type=args.aggregate_operation, 
                                    report_field=args.report_field,
                                    group_by_field=GROUP_BY_FIELD,
                                    year_range=YEAR_RANGE,
                                    is_descending_ordering=IS_DESCENDING_ORDERING,
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
