# Documentazione · {{NAME}}

**Da leggere: [`index.html`](index.html).** Si apre con un doppio clic e porta a
tutto il resto.

| Cartella | Cosa c'è dentro |
| --- | --- |
| **`sales/`** | La scheda per il preventivo, in HTML e PDF |
| **`estimate/`** | `estimate.py`: le giornate per voce, l'unica fonte dei numeri |
| **`infrastructure/`** | L'impianto proposto: servizi, regioni, sicurezza, backup, account |
| **`technical/`** | Architettura, modello dei dati, GDPR e sicurezza, documenti specifici, decisioni in `adr/` |
| **`client-sources/`** | La richiesta originale del cliente e i suoi allegati |
| **`assets/`** | Foglio di stile e tasto del tema comuni |

## Cambiare un numero

Gli importi della scheda **non si correggono a mano**. Si cambia la riga in
`estimate/estimate.py` (o la `RATE`), poi:

```sh
python docs/estimate/estimate.py                    # riscrive tabelle e cifre della scheda
python docs/estimate/estimate.py --csv > voci.csv   # se serve un foglio di calcolo
python tools/make_pdf.py                            # rifà il PDF
```

## Riservatezza

Il repository resta privato. Nei documenti che possono arrivare al cliente non
si nominano altri clienti.

Generato con quote-to-code il {{DATE}}.
