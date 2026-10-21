# Proposal · class-packs

- **Status:** open
- **Estimate item:** Drop-ins and class packs
- **Estimated days:** 7
- **Actual days:** —
- **Opened:** 2026-10-12
- **Archived on:** —

## Why

Packs are tracked on a spreadsheet and paid in cash or by transfer. Members
should buy them by card in a minute, and the front desk should never count
credits by hand again.

## What changes

- Drop-in, pack of 5 and pack of 10, bought with Stripe Checkout.
- Credits added by the Stripe webhook, with an expiry date per pack.
- The front desk refunds a purchase and adjusts credits with a reason.

## Specs touched

- `specs/payments.md`: new module.

## Depends on

- `booking-rules`, for spending credits.

## Out of this change

- Monthly memberships: second release.
