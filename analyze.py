"""
CAS Phase 1 Pilot Analysis (Section 9.2 of CAS v0.8.1)
=======================================================

Reproduces all numerical results reported in Section 9.2 of:
  Shah, A. (2026). Conditional Activation of Clinical Alliance Rubrics for
  Evaluating AI Affective Interactions. arXiv preprint [cs.CY].

Inputs (read from data/):
  - epitome_pilot_human_labels.csv              Ground truth (N = 99)
  - epitome_pilot_classifier_labels.csv         Round 1 classifier output
  - epitome_pilot_classifier_labels_round2.csv  Round 2 classifier output

For each of three Bond-pillar signals (warmth_marker, disclosure_escalation,
return_visit), this script computes:
  - Human positive rate, classifier positive rate
  - Observed agreement
  - Cohen's kappa (per Cohen 1960; Landis & Koch 1977 bands applied)
  - Precision, recall, F1 (treating human labels as ground truth)
  - Full 2x2 confusion matrix (TN, FP, FN, TP)
  - Round-over-round flip analysis: which specific rp_ids changed classification
    between R1 and R2, and whether each flip was good (toward agreement) or bad
    (away from agreement)

Outputs (written to data/reproduced/):
  - combined_results_table_reproduced.csv   One row per signal per round
  - flipped_rpids_reproduced.csv            All rp_ids that changed between R1 and R2

Usage:
  python analyze.py

Dependencies:
  numpy, pandas, scikit-learn

Reproducibility:
  The analysis is fully deterministic given the three input CSVs. Different
  runs on different machines produce identical outputs.
"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "reproduced")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------------
# Load labels
# -------------------------------------------------------------------

human = pd.read_csv(os.path.join(DATA_DIR, "epitome_pilot_human_labels.csv"))
r1    = pd.read_csv(os.path.join(DATA_DIR, "epitome_pilot_classifier_labels.csv"))
r2    = pd.read_csv(os.path.join(DATA_DIR, "epitome_pilot_classifier_labels_round2.csv"))

merged = human.merge(r1, on="rp_id", suffixes=("_human", "_r1")).merge(
    r2, on="rp_id"
)
# Rename the R2 columns (which came in without a suffix)
rename_map = {}
for sig in ["signal_warmth_marker", "signal_disclosure_escalation", "signal_returns_visit"]:
    rename_map[sig] = f"{sig}_r2"
merged = merged.rename(columns=rename_map)

assert len(merged) == 99, f"Expected 99 merged rows, got {len(merged)}"
print(f"Loaded and merged {len(merged)} rows of paired labels")
print()

# -------------------------------------------------------------------
# Analysis
# -------------------------------------------------------------------

SIGNALS = [
    "signal_warmth_marker",
    "signal_disclosure_escalation",
    "signal_returns_visit",
]
SIGNAL_NAMES = {
    "signal_warmth_marker":         "Warmth markers",
    "signal_disclosure_escalation": "Disclosure escalation",
    "signal_returns_visit":         "Return-visit language",
}


def landis_koch(kappa):
    """Interpret a Cohen's kappa value using Landis & Koch (1977) bands."""
    if kappa is None or pd.isna(kappa):
        return "undefined"
    if kappa < 0.00: return "worse than chance"
    if kappa < 0.20: return "slight"
    if kappa < 0.40: return "fair"
    if kappa < 0.60: return "moderate"
    if kappa < 0.80: return "substantial"
    return "almost perfect"


def compute_stats(h, c):
    """Given binary human and classifier arrays, return full stats dict."""
    n = len(h)
    h_pos = int(h.sum())
    c_pos = int(c.sum())
    agree = int((h == c).sum())
    agree_rate = agree / n
    kappa = cohen_kappa_score(h, c)
    cm = confusion_matrix(h, c, labels=[0, 1])
    tn, fp, fn, tp = (int(cm[0,0]), int(cm[0,1]), int(cm[1,0]), int(cm[1,1]))
    precision = tp / (tp + fp) if (tp + fp) > 0 else np.nan
    recall    = tp / (tp + fn) if (tp + fn) > 0 else np.nan
    if np.isnan(precision) or np.isnan(recall) or (precision + recall) == 0:
        f1 = np.nan
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return {
        "n": n,
        "h_pos": h_pos, "c_pos": c_pos,
        "h_rate": h_pos / n, "c_rate": c_pos / n,
        "agree": agree, "agree_rate": agree_rate,
        "kappa": kappa, "band": landis_koch(kappa),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
        "precision": precision, "recall": recall, "f1": f1,
    }


# -------------------------------------------------------------------
# Per-signal round-comparison
# -------------------------------------------------------------------

print("=" * 78)
print("ROUND 1 vs ROUND 2 COMPARISON")
print("=" * 78)

