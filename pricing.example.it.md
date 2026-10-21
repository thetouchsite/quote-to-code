# Listino e regole di stima — Example Studio

> **Valori di esempio.** Copia questo file in `pricing.md` (escluso da git) e
> mettici tariffe, team e giornate di riferimento tuoi. La skill
> `/new-project` legge `pricing.md` prima di ogni stima e lo considera
> vincolante.

Ultimo aggiornamento: ottobre 2026.

## Chi siamo, per la stima

- **Tre sviluppatori senior full-stack** che lavorano con strumenti di sviluppo
  assistito. Designer UX/UI e tester entrano nelle fasi in cui servono.
- Capacità: circa **12 giornate di lavoro a settimana** su un progetto (con
  margine per gli altri clienti e le riunioni).
- Si stimano le giornate di questo team, non quelle di una grande agenzia.

## Stack predefinito

React Native + Expo per le app, Next.js per siti e pannelli, Supabase
(PostgreSQL) in regione UE per i dati, un piccolo worker Node.js su Railway
quando servono lavori lunghi. Si cambia solo con un motivo, scritto in un ADR.

## Tariffe

| Voce | Importo |
| --- | --- |
| Giornata di sviluppo, progettazione, analisi | **400 €** (IVA esclusa) |
| Ora fuori pacchetto | 60 € |
| Fuori orario o festivi | +30% |

## Team

| Figura | Cosa fa | Impegno |
| --- | --- | --- |
| Sviluppatore senior full-stack · capo progetto | Analisi, architettura, dati, sicurezza, integrazioni; unico riferimento per il cliente | tutto il progetto |
| Sviluppatori senior full-stack (×2) | Interfacce, app, pannello, rilasci | tutto il progetto |
| UX/UI designer | Flussi, prototipo, design system, interfacce | in progettazione, poi a supporto |
| Tester | Collaudo prima di ogni rilascio | prima dei rilasci |

## Assistenza post-lancio

| Pacchetto | Ore al mese | Canone | Cosa comprende |
| --- | --- | --- | --- |
| Essenziale | 8 | 480 € | Manutenzione ordinaria, correzione difetti, monitoraggio, supporto via email |
| Standard | 20 | 1.100 € | Come sopra, più piccole evoluzioni e un riferimento telefonico |
| Evolutivo | 40 | 2.000 € | Come sopra, più sviluppo continuativo e una riunione mensile di pianificazione |

- Garanzia: **tre mesi dopo ogni rilascio**, compresa.
- Tempi: bloccante presa in carico 4 ore lavorative, soluzione 1 giorno; grave
  1 giorno / 3 giorni; normale 2 giorni / rilascio successivo.
- Orario: lunedì–venerdì 9–18. Ore non usate si portano al mese dopo, non oltre.

## Pagamenti

- Per fase o rilascio: **50% all'avvio, 50% alla consegna**; in alternativa 30%
  firma, 30% beta, 40% rilascio.
- Progetti grandi: **a fasi**, ognuna confermata dopo la precedente.

## Giornate di riferimento

Valori di progetti chiusi o stimati, per non partire da zero. Si adattano:
più ruoli, integrazioni, eccezioni → più giornate. `/close-project` aggiunge qui
i numeri veri di ogni progetto concluso.

| Componente | Giornate | Da |
| --- | --- | --- |
| Analisi e progettazione, progetto medio | 8–11 | esempio |
| UX/UI di web app con pannello | 8–14 | esempio |
| UX/UI di app più web e pannello | 14–21 | esempio |
| App React Native, codice comune, primo rilascio | 20–25 | esempio |
| Parte specifica iOS o Android | 2–3 ciascuna | esempio |
| Sito pubblico Next.js con pagine indicizzabili | 8–14 | esempio |
| Pannello amministrativo (utenti, contenuti, moderazione, statistiche) | 8–14 | esempio |
| Backend (API, funzioni, regole) | 13–22 | esempio |
| Database: schema, regole di accesso, migrazioni | 6–9 | esempio |
| Ricerca testuale e filtri | 6–9 | esempio |
| Chat in tempo reale con allegati | 5–7 | esempio |
| Notifiche push ed email | 3–5 | esempio |
| Abbonamenti Stripe (piani, limiti, webhook, portale) | 8–11 | esempio |
| Modulo funzionale semplice (profilo, schede, CRUD con regole) | 4–9 | esempio |
| Motore di workflow configurabile | 10–14 | esempio |
| Estrazione AI da documenti con revisione | 8–12 | esempio |
| Componente AI su linguaggio naturale, con tetto di spesa | 5–8 | esempio |
| Valutazione di un'infrastruttura esistente, a prezzo fisso | 3 | esempio |
| Sicurezza (incluso backup e ripristino provato) | 3–5 | esempio |
| GDPR (consensi, esportazione, cancellazione) | 3–4 | esempio |
| Testing | ~6% delle giornate di sviluppo | regola |
| Pubblicazione sugli store | 2–3 | esempio |
| Documentazione tecnica | 2–4 | esempio |
| Formazione | 1 per rilascio | esempio |
| Gestione di progetto | ~4% del totale | regola |

## Ordini di grandezza

- **Sito di prenotazioni con pagamenti e pannello, un rilascio**: ~60 giornate.
- **Marketplace con due app, web, pannello, abbonamenti e AI**: ~290 giornate.
- **Gestionale su misura in tre fasi**: ~150 giornate.

Se un totale esce molto fuori da questi per un perimetro simile, si ricontrolla.

## Costi ricorrenti tipici (servizi terzi, al mese, IVA esclusa)

| Servizio | Lancio | Crescita | Scala |
| --- | --- | --- | --- |
| Supabase (database, auth, storage, funzioni) | 25 € | 110–200 € | 400–900 € |
| Vercel (web e pannello) | 20 € | 40–80 € | 150–300 € |
| Railway (worker, se serve) | 20–50 € | 50–150 € | 150–500 € |
| Email transazionali | 0–20 € | 35–90 € | 90–300 € |
| Monitoraggio errori | 0–26 € | 26–80 € | 80–200 € |
| Build delle app (EAS) | 0–19 € | 99 € | 99–199 € |
| Modelli AI (a consumo, con tetto) | 10–50 € | 100–400 € | 400–1.500 € |
| Copia di sicurezza fuori fornitore | 5–10 € | 20–50 € | 50–150 € |

Una tantum o annuali: Apple Developer 99 USD/anno; Google Play 25 USD una
tantum; dominio 15–30 €/anno. Stripe: ~1,5% + 0,25 € per carta europea, più
~0,7% per gli abbonamenti. Apple e Google: 15–30% se impongono il pagamento in app.

I listini cambiano: prima di un preventivo grande si ricontrollano.

## Regole che valgono sempre

1. **Le voci seguono l'ordine del cliente**, così l'offerta si confronta riga
   per riga.
2. **Il primo rilascio deve servire o incassare**: le parti costose e non
   essenziali vanno nel secondo.
3. **La stima non contiene margine di rischio**: lo si consiglia (10–15%), lo
   decide il commerciale.
4. **Infrastruttura esistente mai vista** → valutazione a prezzo fisso in
   testa, con la regola «se è buona la stima scende, se non lo è non sale».
5. **Account intestati al cliente**, sempre: noi operiamo come amministratori
   invitati.
6. **Niente inventato**: le cifre di leggi, bandi e listini terzi si danno come
   da verificare se non si è controllata la fonte.
7. **Riservatezza**: nei documenti che possono arrivare a un cliente non si
   nominano altri clienti.
