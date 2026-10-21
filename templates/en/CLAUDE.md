# {{NAME}}

Project by {{COMPANY}} for {{CLIENT}}, generated with quote-to-code.
Project language: **English** (`.projectgen.json`): documents, specs and
changes are written in English.

## Phase

**Pre-sales.** The offer documentation is in `docs/`; there is no code yet.
When the client signs, run `/start-project` from the generator: it opens the
first changes and updates this file.

## Where things are

| Path | What |
| --- | --- |
| `docs/estimate/estimate.py` | Days per item: the single source of the offer's numbers |
| `docs/sales/Quote-brief.html` | The quote brief (also as PDF) |
| `docs/technical/` | Architecture, data model, GDPR and security, decisions in `adr/` |
| `specs/` | What the system does today, module by module, with requirements and scenarios |
| `changes/` | Work in progress, and finished work in `archive/` |
| `tools/changes.py` | List, create, check, archive changes; estimated vs actual days |
| `tools/make_pdf.py` | Rebuilds the brief's PDF |

## How we work

Every change to the system's behaviour goes through a change:

1. `/explore` to understand and choose, without writing;
2. `/propose <name>` to write down what changes;
3. `/apply <name>` to build it, task by task, with tests;
4. `/verify <name>` to check it is really done;
5. `/archive <name>` to update `specs/` and record the actual days.

Small fixes that do not change behaviour (a typo, an obvious bug) need no change.

## Rules

- Documents in plain English, short sentences, the reason behind each choice.
- Contestable choices become an ADR in `docs/technical/adr/`.
- Work outside the items of `estimate.py` is flagged: it is a change request,
  and sales decides.
- No secrets in the repository: keys and passwords live in the services.
- No commits or pushes: a person does them.
- Documents that may reach the client never name other clients.
