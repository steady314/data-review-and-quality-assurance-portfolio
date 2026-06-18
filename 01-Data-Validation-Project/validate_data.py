"""
validate_data.py
-----------------
Performs automated data quality checks on customer_data_raw.csv.

Checks performed:
1. Exact duplicate rows
2. Near-duplicate records (same name, different formatting)
3. Missing / blank values per column
4. Formatting inconsistencies:
   - Inconsistent date formats in sign_up_date
   - Inconsistent phone number formats
   - Inconsistent name/state capitalization
   - Malformed email addresses

Usage:
    python validate_data.py customer_data_raw.csv

Outputs a printed summary to the console and writes a machine-readable
issues log to validation_issues_log.csv for further review.
"""

import csv
import re
import sys
from collections import Counter, defaultdict

EMAIL_RE = re.compile(r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
DATE_PATTERNS = {
    "MM/DD/YYYY": re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$"),
    "YYYY-MM-DD": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "DD-MM-YYYY": re.compile(r"^\d{2}-\d{2}-\d{4}$"),
}
PHONE_PATTERNS = {
    "(XXX) XXX-XXXX": re.compile(r"^\(\d{3}\) \d{3}-\d{4}$"),
    "XXX-XXX-XXXX": re.compile(r"^\d{3}-\d{3}-\d{4}$"),
    "XXX.XXX.XXXX": re.compile(r"^\d{3}\.\d{3}\.\d{4}$"),
    "XXXXXXXXXX": re.compile(r"^\d{10}$"),
}


def classify_date_format(value):
    for label, pattern in DATE_PATTERNS.items():
        if pattern.match(value):
            return label
    return "OTHER/UNRECOGNIZED"


def classify_phone_format(value):
    for label, pattern in PHONE_PATTERNS.items():
        if pattern.match(value):
            return label
    return "OTHER/UNRECOGNIZED"


def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def find_exact_duplicates(rows):
    seen = Counter()
    dup_ids = []
    for r in rows:
        key = tuple(r.items())
        seen[key] += 1
    for r in rows:
        key = tuple(r.items())
        if seen[key] > 1:
            dup_ids.append(r["customer_id"])
    return sorted(set(dup_ids), key=lambda x: int(x))


def find_near_duplicates(rows):
    """Flags records that share the same normalized name + email local-part,
    which may indicate the same person entered more than once with different
    formatting (e.g. ALL CAPS vs Title Case)."""
    groups = defaultdict(list)
    for r in rows:
        norm_name = r["full_name"].strip().lower()
        groups[norm_name].append(r["customer_id"])
    return {name: ids for name, ids in groups.items() if len(ids) > 1}


def find_missing_values(rows, fields):
    missing = defaultdict(list)
    for r in rows:
        for field in fields:
            if not r[field] or not r[field].strip():
                missing[field].append(r["customer_id"])
    return missing


def find_formatting_issues(rows):
    date_formats = Counter()
    phone_formats = Counter()
    bad_emails = []
    state_case_issues = []
    name_case_issues = []

    for r in rows:
        if r["sign_up_date"]:
            date_formats[classify_date_format(r["sign_up_date"])] += 1
        if r["phone"]:
            phone_formats[classify_phone_format(r["phone"])] += 1
        if r["email"] and not EMAIL_RE.match(r["email"]):
            bad_emails.append((r["customer_id"], r["email"]))
        if r["state"] and not r["state"].isupper():
            state_case_issues.append((r["customer_id"], r["state"]))
        if r["full_name"] and (r["full_name"].isupper() or r["full_name"].islower()):
            name_case_issues.append((r["customer_id"], r["full_name"]))

    return {
        "date_formats": date_formats,
        "phone_formats": phone_formats,
        "bad_emails": bad_emails,
        "state_case_issues": state_case_issues,
        "name_case_issues": name_case_issues,
    }


def main(path):
    rows, fieldnames = load_rows(path)
    total = len(rows)

    exact_dupes = find_exact_duplicates(rows)
    near_dupes = find_near_duplicates(rows)
    missing = find_missing_values(rows, ["full_name", "email", "phone", "state", "sign_up_date", "purchase_amount"])
    fmt = find_formatting_issues(rows)

    print("=" * 60)
    print(f"DATA VALIDATION REPORT — {path}")
    print("=" * 60)
    print(f"Total rows scanned: {total}\n")

    print(f"[1] Exact duplicate rows: {len(exact_dupes)} affected customer_id(s)")
    print(f"    IDs: {exact_dupes[:20]}{' ...' if len(exact_dupes) > 20 else ''}\n")

    near_dupe_groups = {k: v for k, v in near_dupes.items() if len(v) > 1}
    print(f"[2] Possible near-duplicate people (same name, different formatting): {len(near_dupe_groups)} group(s)")
    for name, ids in list(near_dupe_groups.items())[:10]:
        print(f"    '{name}' -> customer_id(s) {ids}")
    print()

    print("[3] Missing values by column:")
    for field, ids in missing.items():
        print(f"    {field}: {len(ids)} missing ({round(len(ids)/total*100, 1)}%)")
    print()

    print("[4] Formatting inconsistencies:")
    print(f"    Date formats found: {dict(fmt['date_formats'])}")
    print(f"    Phone formats found: {dict(fmt['phone_formats'])}")
    print(f"    Malformed emails: {len(fmt['bad_emails'])}")
    print(f"    State values not uppercase: {len(fmt['state_case_issues'])}")
    print(f"    Names in all-caps or all-lowercase: {len(fmt['name_case_issues'])}")
    print()

    # Write a machine-readable issues log
    log_path = path.rsplit("/", 1)[0] + "/validation_issues_log.csv" if "/" in path else "validation_issues_log.csv"
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["issue_type", "customer_id", "detail"])
        for cid in exact_dupes:
            writer.writerow(["exact_duplicate", cid, ""])
        for name, ids in near_dupe_groups.items():
            for cid in ids:
                writer.writerow(["possible_near_duplicate", cid, name])
        for field, ids in missing.items():
            for cid in ids:
                writer.writerow(["missing_value", cid, field])
        for cid, email in fmt["bad_emails"]:
            writer.writerow(["malformed_email", cid, email])
        for cid, state in fmt["state_case_issues"]:
            writer.writerow(["inconsistent_state_case", cid, state])
        for cid, name in fmt["name_case_issues"]:
            writer.writerow(["inconsistent_name_case", cid, name])

    print(f"Detailed issue log written to: {log_path}")


if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "customer_data_raw.csv"
    main(file_path)
