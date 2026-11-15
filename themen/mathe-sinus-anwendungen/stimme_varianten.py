#!/usr/bin/env python3
"""Mehrere Aufnahmen (Takes) einer Szene mit festem ElevenLabs-`seed` erzeugen, die Betonung messen und die beste in den
Ton-Cache legen – unter dem Schlüssel, den das Video für den Text ohne seed sucht. Anlass 15.11.: Im neuen Merksatz lag
die Betonung wieder auf „fehlenden“ statt auf „Seiten“ (gemessen mit betonung.py).

Aufruf:  python3 stimme_varianten.py <szene> <von> <bis> <seed> [<seed> …]    misst je Take die Wörter von … bis
         python3 stimme_varianten.py <szene> --waehle <seed>                    legt diesen Take in den Cache
Takes liegen in tts_cache/varianten/ (eingecheckt, damit die Wahl nachvollziehbar bleibt)."""
import base64, hashlib, json, os, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
args = sys.argv[1:]
sys.argv = sys.argv[:1]
import sinus_anwendungen as V                              # noqa: E402
import regel as G                                          # noqa: E402
import betonung as B                                       # noqa: E402

VAR = os.path.join(G.CACHE, 'varianten')


def schluessel(text):
    cfg = G.CFG
    sig = f"el|{cfg['voice_id']}|{cfg['model']}|{json.dumps(cfg.get('voice_settings'), sort_keys=True)}|{text}"
    return os.path.join(G.CACHE, hashlib.sha1(sig.encode()).hexdigest()[:16] + '.json')


def take(text, seed):
    os.makedirs(VAR, exist_ok=True)
    ziel = os.path.join(VAR, f'{os.path.basename(schluessel(text))[:-5]}_seed{seed}.json')
    if not os.path.exists(ziel):
        url = (f"https://api.elevenlabs.io/v1/text-to-speech/{G.CFG['voice_id']}/with-timestamps"
               f"?output_format=mp3_44100_128")
        body = {'text': text, 'model_id': G.CFG['model'], 'seed': seed}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
            'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=300) as r:
            daten, kosten = r.read(), r.headers.get('character-cost')
        open(ziel, 'wb').write(daten)
        with open(os.path.join(G.CACHE, 'elevenlabs_log.jsonl'), 'a') as f:
            f.write(json.dumps({'zeichen': len(text), 'character_cost': kosten, 'seed': seed,
                                'datei': 'varianten/' + os.path.basename(ziel)}) + '\n')
        print(f'  ElevenLabs: {len(text)} Zeichen, berechnet {kosten}, seed {seed}')
    return ziel


def woerter_aus(datei, text, von, bis):
    """Wie betonung.woerter, aber für eine gegebene Antwortdatei."""
    d = json.load(open(datei))
    mp3 = datei[:-5] + '.mp3'
    if not os.path.exists(mp3):
        open(mp3, 'wb').write(base64.b64decode(d['audio_base64']))
    alt = G.R.tts_eleven
    G.R.tts_eleven = lambda *_a, **_k: (mp3, d['alignment'])
    try:
        return B.woerter(text, von=von, bis=bis)
    finally:
        G.R.tts_eleven = alt


if __name__ == '__main__':
    sc = next(s for s in V.SZENEN if s['id'] == args[0])
    if args[1] == '--waehle':
        quelle = take(sc['text'], int(args[2]))
        ziel = schluessel(sc['text'])
        open(ziel, 'wb').write(open(quelle, 'rb').read())
        for alt in (ziel[:-5] + '.mp3',):
            if os.path.exists(alt):
                os.remove(alt)
        print('in den Cache gelegt:', os.path.basename(ziel))
        sys.exit()
    von, bis = args[1], args[2]
    for seed in (int(x) for x in args[3:]):
        datei = take(sc['text'], seed)
        print(f'seed {seed:4d}: ' + '  '.join(f'{w} {ms}ms {hz}Hz {db}dB' for w, ms, hz, db in woerter_aus(datei, sc['text'], von, bis)))
