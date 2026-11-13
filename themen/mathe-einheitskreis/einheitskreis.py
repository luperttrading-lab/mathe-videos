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


from regel import BG, C, band, ein, zeile                 # noqa: E402
from animationen import breite, glatt, klemm, p           # noqa: E402

KICKER = {'hook': 'Einheitskreis', 'kreis': 'Der Kreis', 'warum': 'Warum?', 'werte': 'Besondere Winkel',
          'vorzeichen': 'Vorzeichen', 'pythagoras': 'Pythagoras', 'kurve': 'Sinuskurve', 'merke': 'Merke',
          'schluss': 'Merke', 'app': 'Üben'}
for s in SZENEN:
    s['kicker'] = KICKER.get(s['id'], 'Einheitskreis')
    if s['id'] in ('schluss', 'app'):
        s['anhang'] = True

CX, CY, R = 380, 385, 215                                  # Kreis links, rechts Platz für Formeln
RX = 960                                                   # Mitte der rechten Spalte


def punkt(grad, cx=CX, cy=CY, r=R):
    a = math.radians(grad)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def etikett(b, s, x, y, g, c, a=1.0, pfad=INTER_X, anker='m'):
    """Text mit Papier-Hintergrund, damit er über Linien lesbar bleibt."""
    if a <= 0:
        return
    w = breite(s, pfad, g)
    x0 = x - w / 2 if anker == 'm' else (x if anker == 'l' else x - w)
    band(b, x0 - 6, y - g * 0.62, x0 + w + 6, y + g * 0.62, BG, 0.92 * a, r=8)
    b.text(s, x0 + w / 2, y, g, c, pfad, alpha=a)


def achsen(b, a=1.0, cx=CX, cy=CY, r=R):
    """Achsen mit Pfeilen; Zahlen außerhalb des Kreises (Nutzer 13.11.: nicht im Kreis, nicht auf der Linie)."""
    if a <= 0:
        return
    L = 1.32 * r
    b.linie([(cx - L, cy), (cx + L, cy)], GRAU, 3.5, alpha=a)
    b.linie([(cx, cy + L), (cx, cy - L)], GRAU, 3.5, alpha=a)
    b.poly([(cx + L + 12, cy), (cx + L - 4, cy - 7), (cx + L - 4, cy + 7)], fill=GRAU, alpha=a)
    b.poly([(cx, cy - L - 12), (cx - 7, cy - L + 4), (cx + 7, cy - L + 4)], fill=GRAU, alpha=a)
    b.text('x', cx + L + 6, cy + 24, 24, GRAU, INTER_X, alpha=a)
    b.text('y', cx - 22, cy - L - 2, 24, GRAU, INTER_X, alpha=a)
    for v in (1, -1):
        b.linie([(cx + v * r, cy - 7), (cx + v * r, cy + 7)], GRAU, 3.5, alpha=a)
        b.linie([(cx - 7, cy - v * r), (cx + 7, cy - v * r)], GRAU, 3.5, alpha=a)
        s = '1' if v > 0 else '−1'
        b.text(s, cx + v * r + (18 if v > 0 else -24), cy + 22, 22, INK, INTER_X, alpha=a)
        b.text(s, cx - 24 - (6 if v < 0 else 0), cy - v * r - (18 if v > 0 else -18), 22, INK, INTER_X, alpha=a)


def kreislinie(b, f=1.0, a=1.0, cx=CX, cy=CY, r=R):
    if f <= 0 or a <= 0:
        return
    n = max(2, int(180 * f))
    b.linie([(cx + r * math.cos(2 * math.pi * f * k / n), cy - r * math.sin(2 * math.pi * f * k / n))
             for k in range(n + 1)], INK, 4, alpha=a)


def winkel(b, grad, a=1.0, text='α', cx=CX, cy=CY):
    if a <= 0 or grad <= 0.5:
        return
    rr, n = 48, max(2, int(grad / 3))
    pts = [(cx + rr * math.cos(math.radians(grad * k / n)), cy - rr * math.sin(math.radians(grad * k / n)))
           for k in range(n + 1)]
    b.linie(pts, WINKEL, 5, alpha=a)
    m = math.radians(grad / 2)
    if text:
        b.text(text, cx + 74 * math.cos(m), cy - 74 * math.sin(m), 26, WINKEL, INTER_X, alpha=a)


