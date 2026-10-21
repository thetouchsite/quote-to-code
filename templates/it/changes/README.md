# Modifiche

Ogni lavoro sul sistema — un modulo nuovo, una correzione importante, un
cambio di regole — è una **modifica**: una cartella che dice perché, cosa
cambia nelle specifiche, come si fa e a che punto è.

```text
changes/
  motore-workflow/          una modifica aperta
    proposal.md             perché, cosa cambia, voce di stima, giornate
    design.md               le scelte tecniche (facoltativo)
    tasks.md                le attività da spuntare
    specs/
      pratiche.md           requisiti aggiunti, modificati, rimossi
  archive/
    2026-11-13-anagrafiche/ le modifiche concluse, con la data
  _template/                lo scheletro di una modifica nuova
```

## Il ciclo

| Passo | Comando in Claude Code | Cosa succede |
| --- | --- | --- |
| Capire | `/explore` | Legge codice e specifiche, ragiona sulle opzioni, non scrive |
| Proporre | `/propose <nome>` | Apre la modifica: proposta, specifiche toccate, design, attività |
| Costruire | `/apply <nome>` | Implementa le attività una per una e le spunta |
| Verificare | `/verify <nome>` | Controlla codice e test contro gli scenari |
| Chiudere | `/archive <nome>` | Aggiorna `specs/`, registra le giornate reali, archivia |

La parte meccanica (cartelle, date, conteggi, formato) la fa `tools/changes.py`:

```sh
python tools/changes.py list       # cosa è aperto e a che punto
python tools/changes.py actuals    # giornate stimate e reali
```

## Specifiche di una modifica

Nel file `specs/<modulo>.md` di una modifica ci sono solo le differenze:

```markdown
## Requisiti aggiunti

### Requisito: …
Il sistema DEVE …

#### Scenario: …
- **QUANDO** …
- **ALLORA** …

## Requisiti modificati

### Requisito: <titolo identico a quello in specs/>
Il testo completo nuovo, con tutti i suoi scenari.

## Requisiti rimossi

### Requisito: <titolo>
Perché si toglie.
```

## Giornate

`Giornate stimate` viene da `docs/estimate/estimate.py` (la voce indicata in
`Voce di stima`); `Giornate reali` si scrive all'archiviazione. A fine progetto
`/close-project` le confronta e aggiorna il listino dell'azienda: è così che le
stime successive migliorano.
