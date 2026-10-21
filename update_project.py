"""Bring an existing project up to date with the current development skills and tools.

    python update_project.py ../ProjectName            # copy and report what changed
    python update_project.py ../ProjectName --dry-run  # say what would change, write nothing
    python update_project.py --all                     # every generated project next to the generator

Copies only the managed files listed below: development skills, tools, the
templates of changes and specs. It never touches `docs/`, code, written specs,
or open and archived changes. The project's `CLAUDE.md` is created only if
missing: after /start-project it belongs to the project.

A project is recognised by its `.projectgen.json`. No commits: the user does them.
"""

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE / "templates"

# (template folder, path relative to it): whole folders or single files.
MANAGED = [
    ("common", ".claude/skills/explore"),
    ("common", ".claude/skills/propose"),
    ("common", ".claude/skills/apply"),
    ("common", ".claude/skills/verify"),
    ("common", ".claude/skills/archive"),
    ("common", "tools"),
    ("{lang}", "changes/_template"),
    ("{lang}", "changes/README.md"),
    ("{lang}", "specs/README.md"),
]
ONLY_IF_MISSING = [("{lang}", "CLAUDE.md"), ("{lang}", "changes/archive/.gitkeep")]
IGNORE = {"__pycache__"}


def files_of(base, rel):
    root = TEMPLATES / base
    p = root / rel
    if p.is_file():
        return [Path(rel)]
    return sorted(f.relative_to(root) for f in p.rglob("*") if f.is_file() and not IGNORE & set(f.parts))


def settings(project):
    try:
        return json.loads((project / ".projectgen.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def update(project, dry, quiet=False):
    cfg = settings(project)
    if cfg is None:
        if not quiet:
            print(f"Skipping {project}: no .projectgen.json, not a generated project.")
        return
    lang = cfg.get("lang", "en")
    if not (TEMPLATES / lang).is_dir():
        sys.exit(f"{project.name}: unknown language «{lang}» in .projectgen.json")
    new, changed = [], []
    for base, rel in MANAGED:
        base = base.format(lang=lang)
        for f in files_of(base, rel):
            dest = project / f
            src = TEMPLATES / base / f
            if not dest.exists():
                new.append(f)
            elif not filecmp.cmp(src, dest, shallow=False):
                changed.append(f)
            else:
                continue
            if not dry:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
    for base, rel in ONLY_IF_MISSING:
        dest = project / rel
        if dest.exists():
            continue
        new.append(Path(rel))
        if not dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            text = (TEMPLATES / base.format(lang=lang) / rel).read_text(encoding="utf-8")
            for k, v in {"{{NAME}}": cfg.get("name", project.name), "{{CLIENT}}": cfg.get("client", project.name),
                         "{{COMPANY}}": company_name()}.items():
                text = text.replace(k, v)
            dest.write_text(text, encoding="utf-8", newline="\n")
    verb = "would change" if dry else "updated"
    print(f"{project.name}: {len(new)} new, {len(changed)} {verb}")
    for f in new:
        print(f"  + {f.as_posix()}")
    for f in changed:
        print(f"  ~ {f.as_posix()}")


def company_name():
    for name in ("company.json", "company.example.json"):
        p = HERE / name
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8")).get("company", "Your Company")
    return "Your Company"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", nargs="?", type=Path, help="project folder, e.g. ../ProjectName")
    ap.add_argument("--all", action="store_true", help="every generated project next to the generator")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, write nothing")
    args = ap.parse_args()
    if args.all == bool(args.project):
        ap.error("give a project folder or --all")
    projects = ([p for p in sorted(HERE.parent.iterdir()) if p.is_dir() and p != HERE]
                if args.all else [args.project.resolve()])
    for p in projects:
        if not p.is_dir():
            sys.exit(f"Folder not found: {p}")
        update(p, args.dry_run, quiet=args.all)


if __name__ == "__main__":
    main()
