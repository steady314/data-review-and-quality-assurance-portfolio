# Data Validation Report

**Dataset:** `customer_data_raw.csv`
**Rows scanned:** 500
**Tool used:** `validate_data.py` (Python, standard library only — `csv`, `re`, `collections`)

## 1. Purpose

This report documents a data quality audit of a synthetic customer dataset. The dataset was deliberately seeded with common real-world data entry problems so that the detection script could be tested against known issues. The goal of the exercise is to demonstrate a repeatable process for finding duplicates, missing values, and formatting inconsistencies before data is used for analysis or reporting.

## 2. Summary of Findings

| Issue type | Count | % of dataset |
|---|---|---|
| Exact duplicate rows | 12 records | 2.4% |
| Possible near-duplicate people (same name, different casing) | 128 name groups flagged | — |
| Missing phone numbers | 11 | 2.2% |
| Missing purchase amounts | 14 | 2.8% |
| Missing state values | 8 | 1.6% |
| Missing email addresses | 5 | 1.0% |
| Malformed email addresses | 25 | 5.0% |
| State values not uppercase | 29 | 5.8% |
| Names in ALL CAPS or all lowercase | 92 | 18.4% |

## 3. Detailed Findings

### 3.1 Exact Duplicates
Twelve `customer_id` values had fully identical rows (every field matched another row exactly). These are byte-for-byte duplicate entries, most likely caused by a record being submitted or imported twice. Recommended action: remove all but one copy of each duplicate, keeping the earliest `customer_id`.

### 3.2 Near-Duplicate Records
The script also flags customers whose *normalized* name (lowercased, whitespace-trimmed) matches another customer's name. This caught real near-duplicates created intentionally for this test (e.g., the same person entered once in Title Case and once in ALL CAPS). However, this check produced a meaningful number of **false positives** — for example, several different real people can legitimately share a common name like "Charles Jones." In a production setting, name-matching alone is not sufficient; it should be combined with a second identifier (e.g., matching email or phone number) before merging or deleting records. This limitation is intentionally included in this writeup because flagging false-positive risk is itself part of a thorough quality review.

### 3.3 Missing Values
Four columns had blank values: `phone`, `purchase_amount`, `state`, and `email`. None exceeded 3% of total rows, which suggests the missingness is closer to random data entry gaps than a systemic collection failure. Recommended action: for `purchase_amount`, missing values should not be assumed to be zero — they should be flagged for follow-up rather than imputed, since the cause (no purchase vs. unrecorded purchase) cannot be determined from the data alone.

### 3.4 Formatting Inconsistencies
- **Dates:** Three different date formats were present in `sign_up_date` (`MM/DD/YYYY`, `YYYY-MM-DD`, `DD-MM-YYYY`), which is a problem because `03-04-2024` is ambiguous between March 4th and April 3rd depending on the format assumed. This should be standardized to a single ISO format (`YYYY-MM-DD`) before any downstream analysis.
- **Phone numbers:** Four different formatting styles were found. None are "wrong" individually, but inconsistent formatting makes deduplication and search harder. Recommended standard: strip to digits only and re-apply one consistent display format.
- **Emails:** 25 emails failed basic structural validation (e.g., `"sandra.moore at company.com"` instead of using the `@` symbol), which would cause any automated email send to bounce.
- **Capitalization:** ~18% of names and ~6% of state codes were not in the expected case (Title Case for names, uppercase for two-letter state codes). This is a low-risk but common cosmetic issue that should be normalized for consistent display and accurate grouping.

## 4. Recommended Remediation Steps

1. Deduplicate exact-match rows, keeping the first occurrence.
2. Manually review near-duplicate name groups using a secondary identifier (email or phone) before merging.
3. Standardize all dates to `YYYY-MM-DD`.
4. Strip and re-format all phone numbers to one pattern.
5. Re-validate all emails against a standard regex and flag bounced/invalid addresses for manual correction.
6. Normalize text casing for `full_name` (Title Case) and `state` (uppercase).
7. Leave missing `purchase_amount` values as null/blank rather than imputing, and flag them for manual follow-up.

## 5. How to Reproduce

```bash
python validate_data.py customer_data_raw.csv
```

This prints a console summary and writes `validation_issues_log.csv`, a row-level log of every flagged issue with the affected `customer_id`, suitable for handing off to a data-cleaning step or a human reviewer.
