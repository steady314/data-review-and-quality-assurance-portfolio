"""
categorize.py
--------------
Sorts uncategorized text samples (text_samples_raw.csv) into one of eight
topic categories using a rule-based keyword matching approach.

Why rule-based (not a trained ML model)?
For a batch of short, single-topic samples like this, a transparent
keyword approach is easier to audit and explain than a black-box model —
every assignment can be traced back to exactly which words triggered it.
See METHODOLOGY.md for the full rationale and limitations.

Usage:
    python categorize.py text_samples_raw.csv categorized_samples.csv
"""

import csv
import re
import sys

# Keyword sets per category. Order matters: a sample is scored against every
# category and assigned to whichever has the most keyword matches.
CATEGORY_KEYWORDS = {
    "Technology": ["smartphone","laptop","cloud","wearable","software","chip","app","browser",
                   "battery","camera","security flaw","processing speed","data sync","voice recognition",
                   "storage","developers","open-source","update"],
    "Health": ["study","doctors","treatment","clinical trial","symptoms","hospitals","nutritionists",
               "diet","exercise","disease","diabetes","flu","blood pressure","fatigue","anxiety",
               "joint pain","insomnia","sleep"],
    "Business & Finance": ["earnings","shares","stock","investors","merger","jobs","revenue","profit",
                            "quarterly","forecast","price target","subscriber growth","consumer spending",
                            "central bank","analysts"],
    "Sports": ["scored","lineup","playoffs","contract extension","coach","championship","ticket sales",
               "player of the week","victory","rivals","injuries"],
    "Entertainment": ["film","album","streaming","video game","documentary","novel","musical",
                       "animated","trailer","soundtrack","award nominations","director","singer",
                       "studio","showrunner","comedian"],
    "Politics": ["lawmakers","bill","election","voters","funding","budget hearing","governor",
                 "legislature","poll","protesters","negotiations","council","regulatory"],
    "Science": ["astronomers","telescope","researchers","peer-reviewed","scientists","field study",
                "research groups","funding for","breakthrough","gene variant","fossil","gravitational",
                "atmospheric"],
    "Travel": ["tourism","airlines","routes","travelers","guide","hiking trails","resorts",
               "museums","guided tours","national parks","promenades","visit","destination"],
}


def score_text(text, keywords):
    text_lower = text.lower()
    score = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            score += 1
    return score


def categorize(text):
    scores = {cat: score_text(text, kws) for cat, kws in CATEGORY_KEYWORDS.items()}
    best_cat = max(scores, key=scores.get)
    best_score = scores[best_cat]
    if best_score == 0:
        return "Uncategorized", 0
    return best_cat, best_score


def main(in_path, out_path):
    with open(in_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    results = []
    for r in rows:
        category, confidence = categorize(r["text"])
        results.append({
            "sample_id": r["sample_id"],
            "text": r["text"],
            "predicted_category": category,
            "keyword_match_count": confidence,
        })

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id", "text", "predicted_category", "keyword_match_count"])
        writer.writeheader()
        writer.writerows(results)

    uncategorized = sum(1 for r in results if r["predicted_category"] == "Uncategorized")
    low_confidence = sum(1 for r in results if r["keyword_match_count"] == 1)
    print(f"Categorized {len(results)} samples.")
    print(f"Uncategorized (no keyword match): {uncategorized}")
    print(f"Low-confidence assignments (exactly 1 keyword match): {low_confidence}")
    print(f"Output written to: {out_path}")


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "text_samples_raw.csv"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "categorized_samples.csv"
    main(in_file, out_file)
