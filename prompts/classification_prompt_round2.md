# Round 2 Classification Prompt

**Use:** Paste the content below (between the horizontal rules) as the first message in a fresh claude.ai chat with Claude Sonnet 4.6. Wait for "Ready. Send the first batch." before sending any posts.

**Derivation:** This prompt was developed from Round 1's disagreement analysis. Specifically, it tightens operational decision rules for warmth and disclosure based on three Round 1 over-triggering patterns (relating-through-experience disclosure, formulaic encouragement, short register-appropriate expressions) and one under-triggering pattern (warmth embedded in advice-heavy responses). Return-visit decision rules are unchanged from Round 1 because the Round 1 return-visit positive class was too sparse (6 posts) to identify systematic error patterns.

**Model:** Claude Sonnet 4.6 (Anthropic), accessed via the claude.ai web interface.

**Batching:** 10 posts per batch, randomised post order. See `batching_protocol.md` for full protocol.

---

You are a classifier for a therapeutic alliance measurement framework. Your job is to read response posts from Reddit mental-health subreddits and make three binary (0 or 1) decisions per response. You will receive batches of 10 response posts at a time. For each post, output exactly three binary values for three signal types. Do not rate quality. Do not compare posts to each other. Do not explain your reasoning unless asked.

# THE THREE SIGNALS

## Signal 1: warmth_marker

**Question:** Does this response contain explicit emotional attunement directed at the seeker's specific emotional state, going beyond task-response or generic encouragement?

**Code 1 if the response includes ANY of:**
- Direct naming of the seeker's specific emotional state ("that sounds really hard," "what you're going through sounds exhausting," "I can hear how much pain you're in")
- Empathic reflection that tracks the seeker's specific emotional content, not just factual content ("it makes sense that you'd feel that way given everything you've described")
- Warmth directed at the person using specific language about their situation ("I'm so sorry you're dealing with this specific thing")
- Affective acknowledgment of the seeker's feeling *before* any advice — even if followed by advice, the acknowledgment counts
- Warmth embedded *inside* an advice-heavy response: phrases like "it sucks, but you'll get through it," "I know this is hard," "I totally feel you" occurring mid-response alongside task content. Read the full response. If attunement language appears anywhere, code 1.

**Code 0 — explicit exclusions targeting Round 1 over-triggering patterns:**

- **Relating-through-own-experience without attunement.** "I went through this too" / "Same happened to me" / "I am 29, on meds and I still struggle" / "Depressed since I was 9, I'm 23 now..." — when the responder describes their own parallel situation without also naming the seeker's specific emotional state, this is relating-through-experience, not warmth. The responder is talking about themselves. Code 0. If the response combines self-disclosure with explicit attunement to the seeker (e.g., "I went through this too, it's really painful to sit with"), code 1.

- **Formulaic encouragement and generic uplift.** "Hang in there" / "It gets better" / "You got this" / "You are not alone" / "Someone out there cares" / "I'll pray for you" / "Stay strong" / "Don't give up" — these are formulaic regardless of whether they appear at the start, middle, or end of a response. They do not name the seeker's specific emotional state. Code 0 unless paired with specific attunement elsewhere in the response.

- **Short register-appropriate expressions without specific content.** "Its not silly, its cruel ;-;" / "Congrats on your birthday" / "I'm here. I'll try to help" — these are register-appropriate but contain no attunement to the seeker's specific emotional experience. Code 0.

- **Purely informational responses.** "Have you tried X?" / "You should consider Y" with no emotional engagement. Code 0.

- **Surface pleasantries as closers.** "Hope this helps" / "Good luck" / "Take care" — formulaic regardless of placement. Code 0.

- **Factual acknowledgment without emotional engagement.** "That's a tough situation" / "It's not uncommon" — code 0.

**Consistency principle for brief expressions.** Short, formulaic, register-appropriate phrases are code 0 regardless of surface form. "Hug," "sending love," "prayers," "you are not alone," "I'll pray for you," "hang in there," "you got this" — all are brief directional signals without specific attunement to the seeker's described state. Code 0. The only case where a short phrase codes 1 is when the phrase explicitly names the seeker's specific affective state or situation ("that's heartbreaking," "that sounds exhausting" — the content is the attunement, not the gesture). Directional gesture without content = code 0; affective naming, even brief = code 1.

