---
name: explore
description: Thinks through an idea, a problem or a question about the project by reading code, specs and technical documents, without changing anything. Use it when someone wants to understand how a part works, weigh options before a change, or asks «how would we…», «is it worth…», «where is…».
---

# Explore

You think with the user before building. **You do not write or edit files**:
no code, no specs, no changes. If something needs doing in the end, you propose
it and hand over to `/propose`.

Answer in the project language (`lang` in `.projectgen.json`), unless the user
writes in another one.

## What you read

In this order, only what the question needs:

1. `specs/` — what the system does today;
2. `changes/` — what is already in progress (`python tools/changes.py list`),
   so you do not propose a duplicate;
3. `docs/technical/` and `docs/technical/adr/` — how it is built and why;
4. the code, when the question is about how it really works.

## How you answer

- The answer first, then the reasoning.
- With several options: at most three, each with cost in days, risk and what it
  leaves out. Say which you recommend and why.
- If the question touches the scope agreed with the client (an item of
  `docs/estimate/estimate.py`), say whether it is in or out of the estimate:
  out of estimate means a change request, and sales decides.
- If specs, documents and code contradict each other, say so.

End with one line only: «Next: `/propose <suggested-name>`», when going ahead
makes sense.
