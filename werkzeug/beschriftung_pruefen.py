"""Prüft ein Video aus dem Baukasten (zuerst für themen/mathe-einheitskreis). Findet Beschriftungen, die auf Linien/Kurven/Kreis liegen oder sich überlappen.
Je Zeitpunkt: Bild ohne Text und ohne Papierfelder rendern, Text-Kästen merken, Anteil 'Tinte' im Kasten messen."""
import sys, json
from multiprocessing import Pool
sys.path.insert(0, '/home/user/mathe-videos/themen/mathe-einheitskreis'); sys.argv = ['x']
import numpy as np
import einheitskreis as E, regel as G, animationen as A
G.ton_und_zeitplan()
K = A.K
KAESTEN = []
def text_mess(self, s, x, y, g, c, pfad=A.INTER, anker='m', alpha=1.0, skala=1.0, dreh=0.0):
    if alpha <= 0.5 or skala <= 0.01 or dreh or not s.strip():
        return 0
    w = A.breite(s, pfad, g * skala)
    x0 = {'m': x - w / 2, 'l': x, 'r': x - w}[anker]
    KAESTEN.append((s, x0, y - g * skala * 0.5, x0 + w, y + g * skala * 0.5))
    return w
A.Bild.text = text_mess
E.band = lambda *a, **k: None          # Papierfelder hinter Etiketten aus (die verdecken sonst die Linien)
grund = np.asarray(G.grund().convert('RGB')).astype(int)
def pruefe(t):
    KAESTEN.clear()
    i = G.szene_bei(t); sc = G.SZENEN[i]
    b = A.Bild(G.grund()); G.ZEICHNER[sc['id']](b, sc, t - sc['start'])
    img = np.asarray(b.img).astype(int)
    diff = np.abs(img - grund).max(axis=2)
    weiss = img.min(axis=2) > 238
    tinte = (diff > 70) & ~weiss
    funde = []
    ks = list(KAESTEN)
    for j, (s, x0, y0, x1, y1) in enumerate(ks):
        if y0 < 70: continue
        X0, Y0, X1, Y1 = [int(v * K) for v in (x0 - 3, y0, x1 + 3, y1)]
        X0, Y0 = max(X0, 0), max(Y0, 0)
        feld = tinte[Y0:Y1, X0:X1]
        if feld.size and feld.mean() > 0.01:
            funde.append(('Linie', s, round(float(feld.mean()), 3)))
        for s2, a0, b0, a1, b1 in ks[j + 1:]:
            if b0 < 70: continue
            if min(x1, a1) - max(x0, a0) > 4 and min(y1, b1) - max(y0, b0) > 4:
                funde.append(('Text', s + ' / ' + s2, 0))
    return (round(t, 1), sc['id'], funde)
if __name__ == '__main__':
    ende = G.SZENEN[-1]['start'] + G.SZENEN[-1]['dauer']
    ts = list(np.arange(0.2, ende, 0.5))
    with Pool(4) as p:
        res = p.map(pruefe, ts, chunksize=8)
    agg = {}
    for t, sid, f in res:
        for art, s, v in f:
            key = (sid, art, s)
            agg.setdefault(key, []).append((t, v))
    for (sid, art, s), l in sorted(agg.items(), key=lambda kv: kv[1][0][0]):
        print(f'{l[0][0]:6.1f}-{l[-1][0]:6.1f}  {sid:12s} {art:5s} {s!r:40s} n={len(l)} max={max(v for _, v in l)}')
