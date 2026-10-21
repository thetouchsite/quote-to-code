# 0001 · A mobile-first web app on Next.js and Supabase, no native app

**Status:** accepted · 21 September 2026

## Context

Most members will book from their phone. The studio has a budget of
€20,000–30,000 for the first version and wants to be live before January. A
native app was mentioned as a «later» option.

## Decision

- One **Next.js** web application on Vercel (EU functions) for members,
  instructors and front desk, designed mobile-first and installable as a
  home-screen shortcut.
- **Supabase** in an EU region for database, sign-in and scheduled jobs.
- No native app in this project.

## Alternatives considered

- *Native app from the start*: 25–35 more days, store reviews, and Apple's
  in-app purchase rules would apply to digital content; it would not fit the
  budget or the deadline.
- *An off-the-shelf booking platform*: fast, but a monthly fee per member, the
  studio's data on someone else's platform, and no control over the
  cancellation rule the client cares about.

## Consequences

- One codebase; about €50–100 a month to run at launch.
- Members get a web link and a home-screen icon, not an app store page.
- A native app later can reuse the same database, functions and rules.
