"""The estimate of Riverside Yoga: the single source of every number in the quote brief.

Days live here, one line per item. The script recomputes the totals and
rewrites docs/sales/Quote-brief.html:

- the tables between `<!-- begin:... -->` and `<!-- end:... -->` markers;
- every figure quoted in the text inside an element with `data-est="key"`,
  for example `<b data-est="total">…</b>` (keys in `text_figures()`).

Never edit amounts in the brief by hand: change a line here and run again.

    python docs/estimate/estimate.py          # rewrite the brief
    python docs/estimate/estimate.py --csv    # print the items as CSV, for a spreadsheet
"""

import csv
import json
import re
import sys
from pathlib import Path

RATE = 400      # per day, net of VAT: from pricing.md of the generator
HOURLY = 60   # per hour outside a support package
CURRENCY = "€"
ROOT = Path(__file__).resolve().parent.parent.parent
BRIEF = ROOT / "docs" / "sales" / "Quote-brief.html"

LABEL_A = "Launch"            # bookings and class packs, live before the January rush
LABEL_B = "Memberships"       # monthly memberships, waiting list, reports
SHORT = {"Memberships": "Memb."}
DURATION_A = "about 6 weeks"
DURATION_B = "3 more weeks"
DURATION_TOTAL = "about 9 weeks of work"
RANGE = (1.0, 1.15)           # price range for the client: bare estimate → estimate + 15% risk margin
SUPPORT = None

# (group, item, one-line description, days A, days B)
# Groups follow the client's list: schedule, booking, payments, waiting list,
# instructors, front desk, emails, mobile.
ITEMS = [
    ("Design", "Analysis and design",
     "Kick-off workshop, booking and cancellation rules, credits model, architecture, release plan", 5, 1),
    ("Design", "UX/UI",
     "Mobile-first flows for members, instructors and front desk, design system, clickable prototype", 8, 2),

    ("1 · Schedule", "Website and weekly schedule",
     "Next.js pages for classes, instructors and prices, indexable by search engines; live spots left", 6, 0),

    ("2 · Booking", "Accounts and member area",
     "Sign-in by email link, profile, bookings and credits history, consents", 3, 1),
    ("2 · Booking", "Booking and cancellation rules",
     "Book, cancel free up to 12 hours before, late cancellations and no-shows consume the credit", 6, 1),

    ("3 · Payments", "Drop-ins and class packs",
     "Stripe Checkout for 1, 5 and 10 classes, credits ledger with expiry, receipts, refunds", 7, 0),
    ("3 · Payments", "Monthly memberships",
     "Stripe subscriptions for unlimited classes, renewals, pause, cancellation, customer portal", 0, 6),

    ("4 · Waiting list", "Waiting list with automatic promotion",
     "Join a full class, first in line gets the freed spot and an email, rules near the start time", 0, 3),

    ("5 · Instructors", "Instructor view",
     "Their classes on the phone, attendee list, attendance check-in", 3, 1),

    ("6 · Front desk", "Admin panel",
     "Recurring timetable, rooms, instructors, members, manual credits, refunds, cancellations", 7, 3),
    ("6 · Front desk", "Attendance and revenue reports",
     "Monthly attendance per class and instructor, revenue by product, CSV export", 0, 3),

    ("7 · Emails", "Confirmations and reminders",
     "Booking confirmation, reminder the day before, cancellation and payment emails", 3, 1),

    ("Platform", "Database and access rules",
     "PostgreSQL schema, row-level rules per role, migrations, capacity checks in the database", 4, 1),
    ("Platform", "Backend functions and webhooks",
     "Booking transactions, Stripe webhooks, scheduled reminders and expiry jobs", 4, 2),

    ("Quality and release", "Security",
     "Authentication, roles, rate limits, OWASP review, tested backup and restore", 2, 1),
    ("Quality and release", "GDPR",
     "Consents, privacy notice in the flows, data export and deletion, retention", 2, 0),
    ("Quality and release", "Testing",
     "Automated tests on booking rules and payments, acceptance testing with the front desk", 3, 2),
    ("Quality and release", "Technical documentation",
     "Architecture, deployment, backup and restore, front-desk manual", 1, 1),
    ("Quality and release", "Training",
     "Sessions for front desk and instructors", 1, 1),
    ("Quality and release", "Project management",
     "Weekly check-in, demos every Friday, releases", 3, 1),
]

