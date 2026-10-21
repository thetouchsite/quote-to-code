---
name: archive
description: Closes a verified change — merges its added, modified and removed requirements into specs/, records the actual days and moves the folder to changes/archive/ with the date. Use it when a change is finished and verified and someone asks to «close», «archive», «consolidate» it.
---

# Archive

The specs become the new truth and the change goes to the archive. Write in the
project language (`lang` in `.projectgen.json`).

## 1 · Before touching anything

- The change must have **Status** `to verify` (`da verificare`) and a «Ready»
  verdict from `/verify`. If not, ask the user whether to verify first.
- You need the **actual days**. Ask the user if you do not have them: the
  effective work of everyone on the change, in days. Never invent them or copy
  the estimate.

## 2 · Merge the specs

For each file `changes/<name>/specs/<module>.md`, update
`specs/<module>.md` (create it, with a title and a «Purpose» / «Scopo»
section, if missing):

- **added**: at the end of the requirements section, as they are;
- **modified**: replace the whole requirement with the same title, scenarios
  included. If the title is not found, stop and ask;
- **removed**: delete the requirement with that title.

Do not rewrite requirements the change does not touch.

## 3 · Days and archive

1. In `proposal.md` write the actual days (`- **Actual days:** N` or
   `- **Giornate reali:** N`).
2. `python tools/changes.py check` (all specs and changes): fix until clean.
3. `python tools/changes.py archive <name>`: the script sets status and date
   and moves the folder to `changes/archive/YYYY-MM-DD-<name>/`.

## 4 · Hand-over

Reply with: the requirements added, changed and removed in `specs/`, estimated
and actual days with the gap, the archive folder. If the gap exceeds 20%, ask
in one line for the main reason and write it at the end of the archived
`proposal.md`, under `## Actuals` (`## Consuntivo`): `/close-project` uses it.

No commits: the user does them.
