# Specs

What the system does **today**, module by module: one file per module
(`bookings.md`, `payments.md`…). The source of truth for developers and for the
AI. It changes only by archiving a change (`/archive`), never by hand in the
middle of the work.

## Format

```markdown
# Spec · Bookings

## Purpose

One or two sentences: what the module is for and for whom.

## Requirements

### Requirement: Class capacity
The system SHALL refuse a booking when the class is full.

#### Scenario: Last spot taken
- **WHEN** a member books a class whose last spot was just taken
- **THEN** the booking is refused
- **AND** the member is offered the waiting list
```

Rules, checked by `python tools/changes.py check`:

- every requirement has a title and uses **SHALL** or **MUST** (or their
  negative forms);
- every requirement has at least one **scenario** with **WHEN** and **THEN**
  (**AND** for extra conditions or outcomes);
- a scenario is verifiable: it becomes a test.

No implementation details here (table names, libraries): they belong in
`docs/technical/` and in the `design.md` of changes.
