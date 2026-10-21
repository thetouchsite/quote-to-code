# {{NAME}}

Progetto {{COMPANY}} per {{CLIENT}}, generato con quote-to-code.
Lingua del progetto: **italiano** (`.projectgen.json`): documenti, specifiche e
modifiche si scrivono in italiano.

## Fase

**Prevendita.** C'è il documentale per l'offerta in `docs/`; non c'è ancora
codice. Quando il cliente firma, dal generatore si lancia `/start-project`, che
apre le prime modifiche e aggiorna questo file.

## Dove sta cosa

| Percorso | Cosa |
| --- | --- |
| `docs/estimate/estimate.py` | Le giornate per voce: l'unica fonte dei numeri dell'offerta |
| `docs/sales/Quote-brief.html` | La scheda per il preventivo (anche in PDF) |
| `docs/technical/` | Architettura, modello dei dati, GDPR e sicurezza, decisioni in `adr/` |
| `specs/` | Cosa fa il sistema oggi, modulo per modulo, con requisiti e scenari |
| `changes/` | Il lavoro in corso, e quello concluso in `archive/` |
| `tools/changes.py` | Elenco, creazione, controllo, archiviazione, consuntivo delle modifiche |
| `tools/make_pdf.py` | Rifà il PDF della scheda |

## Come si lavora

Ogni cambiamento al comportamento del sistema passa da una modifica:

1. `/explore` per capire e scegliere, senza scrivere;
2. `/propose <nome>` per mettere per iscritto cosa cambia;
3. `/apply <nome>` per costruirlo, attività per attività, con i test;
4. `/verify <nome>` per controllare che sia fatto davvero;
5. `/archive <nome>` per aggiornare `specs/` e registrare le giornate reali.

Le correzioni piccole che non cambiano comportamento (un refuso, un errore
evidente) si fanno senza modifica.

## Regole

- Documenti in italiano, frasi brevi, il perché di ogni scelta.
- Le scelte contestabili diventano un ADR in `docs/technical/adr/`.
- Il lavoro fuori dalle voci di `estimate.py` si segnala: è manutenzione
  evolutiva o variante, e lo decide il commerciale.
- Niente segreti nel repository: chiavi e password stanno nei servizi.
- Non fare commit né push: li fa una persona.
- Nei documenti che possono arrivare al cliente non si nominano altri clienti.
