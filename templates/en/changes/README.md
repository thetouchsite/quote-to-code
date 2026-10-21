# Changes

Every piece of work on the system — a new module, an important fix, a change of
rules — is a **change**: a folder that says why, what changes in the specs, how
it is done and how far along it is.

```text
changes/
  class-booking/            an open change
    proposal.md             why, what changes, estimate item, days
    design.md               technical choices (optional)
    tasks.md                the checklist
    specs/
      bookings.md           added, modified, removed requirements
  archive/
    2026-11-13-schedule/    finished changes, with the date
  _template/                the skeleton of a new change
```

## The cycle

| Step | Command in Claude Code | What happens |
| --- | --- | --- |
| Understand | `/explore` | Reads code and specs, weighs options, writes nothing |
| Propose | `/propose <name>` | Opens the change: proposal, specs touched, design, tasks |
| Build | `/apply <name>` | Implements tasks one by one and ticks them |
| Verify | `/verify <name>` | Checks code and tests against the scenarios |
| Close | `/archive <name>` | Updates `specs/`, records actual days, archives |

The mechanical part (folders, dates, counts, format) is done by `tools/changes.py`:

```sh
python tools/changes.py list       # what is open and how far along
python tools/changes.py actuals    # estimated vs actual days
```

## Specs inside a change

A change's `specs/<module>.md` contains only the differences:

```markdown
## Added requirements

### Requirement: …
The system SHALL …

#### Scenario: …
- **WHEN** …
- **THEN** …

## Modified requirements

### Requirement: <title identical to the one in specs/>
The full new text, with all its scenarios.

## Removed requirements

### Requirement: <title>
Why it goes.
```

## Days

`Estimated days` comes from `docs/estimate/estimate.py` (the item named in
`Estimate item`); `Actual days` is written when archiving. At the end of the
project `/close-project` compares them and updates the company's pricing file:
that is how the next estimates get better.
