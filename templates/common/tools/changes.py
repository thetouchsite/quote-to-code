"""Changes and specs: the mechanical half of the development cycle.

The /propose, /apply, /verify and /archive skills call this script for
everything that has to be exact (folders, dates, counts, format); the skills
do the thinking.

    python tools/changes.py list                  # open changes, progress, days
    python tools/changes.py new <name>            # create changes/<name>/ from the template
    python tools/changes.py check [<name>]        # format of specs and changes
    python tools/changes.py archive <name>        # move to changes/archive/YYYY-MM-DD-<name>/
    python tools/changes.py actuals [--csv]       # estimated vs actual days, item by item

A change name is lowercase with dashes: "class-booking".

Keywords follow the project language (`lang` in .projectgen.json): an Italian
project writes "### Requisito:" and "QUANDO/ALLORA", an English one
"### Requirement:" and "WHEN/THEN".
"""

import csv
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGES = ROOT / "changes"
ARCHIVE = CHANGES / "archive"
TEMPLATE = CHANGES / "_template"
SPECS = ROOT / "specs"

VOCAB = {
    "en": {
        "status": "status", "item": "estimate item", "estimated": "estimated days",
        "actual": "actual days", "archived_on": "archived on",
        "statuses": ("open", "in progress", "to verify", "archived"),
        "requirement": "Requirement", "scenario": "Scenario",
        "shall": ("SHALL", "MUST"), "when": "WHEN", "then": "THEN",
        "added": "Added requirements", "modified": "Modified requirements", "removed": "Removed requirements",
        "marker": "TO-WRITE",
        "m": {
            "bad_name": "«{0}» is not valid: lowercase letters, digits and dashes, for example «class-booking»",
            "exists": "already exists: {0}", "reopen": "Note: a change «{0}» was already archived; opening a new one with the same name.",
            "no_template": "template missing: {0}", "no_change": "change not found: {0}",
            "none_open": "No open changes.", "none": "No changes.",
            "need_name": "missing name: python tools/changes.py {0} <name>",
            "tasks_open": "tasks not done: {0}/{1}. Finish them or move them to another change.",
            "need_actual": "proposal.md is missing «- **Actual days:** N»: needed for the actuals.",
            "ok": "Format OK.", "problems": "{0} problem(s).",
            "no_req": "no «### Requirement:»", "no_shall": "«{0}»: missing SHALL or MUST",
            "no_scen": "«{0}»: no scenario", "scen_wt": "«{0}» / «{1}»: a scenario needs WHEN and THEN",
            "missing_file": "missing {0}", "bad_status": "unknown status «{0}» (valid: {1})",
            "missing_field": "proposal.md is missing «- **{0}:**»",
            "markers": "{0}: {1} TO-WRITE left to fill in (or remove the file)",
            "placeholders": "{0}: unreplaced {{{{…}}}} placeholders",
            "days_zero": "«Estimated days» must be a number greater than zero",
            "delta_sections": "specs/{0}: needs «## Added requirements / Modified requirements / Removed requirements» sections",
            "hdr_list": ("Change", "Status", "Tasks", "Est.", "Actual"),
            "hdr_act": ("Estimate item", "Status", "Est.", "Actual", "Delta"),
            "csv": ["Estimate item", "Change", "Status", "Estimated days", "Actual days"],
            "total": "Total of finished items",
        },
    },
    "it": {
        "status": "stato", "item": "voce di stima", "estimated": "giornate stimate",
        "actual": "giornate reali", "archived_on": "archiviata il",
        "statuses": ("aperta", "in corso", "da verificare", "archiviata"),
        "requirement": "Requisito", "scenario": "Scenario",
        "shall": ("DEVE",), "when": "QUANDO", "then": "ALLORA",
        "added": "Requisiti aggiunti", "modified": "Requisiti modificati", "removed": "Requisiti rimossi",
        "marker": "DA-SCRIVERE",
        "m": {
            "bad_name": "«{0}» non va bene: minuscole, cifre e trattini, per esempio «prenotazione-lezioni»",
            "exists": "esiste già: {0}", "reopen": "Attenzione: una modifica «{0}» è già archiviata; ne apro una nuova con lo stesso nome.",
            "no_template": "modello mancante: {0}", "no_change": "modifica non trovata: {0}",
            "none_open": "Nessuna modifica aperta.", "none": "Nessuna modifica.",
            "need_name": "manca il nome: python tools/changes.py {0} <nome>",
            "tasks_open": "attività non concluse: {0}/{1}. Concludile o spostale in un'altra modifica.",
            "need_actual": "in proposal.md manca «- **Giornate reali:** N»: servono al consuntivo.",
            "ok": "Formato a posto.", "problems": "{0} problemi.",
            "no_req": "nessun «### Requisito:»", "no_shall": "«{0}»: manca DEVE",
            "no_scen": "«{0}»: nessuno scenario", "scen_wt": "«{0}» / «{1}»: lo scenario vuole QUANDO e ALLORA",
            "missing_file": "manca {0}", "bad_status": "stato «{0}» sconosciuto (validi: {1})",
            "missing_field": "in proposal.md manca «- **{0}:**»",
            "markers": "{0}: {1} punti DA-SCRIVERE da riempire (o il file da togliere)",
            "placeholders": "{0}: segnaposti {{{{…}}}} non sostituiti",
            "days_zero": "«Giornate stimate» deve essere un numero maggiore di zero",
            "delta_sections": "specs/{0}: servono sezioni «## Requisiti aggiunti / modificati / rimossi»",
            "hdr_list": ("Modifica", "Stato", "Attività", "Stim.", "Reali"),
            "hdr_act": ("Voce di stima", "Stato", "Stim.", "Reali", "Scarto"),
            "csv": ["Voce di stima", "Modifica", "Stato", "Giornate stimate", "Giornate reali"],
            "total": "Totale delle voci concluse",
        },
    },
}

NAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FIELD = re.compile(r"^- \*\*(?P<k>[^*]+):\*\*\s*(?P<v>.*)$", re.M)
TASK = re.compile(r"^\s*- \[(?P<x>[ xX])\] ", re.M)


def language():
    cfg = ROOT / ".projectgen.json"
    try:
        lang = json.loads(cfg.read_text(encoding="utf-8")).get("lang", "en")
    except (OSError, ValueError):
        lang = "en"
    return lang if lang in VOCAB else "en"


V = VOCAB[language()]
M = V["m"]


def fail(key, *args):
    sys.exit(("Error: " if V is VOCAB["en"] else "Errore: ") + M[key].format(*args))


def fields(proposal):
    if not proposal.is_file():
        return {}
    return {m["k"].strip().lower(): m["v"].strip() for m in FIELD.finditer(proposal.read_text(encoding="utf-8"))}


def number(value):
    """«10», «10 days», «7,5» → 10.0 / 7.5; «—» or empty → None."""
    m = re.search(r"\d+(?:[.,]\d+)?", value or "")
    return float(m.group().replace(",", ".")) if m else None


def progress(folder):
    f = folder / "tasks.md"
    if not f.is_file():
        return 0, 0
    marks = [m["x"] for m in TASK.finditer(f.read_text(encoding="utf-8"))]
    return sum(1 for s in marks if s in "xX"), len(marks)


def open_changes():
    if not CHANGES.is_dir():
        return []
    return sorted(d for d in CHANGES.iterdir() if d.is_dir() and d.name not in ("archive", "_template"))


def archived():
    return sorted(d for d in ARCHIVE.iterdir() if d.is_dir()) if ARCHIVE.is_dir() else []


def fmt(n):
    if n is None:
        return "—"
    s = f"{n:g}"
    return s.replace(".", ",") if V is VOCAB["it"] else s


# ── format rules ─────────────────────────────────────────────────────────