# (item, description, min days, max days)
LATER = [
    ("Native app for iOS and Android",
     "Same booking and payments in an app, push reminders, store publication", 25, 35),
    ("Gift cards and promo codes",
     "Gift vouchers bought online, discount codes for campaigns", 3, 5),
    ("Workshops and retreats",
     "Special events with their own price, deposit and capacity", 4, 6),
    ("Instructor payroll report",
     "Classes taught and attendance per instructor, ready for monthly pay", 2, 3),
    ("Second studio",
     "A second location with its own rooms, timetable and reports", 4, 7),
]

LABELS = {
    "en": {"days": "days", "amount": "Amount", "item": "Item", "total": "Total", "included": "included",
           "warranty": "Warranty", "warranty_d": "Three months after each release, included; then monthly support packages",
           "later": "Later development", "est_amount": "Indicative amount", "none_later": "No later development listed.",
           "support": "Support and maintenance", "per_month": "per month", "per_year": "per year",
           "package": "package", "hours": "hours", "sum": "A + B · Total"},
    "it": {"days": "giornate", "amount": "Importo", "item": "Voce", "total": "Totale", "included": "compresa",
           "warranty": "Garanzia", "warranty_d": "Tre mesi dopo ogni rilascio, compresa; poi pacchetti mensili di assistenza",
           "later": "Sviluppo", "est_amount": "Importo indicativo", "none_later": "Nessuno sviluppo successivo indicato.",
           "support": "Manutenzione e assistenza", "per_month": "al mese", "per_year": "l'anno",
           "package": "pacchetto", "hours": "ore", "sum": "A + B · Totale"},
}


def language():
    try:
        lang = json.loads((ROOT / ".projectgen.json").read_text(encoding="utf-8")).get("lang", "en")
    except (OSError, ValueError):
        lang = "en"
    return lang if lang in LABELS else "en"


LANG = language()
L = LABELS[LANG]


def money(n):
    if LANG == "it":
        return f"{n:,.0f}".replace(",", ".") + f" {CURRENCY}"
    return f"{CURRENCY}{n:,.0f}"


def short(label):
    if label in SHORT:
        return SHORT[label]
    return label if len(label) <= 8 else label[:5] + "."


def totals():
    return sum(v[3] for v in ITEMS), sum(v[4] for v in ITEMS)


def items_table():
    a, b = totals()
    rows, group = [], None
    cols = 3 if b == 0 else 6
    for g, item, descr, da, db in ITEMS:
        if g != group:
            rows.append(f'    <tr class="sez"><td colspan="{cols}">{g}</td></tr>')
            group = g
        if b == 0:
            rows.append(f'    <tr><td>{item}<small>{descr}</small></td><td class="num">{da}</td>'
                        f'<td class="num">{money(da * RATE)}</td></tr>')
            continue

        def cell(d):
            return ('<td class="num">—</td><td class="num">—</td>' if d == 0
                    else f'<td class="num">{d}</td><td class="num">{money(d * RATE)}</td>')
        rows.append(f"    <tr><td>{item}<small>{descr}</small></td>{cell(da)}{cell(db)}"
                    f'<td class="num">{money((da + db) * RATE)}</td></tr>')
    if b == 0:
        rows.append(f'    <tr><td>{L["warranty"]}<small>{L["warranty_d"]}</small></td><td class="num">—</td>'
                    f'<td class="num">{L["included"]}</td></tr>')
        rows.append(f'    <tr class="somma"><td>{L["total"]}</td><td class="num">{a}</td>'
                    f'<td class="num">{money(a * RATE)}</td></tr>')
        head = (f'<th>{L["item"]}</th><th class="num" style="width:14%">{L["days"].capitalize()}</th>'
                f'<th class="num" style="width:20%">{L["amount"]}</th>')
    else:
        rows.append(f'    <tr><td>{L["warranty"]}<small>{L["warranty_d"]}</small></td>'
                    f'<td class="num" colspan="2">{L["included"]}</td><td class="num" colspan="2">{L["included"]}</td>'
                    '<td class="num">—</td></tr>')
        rows.append(f'    <tr class="somma"><td>{L["total"]}</td><td class="num">{a}</td><td class="num">{money(a * RATE)}</td>'
                    f'<td class="num">{b}</td><td class="num">{money(b * RATE)}</td>'
                    f'<td class="num">{money((a + b) * RATE)}</td></tr>')
        head = (f'<th>{L["item"]}</th><th class="num">{short(LABEL_A)}<small>{L["days"]}</small></th>'
                f'<th class="num">A · {LABEL_A}</th>'
                f'<th class="num">{short(LABEL_B)}<small>{L["days"]}</small></th><th class="num">B · {LABEL_B}</th>'
                '<th class="num">A + B</th>')
    return ('<div class="tabella">\n<table>\n'
            f'  <thead><tr>{head}</tr></thead>\n  <tbody>\n'
            + "\n".join(rows) + "\n  </tbody>\n</table>\n</div>")


