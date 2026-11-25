#!/usr/bin/env python3
"""Controlla gli articoli del blog di appcaloria.com prima della pubblicazione.

Uso:  python3 validate.py            (controlla tutti gli articoli)
      python3 validate.py SLUG       (controlla un articolo, con le regole complete)
Esce con codice 1 se trova errori.
"""
import json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, 'articles')
ALLOWED = {'p', 'h2', 'h3', 'ul', 'ol', 'li', 'strong', 'em', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'a', 'br'}
BANNED_WORDS = ['yazio', 'myfitnesspal', 'fastic', 'lifesum', 'cal ai', 'fatsecret', 'chatgpt']


class Checker(HTMLParser):
    def __init__(self, slugs):
        super().__init__()
        self.errors, self.slugs, self.links = [], slugs, []

    def handle_starttag(self, tag, attrs):
        if tag not in ALLOWED:
            self.errors.append(f'tag non ammesso <{tag}>')
        for k, v in attrs:
            if tag == 'a' and k == 'href':
                m = re.fullmatch(r'/blog/([a-z0-9-]+)', v or '')
                if not m:
                    self.errors.append(f'link non ammesso: {v} (solo /blog/slug-esistente)')
                elif m.group(1) not in self.slugs:
                    self.errors.append(f'link a un articolo inesistente: {v}')
                self.links.append(v)
            else:
                self.errors.append(f'attributo non ammesso: <{tag} {k}=...>')


def check(path, slugs, strict):
    errs = []
    try:
        a = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        return [f'JSON non valido: {e}']
    fname = os.path.basename(path)[:-5]
    for k in ['slug', 'title', 'description', 'date', 'html', 'faq']:
        if k not in a or a[k] in (None, ''):
            errs.append(f'campo mancante: {k}')
    if errs:
        return errs
    if a['slug'] != fname:
        errs.append('lo slug deve essere uguale al nome del file')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a['slug']) or len(a['slug']) > 70:
        errs.append('slug non valido (minuscole, numeri, trattini, max 70)')
    if not re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$', a['date']):
        errs.append('date deve essere ISO 8601 con fuso, es. 2026-11-26T07:15:00+01:00')
    c = Checker(slugs - {a['slug']})
    c.feed(a['html'])
    errs += c.errors
    if not isinstance(a['faq'], list) or not all(isinstance(q, dict) and q.get('q') and q.get('a') for q in a['faq']):
        errs.append('faq deve essere una lista di {"q": ..., "a": ...}')
    if strict:
        text = re.sub(r'<[^>]+>', ' ', a['html'])
        words = len(text.split())
        if words < 800:
            errs.append(f'troppo corto: {words} parole (minimo 800)')
        if len(a['title']) > 70:
            errs.append(f'titolo troppo lungo: {len(a["title"])} caratteri (max 70)')
        if not 120 <= len(a['description']) <= 165:
            errs.append(f'description di {len(a["description"])} caratteri (120-165)')
        if '<h2>' not in a['html']:
            errs.append('servono sezioni <h2>')
        if not 3 <= len(a['faq']) <= 5:
            errs.append('servono da 3 a 5 FAQ')
        low = (a['title'] + ' ' + text + ' ' + json.dumps(a['faq'], ensure_ascii=False)).lower()
        for w in BANNED_WORDS:
            if w in low:
                errs.append(f'nome di un marchio concorrente o di terzi: "{w}"')
    return errs


def main():
    files = sorted(f for f in os.listdir(ART) if f.endswith('.json'))
    slugs = {f[:-5] for f in files}
    target = sys.argv[1] if len(sys.argv) > 1 else None
    bad = 0
    for f in files:
        strict = target is not None and f[:-5] == target
        if target and not strict:
            continue
        errs = check(os.path.join(ART, f), slugs, strict)
        if errs:
            bad += 1
            print(f'ERRORE {f}:')
            for e in errs:
                print('  -', e)
    if target and target not in slugs:
        print(f'ERRORE: articles/{target}.json non esiste')
        bad += 1
    if not bad:
        print('OK' + (f' ({target})' if target else f' ({len(files)} articoli)'))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
