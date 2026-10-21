---
name: new-project
description: Creates a project folder from a client's request for a quote and writes the whole pre-sales documentation — quote brief with an item-by-item estimate and PDF, infrastructure, technical documents, decisions (ADRs). Use it when someone pastes or points to a request for a quote and asks to generate the project, the estimate or the documentation.
---

# New project from the client's request

You turn a request for a quote into a complete project folder, at the level of
the project in `examples/`. Four steps: **folder, analysis, estimate,
documents**. At the end there is a PDF sales can use to write the offer, and
documentation colleagues use to build.

## Language

Every document is written in the **project language**: `--lang` of
`new_project.py`, saved in the project's `.projectgen.json` (`it` or `en`).
Default: `lang` in `company.json`. The style is the same in both: short,
concrete sentences, no needless jargon, the reason for each choice. Sales is
not technical.

The fill-in marker is `TO-WRITE` in English projects and `DA-SCRIVERE` in
Italian ones.

## 0 · What you need

- **Project name** (e.g. «Yoga Studio») and, if different, the **client
  name**. Ask if missing.
- **The request**: pasted text or a file (.txt, .md, .pdf). If pasted, save it
  to `requests/<ProjectName>.md` first.
- **Language**, if the request is in a different language from the default.
- Client attachments (PDFs, photos, diagrams) go to `docs/client-sources/`
  after step 1.

## 1 · Create the folder

```sh
python new_project.py "Project Name" requests/<file> [--client "Client"] [--lang it|en]
```

It prints the path created (usually `../ProjectName`). From now on work inside
it, with absolute paths. No commits or pushes: the user does them.

## 2 · Read before writing

1. `pricing.md` — rates, packages, reference days, service costs, team,
   payments, rules. **Binding.** If only `pricing.example.md` (or
   `pricing.example.it.md` for Italian) exists, use it and
   tell the user the figures are examples.
2. The project in `examples/` — a finished one: see how the brief, the
   infrastructure, `estimate.py` and the technical documents are written. It is
   the level to reach. Do not copy its content: it is another project.
3. The client's request, in full, twice.

## 3 · Analyse

Before touching files, settle (for yourself, not in a file):

- **What they ask**: sections and modules in the client's order; cross-cutting
  features; requests about timing, ownership, support, format of the quote.
- **What product it is**: app, web, back-office, integration… and therefore the
  stack. Default: the stack in `pricing.md`. Change it only with a reason, and
  write it in an ADR.
- **Releases**: one release only if the project is small; otherwise a first
  release (MVP, Phase 1…) that is already useful or earns money, then the rest.
- **Open points**: ambiguous requests (write the possible readings and how
  each changes the estimate), constraints the client may not know (app store
  payment rules, data licences, GDPR, forbidden content), dependencies on the
  client's material.
- **Existing assets**: if the client already has code or infrastructure, a
  fixed-price assessment item goes first (see `pricing.md`).
- **Deadlines**: compare the client's deadline with the team's weekly capacity
  in `pricing.md`. If it does not fit, say so before estimating.
- **Public funding**: if mentioned, check requirements and thresholds on the
  web (official or recent source) and prepare a dedicated section. Never pad
  the estimate.

If an open point changes the project substantially (e.g. it is unclear whether
it is an app or a website, or the deadline is impossible), ask the user before
estimating. Otherwise pick the most reasonable reading, state it in the open
points, and go on.

## 4 · Estimate

Edit the project's `docs/estimate/estimate.py`:

- `ITEMS`: keep the fixed Design and Quality-and-release items, and put the
  project groups in between in the client's order. Each item has a one-line
  description of what it includes.
- Days from the «Reference days» table of `pricing.md`, adapted. Testing about
  6% and project management about 4% of development days; never zero.
- `LATER`: what the client mentioned that stays out, plus natural next steps
  after launch, with a min–max range.
- `LABEL_A`, `LABEL_B`, durations. With one release, all B days at 0 (the
  table then shows a single column) and optionally `SUPPORT` to show the
  recommended package next to the price.
- Check the total against the «orders of magnitude» in `pricing.md`. If it is
  far off for a similar scope, check again.

Then `python docs/estimate/estimate.py` from the project root.

## 5 · Write the documents

Every marker block is replaced; at the end a search for the marker in `docs/`
finds nothing.

**`docs/sales/Quote-brief.html`** — the main document.
- Figures are never typed: tables sit between the `begin/end` markers, figures
  in text go in `<b data-est="total">—</b>` (keys: `rate`, `hourly`, `first`,
  `second`, `total`, `days-first`, `days-second`, `days-total`, `range-min`,
  `range-max`). `estimate.py` fills them.
- Team, support and payment milestones come from `pricing.md`; adapt them to the
  project (e.g. drop the app sentences if there are no apps).
- Add sections when needed (existing infrastructure, deadline plan, public
  funding), updating the index and the `§` references.
- Recurring costs: only the services the project uses, values from `pricing.md`.

**`docs/infrastructure/Infrastructure.html`** — SVG diagram of the system
(style and classes as in the example), rules, environments, growth, security
and GDPR, backups, accounts to open.

**`docs/technical/`**, in Markdown:
- always: `architecture.md` (with a mermaid diagram), `data-model.md`,
  `gdpr-and-security.md`;
- plus one document for each hard or unusual part of the project;
- `adr/NNNN-title.md` for every choice someone could challenge (stack,
  payments, data sources…): Status, Context, Decision, Consequences.
- Days quoted in technical documents must match `estimate.py`.

**`docs/index.html`** — the summary sentence and one `.doc` card per technical
document.

## 6 · PDF and checks

```sh
python docs/estimate/estimate.py
python tools/make_pdf.py
```

Then **open the PDF and look at it page by page**: badly split tables, blank
pages, cut text, figures inconsistent between text and tables. Fix and
regenerate. Also check that no marker is left and that no other client is named.

## 7 · Hand-over

Reply to the user with:
- the project folder and PDF paths;
- totals (days and amount per release);
- open points to clarify with the client, by weight;
- what you could not verify (price lists, funding rules);
- the next step: when the client signs, `/start-project` from the generator;
- the reminder: commits and pushes are theirs, for example
  `git add -A && git commit -m "Initial documentation" && git remote add origin <url> && git push -u origin main`.
