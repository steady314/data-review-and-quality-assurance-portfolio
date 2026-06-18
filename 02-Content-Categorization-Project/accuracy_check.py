"""
accuracy_check.py
------------------
Scores categorize.py's output against the held-out answer key and produces
both an overall accuracy figure and a per-category breakdown, plus a random
manual-review sample for spot-checking (mirroring how a QA reviewer would
sample-audit a categorization job rather than only trusting the aggregate
metric).

Usage:
    python accuracy_check.py categorized_samples.csv answer_key_for_accuracy_check.csv
"""

import csv
import random
import sys
from collections import defaultdict

random.seed(11)


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(pred_path, key_path):
    predictions = {r["sample_id"]: r for r in load_csv(pred_path)}
    answer_key = {r["sample_id"]: r["true_category"] for r in load_csv(key_path)}

    total = 0
    correct = 0
    per_category_total = defaultdict(int)
    per_category_correct = defaultdict(int)
    misses = []

    for sample_id, true_cat in answer_key.items():
        pred_row = predictions.get(sample_id)
        if not pred_row:
            continue
        total += 1
        per_category_total[true_cat] += 1
        predicted_cat = pred_row["predicted_category"]
        if predicted_cat == true_cat:
            correct += 1
            per_category_correct[true_cat] += 1
        else:
            misses.append((sample_id, pred_row["text"], true_cat, predicted_cat))

    overall_accuracy = correct / total * 100 if total else 0

    print("=" * 60)
    print("ACCURACY CHECK")
    print("=" * 60)
    print(f"Total samples scored: {total}")
    print(f"Correct: {correct}")
    print(f"Overall accuracy: {overall_accuracy:.1f}%\n")

    print("Per-category accuracy:")
    for cat in sorted(per_category_total):
        c = per_category_correct[cat]
        t = per_category_total[cat]
        print(f"  {cat:20s} {c}/{t}  ({c/t*100:.1f}%)")

    print(f"\nMisclassified samples: {len(misses)}")
    print("Examples of misclassifications (up to 8):")
    for sample_id, text, true_cat, predicted_cat in misses[:8]:
        print(f"  [{sample_id}] true={true_cat} | predicted={predicted_cat} | \"{text}\"")

    # Random manual-review sample, regardless of correctness — simulates a
    # human QA spot-check rather than relying solely on the automated score.
    sample_ids = list(answer_key.keys())
    spot_check = random.sample(sample_ids, 20)
    print("\n20-sample manual spot-check set (for human review):")
    for sid in spot_check:
        pred_row = predictions.get(sid, {})
        print(f"  [{sid}] predicted={pred_row.get('predicted_category')} | true={answer_key[sid]} | \"{pred_row.get('text')}\"")


if __name__ == "__main__":
    pred_file = sys.argv[1] if len(sys.argv) > 1 else "categorized_samples.csv"
    key_file = sys.argv[2] if len(sys.argv) > 2 else "answer_key_for_accuracy_check.csv"
    main(pred_file, key_file)
