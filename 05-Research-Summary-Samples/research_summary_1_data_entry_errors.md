# Research Summary: Common Causes of Data Entry Errors

*This is an original summary written for portfolio purposes, synthesizing general, widely-known concepts in data quality rather than quoting or paraphrasing any single source.*

## Overview

Data entry errors are among the most common — and most preventable — causes of poor data quality in organizations of every size. Understanding where these errors typically originate helps teams decide where to focus prevention efforts, rather than treating every dataset as equally risky.

## Key Sources of Error

**Manual transcription.** Whenever a person copies information from one place to another — from a paper form into a spreadsheet, or from one system into another — there's an opportunity for transposed digits, mistyped names, or skipped fields. This is one of the oldest and best-documented sources of data error, and it scales with volume: the more records a person enters by hand, the more likely a small percentage of them will contain a mistake.

**Inconsistent formatting standards.** When there's no agreed-upon format for dates, phone numbers, or categorical labels, different people (or even the same person on different days) will enter the same kind of information in different ways. Individually, each entry might be "correct," but the inconsistency makes the dataset as a whole harder to search, sort, and aggregate.

**Copy-paste and duplication errors.** Duplicate records often aren't caused by careless typing — they happen when a record is imported twice, when a form is submitted twice due to a slow page load, or when two different systems contribute overlapping data without a shared unique identifier to catch the overlap.

**Ambiguous or missing validation rules.** Many entry errors are technically allowed by the system collecting the data. If a form field accepts any text, nothing stops someone from typing a state abbreviation in lowercase, or leaving an optional field blank that should have been required. The error isn't really a typing mistake — it's a gap in the rules the system enforces.

## Why This Matters for Review Work

Recognizing these categories matters because they call for different prevention strategies. Transcription errors are best caught by automated validation checks (format and range checks) rather than by asking people to type more carefully. Formatting inconsistencies are best solved upstream, with dropdown menus or input masks that don't allow free-form entry in the first place. Duplication is best caught with a uniqueness check, while validation gaps require revisiting the rules of the data collection system itself, not just cleaning the data after the fact.

## Takeaway

Most data entry errors are not random — they cluster around a small number of structural causes. A review process that treats every error the same way (just "fix it and move on") misses the opportunity to address the upstream cause, which is the difference between cleaning a dataset once and preventing the same errors from reappearing in the next one.
