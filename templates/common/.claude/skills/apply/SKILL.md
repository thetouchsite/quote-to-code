---
name: apply
description: Implements a change already proposed in changes/<name>/ by following tasks.md, one task at a time, with a test for every scenario, ticking what is done. Use it when someone asks to «build», «implement», «carry on with» an existing change.
---

# Apply

Build what the change says, nothing more. If the work needs to step outside the
proposal, stop and say so. Reports to the user follow the project language
(`lang` in `.projectgen.json`).

## Before starting

1. If no name is given, run `python tools/changes.py list` and ask which.
2. Read the whole change: `proposal.md`, `design.md`, `specs/`, `tasks.md`.
   Then the current specs of the modules touched and the code involved.
3. In `proposal.md` set **Status** to `in progress` (`in corso`).

## The loop, for each task

1. Take the first unticked task.
2. Implement it following the conventions of the existing code (names,
   structure, comments) and the ADRs.
3. Write or update the tests: every scenario in the change's specs becomes at
   least one test.
4. Run the tests and the project's type check or linter. If they fail, fix
   before moving on.
5. Only then tick the task in `tasks.md` (`- [x]`).

Work in order. If you discover a missing task, add it at the right place in
`tasks.md` and mention it in the report.

## When to stop and ask

- A choice not covered by `design.md` that changes data, permissions or APIs.
- A requirement that, once built, turns out ambiguous or contradictory.
- The work is clearly exceeding the estimated days: say so as soon as you see
  it, with an estimate of what is left, not at the end.
- A module the change does not name needs to be touched.

In those cases update proposal or design only after the user answers.

## At the end

When every task is ticked, set **Status** to `to verify` (`da verificare`) and
reply with: what was done, the tests run and their result, tasks added along
the way, departures from the design, and the next step: `/verify <name>`.

No commits or pushes: the user does them. Do not touch `specs/` outside the
change: it is updated when archiving.
