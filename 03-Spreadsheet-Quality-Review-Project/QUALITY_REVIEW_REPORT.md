# Spreadsheet Quality Review Report

**File reviewed:** `inventory_data_raw.xlsx` (sheet: "Inventory")
**Rows reviewed:** 61 (60 unique product entries + 1 duplicate row)
**Columns:** SKU, Product Name, Category, Warehouse, Unit Price, Quantity On Hand, Reorder Level, Last Restock Date

## 1. Summary

This is a quality review of a sample inventory tracking spreadsheet. The review checks for the kinds of issues that commonly slip into spreadsheets maintained by hand or pulled together from multiple sources: duplicate or reused identifiers, missing values, inconsistent data types within a column, inconsistent text formatting, and values that are technically present but logically implausible (e.g., a negative quantity).

| Issue | Count |
|---|---|
| Duplicate / reused SKU values | 2 SKUs affected (`SKU-1002`, `SKU-1004`) |
| Missing values | 3 cells (1 each in Unit Price, Quantity On Hand, Last Restock Date) |
| Negative quantity on hand | 1 row |
| Price stored as text instead of a number | 1 row |
| Inconsistent category capitalization / naming | 3 rows |
| Inconsistent date formatting | 2 rows |
| Likely data-entry outlier (price) | 1 row |

## 2. Detailed Findings

### 2.1 Duplicate / Reused SKU
`SKU-1002` appears twice — once correctly assigned to "Mechanical Keyboard" and once incorrectly assigned to "Phone Tripod." This is a data integrity issue, not a cosmetic one: a SKU is supposed to be a unique identifier, so any system using this sheet to look up a product by SKU would retrieve the wrong item for one of these two rows. `SKU-1004` also appears as an exact duplicate row (same product, same data, repeated). **Recommendation:** assign the Phone Tripod a new, unused SKU, and delete the exact duplicate row for `SKU-1004` after confirming with the source system which entry is current.

### 2.2 Missing Values
One row each is missing a Unit Price, a Quantity On Hand, and a Last Restock Date. None of these should be left blank in an inventory system — a blank quantity is especially risky because it could be misread by downstream tools as zero, falsely suggesting an item is out of stock. **Recommendation:** treat blanks as "unknown," not "zero," and route them to whoever last touched that SKU for confirmation before they're used in any reporting.

### 2.3 Negative Quantity
One row shows a Quantity On Hand of **-8**. Inventory counts cannot be negative; this typically indicates an unreconciled adjustment (e.g., a sale recorded against stock that was already at zero) rather than a literal count. **Recommendation:** flag for inventory reconciliation rather than correcting the number directly, since the right fix depends on what actually happened in the warehouse.

### 2.4 Price Stored as Text
One Unit Price value is stored as the text string `"$45.00"` rather than a numeric value, while every other row stores a plain number (e.g., `45.00`). Spreadsheet formulas like `SUM()` or `AVERAGE()` will silently skip a text-formatted cell, which would quietly under-count this product in any price total or average calculation. **Recommendation:** strip the currency symbol and re-enter as a number, and apply currency *number formatting* (not literal `$` characters) so the column stays consistent and formula-compatible.

### 2.5 Inconsistent Category Values
The Category column contains six distinct values where only three categories actually exist: `Electronics`, `Accessories`, and `Office` appear correctly, but `electronics` (lowercase), `OFFICE` (all caps), and `Electronic ` (singular, with a trailing space) also appear. Because spreadsheet filters and pivot tables typically treat these as different categories, any category-level summary built from this column right now would incorrectly show up to six categories instead of three. **Recommendation:** normalize all category text to a single consistent casing and spelling, and consider replacing the free-text column with a dropdown (data validation list) to prevent this from recurring.

### 2.6 Inconsistent Date Formatting
Most `Last Restock Date` values follow `MM/DD/YYYY` (e.g., `04/26/2025`), but two rows use different formats: `2025-03-14` (ISO format) and `14-Mar-2025` (day-month-name-year). Mixed date formats in one column risk being misread — `03/14/2025` and `14-Mar-2025` represent the same date, but a formula or a person skimming the sheet could easily misinterpret the day/month order on the inconsistent rows. **Recommendation:** reformat the entire column to one standard date format and apply Excel's actual Date type/format rather than storing dates as text, so date math and sorting work correctly.

### 2.7 Likely Outlier / Data-Entry Typo
One row has a Unit Price of **$4,500.00** for a product (a desk accessory) where every comparable item in the sheet is priced under $200. This is very likely a misplaced decimal point (e.g., `$45.00` typed as `$4500.00`) rather than a real price. **Recommendation:** flag for confirmation with whoever entered the price rather than auto-correcting, since the review process cannot be certain whether this was a typo or a legitimately mispriced item.

## 3. Overall Assessment

None of the issues found are severe enough to make the dataset unusable, but several (the duplicate SKU, the text-formatted price, and the price outlier) would silently distort any totals, averages, or lookups run directly against this sheet without cleanup first. The issues cluster into two risk tiers: **data integrity risks** (duplicate SKU, negative quantity, price outlier) that need human confirmation before correction, and **formatting consistency risks** (category casing, date formats, price as text) that can be safely standardized using find-and-replace or a cleaning script without needing to ask anyone what the "right" value should be.

## 4. Suggested Process Improvement

To prevent these issues going forward: apply Excel data validation (dropdown lists) to the Category and Warehouse columns, format the Unit Price and Last Restock Date columns with explicit Number/Date types rather than allowing free text entry, and add a simple uniqueness check on the SKU column (conditional formatting to highlight duplicates) so a reused SKU is visible immediately rather than discovered later during a review like this one.