def section_titles(text, section):
    m = re.search(rf"^## {re.escape(section)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S | re.I)
    return re.findall(rf"^### {V['requirement']}:\s*(.+)$", m.group(1), re.M) if m else []


def spec_problems(f, delta=False):
    """Each requirement says SHALL/DEVE and has at least one WHEN/THEN scenario."""
    text = f.read_text(encoding="utf-8")
    out = []
    removed = set(section_titles(text, V["removed"])) if delta else set()
    blocks = re.split(rf"^### {V['requirement']}:", text, flags=re.M)[1:]
    if not blocks and not delta:
        out.append(M["no_req"])
    for b in blocks:
        title = b.splitlines()[0].strip() or "(untitled)"
        if title in removed:
            continue
        body = re.split(r"^## ", b, flags=re.M)[0]
        if not any(re.search(rf"\b{w}\b", body) for w in V["shall"]):
            out.append(M["no_shall"].format(title))
        scenarios = re.split(rf"^#### {V['scenario']}:", body, flags=re.M)[1:]
        if not scenarios:
            out.append(M["no_scen"].format(title))
        for s in scenarios:
            name = s.splitlines()[0].strip()
            if f"**{V['when']}**" not in s or f"**{V['then']}**" not in s:
                out.append(M["scen_wt"].format(title, name))
    return out


def change_problems(d):
    out = []
    for name in ("proposal.md", "tasks.md"):
        if not (d / name).is_file():
            out.append(M["missing_file"].format(name))
    c = fields(d / "proposal.md")
    if c.get(V["status"]) and c[V["status"]] not in V["statuses"]:
        out.append(M["bad_status"].format(c[V["status"]], ", ".join(V["statuses"])))
    for k in (V["item"], V["estimated"], V["status"]):
        if k not in c:
            out.append(M["missing_field"].format(k.capitalize()))
    if V["estimated"] in c and not number(c[V["estimated"]]):
        out.append(M["days_zero"])
    for f in sorted(d.rglob("*.md")):
        t = f.read_text(encoding="utf-8")
        rel = f.relative_to(d).as_posix()
        if t.count(V["marker"]):
            out.append(M["markers"].format(rel, t.count(V["marker"])))
        if "{{" in t:
            out.append(M["placeholders"].format(rel))
    for f in sorted((d / "specs").glob("*.md")) if (d / "specs").is_dir() else []:
        t = f.read_text(encoding="utf-8")
        heads = "|".join(re.escape(V[k]) for k in ("added", "modified", "removed"))
        if not re.search(rf"^## ({heads})", t, re.M | re.I):
            out.append(M["delta_sections"].format(f.name))
        out += [f"specs/{f.name}: {p}" for p in spec_problems(f, delta=True)]
    return out


# ── commands ─────────────────────────────────────────────────────────────

def cmd_list(_):
    rows = open_changes()
    if not rows:
        print(M["none_open"])
        return
    h = M["hdr_list"]
    print(f"{h[0]:32} {h[1]:14} {h[2]:>9} {h[3]:>6} {h[4]:>7}")
    for d in rows:
        c = fields(d / "proposal.md")
        done, tot = progress(d)
        print(f"{d.name:32} {c.get(V['status'], '?'):14} {f'{done}/{tot}':>9} "
              f"{fmt(number(c.get(V['estimated']))):>6} {fmt(number(c.get(V['actual']))):>7}")


def cmd_new(args):
    if not args:
        fail("need_name", "new")
    name = args[0]
    if not NAME_OK.match(name):
        fail("bad_name", name)
    dest = CHANGES / name
    if dest.exists():
        fail("exists", dest)
    if any(d.name.endswith("-" + name) for d in archived()):
        print(M["reopen"].format(name))
    if not TEMPLATE.is_dir():
        fail("no_template", TEMPLATE)
    shutil.copytree(TEMPLATE, dest)
    for f in dest.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        f.write_text(t.replace("{{CHANGE}}", name).replace("{{TODAY}}", date.today().isoformat()),
                     encoding="utf-8", newline="\n")
    print(dest)


def cmd_check(args):
    errors = 0
    if args:
        targets = [CHANGES / args[0]]
        if not targets[0].is_dir():
            fail("no_change", args[0])
        specs = []
    else:
        targets = open_changes()
        specs = sorted(f for f in SPECS.glob("*.md") if f.name.lower() != "readme.md") if SPECS.is_dir() else []
    for f in specs:
        for p in spec_problems(f):
            print(f"specs/{f.name}: {p}")
            errors += 1
    for d in targets:
        for p in change_problems(d):
            print(f"changes/{d.name}: {p}")
            errors += 1
    print(M["ok"] if not errors else M["problems"].format(errors))
    sys.exit(1 if errors else 0)


def cmd_archive(args):
    if not args:
        fail("need_name", "archive")
    d = CHANGES / args[0]
    if not d.is_dir():
        fail("no_change", args[0])
    done, tot = progress(d)
    if done < tot:
        fail("tasks_open", done, tot)
    c = fields(d / "proposal.md")
    if number(c.get(V["actual"])) is None:
        fail("need_actual")
    p = d / "proposal.md"
    t = p.read_text(encoding="utf-8")
    t = re.sub(rf"^(- \*\*{V['status']}:\*\*).*$", rf"\1 {V['statuses'][-1]}", t, flags=re.M | re.I)
    t = re.sub(rf"^(- \*\*{V['archived_on']}:\*\*).*$", rf"\1 {date.today().isoformat()}", t, flags=re.M | re.I)
    p.write_text(t, encoding="utf-8", newline="\n")
    ARCHIVE.mkdir(exist_ok=True)
    dest = ARCHIVE / f"{date.today().isoformat()}-{d.name}"
    if dest.exists():
        fail("exists", dest)
    shutil.move(str(d), str(dest))
    print(dest)


def cmd_actuals(args):
    rows = []
    for d in archived() + open_changes():
        c = fields(d / "proposal.md")
        rows.append((c.get(V["item"], "—"), d.name, c.get(V["status"], "?"),
                     number(c.get(V["estimated"])), number(c.get(V["actual"]))))
    if "--csv" in args:
        w = csv.writer(sys.stdout, delimiter=";")
        w.writerow(M["csv"])
        for r in rows:
            w.writerow([r[0], r[1], r[2], fmt(r[3]), fmt(r[4])])
        return
    if not rows:
        print(M["none"])
        return
    h = M["hdr_act"]
    print(f"{h[0]:40} {h[1]:14} {h[2]:>6} {h[3]:>7} {h[4]:>7}")
    est = act = 0.0
    for item, _, status, e, a in rows:
        delta = f"{(a - e) / e:+.0%}" if e and a is not None else "—"
        print(f"{item[:40]:40} {status:14} {fmt(e):>6} {fmt(a):>7} {delta:>7}")
        if e and a is not None:
            est += e
            act += a
    if est:
        print(f"{M['total']:40} {'':14} {fmt(est):>6} {fmt(act):>7} {(act - est) / est:>+7.0%}")


COMMANDS = {"list": cmd_list, "new": cmd_new, "check": cmd_check, "archive": cmd_archive, "actuals": cmd_actuals}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