def later_table():
    if not LATER:
        return f'<p class="nota">{L["none_later"]}</p>'
    rows = [f'    <tr><td>{v}<small>{d}</small></td><td class="num">{lo}–{hi}</td>'
            f'<td class="num">{money(lo * RATE)} – {money(hi * RATE)}</td></tr>'
            for v, d, lo, hi in LATER]
    return ('<div class="tabella">\n<table>\n'
            f'  <thead><tr><th>{L["later"]}</th><th class="num" style="width:14%">{L["days"].capitalize()}</th>'
            f'<th class="num" style="width:28%">{L["est_amount"]}</th></tr></thead>\n  <tbody>\n'
            + "\n".join(rows) + "\n  </tbody>\n</table>\n</div>")


def figures():
    a, b = totals()

    def box(label, d, detail):
        return (f'  <div class="cifra"><div class="et">{label}</div><div class="val">{money(d * RATE)}</div>'
                f'<div class="dett">{d} {L["days"]} · {detail}</div></div>')
    boxes = [box(f"A · {LABEL_A}", a, DURATION_A)]
    if b:
        boxes += [box(f"B · {LABEL_B}", b, DURATION_B), box(L["sum"], a + b, DURATION_TOTAL)]
    elif SUPPORT:
        name, hours, fee = SUPPORT
        boxes.append(f'  <div class="cifra"><div class="et">{L["support"]}</div>'
                     f'<div class="val">{money(fee)} {L["per_month"]}</div>'
                     f'<div class="dett">{L["package"]} {name}, {hours} {L["hours"]} · {money(fee * 12)} {L["per_year"]}</div></div>')
    return '<div class="tre">\n' + "\n".join(boxes) + "\n</div>"


def text_figures():
    a, b = totals()
    t = (a + b) * RATE
    return {
        "rate": money(RATE), "hourly": money(HOURLY),
        "first": money(a * RATE), "second": money(b * RATE), "total": money(t),
        "days-first": str(a), "days-second": str(b), "days-total": str(a + b),
        "range-min": money(round(t * RANGE[0], -2)), "range-max": money(round(t * RANGE[1], -2)),
    }


def replace_block(text, name, content):
    pattern = re.compile(rf"(<!-- begin:{name} -->\n).*?(<!-- end:{name} -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"Marker «{name}» not found in the brief")
    return pattern.sub(lambda m: m.group(1) + content + "\n" + m.group(2), text)


def replace_text(text):
    values = text_figures()

    def swap(m):
        key = m.group(3)
        if key not in values:
            sys.exit(f"Unknown data-est key «{key}»")
        return m.group(1) + values[key] + m.group(4)
    return re.sub(r'(<(\w+)[^>]*\bdata-est="([\w-]+)"[^>]*>).*?(</\2>)', swap, text, flags=re.S)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if "--csv" in sys.argv:
        w = csv.writer(sys.stdout, delimiter=";")
        w.writerow(["Group", "Item", "Description", f"Days {LABEL_A}", f"Amount {LABEL_A}",
                    f"Days {LABEL_B}", f"Amount {LABEL_B}"])
        for g, item, d, da, db in ITEMS:
            w.writerow([g, item, d, da, da * RATE, db, db * RATE])
        return
    text = BRIEF.read_text(encoding="utf-8")
    text = replace_block(text, "figures", figures())
    text = replace_block(text, "items-table", items_table())
    text = replace_block(text, "later-table", later_table())
    text = replace_text(text)
    BRIEF.write_text(text, encoding="utf-8", newline="\n")
    a, b = totals()
    print(f"A {a} d = {money(a * RATE)} · B {b} d = {money(b * RATE)} · total {a + b} d = {money((a + b) * RATE)}")


if __name__ == "__main__":
    main()
