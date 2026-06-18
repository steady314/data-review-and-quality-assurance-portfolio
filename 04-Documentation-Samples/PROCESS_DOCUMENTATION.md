# Process Documentation: Data Quality Review Workflow

**Document type:** Standard Operating Procedure (SOP)
**Applies to:** Any incoming dataset (CSV or spreadsheet) prior to use in reporting, analysis, or system import.
**Owner role:** Data Quality Reviewer

## 1. Purpose

This document describes the end-to-end process for reviewing a new dataset before it is approved for downstream use. It exists so that data quality review is performed consistently, regardless of who on the team is doing it, and so that decisions about ambiguous issues (like a possible duplicate or an outlier value) are made the same way every time.

## 2. When This Process Applies

- A new dataset is received from an external source (vendor file, exported report, manual collection).
- An existing dataset has been substantially edited and needs re-review before reuse.
- A recurring dataset (e.g., a weekly export) is being reviewed as part of a scheduled check.

## 3. Process Steps

### Step 1 — Initial Intake
Record the source of the file, the date received, and the expected row/column structure. If the structure doesn't match what was expected (extra or missing columns), stop and confirm with the source before proceeding — don't attempt to reshape the file to fit assumptions.

### Step 2 — Automated Scan
Run the appropriate validation script (see `01-Data-Validation-Project/validate_data.py` for the CSV case) to produce an initial issue list covering duplicates, missing values, and formatting inconsistencies.

### Step 3 — Triage the Findings
Sort findings into two categories:

- **Auto-correctable:** issues with one unambiguous correct fix (e.g., standardizing date format, fixing text casing). These can be corrected directly and noted in the change log.
- **Needs human judgment:** issues where the "correct" answer depends on context the reviewer doesn't have (e.g., is this a true duplicate or two different people with the same name? Is this outlier a typo or a real value?). These are escalated per Step 4.

### Step 4 — Escalation
For anything needing human judgment, the reviewer documents the specific question and routes it to whoever owns the source data (not to whoever happens to be available). The dataset should not be marked "approved" while open escalations remain unresolved, even if the rest of the file is clean.

### Step 5 — Apply Corrections and Re-Scan
Once corrections are made (directly for auto-correctable issues, or based on the source owner's answer for escalated ones), re-run the automated scan on the corrected file to confirm the fixes worked and didn't introduce new issues.

### Step 6 — Sign-Off
The reviewer records: the date of final review, the number of issues found and resolved, any issues that were knowingly left unresolved (with a reason), and a final approval status.

## 4. Change Log Requirements

Every correction made to a dataset during review should be logged with: what was changed, why, and who approved it (for escalated items). This is not optional — a dataset that has been silently edited without a record of what changed is itself a data quality risk, even if the edits were correct.

## 5. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Data Quality Reviewer | Runs the scan, triages findings, applies auto-correctable fixes, tracks escalations |
| Source Data Owner | Answers escalated questions about ambiguous records (duplicates, outliers, missing values) |
| Requester / Downstream User | Confirms the expected file structure at intake; is notified if sign-off is delayed due to unresolved escalations |

## 6. Related Documents

- `01-Data-Validation-Project/VALIDATION_REPORT.md` — example output of Steps 2–3 applied to a sample dataset
- `03-Spreadsheet-Quality-Review-Project/QUALITY_REVIEW_REPORT.md` — example output of this process applied to a spreadsheet rather than a CSV
- `04-Documentation-Samples/STEP_BY_STEP_GUIDE.md` — the detailed how-to for Step 2 of this process
