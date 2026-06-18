# Methodology — Content Categorization Project

## 1. Task

Sort 560 short text samples (`text_samples_raw.csv`) into one of eight topic categories: Technology, Health, Business & Finance, Sports, Entertainment, Politics, Science, and Travel. No labels were provided in the input file — categorization had to be performed from the text content alone.

## 2. Approach: Rule-Based Keyword Matching

A keyword-matching classifier (`categorize.py`) was used instead of a trained machine-learning model, for two reasons relevant to a quality-assurance context:

1. **Auditability.** Every category assignment can be traced back to the exact keyword(s) that triggered it. This matters in QA work — when something is miscategorized, the reviewer needs to know *why*, not just that a model produced a probability score.
2. **No training data required.** A keyword approach can be deployed and corrected immediately by editing a keyword list, which is realistic for a small, fast-turnaround content-sorting task.

For each sample, the script counts how many keywords from each category's list appear in the text and assigns the category with the highest match count. If no keywords matched at all, the sample is labeled `Uncategorized` rather than being forced into a category, so that low-information samples are surfaced for manual review instead of silently guessed.

## 3. Keyword List Construction

Keyword lists were built by reading a sample of text from each category and extracting words and short phrases that were distinctive to that topic (e.g., "earnings," "shares," and "merger" for Business & Finance; "telescope," "researchers," and "peer-reviewed" for Science). Care was taken to avoid generic words that could plausibly appear across multiple categories (e.g., "new," "announced").

## 4. Known Limitations

- **Overlapping vocabulary.** Some categories share vocabulary in edge cases — for example, a sentence about science *funding* can be misread as a Politics story if it contains a phrase like "funding for," since government funding is also a Politics keyword. This is a real limitation of keyword matching and is visible in the accuracy report.
- **No context understanding.** The classifier cannot use sentence structure or context, only the presence of words. A sentence with zero matching keywords is marked `Uncategorized` even if a human would obviously be able to categorize it.
- **Keyword list quality determines accuracy.** This approach is only as good as the keyword lists behind it. Expanding or refining the lists based on the accuracy report's misclassification examples is the primary way to improve results — see `ACCURACY_REPORT.md`.

## 5. Process Summary

1. Generate / receive uncategorized text samples (`text_samples_raw.csv`).
2. Run `categorize.py` to produce `categorized_samples.csv` with a `predicted_category` and `keyword_match_count` (a simple confidence signal) per row.
3. Run `accuracy_check.py` against a held-out answer key to measure overall and per-category accuracy.
4. Review misclassified examples and low-confidence rows (`keyword_match_count` of 0 or 1) manually, and use them to refine the keyword lists.
5. Re-run and re-check until accuracy is acceptable for the use case.

This mirrors a realistic QA workflow: automate the bulk of the sorting, then focus human review time specifically on the cases the automated method is least confident about, rather than re-checking everything.
