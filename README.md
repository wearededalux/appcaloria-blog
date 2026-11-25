# Blog di appcaloria.com

Articoli del blog di [appcaloria.com](https://appcaloria.com/blog), un file JSON per articolo in `articles/`.

- Ogni mattina un agente Claude scrive un articolo seguendo `AGENT.md`, lo controlla con `validate.py` e fa push su `main`.
- Hostinger scarica il repository nella cartella `public_html/content/blog` del sito, che mostra gli articoli in automatico.
- Per togliere un articolo: cancella il suo file da `articles/` e fai push.
