# Bookings and credits

The part that must never be wrong: a spot sold twice, a credit spent twice or a
late cancellation refunded costs the studio money and trust. In the estimate:
booking and cancellation rules **6 + 1** days, drop-ins and class packs
**7 + 0**, waiting list **0 + 3**.

## The credits ledger

Credits are not a number on the member's profile. They are a **ledger**: every
change is a row, and the balance is the sum.

| Entry | Amount | Example |
| --- | --- | --- |
| `purchase` | +1, +5, +10 | pack of 10 bought on 3 October, expires 3 February |
| `booking` | −1 | Tuesday 18:30 Vinyasa |
| `refund` | +1 | cancelled 20 hours before |
| `adjustment` | ± n | front desk, with a mandatory reason |
| `expiry` | − remaining | the job closes expired packs at night |

Why a ledger: the front desk can always answer «why do I have 3 credits?», the
import from the spreadsheet is just a set of `adjustment` rows, and reports are
sums over the same table.

**Which credit is spent.** The one that expires first (first expiring, first
used), so members never lose credits they could have used.

## Booking rules

All enforced in `book_session` and `cancel_booking`, SQL functions running as
the member, inside one transaction with the session row locked:

- the session is not cancelled and starts in the future;
- bookings are open (from 14 days before to 30 minutes before the start —
  values in `studio_settings`, editable by the owner);
- there is a free spot: `count(active bookings) < room capacity`;
- the member has a valid credit (or, from the second release, an active
  membership);
- the member is not already booked on that session.

Cancellation:

- **more than 12 hours before**: booking cancelled, `refund +1`;
- **12 hours or less**: booking cancelled, no refund (the policy text says so
  at the moment of booking);
- **no-show**: the job after class marks bookings without check-in as
  `no_show`; nothing to refund, the credit was spent at booking.

The UI mirrors these rules to show friendly messages, but the database is the
judge: a call that skips the UI gets the same answer.

## Waiting list (second release)

- A member can join the waiting list of a full session, without spending a
  credit.
- When a spot frees up, `promote_waitlist` gives it to the first in line
  **who still has a valid credit**, spends it, and emails them.
- Closer than 2 hours to the start, nobody is promoted automatically: people
  would not see the email in time. The spot stays open for direct booking.
- A promoted member who cancels follows the normal 12-hour rule; if the
  promotion happened inside 12 hours, the cancellation is refunded (it was not
  their choice to be booked late).

## Tests that must exist

- two members booking the last spot at the same time: exactly one succeeds;
- cancellation at 12 h 01 m and at 11 h 59 m before the start;
- a pack expiring the day of the class;
- a webhook delivered twice adds credits once (idempotency on the Stripe event id);
- an instructor cannot see bookings of another instructor's class.
