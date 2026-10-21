# Pricing and estimating rules — Example Studio

> **Example values.** Copy this file to `pricing.md` (ignored by git) and put
> your own rates, team and reference days in it. The `/new-project` skill reads
> `pricing.md` before every estimate and treats it as binding.

Last updated: October 2026.

## Who we are, for the estimate

- **Three senior full-stack developers** working with AI-assisted development
  tools. A UX/UI designer and a tester join the phases where they are needed.
- Capacity: about **12 working days per week** on one project (keeping margin
  for other clients and meetings).
- Estimate days as this team works, not as a large agency would.

## Default stack

React Native + Expo for mobile apps, Next.js for websites and admin panels,
Supabase (PostgreSQL) in an EU region for data, a small Node.js worker on
Railway when long-running jobs are needed. Change it only with a reason, and
write the reason in an ADR.

## Rates

| Item | Amount |
| --- | --- |
| Day of development, design, analysis | **€400** (net of VAT) |
| Hour outside a support package | €60 |
| Out-of-hours or public holidays | +30% |

## Team

| Role | What they do | Commitment |
| --- | --- | --- |
| Senior full-stack developer · project lead | Analysis, architecture, data, security, integrations; the client's single contact | whole project |
| Senior full-stack developers (×2) | Interfaces, apps, admin, releases | whole project |
| UX/UI designer | Flows, prototype, design system, screens | design phase, then on call |
| Tester | Acceptance testing before each release | before releases |

## Support after launch

| Package | Hours per month | Fee | What is included |
| --- | --- | --- | --- |
| Essential | 8 | €480 | Routine maintenance, bug fixing, monitoring, email support |
| Standard | 20 | €1,100 | As above, plus small improvements and a phone contact |
| Evolution | 40 | €2,000 | As above, plus continuous development and a monthly planning meeting |

- Warranty: **three months after each release**, included.
- Response times: blocking — taken in 4 working hours, solved in 1 day;
  severe — 1 day / 3 days; normal — 2 days / next release.
- Service hours: Monday–Friday 9–18. Unused hours roll over to the next month,
  not beyond.

## Payments

- Per phase or release: **50% at kick-off, 50% on delivery**; or 30% on
  signature, 30% at beta, 40% at release.
- Large projects: **in phases**, each confirmed after the previous one.

## Reference days

Values from closed or estimated projects, so estimates do not start from
scratch. Adapt them: more roles, integrations, exceptions → more days.
`/close-project` adds the real numbers of every finished project here.

| Component | Days | From |
| --- | --- | --- |
| Analysis and design, medium project | 8–11 | example |
| UX/UI, web app with admin | 8–14 | example |
| UX/UI, app plus web and admin | 14–21 | example |
| Mobile app (React Native), shared code, first release | 20–25 | example |
| iOS- or Android-specific part | 2–3 each | example |
| Public website (Next.js) with indexable pages | 8–14 | example |
| Admin panel (users, content, moderation, basic stats) | 8–14 | example |
| Backend (API, functions, rules) | 13–22 | example |
| Database: schema, access rules, migrations | 6–9 | example |
| Text search and filters | 6–9 | example |
| Real-time chat with attachments | 5–7 | example |
| Push and email notifications | 3–5 | example |
| Stripe subscriptions (plans, limits, webhooks, portal) | 8–11 | example |
| Simple functional module (profile, records, CRUD with rules) | 4–9 | example |
| Configurable workflow engine | 10–14 | example |
| AI document extraction with human review | 8–12 | example |
| AI component on natural language, with spending caps | 5–8 | example |
| Assessment of existing infrastructure, fixed price | 3 | example |
| Security (incl. tested backup and restore) | 3–5 | example |
| GDPR (consents, export, deletion) | 3–4 | example |
| Testing | ~6% of development days | rule |
| App store publication | 2–3 | example |
| Technical documentation | 2–4 | example |
| Training | 1 per release | example |
| Project management | ~4% of the total | rule |

## Orders of magnitude

- **Booking website with payments and admin, one release**: ~60 days.
- **Marketplace with two apps, web, admin, subscriptions and AI**: ~290 days.
- **Custom back-office in three phases**: ~150 days.

If a total is far off these for a similar scope, check again before handing over.

## Typical recurring costs (third-party services, per month, net of VAT)

| Service | Launch | Growth | Scale |
| --- | --- | --- | --- |
| Supabase (database, auth, storage, functions) | €25 | €110–200 | €400–900 |
| Vercel (web and admin) | €20 | €40–80 | €150–300 |
| Railway (worker, if needed) | €20–50 | €50–150 | €150–500 |
| Transactional email | €0–20 | €35–90 | €90–300 |
| Error monitoring | €0–26 | €26–80 | €80–200 |
| App builds (EAS) | €0–19 | €99 | €99–199 |
| AI models (usage-based, capped) | €10–50 | €100–400 | €400–1,500 |
| Off-provider backup copy | €5–10 | €20–50 | €50–150 |

One-off or yearly: Apple Developer 99 USD/year; Google Play 25 USD once;
domain €15–30/year. Stripe: ~1.5% + €0.25 per European card, plus ~0.7% for
subscriptions. Apple and Google: 15–30% when they impose in-app purchases.

Price lists change: check the main services again before a large quote.

## Rules that always apply

1. **Items follow the client's order**, so the offer compares line by line.
2. **The first release must be useful or earn money**: costly, non-essential
   parts go in the second.
3. **The estimate contains no risk margin**: recommend one (10–15%), sales
   decides.
4. **Client's existing infrastructure never seen** → fixed-price assessment
   first, with the rule «if it is good the estimate goes down, if not it does
   not go up».
5. **Accounts in the client's name**, always: we act as invited administrators.
6. **Nothing invented**: figures from laws, funding schemes and third-party
   price lists are marked «to verify» unless the source was checked.
7. **Confidentiality**: documents that may reach a client never name other
   clients.
