#!/usr/bin/env python3
"""Reihe „Mathe verstehen“, Trigonometrie: Der Einheitskreis (Entwurf 13.11., Drehbuch drehbuch.md).

Sprechtext steht nur in drehbuch.md (Zeilen mit „>“ unter „## <n> <id>“) und wird hier eingelesen.
Baukasten aus der Kopfrechnen-Reihe (`../mathe-einmaleins/regel.py`): Ton, Zeitmarken, Kapitelkopf, Rendern.
Stand 13.11.: Hörprobe mit einem Standbild je Szene (Bilder noch nicht animiert).

Aufruf wie regel.py: python3 einheitskreis.py <ausgabe.mp4> [--nur-ton] [--bild <s>[,<s>…]]
"""
import math, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-einmaleins'))
import regel as G                                          # noqa: E402
from regel import INK, GRAU, HELL, INTER, INTER_X          # noqa: E402

# Gemeinsame Farben mit der App einheitskreis/ (Vorgabe Hauptsitzung 13.11.)
SIN, COS, WINKEL = '#e63946', '#3a86ff', '#ff9f1c'


def szenen_aus_drehbuch():
    szenen, sc = [], None
    for z in open(os.path.join(HIER, 'drehbuch.md'), encoding='utf-8'):
        m = re.match(r'## \d+ (\w+)', z)
        if m:
            sc = dict(id=m.group(1), kicker='Einheitskreis', text='')
            szenen.append(sc)
        elif z.startswith('>') and sc is not None:
            sc['text'] = (sc['text'] + ' ' + z[1:].strip()).strip()
    return szenen


SZENEN = szenen_aus_drehbuch()
for s in SZENEN:
    if s['id'] == 'app':
        s['pause'] = 2.5                                   # Seite länger stehen lassen zum Scannen

# Standbild je Szene (Hörprobe): Winkel von P, Dreieck ja/nein, Kurve ja/nein, Formel rechts
STAND = {
    'hook':       (180, False, False, ['sin 180° = ?', '0  oder  −1 ?']),
    'kreis':      (50, False, False, ['Radius 1', 'Winkel α ab der x-Achse']),
    'warum':      (50, True, False, ['P(cos α | sin α)', 'sin α = Gegenkathete / 1']),
    'werte':      (30, True, False, ['sin 30° = ½', 'cos 30° = √3 / 2 ≈ 0,87']),
    'vorzeichen': (150, True, False, ['sin 150° = ½', 'cos 150° = −√3 / 2']),
    'pythagoras': (50, True, False, ['sin²α + cos²α = 1']),
    'kurve':      (120, False, True, ['Sinuskurve']),
    'merke':      (50, True, False, ['x = cos α,  y = sin α', 'sin²α + cos²α = 1']),
    'schluss':    (50, True, False, ['Übung macht den Meister.']),
    'app':        (50, False, False, ['App: QR-Code folgt']),
}


def kreisbild(b, sc, t):
    grad, dreieck, kurve, zeilen = STAND[sc['id']]
    cx, cy, R = (330, 380, 210) if kurve else (420, 380, 230)
    a = math.radians(grad)
    px, py = cx + R * math.cos(a), cy - R * math.sin(a)
    # Achsen und Kreis
    b.linie([(cx - 1.3 * R, cy), (cx + 1.3 * R, cy)], GRAU, 2.5)
    b.linie([(cx, cy + 1.3 * R), (cx, cy - 1.3 * R)], GRAU, 2.5)
    b.text('x', cx + 1.3 * R + 14, cy - 16, 22, GRAU, INTER)
    b.text('y', cx + 16, cy - 1.3 * R, 22, GRAU, INTER)
    for v, s in ((1, '1'), (-1, '−1')):
        b.text(s, cx + v * R + (10 if v > 0 else -14), cy + 22, 20, GRAU, INTER)
        b.text(s, cx - 24, cy - v * R, 20, GRAU, INTER)
    n = 180
    b.linie([(cx + R * math.cos(2 * math.pi * k / n), cy - R * math.sin(2 * math.pi * k / n)) for k in range(n + 1)],
            INK, 4)
    # Winkelbogen
    r = 46
    b.linie([(cx + r * math.cos(a * k / 40), cy - r * math.sin(a * k / 40)) for k in range(41)], WINKEL, 5)
    b.text('α', cx + 66 * math.cos(a / 2), cy - 66 * math.sin(a / 2), 26, WINKEL, INTER_X)
    # Radius, sin (senkrecht), cos (waagrecht)
    b.linie([(cx, cy), (px, py)], INK, 4)
    if dreieck:
        b.linie([(cx, cy), (px, cy)], COS, 7)
        b.linie([(px, cy), (px, py)], SIN, 7)
        b.text('1', (cx + px) / 2 - 18 * math.sin(a), (cy + py) / 2 - 18 * math.cos(a), 24, INK, INTER_X)
    b.kreis(px, py, 9, INK)
    b.text('P', px + (22 if px >= cx else -22), py - 20, 26, INK, INTER_X)
    if kurve:                                              # Sinuskurve 0° … 360° rechts daneben
        x0, x1 = cx + 1.45 * R, 1220
        b.linie([(x0, cy), (x1, cy)], GRAU, 2.5)
        b.linie([(x0 + (x1 - x0) * k / 200, cy - R * math.sin(2 * math.pi * k / 200)) for k in range(201)], SIN, 5)
        for g in (90, 180, 270, 360):
            b.text(f'{g}°', x0 + (x1 - x0) * g / 360, cy + 26, 18, GRAU, INTER)
        kx = x0 + (x1 - x0) * grad / 360
        b.linie([(px, py), (kx, py)], SIN, 2, alpha=0.5)
        b.kreis(kx, py, 8, SIN)
    else:
        for i, z in enumerate(zeilen):
            b.text(z, 960, 300 + 80 * i, 40 if i == 0 else 32, INK if i == 0 else GRAU, INTER_X if i == 0 else INTER)


ZEICHNER = {s['id']: kreisbild for s in SZENEN}
KLAENGE = {}
MERKSAETZE = []

G.SZENEN, G.ZEICHNER, G.KLAENGE, G.MERKSAETZE = SZENEN, ZEICHNER, KLAENGE, MERKSAETZE
G.CACHE = os.path.join(HIER, 'tts_cache')

if __name__ == '__main__':
    G.main()
