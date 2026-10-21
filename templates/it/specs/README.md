# Specifiche

Cosa fa il sistema **oggi**, modulo per modulo: un file per modulo
(`anagrafiche.md`, `pratiche.md`…). È la fonte di verità per chi sviluppa e per
l'AI. Si cambia solo archiviando una modifica (`/archive`), mai a mano nel
mezzo di un lavoro.

## Formato

```markdown
# Specifica · Pratiche

## Scopo

Una o due frasi: a cosa serve il modulo e per chi.

## Requisiti

### Requisito: Avanzamento di fase
Il sistema DEVE permettere il passaggio a una fase solo se i documenti e i
campi richiesti dalla fase sono presenti.

#### Scenario: Documento mancante
- **QUANDO** l'operatore chiede il passaggio a «istruttoria» senza l'incarico firmato
- **ALLORA** il passaggio è rifiutato
- **E** il messaggio indica il documento che manca
```

Regole, controllate da `python tools/changes.py check`:

- ogni requisito ha un titolo e usa **DEVE** (o **NON DEVE**);
- ogni requisito ha almeno uno **scenario** con **QUANDO** e **ALLORA**
  (**E** per le condizioni o i risultati in più);
- uno scenario è verificabile: diventa un test.

Niente dettagli di implementazione qui (nomi di tabelle, librerie): stanno in
`docs/technical/` e nel `design.md` delle modifiche.
