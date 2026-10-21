# Documentation · Riverside Yoga

**Start here: [`index.html`](index.html).** Open it with a double click; it
links to everything else.

| Folder | What is inside |
| --- | --- |
| **`sales/`** | The quote brief, as HTML and PDF |
| **`estimate/`** | `estimate.py`: days per item, the single source of the numbers |
| **`infrastructure/`** | The proposed setup: services, regions, security, backups, accounts |
| **`technical/`** | Architecture, data model, GDPR and security, project-specific documents, decisions in `adr/` |
| **`client-sources/`** | The client's original request and attachments |
| **`assets/`** | Shared stylesheet and theme toggle |

## Changing a number

Amounts in the brief are **never edited by hand**. Change the line in
`estimate/estimate.py` (or the `RATE`), then:

```sh
python docs/estimate/estimate.py                    # rewrites the brief's tables and figures
python docs/estimate/estimate.py --csv > items.csv  # for a spreadsheet
python tools/make_pdf.py                            # rebuilds the PDF
```

## Confidentiality

The repository stays private. Documents that may reach the client never name
other clients.

Generated with quote-to-code on 7 September 2026.
