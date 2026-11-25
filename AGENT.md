# Istruzioni per l'agente che scrive il blog di appcaloria.com

Ogni mattina un'attività pianificata scrive **un** articolo nuovo e lo pubblica.
Il sito legge gli articoli dalla cartella `articles/` di questo repository: un file JSON per articolo.

## Cos'è Caloria

App italiana (iPhone e Android, gratis con abbonamento Premium opzionale) che conta calorie e macronutrienti
con una foto del piatto. Funzioni: foto del piatto con IA, chat IA ("scrivi cosa hai mangiato"), scanner del
codice a barre, database con oltre 200.000 prodotti italiani, ricette su misura, obiettivo calorico e macro,
grafico del peso, calorie bruciate. Non promettere funzioni diverse da queste.

## Procedura

1. Prendi il primo argomento di `topics.json` che non è in `used_topics.json`.
   Se sono finiti, scegli tu una nuova parola chiave a coda lunga in italiano (calorie di cibi italiani,
   porzioni, dieta equilibrata, conteggio delle calorie) diversa dai titoli già pubblicati, e aggiungila a `topics.json`.
2. Scrivi l'articolo e salvalo in `articles/<slug>.json` (formato sotto).
3. Aggiungi l'argomento a `used_topics.json`.
4. Esegui `python3 validate.py <slug>` e correggi finché stampa `OK`.
5. Commit e push sul branch `main` (messaggio: `Articolo: <titolo>`).

## Formato del file

```json
{
  "slug": "calorie-cornetto-alla-crema",
  "title": "Quante calorie ha un cornetto alla crema?",
  "description": "Meta description di 120-165 caratteri, con la parola chiave e un beneficio.",
  "keyword": "calorie di un cornetto alla crema",
  "date": "2026-11-26T07:15:00+01:00",
  "reading_minutes": 5,
  "html": "<p>...</p><h2>...</h2>...",
  "faq": [{"q": "Domanda?", "a": "Risposta breve."}]
}
```

- `slug`: minuscole, numeri e trattini, senza accenti, max 70 caratteri, uguale al nome del file.
- `title`: max 70 caratteri, contiene la parola chiave. Spesso funziona la forma domanda.
- `date`: data e ora di pubblicazione, fuso di Roma.
- `reading_minutes`: parole / 220, arrotondato.
- `faq`: da 3 a 5 domande che la gente cerca davvero, risposte di 1-3 frasi.

## Regole di contenuto (obbligatorie)

- In italiano, tono chiaro e amichevole, frasi brevi, si dà del "tu". Niente frasi di riempimento.
- Rispondi alla domanda principale nel **primo paragrafo**, con un numero o una risposta concreta.
- Da 900 a 1.400 parole, 4-7 sezioni `<h2>` che contengono varianti della parola chiave.
  Quando ha senso, una tabella con porzioni e calorie.
- Valori nutrizionali: valori medi plausibili delle tabelle italiane (es. CREA), sempre come stime
  ("circa", intervalli). Controlla i conti: i totali devono tornare con gli ingredienti.
- Non inventare studi, statistiche, percentuali, citazioni, fonti o testimonianze.
- Sicurezza: niente diete estreme, digiuni prolungati o consigli sotto circa 1.200 kcal al giorno per le donne
  e 1.500 per gli uomini; nessuna promessa di dimagrimento in tempi precisi; niente colpevolizzazione del cibo
  o del corpo. Per patologie, gravidanza o disturbi alimentari invita a rivolgersi a un medico o a un nutrizionista.
- Non nominare app o marchi concorrenti né ChatGPT.
- Cita Caloria al massimo 2 volte nel testo, dove è utile (es. stimare le porzioni con una foto), senza toni
  da pubblicità. Il riquadro per scaricare l'app lo aggiunge già il sito.
- HTML: solo `p, h2, h3, ul, ol, li, strong, em, table, thead, tbody, tr, th, td, a, br`, senza attributi
  tranne `href` sui link. Niente `<h1>` (il titolo lo mette il sito) e niente FAQ nell'HTML (vanno nel campo `faq`).
- Link: da 1 a 3 link interni ad articoli già presenti in `articles/`, nella forma `/blog/<slug>`. Nessun link esterno.
- Non ripetere un argomento già trattato: controlla i titoli in `articles/`.
