import logging

from src.app.cli.parser import CliParser
from src.presenters.console_presenter import ConsolePresenter
from src.infrastructure.repositories import CsvRepository
from src.infrastructure.schemas import CsvCountryDataSchema
from src.services.analyzers import MacroeconomicAnalyzer
from src.domain.calculators import OPERATIONS


logger = logging.basicConfig()


def main(argv: list[str] | None = None):
    
    parser = CliParser()
    args = parser.parse_args(argv)
    
    repo = CsvRepository(file_paths=args.file_paths, 
                         schema=CsvCountryDataSchema())
    analyzer = MacroeconomicAnalyzer(repository=repo)
    report = analyzer.form_data(report_type=args.aggregate_operation, 
                                report_field=args.report_field,
                                group_by_field="country",
                                year_range=range(1970, 2030),
                                is_descending_ordering=True,
                                aggregation_funcs=OPERATIONS)
    table = ConsolePresenter.convert_into_table(report=report)
    print(table)
    
    
if __name__ == "__main__":
    main()
