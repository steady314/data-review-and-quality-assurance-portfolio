# Accuracy Report — Content Categorization Project

## 1. Overall Result

| Metric | Value |
|---|---|
| Total samples scored | 560 |
| Correctly categorized | 518 |
| **Overall accuracy** | **92.5%** |
| Uncategorized (no keyword match) | 22 (3.9%) |
| Low-confidence assignments (exactly 1 keyword match) | 185 (33.0%) |

## 2. Per-Category Accuracy

| Category | Correct / Total | Accuracy |
|---|---|---|
| Technology | 70 / 70 | 100.0% |
| Health | 70 / 70 | 100.0% |
| Entertainment | 70 / 70 | 100.0% |
| Politics | 67 / 70 | 95.7% |
| Travel | 67 / 70 | 95.7% |
| Sports | 60 / 70 | 85.7% |
| Business & Finance | 57 / 70 | 81.4% |
| Science | 57 / 70 | 81.4% |

## 3. Where Accuracy Dropped, and Why

**Business & Finance** and **Science** were the weakest categories. Reviewing the misclassified rows showed a consistent pattern: several samples used phrases like *"funding for [science topic] research"*, which triggered the Politics keyword "funding" instead of any Science keyword, since the sentence didn't happen to contain a stronger Science-specific term. Similarly, a Business & Finance sentence about the real estate industry's "export volume" had no exact keyword match and was left `Uncategorized` rather than misclassified — a safer failure mode, but still a miss.

**Sports** had two recurring misses: sentences like *"Fans were disappointed after [Team] lost to [Team] at home"* matched zero sports-specific keywords (no word like "scored," "playoffs," or "coach" was present) and instead picked up a stray match elsewhere, illustrating that a sentence can be obviously about sports to a human reader while containing none of the literal keywords the script was looking for.

## 4. Manual Spot-Check

In addition to scoring against the full answer key, a random 20-sample set was pulled for manual human-style review (see console output of `accuracy_check.py`, "20-sample manual spot-check set"). This step matters because aggregate accuracy can hide patterns — a manual spot-check is how a reviewer would catch, for example, a category that always looks fine in the metric but has a subtle, repeated misjudgment. All 20 spot-checked samples in this run matched the answer key, which is consistent with the high overall accuracy score.

## 5. Recommended Next Steps

1. Add keywords like "lost," "won," "home game," and "fans" to the Sports list to catch result-recap style sentences.
2. Add "research funding," "grant," and "study funding" as Science-specific funding phrases so they outscore the generic Politics "funding" keyword.
3. For any sample landing in `Uncategorized`, route it to a short manual review queue rather than guessing — this affected 3.9% of the batch here and is a safer failure mode than a wrong guess.
4. Track `keyword_match_count` over time; if the proportion of low-confidence (1-keyword) assignments grows on new data, it's a signal the keyword lists need to be revisited before trusting the categorization output for reporting.
