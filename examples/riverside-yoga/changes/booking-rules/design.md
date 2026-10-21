# Design · booking-rules

## Context

Sessions and capacity exist (`weekly-schedule`). Credits will be a ledger
(`docs/technical/bookings-and-credits.md`). Several members may try to take the
last spot in the same second, typically on Sunday evening.

## Choices

| Choice | Alternatives rejected | Why |
| --- | --- | --- |
| `book_session` and `cancel_booking` as SQL functions, session row locked with `FOR UPDATE` | Check in the Next.js server, then insert | The check and the insert must be one transaction, or two people get the last spot |
| Credit spent at booking, refunded on early cancellation | Spend at check-in | Spending at check-in makes no-shows free, which is the problem to solve |
| Cancellation window in `studio_settings` (12 hours) | Hard-coded | The owner may change the policy without a release |

## Data

- `bookings` table with status, timestamps and the ledger entry it created.
- `studio_settings.cancellation_hours`, `booking_opens_days`, `booking_closes_minutes`.
- RLS: members insert and update bookings only through the two functions.

## Risks

- Time zones around daylight saving time: all times stored in UTC, the window
  computed in the studio's time zone; tests on the last Sunday of October.