def zeiger(b, grad, a=1.0, mit_p=True, p_a=1.0, cx=CX, cy=CY, r=R):
    px, py = punkt(grad, cx, cy, r)
    b.linie([(cx, cy), (px, py)], INK, 4, alpha=a)
    if mit_p and p_a > 0:
        b.kreis(px, py, 9, INK, alpha=a * p_a)
        dx = 24 if px >= cx - 2 else -24
        b.text('P', px + dx, py + (-22 if py <= cy + 1 else 24), 28, INK, INTER_X, alpha=a * p_a)
    return px, py


def strecken(b, grad, f_sin=1.0, f_cos=1.0, a=1.0, lab_sin='', lab_cos='', la_s=1.0, la_c=1.0):
    """Sinus rot senkrecht von der x-Achse zu P (wächst von P nach unten), Kosinus blau waagrecht vom Ursprung."""
    px, py = punkt(grad)
    if f_cos > 0:
        b.linie([(CX, CY), (CX + (px - CX) * f_cos, CY)], COS, 8, alpha=a)
    if f_sin > 0:
        b.linie([(px, py), (px, py + (CY - py) * f_sin)], SIN, 8, alpha=a)
    if lab_sin and abs(CY - py) > 20:
        rechts = px >= CX
        etikett(b, lab_sin, px + (16 if rechts else -16), (py + CY) / 2, 26, SIN, a * la_s,
                anker='l' if rechts else 'r')
    if lab_cos and abs(px - CX) > 30:
        etikett(b, lab_cos, (px + CX) / 2, CY + (28 if py <= CY else -28), 26, COS, a * la_c)


def zeit_zeile(b, t, start, teile, y, g=32, pfad=INTER_X, ende=None):
    a = ein(t, start) * (1 - (ein(t, ende, 0.4) if ende is not None else 0))
    if a > 0:
        zeile(b, teile, RX, y + 14 * (1 - ein(t, start)), g, pfad, alpha=a)


def s_hook(b, sc, t):
    tS, tE, tJ = C(sc, 'Sinus'), C(sc, 'Einheitskreis'), C(sc, 'jedem Winkel')
    zeit_zeile(b, t, tS, [('sin', SIN), (' 180° = ?', INK)], 230, 56)
    for x, s, w in ((RX - 100, '0', 'null'), (RX + 100, '−1', 'minus eins?')):
        a = ein(t, C(sc, w))
        if a > 0:
            band(b, x - 60, 330 + 12 * (1 - a), x + 60, 420 + 12 * (1 - a), '#ffffff', 0.95 * a, r=18)
            b.text(s, x, 375 + 12 * (1 - a), 48, INK, INTER_X, alpha=a)
    b.text('oder', RX, 375, 26, GRAU, INTER, alpha=ein(t, C(sc, 'oder')))
    a = ein(t, tE - 0.4, 0.4)
    achsen(b, a)
    kreislinie(b, glatt(p(t, tE - 0.2, 0.9)), a)
    # Zeiger dreht von 0° auf 180°, Winkel läuft mit (Nutzer 13.11.: zeigen, wo die 180° herkommen)
    d0 = tE + 0.8
    g = 180 * glatt(p(t, d0, 2.6))
    if t > tJ:
        g = 180 + 75 * (t - tJ)
    za = ein(t, d0 - 0.2, 0.3)
    if za > 0:
        gm = g % 360
        winkel(b, gm, za, text='')
        m = math.radians(gm / 2)
        etikett(b, f'{int(round(gm)) % 360}°', CX + 82 * math.cos(m), CY - 82 * math.sin(m),
                26, WINKEL, za)
        ls = ein(t, tJ, 0.5)
        strecken(b, g, a=ls)
        zeiger(b, g, za)


