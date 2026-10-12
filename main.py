import logging
import sys

from src.app.cli.parser import CliParser
from src.presenters.console_presenter import ConsolePresenter
from src.infrastructure.repositories import CsvRepository
from src.infrastructure.schemas import CountryDataSchema
from src.services.analyzers import MacroeconomicAnalyzer
from src.domain.calculators import operations


logger = logging.basicConfig()


def main():
    
    cli_args = CliParser()
    
    repo = CsvRepository(file_paths=cli_args.csv_file_paths, 
                         schema=CountryDataSchema())
    analyzer = MacroeconomicAnalyzer(repository=repo, 
                                     aggregation_operations=operations)
    report = analyzer.form_data(report_type=cli_args.aggregate_func, 
                                report_field=cli_args.report_field,
                                group_by_field="country",
                                year_range=range(1970, 2030),
                                is_descending_ordering=True)
    table = ConsolePresenter.convert_into_table(report=report)
    print(table)
    
    
if __name__ == "__main__":
    main()
