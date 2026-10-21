# 0002 · Stripe for packs and memberships, credits in our own ledger

**Status:** accepted · 21 September 2026

## Context

The studio sells drop-ins and packs of 5 or 10 classes now, and monthly
memberships later. Credits must expire, be refunded on early cancellation and
be adjusted by the front desk.

## Decision

- **Stripe Checkout** for one-off purchases, **Stripe Billing** for
  memberships, with the customer portal for card changes and cancellation.
- Stripe is the source of truth for **money**; our `credit_ledger` is the
  source of truth for **credits**. A webhook links them, idempotent on the
  Stripe event id.
- Prices live in Stripe and are mirrored in `products`.

## Consequences

- No card data on our side; receipts and refunds handled by Stripe.
- Fees: about 1.5% + €0.25 per European card, about 0.7% more on
  subscriptions.
- Credits logic (expiry, refunds, adjustments) is ours and fully tested; it
  does not depend on Stripe features.
- If the studio changes payment provider, only the webhook and checkout code
  change.
