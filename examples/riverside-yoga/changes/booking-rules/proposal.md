# Proposal · booking-rules

- **Status:** in progress
- **Estimate item:** Booking and cancellation rules
- **Estimated days:** 6
- **Actual days:** —
- **Opened:** 2026-10-09
- **Archived on:** —

## Why

Bookings on WhatsApp mean double bookings and no-shows nobody pays for. The
studio's rule — free cancellation up to 12 hours before, then the credit is
lost — only works if the system applies it the same way every time.

## What changes

- Members book a session from the schedule, spending one credit.
- Members cancel: refunded more than 12 hours before, not refunded after.
- After class, bookings without check-in become no-shows.
- **The schedule's «spots left» now counts real bookings** instead of the
  test data used so far.

## Specs touched

- `specs/bookings.md`: new module.

## Depends on

- `weekly-schedule` (archived).
- Credits come from `class-packs`; until it is archived, tests use credits
  added by hand.

## Out of this change

- Paying for credits: `class-packs`.
- Waiting list: second release.