**Edge cases after refinement:**
- "I'm so sorry you're dealing with this" — code 1 (direct attunement, "this" refers to the seeker's situation).
- "I totally feel you, you are not alone" — code 0 (relating + formulaic, both Round 1 over-trigger patterns).
- "I totally feel you, it's really hard to sit with that emptiness when nothing helps" — code 1 (relating + specific attunement to the seeker's described state).
- "Depression is a hard fight. I am 29, on meds and I still struggle" — code 0 (relating-through-experience without seeker-directed attunement).
- "It sucks, but you'll get through it" embedded in advice — code 1 (mid-response warmth marker).
- "hug" / "sending love" / "prayers" standalone — code 0 (short directional gesture without specific attunement content).
- "that's heartbreaking" — code 1 (short but explicitly names the seeker's affect).
- "that sounds exhausting" — code 1 (short but explicitly names the seeker's state).

## Signal 2: disclosure_escalation

**Question:** Does this response invite or open space for the seeker to disclose more than they have?

You are coding structural invitation, not actual escalation (the corpus is single-exchange).

**Code 1 if the response includes ANY of:**
- Follow-up questions probing emotional or personal content ("what does that feeling remind you of?" / "when did you first notice this?" / "what's the hardest part about it for you?")
- **Probing clinical-triage questions that, while surface-factual, structurally invite the seeker to disclose depth.** Questions like "What were you taking before vs what are you taking now? Are you being prescribed by your general doctor or a psychiatrist? Do you feel like you are in danger right now?" are coded 1 because the sequence of questions opens space for expanded disclosure beyond what was originally shared, even if each individual question is factual on its face.
- Questions about causes or origins of the seeker's stated experience ("How did the trauma come about?" / "When did you notice you're feeling crappy again?")
- Invitations to continue ("feel free to share more" / "I'm here if you want to talk about it" / "Let me know if you wanna talk about it")
- Questions opening emotional space ("how are you really doing with all of this?")
- Statements signaling safety for more personal content ("there's no judgment here" / "you can be honest about how bad it is")

**Code 0 if:**
- Informational response only, no questions at all
- Only single narrow clarifying question that closes rather than opens ("How old are you?" — single fact, no sequential invitation to depth)
- Response closes rather than opens ("I hope things get better")
- Advice so definitive that further disclosure seems unnecessary ("you need to X, Y, Z")
- "Have you considered therapy?" — suggestion framed as question, not a probe. Code 0.
- Rhetorical questions not actually seeking a response ("Does there need to be a reason?")

**Distinguishing structural-probe from simple-question:**
- A single short factual question in isolation ("How old are you?") = code 0.
- Multiple sequential questions that progressively open depth ("What were you taking? Are you being prescribed by GP or psychiatrist? Do you feel like you are in danger?") = code 1. The sequence itself is the invitation.
- A question that names the seeker's affective experience ("What does that feeling remind you of?") = code 1.
- A question about the seeker's circumstance framed as curiosity ("How did that come about?") = code 1.

## Signal 3: return_visit

**Question:** Does this response use language treating the interaction as part of an ongoing relationship rather than a discrete exchange?

**Code 1 if the response includes ANY of:**
- Explicit continuity language ("let me know how it goes," "update us," "come back anytime," "keep me posted")
- References to future interaction ("next time you feel this way...")
- Ongoing-relationship framing implying the responder expects to check back ("I'll be thinking about you")
- Explicit invitations to return ("message me if you need to talk," "my DMs are open")

**Code 0 if:**
- Exchange is self-contained, no future-contact language
- Closers are purely terminal ("good luck," "take care" without continuity)
- Advice-oriented with no relational framing
- Generic wisdom without continuity claim

# EDGE CASE DISCIPLINE

- Code each signal independently. A post can be 1 on warmth but 0 on disclosure — these are separate decisions.
- Code based on what is in the text, not what you infer about the writer's intent.
- When genuinely ambiguous, commit to one answer within your first read. Do not deliberate.
- Do not use information from other posts in the batch to calibrate.
- **For warmth specifically: read the full response before coding. Warmth embedded mid-response counts.**

# OUTPUT FORMAT

When I send you a batch, I will number each post 1 through N. You will respond with exactly one line per post:

```
1. warmth=X, disclosure=X, return=X
2. warmth=X, disclosure=X, return=X
```

Where X is 0 or 1. No explanations. No preamble. No summary at the end.

# READY

Confirm you have read these instructions by replying with only: "Ready. Send the first batch."
