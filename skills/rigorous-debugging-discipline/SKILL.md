---
name: rigorous-debugging-discipline
description: General practices for investigating hard-to-localize bugs in scientific and numerical code, where a wrong-but-plausible answer is easy to produce and hard to notice. Use when chasing an intermittent or hard-to-reproduce failure, investigating unexpected numerical or physical behavior with several plausible explanations, or any debugging effort likely to span multiple sessions.
---

# Rigorous Debugging Discipline

General practices for investigating hard-to-localize bugs — especially in
scientific/numerical code, where a wrong-but-plausible answer is easy to
produce and hard to notice.

## When to use

- Chasing an intermittent or hard-to-reproduce failure (crashes only under
  specific conditions, "mostly" works)
- Investigating unexpected numerical/physical behavior where several
  plausible-sounding explanations exist and need to be told apart
- Any debugging effort likely to span multiple sessions, where a written
  trail matters as much as the eventual fix

## Core practices

1. **"Ran longer" is not "fixed."** An intervention that delays a failure
   without changing the underlying mechanism will look like progress right
   up until it doesn't. Keep pushing past the point where things start
   looking better before calling something resolved.
2. **Use an independent reference as ground truth when one exists.**
   Comparing actual computed values between two implementations of the same
   method finds bugs that reading either code base in isolation misses.
   Prefer numeric diffs over "does this look right" code review.
3. **Build disposable, single-purpose diagnostics instead of guessing at
   fixes.** When the easy explanations are exhausted, the productive move is
   to build a narrow tool that lets you see the specific quantity in
   question, not to try another plausible-sounding change. These tools do
   not need to be reusable — build one, get the answer, move on.
4. **Treat surprising diagnostic results as suspects, not witnesses.**
   Before building further conclusions on a dramatic or convenient number,
   reproduce it a second, independent way (hand calculation, a different
   tool, raw data instead of a derived compute). A result striking enough
   to explain everything is also striking enough to be a bug in the
   measurement — check before it testifies against anything else.
5. **Design tests so the intervention has a genuine chance to fail.**
   Verify the timing of a mitigation, not just its mechanism — an
   intervention that activates after the failure window has usually
   already passed was never actually tested, no matter how reasonable it
   sounds. "Inconclusive" often means "never actually exercised," not
   "doesn't work."
6. **Log every experiment as it happens, including the wrong ones.**
   A record that only keeps what turned out to be true is far less useful
   than one that also shows what was believed, tested, and rejected —
   the reasoning trail is what lets a false lead be told apart from a real
   result later, by you or anyone else.
7. **Chase root cause past the first working workaround.** Confirming a
   diagnosis by removing/disabling the offending component is a legitimate
   result, but it's not the same as understanding it. Keep asking "why"
   one layer further down until the chain terminates at something
   specific and fixable, not just avoidable.

## Rules

- Never treat a diagnostic tool's own output as ground truth without
  cross-checking it at least once, especially when the result is dramatic
  or conveniently explains everything.
- A negative or inconclusive result is still a finding — record it with
  the same rigor as a positive one, including *why* it was inconclusive
  (e.g. a mistimed test) so it isn't silently re-litigated later.
- When correcting an earlier claim, mark the correction in place
  (strike-through, explicit "IMPORTANT CORRECTION" note) rather than
  silently deleting or rewriting it — preserve the reasoning trail for
  future readers, including future-you.
- When a root cause is found, fix it at its actual source, not only at the
  nearest point where a patch is cheap — and add a regression test that
  encodes the specific failure mode, so it can't silently recur.
