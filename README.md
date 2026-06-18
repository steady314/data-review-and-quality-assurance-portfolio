# Data Review & Quality Assurance Portfolio

This repository is a portfolio of sample projects demonstrating core data review and quality assurance skills: catching duplicates, missing values, and formatting errors; categorizing unstructured text accurately and checking that accuracy; reviewing spreadsheets for data integrity issues; writing clear technical documentation; and summarizing information accurately in writing.

All datasets in this repository are **synthetic** — generated specifically for this portfolio, with errors deliberately seeded in so that the detection methods could be demonstrated and verified against a known answer. No real customer, company, or personal data is included anywhere in this repository.

## Repository Structure

### `01-Data-Validation-Project/`
A synthetic customer CSV dataset with intentional duplicates, missing values, and formatting inconsistencies, plus a Python script (`validate_data.py`) that detects all three categories of issues, and a written report of the findings.

### `02-Content-Categorization-Project/`
560 short text samples sorted into eight topic categories using a rule-based keyword classifier, with a documented methodology and an accuracy report scoring the categorization against a held-out answer key (92.5% overall accuracy).

### `03-Spreadsheet-Quality-Review-Project/`
An Excel inventory dataset with intentional errors (duplicate SKUs, missing values, inconsistent category formatting, a negative quantity, a price stored as text, and a likely data-entry typo), reviewed in a written quality-review report with specific, actionable recommendations.

### `04-Documentation-Samples/`
Three writing samples demonstrating different documentation styles: a project README, step-by-step user instructions, and a formal process document (SOP) for running a data quality review.

### `05-Research-Summary-Samples/`
Two short, original written summaries on data-quality-related topics, demonstrating the ability to synthesize a topic clearly and concisely in writing.

## How to Navigate This Repository

Each project folder is self-contained and includes its own report or methodology document explaining what was done and why. Start with the report or methodology file in any folder for the full context before looking at the raw data or code.

## Tools and Skills Demonstrated

- Python (`pandas`-free standard-library scripting for portability — no special setup required to run any script in this repo)
- CSV and Excel (`.xlsx`) data handling
- Rule-based text classification and accuracy measurement
- Spreadsheet auditing and data integrity review
- Technical writing: reports, methodology documents, step-by-step guides, and process documentation

## Running the Code

Each script can be run with no dependencies beyond the Python standard library:

```bash
cd 01-Data-Validation-Project
python validate_data.py customer_data_raw.csv

cd ../02-Content-Categorization-Project
python categorize.py text_samples_raw.csv categorized_samples.csv
python accuracy_check.py categorized_samples.csv answer_key_for_accuracy_check.csv
```

The spreadsheet in `03-Spreadsheet-Quality-Review-Project/` can be opened directly in Excel, Google Sheets, or LibreOffice — no script is required to review it, though the included report documents the full review process.
