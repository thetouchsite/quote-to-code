"""Create a new project folder with the empty documentation set.

    python new_project.py "Project Name" request.txt
    python new_project.py "Project Name" request.txt --client "Client Ltd" --lang it
    python new_project.py "Project Name" request.pdf --out ~/projects

The folder is created next to the generator (../ProjectName) unless --out is
given. It copies templates/common and templates/<lang>, fills in the
placeholders ({{NAME}}, {{CLIENT}}, {{DATE}}, {{MONTH}}, {{COMPANY}},
{{RATE_DAY}}, {{RATE_HOUR}}, {{CURRENCY}}) from company.json, saves the request
in docs/client-sources/ and runs `git init` on main, without committing.

The documents come out with TO-WRITE (or DA-SCRIVERE) blocks to fill in: the
/new-project skill in Claude Code does it, or a person.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE / "templates"
VERSION = "1.0.0"
TEXT = {".html", ".md", ".py", ".css", ".js", ".txt", ".json", ""}
MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
    "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
           "agosto", "settembre", "ottobre", "novembre", "dicembre"],
}

# The estimate template is shared; its default items are written in English
# and translated here for Italian projects.
ESTIMATE_IT = [
    ('"MVP"               # first release: «MVP», «Phase 1», «Lotto 1»…', '"MVP"               # primo rilascio: «MVP», «Lotto 1», «Fase 1»…'),
    ('"Completion"        # second release; with one release only, all B days are 0', '"Completamento"     # secondo rilascio; con un rilascio solo, giornate B tutte a 0'),
    ('{}                    # narrow column headers, e.g. {"Completion": "Compl."}', '{"Completamento": "Compl."}  # intestazioni strette delle colonne'),
    ('"about 3 months"', '"circa 3 mesi"'), ('"3 more months"', '"altri 3 mesi"'), ('"about 6 months"', '"circa 6 mesi"'),
    ('("Design", "Analysis and design",\n     "Meetings, requirements, user stories, architecture, release plan"',
     '("Progettazione", "Analisi e progettazione",\n     "Incontri, requisiti, storie d\'uso, architettura, piano dei rilasci"'),
    ('("Design", "UX/UI",\n     "Flows, wireframes, design system, screens, clickable prototype"',
     '("Progettazione", "UX/UI",\n     "Flussi, wireframe, design system, interfacce, prototipo cliccabile"'),
    ('("Quality and release", "Security",\n     "Authentication, authorization, rate limits, OWASP review, tested backup and restore"',
     '("Qualità e rilascio", "Sicurezza",\n     "Autenticazione, autorizzazioni, limiti di richieste, revisione OWASP, backup e ripristino provato"'),
    ('("Quality and release", "GDPR",\n     "Consents, notices, data export and deletion, retention"',
     '("Qualità e rilascio", "GDPR",\n     "Consensi, informative, esportazione e cancellazione dei dati, conservazione"'),
    ('("Quality and release", "Testing",\n     "Automated tests, acceptance testing, beta"',
     '("Qualità e rilascio", "Testing",\n     "Test automatici, collaudo, beta"'),
    ('("Quality and release", "Technical documentation",\n     "Architecture, API, deployment, backup and restore, admin manual"',
     '("Qualità e rilascio", "Documentazione tecnica",\n     "Architettura, API, deploy, backup e ripristino, manuale dell\'amministratore"'),
    ('("Quality and release", "Training",\n     "Sessions for the client\'s administrators"',
     '("Qualità e rilascio", "Formazione iniziale",\n     "Sessioni per gli amministratori del cliente"'),
    ('("Quality and release", "Project management",\n     "Coordination, progress, releases, regular meetings"',
     '("Qualità e rilascio", "Gestione di progetto",\n     "Coordinamento, avanzamento, rilasci, riunioni periodiche"'),
]


def folder_name(name):
    """«Yoga Studio» → «YogaStudio»: no spaces or odd characters."""
    words = re.findall(r"[A-Za-z0-9]+", name)
    if not words:
        sys.exit("The project name needs at least one letter or digit.")
    return "".join(w[:1].upper() + w[1:] for w in words)


def load_company():
    for name in ("company.json", "company.example.json"):
        p = HERE / name
        if p.is_file():
            if name != "company.json":
                print("Note: company.json not found, using company.example.json. "
                      "Copy it to company.json and put your own details in it.")
            return json.loads(p.read_text(encoding="utf-8"))
    sys.exit("company.json missing: copy company.example.json and fill it in.")


def read_request(path):
    if path == "-":
        return sys.stdin.read()
    p = Path(path)
    if not p.is_file():
        sys.exit(f"Request not found: {p}")
    if p.suffix.lower() == ".pdf":
        return None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    sys.exit(f"Cannot read {p}: save it as UTF-8.")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    company = load_company()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name", help="project name, for example «Yoga Studio»")
    ap.add_argument("request", help="client request (.txt, .md or .pdf), or - for stdin")
    ap.add_argument("--client", help="client name, if different from the project name")
    ap.add_argument("--lang", choices=sorted(MONTHS), default=company.get("lang", "en"),
                    help="language of the generated documents (default from company.json)")
    ap.add_argument("--out", type=Path, default=HERE.parent, help="where to create the folder (default: %(default)s)")
    args = ap.parse_args()

    dest = args.out.expanduser() / folder_name(args.name)
    if dest.exists():
        sys.exit(f"Already exists: {dest}. Pick another name or move it first.")

    today = date.today()
    month = f"{MONTHS[args.lang][today.month - 1]} {today.year}"
    values = {
        "{{NAME}}": args.name,
        "{{CLIENT}}": args.client or args.name,
        "{{DATE}}": (f"{today.day} {MONTHS['it'][today.month - 1]} {today.year}" if args.lang == "it"
                     else f"{today.day} {MONTHS['en'][today.month - 1]} {today.year}"),
        "{{MONTH}}": month,
        "{{COMPANY}}": company.get("company", "Your Company"),
        "{{RATE_DAY}}": str(company.get("rate_day", 0)),
        "{{RATE_HOUR}}": str(company.get("rate_hour", 0)),
        "{{CURRENCY}}": company.get("currency", "€"),
    }

    request = read_request(args.request)
    shutil.copytree(TEMPLATES / "common", dest, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(TEMPLATES / args.lang, dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))

    for f in dest.rglob("*"):
        if f.is_file() and f.suffix.lower() in TEXT:
            text = f.read_text(encoding="utf-8")
            for k, v in values.items():
                text = text.replace(k, v)
            if args.lang == "it" and f.name == "estimate.py":
                for en, it in ESTIMATE_IT:
                    text = text.replace(en, it)
            f.write_text(text, encoding="utf-8", newline="\n")

    (dest / ".projectgen.json").write_text(json.dumps(
        {"lang": args.lang, "generator": "quote-to-code", "version": VERSION,
         "created": today.isoformat(), "name": args.name, "client": values["{{CLIENT}}"]},
        indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    sources = dest / "docs" / "client-sources"
    stem = f"Request-{today.isoformat()}"
    if request is None:
        shutil.copy2(args.request, sources / f"{stem}.pdf")
    else:
        title = "Richiesta del cliente" if args.lang == "it" else "Client request"
        note = ("Testo originale, non modificato." if args.lang == "it" else "Original text, unchanged.")
        (sources / f"{stem}.md").write_text(f"# {title} · {args.name}\n\n> {month}. {note}\n\n---\n\n"
                                            + request.strip() + "\n", encoding="utf-8", newline="\n")
    keep = sources / ".gitkeep"
    if keep.exists():
        keep.unlink()

    try:
        subprocess.run(["git", "init", "-b", "main", "-q"], cwd=dest, check=True)
    except (OSError, subprocess.CalledProcessError):
        print("Warning: git not available, repository not initialised.")

    print(dest)


if __name__ == "__main__":
    main()