def s_kreis(b, sc, t):
    tR, tM, tX = C(sc, 'Radius eins'), C(sc, 'Mittelpunkt'), C(sc, 'positiven x-Achse')
    tU, tP = C(sc, 'gegen den Uhrzeigersinn'), C(sc, 'Punkt P')
    achsen(b)
    kreislinie(b)
    # Radius wächst waagrecht, dreht sich später auf 50°
    f = glatt(p(t, tR, 0.6))
    g = 50 * glatt(p(t, tU, 1.6))
    if f > 0:
        px, py = punkt(g)
        b.linie([(CX, CY), (CX + (px - CX) * f, CY + (py - CY) * f)], INK, 4)
        if g < 1:
            etikett(b, 'r = 1', CX + R / 2, CY - 26, 28, INK, ein(t, tR + 0.3) * (1 - ein(t, tX, 0.3)))
    am = ein(t, tM, 0.3)
    if am > 0:
        b.kreis(CX, CY, 8 + 6 * math.sin(math.pi * klemm((t - tM) / 0.6)), INK, alpha=am)
        etikett(b, '(0 | 0)', CX - 52, CY + 28, 22, INK, am)
    ax = ein(t, tX, 0.4) * (1 - ein(t, tU + 1.6, 0.6))
    if ax > 0:
        b.linie([(CX, CY), (CX + 1.32 * R, CY)], WINKEL, 10, alpha=0.45 * ax)
    winkel(b, g, ein(t, tU, 0.3))
    if f > 0:
        px, py = punkt(g)
        ap = ein(t, tP, 0.3)
        if ap > 0:
            b.kreis(px, py, 9 * (0.6 + 0.4 * ap), INK, alpha=ap)
            b.text('P', px + 24, py - 22, 28, INK, INTER_X, alpha=ap)
    zeit_zeile(b, t, tR, [('Radius 1', INK)], 200, 38)
    zeit_zeile(b, t, tM, [('Mittelpunkt im Ursprung', INK)], 270, 32, INTER)
    zeit_zeile(b, t, tX, [('Winkel ', INK), ('α', WINKEL), (' ab der positiven x-Achse', INK)], 340, 30, INTER)
    zeit_zeile(b, t, tU, [('gegen den Uhrzeigersinn ↺', WINKEL)], 400, 30, INTER)
    zeit_zeile(b, t, tP, [('P liegt auf dem Kreis', INK)], 470, 32)


