# GDPR and security

Riverside Yoga is the **controller** of its members' data. Example Studio is a
**processor** during development and support, under a data processing
agreement signed with the contract. Cloud services are sub-processors.

## Data processed

| Category | Examples | Legal basis | Notes |
| --- | --- | --- | --- |
| Account | name, email, phone | contract | |
| Bookings and attendance | sessions booked, cancellations, check-ins | contract | instructors see only their own sessions |
| Payments | purchases, Stripe customer id | contract, tax law | card data never reaches our systems |
| Marketing | newsletter consent | consent | opt-in, revocable from the account |
| Health information | injuries, pregnancy | — | **not collected**; if the studio wants it, explicit consent and a separate notice |

## Sub-processors

| Service | Data | Location | Transfer safeguard |
| --- | --- | --- | --- |
| Supabase | database | EU region | DPA, standard contractual clauses |
| Vercel | logs, IP addresses, pages in transit | EU functions, global edge | DPA, Data Privacy Framework |
| Stripe | payment and billing data | EU and US | DPA, Data Privacy Framework |
| Email service | address and content of emails | EU region available | DPA |
| Error monitoring | technical traces, user id | EU available | DPA, no booking contents |

## In the product

- consents at sign-up, with notice version and date;
- «My data» page: download everything as JSON, delete the account;
- on deletion: profile and bookings anonymised, purchases kept for tax law
  (10 years), marketing consent removed;
- staff actions on credits and refunds logged in `admin_log`.

## Retention

| Data | How long |
| --- | --- |
| Account and bookings | while the account is active; anonymised 24 months after the last booking |
| Purchases and receipts | 10 years (tax law, to verify for the studio's country) |
| Admin log | 5 years |
| Backups | 12 months at most, rotated |

## Security

- RLS on every table, tested per role with pgTAP; a test fails if a new table
  has no policy;
- booking and credits only through SQL functions, never direct writes;
- Stripe webhooks verified by signature and deduplicated by event id;
- staff sign-in with two factors; members by email link, no passwords to leak;
- rate limits on sign-in and booking endpoints;
- OWASP review before each release; dependency updates checked automatically;
- nightly off-provider backup and quarterly test restore.
