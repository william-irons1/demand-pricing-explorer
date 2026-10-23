"""Regenerate findings documents and full-precision benchmark comparisons."""

import csv
from pathlib import Path

from analysis import chosen_price_rows, model_risk_rows, report_markdown, summary_markdown
from models import Parameters, analytical_optimum


def write_reports(destination):
    """Write reproducible deliverables to a project directory, returning paths."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    evidence = destination / 'evidence'
    evidence.mkdir(exist_ok=True)
    params = Parameters()
    # A reproducible chosen-price example, derived rather than hard-coded.
    test_price = analytical_optimum('constant_elasticity', params).price
    files = {
        destination / 'investigation_worksheet.md': report_markdown(),
        destination / 'FINDINGS_SUMMARY.md': summary_markdown(),
    }
    for path, content in files.items():
        path.write_text(content, encoding='utf-8')
    comparisons = {
        evidence / 'chosen_price_comparison.csv': chosen_price_rows(params, test_price),
        evidence / 'model_risk.csv': model_risk_rows(params),
    }
    for path, rows in comparisons.items():
        with path.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return tuple(files) + tuple(comparisons)


def main():
    for path in write_reports(Path(__file__).resolve().parent):
        print(f'Generated {path.relative_to(Path(__file__).resolve().parent)} from the current model calculations.')


if __name__ == '__main__':
    main()
