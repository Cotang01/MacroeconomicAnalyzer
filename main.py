from parsers import ClaParser, CfgIniParser
from analyzers import CsvAnalyzer

import os
from pathlib import Path


def main():
    cla_args = ClaParser()
    config = CfgIniParser(
        ini_file_path=os.path.join(Path(__file__).parent, "config.ini")
    )

    config.validate_report_args(
        aggreg_func=cla_args.aggregate_func,
        report_field=cla_args.report_field
    )
    analyzer = CsvAnalyzer(
        csv_files_paths=cla_args.csv_files,
        report_year_range=config.report_year_range,
        report_field=cla_args.report_field,
        report_group_by=config.report_group_by,
        aggregate_func=cla_args.aggregate_func,
        sort_order=config.report_sort_order
    )
    report = analyzer.get_report()
    print(analyzer.convert_into_table(report))


if __name__ == "__main__":
    main()
