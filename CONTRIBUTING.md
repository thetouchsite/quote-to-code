# Contributing

Thanks for helping. A few things keep this project useful:

## Principles

- **Standard library only.** The tools run on a fresh Python 3.9 with no
  `pip install`. If you need a dependency, open an issue first.
- **Numbers come from scripts.** Nothing in the generated documents should
  require typing a figure by hand.
- **Plain language.** Generated documents are read by sales people and
  clients. Short sentences, the reason behind each choice.
- **Both languages.** A change to a template in `templates/en/` needs the same
  change in `templates/it/` (and the other way round). If you cannot write
  one of them, say so in the pull request and someone will help.

## Adding a language

1. Copy `templates/en/` to `templates/<code>/` and translate it.
2. Add a `<code>` entry to `VOCAB` in `templates/common/tools/changes.py`
   (requirement keywords, field names, statuses, messages).
3. Add labels to `LABELS` in `templates/common/docs/estimate/estimate.py`.
4. Add month names to `MONTHS` in `new_project.py`, and default estimate items
   if needed.
5. Generate a project with `--lang <code>` and run the checks below.

## Checks before a pull request

```sh
python new_project.py "Check" README.md --out /tmp/pgc --lang en
cd /tmp/pgc/Check
python docs/estimate/estimate.py
python tools/changes.py new sample && python tools/changes.py check sample   # reports TO-WRITE markers: expected
python tools/make_pdf.py
```

Repeat with `--lang it`. Then run `python tools/changes.py check` in
`examples/riverside-yoga/`: it must report no problems.

## Skills

Skills live in `.claude/skills/` (generator) and
`templates/common/.claude/skills/` (projects). Keep them in English, and keep
the rule that generated content follows the project language.
