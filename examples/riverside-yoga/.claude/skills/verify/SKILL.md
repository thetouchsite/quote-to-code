---
name: verify
description: Checks that a change in changes/<name>/ is really done — every requirement implemented, every scenario covered by a passing test, tasks ticked, no work outside the proposal — and gives a verdict listing what is missing. Use it after /apply and before /archive, or when someone asks whether a change is ready.
---

# Verify

You are the reviewer, not the author: you look for what is missing. You do not
fix anything during verification; you list. Report in the project language
(`lang` in `.projectgen.json`).

## Checks

1. **Format**: `python tools/changes.py check <name>`.
2. **Tasks**: all ticked, and each one leaves a trace in the code.
3. **Requirements and scenarios**: for each requirement in
   `changes/<name>/specs/`
   - where it is implemented (file and function);
   - which test covers each scenario, and that the test really checks the THEN,
     not just that the code runs.
4. **Tests**: run the project's whole suite, not only the new tests.
5. **Permissions and data**: if the change touches data or roles, a test tries
   the access that must NOT succeed.
6. **Scope**: the code changed does nothing the proposal does not say. Extra
   work is flagged: it either enters the proposal or goes.
7. **Documents**: ADRs written for contestable choices; `docs/technical/`
   updated if architecture or data model changed.

## Verdict

Reply with a table requirement → scenario → test → result, then one of three
verdicts:

- **Ready**: it can be archived. Remind the user to give the actual days for
  `/archive <name>`.
- **Almost**: small gaps, listed; they close with `/apply <name>`.
- **Not ready**: substantial gaps; set **Status** back to `in progress`.

Each gap says where (file, requirement, scenario) and what is needed. Quote the
output of failing tests, not a summary.
