# Step-by-Step Guide: Running a Data Quality Check on a New CSV File

This guide walks through the process used in the Data Validation Project of this portfolio, written so that someone with basic command-line familiarity but no Python background could follow it without getting stuck.

## Before You Start

You will need:
- The CSV file you want to check
- Python 3.8 or later installed on your computer
- The `validate_data.py` script (included in `01-Data-Validation-Project/`)

## Step 1: Open a Terminal in the Project Folder

Navigate to the folder containing both your CSV file and `validate_data.py`.

```bash
cd path/to/01-Data-Validation-Project
```

If you're not sure where the folder is, you can drag the folder into the terminal window on most operating systems and it will fill in the path automatically.

## Step 2: Confirm Python Is Installed

```bash
python --version
```

You should see something like `Python 3.11.4`. If you instead see an error like "command not found," try `python3 --version` instead — some systems use that name.

## Step 3: Run the Validation Script

```bash
python validate_data.py your_file.csv
```

Replace `your_file.csv` with the actual name of the file you're checking. If your file has spaces in the name, put quotes around it: `"my data file.csv"`.

## Step 4: Read the Console Summary

The script will print a summary directly in the terminal, organized into four sections:

1. Exact duplicate rows
2. Possible near-duplicate records
3. Missing values, by column
4. Formatting inconsistencies (dates, phone numbers, emails, capitalization)

Each section tells you how many rows are affected, so you can quickly judge whether the file needs cleanup before you use it.

## Step 5: Open the Detailed Issue Log

The script also creates a file called `validation_issues_log.csv` in the same folder. Open it in Excel, Google Sheets, or any text editor. Each row lists one specific issue: which record it affects, what kind of issue it is, and any relevant detail (for example, which column was blank, or what the malformed value looked like).

## Step 6: Decide What to Fix vs. What to Flag

Not every issue should be auto-corrected. As a rule of thumb used throughout this portfolio:

- **Safe to standardize directly:** formatting issues like inconsistent date formats, phone number formats, or text casing — these have one obviously correct fix.
- **Needs a human decision first:** anything involving duplicates, missing values, or unusually large/small numbers — these require knowing *why* the data looks that way, which the script can't determine on its own.

## Step 7: Re-run After Cleanup

Once changes have been made to the CSV file, run the script again on the cleaned version to confirm the flagged issues are resolved and that the cleanup didn't introduce new ones.

```bash
python validate_data.py your_file_cleaned.csv
```

## Troubleshooting

| Problem | Likely Cause |
|---|---|
| "FileNotFoundError" | The CSV filename was typed incorrectly, or you're not in the right folder. |
| Script runs but finds 0 issues on a file you know has problems | Check that the column names in your file exactly match what the script expects (see the script's header comments). |
| Output looks garbled with strange characters | The file may be saved in a different text encoding; try re-saving it as UTF-8 CSV from your spreadsheet program. |
