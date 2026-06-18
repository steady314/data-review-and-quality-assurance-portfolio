# QuickClean Data Validator

A lightweight command-line tool for catching common data quality issues — duplicates, missing values, and inconsistent formatting — in CSV files before they reach a report, dashboard, or database.

> **Note:** This README is a writing sample included in this portfolio to demonstrate documentation style. It describes a tool modeled closely on `validate_data.py` in the Data Validation Project folder of this repository.

## Why This Exists

Most data quality problems are caught too late — after a report has already gone out with double-counted rows, or a mail merge has bounced because of malformed email addresses. QuickClean is meant to run *before* that point, as a five-second check anyone can run on a CSV file without needing to know Python or write their own validation logic.

## What It Checks

- **Duplicates** — exact duplicate rows, plus a "possible duplicate" flag for records that look like the same person or item entered more than once with different formatting.
- **Missing values** — a per-column count and percentage of blank cells.
- **Formatting inconsistencies** — mixed date formats, mixed phone number formats, malformed email addresses, and inconsistent text casing.

## Installation

```bash
git clone https://github.com/your-username/quickclean-validator.git
cd quickclean-validator
pip install -r requirements.txt
```

Requires Python 3.8 or later. No external dependencies are needed beyond the standard library for the core checks.

## Usage

```bash
python validate_data.py path/to/your_file.csv
```

This prints a summary to the console and writes a detailed, row-level issue log (`validation_issues_log.csv`) in the same folder, which lists every flagged row along with the specific issue found — useful for handing off to whoever owns the data for correction.

### Example Output

```
[1] Exact duplicate rows: 12 affected customer_id(s)
[2] Possible near-duplicate people: 8 group(s)
[3] Missing values by column:
    phone: 11 missing (2.2%)
[4] Formatting inconsistencies:
    Date formats found: {'MM/DD/YYYY': 239, 'YYYY-MM-DD': 121}
```

## What This Tool Does Not Do

QuickClean flags issues — it does not automatically fix them. Deciding whether two near-duplicate records are actually the same person, or whether a missing value should be treated as zero or as "unknown," requires human judgment. The tool is designed to make that judgment faster by surfacing exactly where to look, not to replace it.

## Contributing

Issues and pull requests are welcome. If you're adding a new check, please include a short note in the README's "What It Checks" section describing what it catches and why it matters.

## License

This project is provided as a portfolio writing sample and is not a published package.
