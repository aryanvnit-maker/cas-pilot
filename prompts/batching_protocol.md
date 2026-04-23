# Batching Protocol — claude.ai Manual Classification Pipeline

## Setup (once, takes 5 minutes)

1. Open a fresh claude.ai chat. Use Claude Opus 4.7 (the default). Do not use Claude Haiku — it's cheaper but weaker on nuanced classification.
2. Paste the contents of `classification_prompt.md` as your first message.
3. Wait for the response "Ready. Send the first batch." If Claude responds with anything else, start over with a fresh chat — the prompt was misapplied.

## Batch format

You'll send 10 response posts per batch. Format each batch exactly like this:

```
Batch 1 of 10:

1. [paste response_post text for rp_id ABC123]

2. [paste response_post text for rp_id DEF456]

3. [paste response_post text for rp_id GHI789]

...

10. [paste response_post text for rp_id XYZ999]
```

Keep track separately (in a spreadsheet) which rp_id corresponds to positions 1-10 in each batch. Claude sees only numbered posts — it does not see rp_ids, and you don't want it to.

## What Claude returns

Claude should return exactly 10 lines:

```
1. warmth=0, disclosure=0, return=0
2. warmth=1, disclosure=0, return=0
3. warmth=0, disclosure=1, return=0
...
10. warmth=1, disclosure=0, return=1
```

If Claude returns anything else — explanations, preamble, a different format — reply with: "Please output only the structured format specified. Retry the batch." It should re-output correctly.

## Assembling the classifier CSV

Create a spreadsheet with columns:

```
rp_id | classifier_warmth | classifier_disclosure | classifier_return
```

For each batch, match Claude's numbered output back to the rp_ids you tracked in the batch. Enter the 0/1 values into the spreadsheet.

When all 99 posts are classified, save as `epitome_pilot_classifier_labels.csv` with the exact column names above.

## Batching strategy for 99 posts

- **10 batches of 10 posts each** = 100 posts. You have 99. Last batch is 9 posts.
- **Randomise batch order.** Don't feed posts in the order they appear in your CSV. Shuffle them. This prevents any ordering bias (e.g., Claude calibrating against earlier batches). A quick way: in your spreadsheet, add a column of random numbers, sort by that column, then batch sequentially.
- **One sitting if possible.** 99 classifications should take 30-45 minutes if you paste batches efficiently and Claude responds in under 30 seconds each.
- **If you split into two sittings, use the same chat.** Don't open a fresh chat for sitting 2 — Claude needs to maintain the classification discipline established in the prompt.

## Consistency checks while you work

After every 3 batches (30 posts), scan Claude's outputs for patterns that suggest drift:
- Is Claude coding warmth=1 on almost everything? Possible over-triggering. Check a few examples yourself.
- Is Claude coding disclosure=1 at much higher rates than your ~13% human rate? Possible prompt ambiguity on structural invitation vs literal question.
- If you see drift, you can send: "Reminder of coding discipline: warmth requires explicit emotional attunement beyond task-response. Re-read the last 10 and resubmit." But use this sparingly — too much interference corrupts the comparison.

## What you should NOT do

- **Don't show Claude your human labels.** Not even accidentally. Don't mention that you've already coded these. The classifier must be blind to your coding.
- **Don't ask Claude to "double-check" or "be more careful."** That modifies its behavior in ways your human coding was not modified. Keep the classification procedure identical to how you coded: first-pass, committed, no deliberation.
- **Don't re-classify a batch if you don't like the output.** Whatever Claude returns on first pass is the classifier output. Changing your mind and re-running biases the comparison.
- **Don't feed posts longer than about 1000 tokens in a single batch.** If a response_post is extremely long (multi-paragraph), it's fine, but keep a batch under ~4000 total tokens to stay within Claude's working context cleanly.

## When you finish

Send me both files:
1. `epitome_pilot_human_labels.csv` (your 99 coded rows — the file you already have)
2. `epitome_pilot_classifier_labels.csv` (the 99 Claude-classified rows)

I'll build the analysis harness in Python that:
- Joins the two files on rp_id
- Computes Cohen's κ per signal
- Produces a 2x2 confusion matrix per signal
- Identifies the specific rp_ids where human and classifier disagreed (the interesting cases)
- Outputs a results table suitable for inclusion in the v0.7 paper

## Time estimate

- Setup: 5 minutes
- Batching and classification: 30-45 minutes
- Assembly of classifier CSV: 10-15 minutes
- Total: ~60 minutes

## One honest note

Claude classifying Claude is a known methodological limitation. The paper should name this: "Phase 1 pilot used Claude Opus 4.7 as the Stage 1 classifier, which introduces potential self-preference bias when the framework is later applied to Claude outputs. Full Phase 1 validation should include classifier diversity (GPT-4, open-source models) to assess classifier-agnostic performance." This is an honest limitation to flag and does not undermine the pilot — it correctly sets up what full Phase 1 needs.
