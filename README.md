# CAS Phase 1 Pilot

This repository contains the Phase 1 pilot data and analysis reported in Section 9.2 of:

**Shah, A. (2026).** *Conditional Activation of Clinical Alliance Rubrics for Evaluating AI Affective Interactions*. arXiv preprint [cs.CY].

[Preprint link will go here once live.]

---

## What this repository contains

```
cas-pilot/
├── README.md
├── LICENSE
├── .gitignore
├── analyze.py                                          Analysis script
├── prompts/
│   ├── classification_prompt_round1.md                Round 1 classifier instructions
│   ├── classification_prompt_round2.md                Round 2 refined prompt
│   └── batching_protocol.md                           Classification protocol
└── data/
    ├── epitome_pilot_human_labels.csv                 Human ground truth (N=99)
    ├── epitome_pilot_classifier_labels.csv            Round 1 classifier output
    ├── epitome_pilot_classifier_labels_round2.csv     Round 2 classifier output
    ├── combined_results_table.csv                     Canonical per-signal per-round results
    ├── disagreements.csv                              Round 1 human-classifier disagreements
    └── flipped_rpids.csv                              R1-to-R2 classification changes
```

---

## What the pilot tested

Three Bond-pillar signals from the Conditional Activation framework were coded on 99 response posts from the EPITOME emotional-reactions Reddit subset (Sharma et al. 2020):

1. **Warmth markers** — explicit emotional attunement to the seeker's specific state
2. **Disclosure escalation invitation** — structural invitation to deeper disclosure
3. **Return-visit language** — ongoing-relationship framing

Each signal was coded as binary (0/1). A single human rater (the author) produced the ground truth. Claude Sonnet 4.6 served as the Stage 1 classifier across two rounds: a baseline Round 1, and a refined Round 2 prompt targeting Round 1's observed error patterns.

**Headline finding** (reproduced from Section 9.2.2 of the paper):

| Signal | R1 κ | R2 κ | Δκ | R1 F1 | R2 F1 | ΔF1 |
|---|---|---|---|---|---|---|
| Warmth markers | 0.529 | 0.581 | +0.052 | 0.655 | 0.647 | −0.008 |
| Disclosure escalation | 0.460 | 0.449 | −0.011 | 0.522 | 0.500 | −0.022 |
| Return-visit language | 0.353 | 0.519 | +0.166 | 0.400 | 0.545 | +0.145 |

F1 was essentially unchanged across rounds on warmth and disclosure; return-visit showed a Pareto improvement on a sparse positive class. The refinement shifted the classifier's operating point along the precision–recall frontier but did not move the frontier itself. Section 9.2 of the preprint presents the full frontier-framed interpretation.

---

## How to reproduce the analysis

### If you already have Python installed

Open a terminal in this repository and run:

```
python analyze.py
```

The script prints all Section 9.2 numerical results to the console and writes reproduced copies of the canonical CSVs to `data/reproduced/`. Running time: under 2 seconds.

**Dependencies:** `numpy`, `pandas`, and `scikit-learn`. If any are missing, install with:

```
pip install numpy pandas scikit-learn
```

### If you don't have Python installed

The full canonical results are in `data/combined_results_table.csv` and `data/flipped_rpids.csv`. You can inspect these directly without running anything. The paper's Section 9.2.2 tables are direct transcriptions of `combined_results_table.csv`.

### Verifying reproducibility

After running `analyze.py`, compare:

- `data/reproduced/combined_results_table_reproduced.csv` against `data/combined_results_table.csv`
- `data/reproduced/flipped_rpids_reproduced.csv` against `data/flipped_rpids.csv`

These should match exactly — the analysis is fully deterministic given the three input label CSVs.

---

## How the classification itself was run (for re-running pilot or Phase 1)

The classification was conducted via the claude.ai web interface, not via API. Steps:

1. Open a fresh claude.ai chat with Claude Sonnet 4.6 selected.
2. Paste the full content of `prompts/classification_prompt_round1.md` (for Round 1) or `prompts/classification_prompt_round2.md` (for Round 2) as the first message.
3. Wait for the classifier's "Ready. Send the first batch." reply.
4. Send response posts in batches of ten following the protocol in `prompts/batching_protocol.md`.
5. Collect outputs in the format specified by the prompt.

Note that the claude.ai web interface does not expose decoding parameters (temperature, seed, sampling strategy) to the user. The classification was conducted with whatever inference settings Anthropic's backend specified at the time. This is a reproducibility constraint noted as a limitation in Section 10 of the preprint.

---

## Author context

This repository is released alongside a methods-paper preprint. The author (Aryan Shah) designed the Conditional Activation framework, wrote the signal taxonomy, developed the classification prompts, coded the human ground truth, executed the two-round classification protocol, and conducted the analysis. The author does not come from a software-engineering background and is shipping this repository as research material rather than as production software. The analysis code is intentionally simple and written to be read.

If you find issues with the code, with the classification prompts, or with the analysis, please open a GitHub issue on this repository.

---

## Citation

If you use or adapt the pilot data or analysis, please cite:

```
Shah, A. (2026). Conditional Activation of Clinical Alliance Rubrics for
Evaluating AI Affective Interactions. arXiv preprint [cs.CY]. [DOI pending]
```

Additionally, the underlying EPITOME corpus is:

```
Sharma, A., Miner, A. S., Atkins, D. C., & Althoff, T. (2020). A Computational
Approach to Understanding Empathy Expressed in Text-Based Mental Health Support.
Proceedings of the 2020 Conference on Empirical Methods in Natural Language
Processing (EMNLP), 5263–5276.
```

Please cite EPITOME when using its data.

---

## License

MIT License for the analysis code and prompts. See `LICENSE` file for full terms. EPITOME corpus data is reused under its own licensing terms — the rp_id identifiers and derived labels are shared here; the underlying post text is not redistributed in this repo and must be obtained directly from the EPITOME authors' release.