def s_warum(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(L='senkrecht nach unten', D='rechtwinkliges', H='Hypotenuse', G='Gegenkathete durch Hyp',
                                       G1='Gegenkathete durch eins', Ho='Höhe von P', K='Kosinus Ankathete',
                                       Xk='x-Koordinate', Ko='Koordinaten Kosinus', Al='Alphabet', N='nur zwischen',
                                       F='legt man fest', J='jeder Winkel').items()}
    g = 50 + 95 * glatt(p(t, T['F'] + 0.3, 2.2))
    if t > T['J']:
        g = 145 + 70 * (t - T['J'])
    achsen(b)
    kreislinie(b)
    px, py = punkt(g)
    dreieck = ein(t, T['D'], 0.4) * (1 - ein(t, T['F'], 0.4))
    if dreieck > 0:
        b.poly([(CX, CY), (px, CY), (px, py)], fill=WINKEL, alpha=0.10 * dreieck)
        # rechter Winkel wie in der Schule: Viertelbogen mit Punkt (Nutzer 13.11.)
        sx = -1 if px > CX else 1                          # Richtung zum Ursprung
        sy = -1 if py < CY else 1                          # Richtung zu P
        rw = 28
        b.linie([(px + sx * rw * math.cos(math.pi / 2 * k / 12), CY + sy * rw * math.sin(math.pi / 2 * k / 12))
                 for k in range(13)], INK, 2.5, alpha=dreieck)
        b.kreis(px + sx * 11, CY + sy * 11, 3.5, INK, alpha=dreieck)
    winkel(b, g % 360, 1.0)
    lab_s = 'Gegenkathete' if t < T['Ho'] else 'sin α'
    lab_c = 'Ankathete' if t < T['Xk'] else 'cos α'
    strecken(b, g, f_sin=glatt(p(t, T['L'], 0.9)), f_cos=glatt(p(t, T['K'], 0.9)), lab_sin=lab_s, lab_cos=lab_c,
             la_s=ein(t, T['G'] if t < T['Ho'] else T['Ho'], 0.4), la_c=ein(t, T['K'] if t < T['Xk'] else T['Xk'], 0.4))
    # y-Wert an der y-Achse ablesen (Nutzer 13.11.): gestrichelt von P waagrecht zur y-Achse, dort der Sinus als rote
    # Strecke. Der x-Wert braucht keine Hilfslinie: Die rote Senkrechte trifft die x-Achse genau dort (Fußpunkt).
    ay = ein(t, C(sc, 'y-Koordinate'), 0.5)
    if ay > 0:
        n = 14
        for k in range(n):
            if k % 2 == 0:
                x0_, x1_ = px + (CX - px) * k / n, px + (CX - px) * (k + 1) / n
                b.linie([(x0_, py), (x1_, py)], SIN, 3, alpha=0.8 * ay)
        b.linie([(CX, CY), (CX, CY + (py - CY) * glatt(p(t, C(sc, 'y-Koordinate') + 0.3, 0.6)))], SIN, 8, alpha=0.75 * ay)
        b.kreis(CX, py, 7, SIN, alpha=ay)
        rechts = px >= CX
        etikett(b, 'y', CX + (-20 if rechts else 20), py, 28, SIN, ay, anker='r' if rechts else 'l')
    ax_ = ein(t, C(sc, 'x-Koordinate'), 0.5)
    if ax_ > 0:
        b.kreis(px, CY, 7, COS, alpha=ax_)
        etikett(b, 'x', px, CY + (58 if py <= CY else -58), 28, COS, ax_)
    zeiger(b, g)
    # Hypotenuse: Linie leuchtet kurz auf, Name wird Buchstabe für Buchstabe entlang der Linie geschrieben
    # (Nutzer 13.11.: „damit man weiß, wo sie ist“)
    weg_h = 1 - ein(t, T['F'], 0.4)
    hl = math.sin(math.pi * klemm((t - T['H']) / 1.6))
    if hl > 0:
        b.linie([(CX, CY), (px, py)], WINKEL, 14, alpha=0.35 * hl)
    m = math.radians(g)
    ux, uy = math.cos(m), -math.sin(m)                     # Richtung Ursprung → P (Bildschirm)
    nx, ny = -math.sin(m), -math.cos(m)                    # Normale nach links oben (außerhalb des Dreiecks)
    wort = 'Hypotenuse' + (' = 1' if t >= C(sc, 'genau eins') else '')
    ws = [breite(ch, INTER_X, 26) for ch in wort]
    pos = R / 2 - sum(ws) / 2
    for i, (ch, w) in enumerate(zip(wort, ws)):
        start = T['H'] + 0.07 * i if i < 10 else C(sc, 'genau eins') + 0.05 * (i - 10)
        a_ch = ein(t, start, 0.18) * weg_h
        mitte = pos + w / 2
        if a_ch > 0 and ch != ' ':
            b.text(ch, CX + ux * mitte + nx * 22, CY + uy * mitte + ny * 22, 26, INK, INTER_X, alpha=a_ch, dreh=g)
        pos += w
    weg = T['N']
    zeit_zeile(b, t, T['G'], [('sin α', SIN), (' = Gegenkathete : Hypotenuse', INK)], 190, 28, INTER, ende=weg)
    zeit_zeile(b, t, T['G1'], [('sin α', SIN), (' = Gegenkathete : 1', INK)], 240, 28, INTER, ende=weg)
    zeit_zeile(b, t, T['Ho'], [('sin α', SIN), (' = Höhe von P = ', INK), ('y', SIN)], 300, 34, ende=weg)
    zeit_zeile(b, t, T['K'], [('cos α', COS), (' = Ankathete : 1 = ', INK), ('x', COS)], 360, 34, ende=weg)
    zeit_zeile(b, t, T['N'], [('Dreieck nur für 0° < ', INK), ('α', WINKEL), (' < 90°', INK)], 220, 30, INTER)
    zeit_zeile(b, t, T['F'], [('sonst festgelegt:', GRAU)], 280, 30, INTER)
    zeit_zeile(b, t, T['Ko'], [('P(', INK), ('cos α', COS), (' | ', INK), ('sin α', SIN), (')', INK)], 450, 46)
    a = ein(t, T['Al'])
    if a > 0:
        band(b, RX - 190, 520, RX + 190, 576, '#ffffff', 0.95 * a, r=16)
        zeile(b, [('K', COS), (' vor ', INK), ('S', SIN), ('   wie   ', GRAU), ('x', COS), (' vor ', INK), ('y', SIN)],
              RX, 548, 30, INTER_X, alpha=a)


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
ZEICHNER.update(hook=s_hook, kreis=s_kreis, warum=s_warum)
KLAENGE = {}
MERKSAETZE = []

G.SZENEN, G.ZEICHNER, G.KLAENGE, G.MERKSAETZE = SZENEN, ZEICHNER, KLAENGE, MERKSAETZE
G.CACHE = os.path.join(HIER, 'tts_cache')

if __name__ == '__main__':
    G.main()
