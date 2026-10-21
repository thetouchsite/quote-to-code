# Tasks · class-packs

## 1 · Data

- [ ] 1.1 Migration: `products`, `purchases`, `credit_ledger`, `stripe_events`
- [ ] 1.2 Balance view: valid credits per member, first expiring first

## 2 · Payments

- [ ] 2.1 Checkout session for each product
- [ ] 2.2 Webhook `checkout.session.completed`, idempotent on the event id
- [ ] 2.3 Nightly expiry job

## 3 · Front desk

- [ ] 3.1 Refund a purchase through Stripe, removing the unused credits
- [ ] 3.2 Manual adjustment with mandatory reason, logged

## 4 · Verification

- [ ] 4.1 A test for every scenario in `specs/payments.md`
- [ ] 4.2 `python tools/changes.py check class-packs` with no problems
