# quote-to-code

Takes a software project from a client's request for a quote to delivery, and
feeds actual days back into the estimates. Projects are created next to this
folder (`../<ProjectName>/`).

- Pre-sales: `/new-project` (`.claude/skills/new-project/SKILL.md`).
- Kick-off when the client signs: `/start-project`.
- Development: skills in `templates/common/.claude/skills/` (explore, propose,
  apply, verify, archive), copied into every project; they run with Claude Code
  opened in the project folder.
- Close and actuals: `/close-project`, which updates `pricing.md`.

Rules:

- Rates and estimating rules: `pricing.md` (or `pricing.example.md` /
  `pricing.example.it.md` if the user has not created it yet — say so). Binding.
- Company settings: `company.json` (or `company.example.json`).
- Finished example: `examples/riverside-yoga/`.
- Generated documents are written in the project's language (`lang` in its
  `.projectgen.json`).
- No commits or pushes in generated projects: the user does them.
- Documents that may reach a client never name other clients.
- Change a development skill or tool in `templates/`, then bring it to projects
  with `python update_project.py`, never in one project only.
- `new_project.py` placeholders: `{{NAME}}`, `{{CLIENT}}`, `{{DATE}}`,
  `{{MONTH}}`, `{{COMPANY}}`, `{{RATE_DAY}}`, `{{RATE_HOUR}}`, `{{CURRENCY}}`.
  Templates that must stay templates use others (`{{CHANGE}}`, `{{TODAY}}`).
- Keep the tools on the Python standard library, Python 3.9+.