rows = []
for sig in SIGNALS:
    h = merged[f"{sig}_human"].values
    c_r1 = merged[f"{sig}_r1"].values
    c_r2 = merged[f"{sig}_r2"].values

    r1_stats = compute_stats(h, c_r1)
    r2_stats = compute_stats(h, c_r2)

    print()
    print(f"{SIGNAL_NAMES[sig]}")
    print(f"  Human positive rate: {r1_stats['h_rate']:.1%} ({r1_stats['h_pos']}/{r1_stats['n']})")
    print()
    print(f"  ROUND 1:  κ = {r1_stats['kappa']:.3f} [{r1_stats['band']}]"
          f"  |  Precision = {r1_stats['precision']:.3f}"
          f"  |  Recall = {r1_stats['recall']:.3f}"
          f"  |  F1 = {r1_stats['f1']:.3f}")
    print(f"            Classifier rate = {r1_stats['c_rate']:.1%}"
          f"  |  Confusion: TN={r1_stats['tn']} FP={r1_stats['fp']} FN={r1_stats['fn']} TP={r1_stats['tp']}")
    print()
    print(f"  ROUND 2:  κ = {r2_stats['kappa']:.3f} [{r2_stats['band']}]"
          f"  |  Precision = {r2_stats['precision']:.3f}"
          f"  |  Recall = {r2_stats['recall']:.3f}"
          f"  |  F1 = {r2_stats['f1']:.3f}")
    print(f"            Classifier rate = {r2_stats['c_rate']:.1%}"
          f"  |  Confusion: TN={r2_stats['tn']} FP={r2_stats['fp']} FN={r2_stats['fn']} TP={r2_stats['tp']}")
    print()
    print(f"  Deltas:   Δκ = {r2_stats['kappa'] - r1_stats['kappa']:+.3f}"
          f"  |  ΔPrecision = {r2_stats['precision'] - r1_stats['precision']:+.3f}"
          f"  |  ΔRecall = {r2_stats['recall'] - r1_stats['recall']:+.3f}"
          f"  |  ΔF1 = {r2_stats['f1'] - r1_stats['f1']:+.3f}")

    for round_name, stats in [("R1", r1_stats), ("R2", r2_stats)]:
        rows.append({
            "signal": SIGNAL_NAMES[sig],
            "round": round_name,
            "n": stats["n"],
            "human_positive_rate":      round(stats["h_rate"], 4),
            "classifier_positive_rate": round(stats["c_rate"], 4),
            "observed_agreement":       round(stats["agree_rate"], 4),
            "cohen_kappa":              round(stats["kappa"], 4),
            "landis_koch_band":         stats["band"],
            "precision":                round(stats["precision"], 4),
            "recall":                   round(stats["recall"], 4),
            "f1":                       round(stats["f1"], 4),
            "true_negatives":           stats["tn"],
            "false_positives":          stats["fp"],
            "false_negatives":          stats["fn"],
            "true_positives":           stats["tp"],
        })

pd.DataFrame(rows).to_csv(
    os.path.join(OUTPUT_DIR, "combined_results_table_reproduced.csv"),
    index=False,
)

# -------------------------------------------------------------------
# Flip analysis: which rp_ids changed between R1 and R2?
# -------------------------------------------------------------------

print()
print("=" * 78)
print("FLIP ANALYSIS (R1 to R2)")
print("=" * 78)

flip_rows = []
for sig in SIGNALS:
    h_col  = f"{sig}_human"
    r1_col = f"{sig}_r1"
    r2_col = f"{sig}_r2"

    flipped = merged[merged[r1_col] != merged[r2_col]].copy()

    corrected_fp = flipped[(flipped[h_col] == 0) & (flipped[r1_col] == 1) & (flipped[r2_col] == 0)]
    introduced_fn = flipped[(flipped[h_col] == 1) & (flipped[r1_col] == 1) & (flipped[r2_col] == 0)]
    corrected_fn = flipped[(flipped[h_col] == 1) & (flipped[r1_col] == 0) & (flipped[r2_col] == 1)]
    introduced_fp = flipped[(flipped[h_col] == 0) & (flipped[r1_col] == 0) & (flipped[r2_col] == 1)]

    net_toward_correctness = len(corrected_fp) + len(corrected_fn) - len(introduced_fn) - len(introduced_fp)

    print()
    print(f"{SIGNAL_NAMES[sig]}: {len(flipped)} total flips")
    print(f"  GOOD  (corrected FP, R1=1->R2=0 where human=0): {len(corrected_fp)}")
    print(f"  GOOD  (corrected FN, R1=0->R2=1 where human=1): {len(corrected_fn)}")
    print(f"  BAD   (introduced FN, R1=1->R2=0 where human=1): {len(introduced_fn)}")
    print(f"  BAD   (introduced FP, R1=0->R2=1 where human=0): {len(introduced_fp)}")
    print(f"  Net shift toward correctness: {net_toward_correctness}")

    for _, row in corrected_fp.iterrows():
        flip_rows.append({"signal": SIGNAL_NAMES[sig], "rp_id": row["rp_id"],
                          "human": row[h_col], "r1": row[r1_col], "r2": row[r2_col],
                          "flip_type": "corrected_fp", "direction": "good"})
    for _, row in introduced_fn.iterrows():
        flip_rows.append({"signal": SIGNAL_NAMES[sig], "rp_id": row["rp_id"],
                          "human": row[h_col], "r1": row[r1_col], "r2": row[r2_col],
                          "flip_type": "introduced_fn", "direction": "bad"})
    for _, row in corrected_fn.iterrows():
        flip_rows.append({"signal": SIGNAL_NAMES[sig], "rp_id": row["rp_id"],
                          "human": row[h_col], "r1": row[r1_col], "r2": row[r2_col],
                          "flip_type": "corrected_fn", "direction": "good"})
    for _, row in introduced_fp.iterrows():
        flip_rows.append({"signal": SIGNAL_NAMES[sig], "rp_id": row["rp_id"],
                          "human": row[h_col], "r1": row[r1_col], "r2": row[r2_col],
                          "flip_type": "introduced_fp", "direction": "bad"})

pd.DataFrame(flip_rows).to_csv(
    os.path.join(OUTPUT_DIR, "flipped_rpids_reproduced.csv"),
    index=False,
)

print()
print("=" * 78)
print("OUTPUTS WRITTEN")
print("=" * 78)
print(f"  {os.path.join(OUTPUT_DIR, 'combined_results_table_reproduced.csv')}")
print(f"  {os.path.join(OUTPUT_DIR, 'flipped_rpids_reproduced.csv')}")
print()
print("Compare these against the canonical data/combined_results_table.csv and")
print("data/flipped_rpids.csv for reproducibility verification. They should match.")
