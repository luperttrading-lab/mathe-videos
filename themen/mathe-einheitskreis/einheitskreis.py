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
    if s['id'] == 'werte':                                 # Nutzer 13.11.: Erweitern mit √2 langsamer zeigen
        s['pause_nach'] = {'erweitert:': 1.4, 'null Komma sieben.': 1.6}
    if s['id'] == 'app':
        s['pause'] = 2.5                                   # Seite länger stehen lassen zum Scannen

# Standbild je Szene (Hörprobe): Winkel von P, Dreieck ja/nein, Kurve ja/nein, Formel rechts
STAND = {
    'hook':       (180, False, False, ['sin 180° = ?', '0  oder  −1 ?']),
    'kreis':      (50, False, False, ['Radius 1', 'Winkel α ab der x-Achse']),
    'orientierung': (135, False, False, ['']),
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

KICKER = {'hook': 'Einheitskreis', 'kreis': 'Der Kreis', 'orientierung': 'Der Kreis', 'warum': 'Warum?', 'werte': 'Besondere Winkel',
          'vorzeichen': 'Vorzeichen', 'pythagoras': 'Pythagoras', 'kurve': 'Sinuskurve', 'merke': 'Merke',
          'schluss': 'Merke', 'app': 'Üben'}
for s in SZENEN:
    s['kicker'] = KICKER.get(s['id'], 'Einheitskreis')
    if s['id'] in ('schluss', 'app', 'orientierung'):
        s['anhang'] = True

CX, CY, R = 380, 385, 215                                  # Kreis links, rechts Platz für Formeln
RX = 960                                                   # Mitte der rechten Spalte


def punkt(grad, cx=CX, cy=CY, r=R):
    a = math.radians(grad)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def etikett(b, s, x, y, g, c, a=1.0, pfad=INTER_X, anker='m', grund=True):
    """Text mit Papier-Hintergrund, damit er über Linien lesbar bleibt; grund=False für Stellen im freien Raum
    (Nutzer 13.11.: Beschriftungen sollen Linien und Kreis nicht unterbrechen)."""
    if a <= 0:
        return
    w = breite(s, pfad, g)
    x0 = x - w / 2 if anker == 'm' else (x if anker == 'l' else x - w)
    if grund:
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
    b.text('y', cx + 22, cy - L + 6, 24, GRAU, INTER_X, alpha=a)
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
        kl = grad < 40                                     # schmaler Winkel: kleiner und weiter außen (Nutzer 13.11.)
        rr2, gs = (88, 20) if kl else (82, 26)
        x_, y_ = cx + rr2 * math.cos(m), cy - rr2 * math.sin(m)
        w_ = breite(text, INTER_X, gs)
        if abs(x_ - cx) < w_ / 2 + 8:                      # nicht auf der y-Achse (z. B. 180°, 150°)
            x_ = cx + (w_ / 2 + 10) * (1 if math.cos(m) >= 0 else -1)
        if abs(y_ - cy) < gs * 0.5 + 8:                    # nicht auf der x-Achse (z. B. 360°)
            y_ = cy + (gs * 0.5 + 10) * (-1 if math.sin(m) >= 0 else 1)
        b.text(text, x_, y_, gs, WINKEL, INTER_X, alpha=a)


def zeiger(b, grad, a=1.0, mit_p=True, p_a=1.0, cx=CX, cy=CY, r=R, p_name=True):
    px, py = punkt(grad, cx, cy, r)
    b.linie([(cx, cy), (px, py)], INK, 4, alpha=a)
    if mit_p and p_a > 0:
        b.kreis(px, py, 9, INK, alpha=a * p_a)
        dx = 24 if px >= cx - 2 else -24
        if p_name:
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
        ym = (py + CY) / 2
        rand = math.sqrt(max(R * R - (ym - CY) ** 2, 0))     # Kreislinie auf dieser Höhe
        w_ = breite(lab_sin, INTER_X, 26)
        innen = abs(px - CX) + 16 + w_ < rand - 6
        x_ = (px + (16 if rechts else -16)) if innen else (CX + (rand + 12 if rechts else -rand - 12))
        etikett(b, lab_sin, x_, ym, 26, SIN, a * la_s, anker='l' if rechts else 'r', grund=False)
    if lab_cos and abs(px - CX) > 30:
        wc = breite(lab_cos, INTER_X, 26)
        xm = (px + CX) / 2
        xm = max(xm, CX + wc / 2 + 10) if px > CX else min(xm, CX - wc / 2 - 10)
        etikett(b, lab_cos, xm, CY + (28 if py <= CY else -28), 26, COS, a * la_c, grund=False)


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
        winkel(b, gm, za, text=f'{int(round(gm)) % 360}°')      # Beschriftung weicht den Achsen aus
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


def s_orientierung(b, sc, t):
    """Wo liegt welcher Winkel? P läuft hin, ein oranger Strich mit Gradzahl bleibt außen stehen (Nutzer 13.11.)."""
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    halte = [(0, 'Null Grad', 0), (90, 'neunzig Grad oben', 90), (180, 'hundertachtzig Grad links', 180),
             (270, 'zweihundertsiebzig', 270), (30, 'dreißig', 390), (45, 'fünfundvierzig', 405), (60, 'sechzig', 420),
             (135, 'hundertfünfunddreißig', 495)]
    g = bahn(t, [(0, 50)] + [(w(wort) - 0.5, ziel) for _, wort, ziel in halte], 0.9)
    achsen(b)
    kreislinie(b)
    for grad, wort, _ in halte:
        a = ein(t, w(wort) + 0.3, 0.3)
        if a > 0:
            m = math.radians(grad)
            b.linie([(CX + (R - 10) * math.cos(m), CY - (R - 10) * math.sin(m)),
                     (CX + (R + 10) * math.cos(m), CY - (R + 10) * math.sin(m))], WINKEL, 4, alpha=a)
            # Gradzahl außen; an den Achsen etwas seitlich, damit sie nicht auf Achse oder „1“ liegt
            ox, oy = {0: (34, -22), 90: (34, -24), 180: (-40, -22), 270: (40, 30)}.get(
                grad, (44 * math.cos(m), -44 * math.sin(m)))
            etikett(b, f'{grad}°', CX + R * math.cos(m) + ox, CY - R * math.sin(m) + oy, 22, WINKEL, a, grund=False)
    gm = g % 360
    winkel(b, gm, 1.0, text='')
    zeiger(b, gm, p_name=False)                            # hier stehen die Gradzahlen am Kreis
    zeit_zeile(b, t, w('Null Grad'), [('0° rechts · 90° oben', INK)], 250, 32, INTER)
    zeit_zeile(b, t, w('hundertachtzig Grad links'), [('180° links · 270° unten', INK)], 305, 32, INTER)
    zeit_zeile(b, t, w('dreißig'), [('30°, 45°, 60°: erstes Viertel', INK)], 380, 30, INTER)
    zeit_zeile(b, t, w('hundertfünfunddreißig'), [('135° = Mitte zwischen 90° und 180°', INK)], 435, 30, INTER)


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
    ay = ein(t, C(sc, 'y-Koordinate'), 0.5) * (1 - ein(t, T['J'], 0.4))   # beim Kreisen ausblenden
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
    ax_ = ein(t, C(sc, 'x-Koordinate'), 0.5) * (1 - ein(t, T['J'], 0.4))
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
    ws = [breite(ch, INTER_X, 22) for ch in wort]
    pos = R / 2 - sum(ws) / 2
    for i, (ch, w) in enumerate(zip(wort, ws)):
        start = T['H'] + 0.07 * i if i < 10 else C(sc, 'genau eins') + 0.05 * (i - 10)
        a_ch = ein(t, start, 0.18) * weg_h
        mitte = pos + w / 2
        if a_ch > 0 and ch != ' ':
            b.text(ch, CX + ux * mitte + nx * 20, CY + uy * mitte + ny * 20, 22, INK, INTER_X, alpha=a_ch, dreh=g)
        pos += w
    weg = T['N']
    zeit_zeile(b, t, T['G'], [('sin α', SIN), (' = ', INK), ('Gegenkathete', SIN), (' : Hypotenuse', INK)], 190, 28, INTER, ende=weg)
    zeit_zeile(b, t, T['G1'], [('sin α', SIN), (' = ', INK), ('Gegenkathete', SIN), (' : 1', INK)], 240, 28, INTER, ende=weg)
    zeit_zeile(b, t, T['Ho'], [('sin α', SIN), (' = ', INK), ('Höhe von P', SIN), (' = ', INK), ('y', SIN)], 300, 34, ende=weg)
    zeit_zeile(b, t, T['K'], [('cos α', COS), (' = ', INK), ('Ankathete', COS), (' : 1 = ', INK), ('x', COS)], 360, 34, ende=weg)
    zeit_zeile(b, t, T['N'], [('Dreieck nur für 0° < ', INK), ('α', WINKEL), (' < 90°', INK)], 220, 30, INTER)
    zeit_zeile(b, t, T['F'], [('sonst festgelegt:', GRAU)], 280, 30, INTER)
    zeit_zeile(b, t, T['Ko'], [('P(', INK), ('cos α', COS), (' | ', INK), ('sin α', SIN), (')', INK)], 450, 46)
    a = ein(t, T['Al'])
    if a > 0:
        band(b, RX - 190, 520, RX + 190, 576, '#ffffff', 0.95 * a, r=16)
        zeile(b, [('K', COS), (' vor ', INK), ('S', SIN), ('   wie   ', GRAU), ('x', COS), (' vor ', INK), ('y', SIN)],
              RX, 548, 30, INTER_X, alpha=a)


# ---------------------------------------------------------------- Szenen 4–10
from regel import GRUEN, TEAL, karte              # noqa: E402
from animationen import einfuegen                         # noqa: E402
from motivation import spruch                              # noqa: E402
from PIL import Image                                      # noqa: E402
SPRUCH = spruch('mathe-einheitskreis', 'schluss')
QR_BILD = os.path.join(HIER, 'bilder', 'qr_einheitskreis.png')   # …/mathe-videos/einheitskreis/ (App-Sitzung)


def bahn(t, punkte, dauer=1.2):
    """Winkel aus Stützpunkten [(zeit, grad), …]: weich von einem zum nächsten."""
    prev = punkte[0][1]
    for t1, g1 in punkte[1:]:
        f = glatt(p(t, t1, dauer))
        g = prev + (g1 - prev) * f
        if f < 1:
            return g
        prev = g1
    return prev


def koord(b, grad, s, a=1.0, g=24, c=INK, abst=46):
    if a <= 0:
        return
    x, y = punkt(grad, r=R + abst)
    etikett(b, s, x, y, g, c, a)


def dreieck_fuell(b, grad, a, rw=True):
    if a <= 0:
        return
    px, py = punkt(grad)
    b.poly([(CX, CY), (px, CY), (px, py)], fill=WINKEL, alpha=0.10 * a)
    if rw and abs(px - CX) > 40 and abs(py - CY) > 40:
        sx = -1 if px > CX else 1
        sy = -1 if py < CY else 1
        b.linie([(px + sx * 28 * math.cos(math.pi / 2 * k / 12), CY + sy * 28 * math.sin(math.pi / 2 * k / 12))
                 for k in range(13)], INK, 2.5, alpha=a)
        b.kreis(px + sx * 11, CY + sy * 11, 3.5, INK, alpha=a)


def formel(b, elemente, x0, y, g, a=1.0, messen=False):
    """Formelzeile mit echten Brüchen. Elemente: ('t', text, farbe, alpha), ('b', zähler, nenner, alpha) oder
    ('b2', zähler, nenner_alt, nenner_neu, alpha, überblendung). Zähler/Nenner = Liste von (text, farbe)."""
    x, gb = x0, g * 0.85
    for el in elemente:
        if el[0] == 't':
            _, s_, c, al = el
            w_ = breite(s_, INTER_X, g)
            if not messen and al * a > 0:
                b.text(s_, x + w_ / 2, y, g, c, INTER_X, alpha=a * al)
            x += w_
            continue
        if el[0] == 'b':
            _, zt, nt, al = el
            n2, f = None, 0
        else:
            _, zt, nt, n2, al, f = el
        bz = sum(breite(s_, INTER_X, gb) for s_, _ in zt)
        bn = sum(breite(s_, INTER_X, gb) for s_, _ in nt)
        bn2 = sum(breite(s_, INTER_X, gb) for s_, _ in n2) if n2 else 0
        w_ = max(bz, bn * (1 - f) + bn2 * f) + 12
        if not messen and al * a > 0:
            zeile(b, zt, x + w_ / 2, y - g * 0.62, gb, INTER_X, alpha=a * al)
            b.linie([(x + 3, y), (x + w_ - 3, y)], INK, 2.5, alpha=a * al)
            zeile(b, nt, x + w_ / 2, y + g * 0.66, gb, INTER_X, alpha=a * al * klemm(1 - 2 * f))   # erst aus-, dann einblenden
            if n2:
                zeile(b, n2, x + w_ / 2, y + g * 0.66, gb, INTER_X, alpha=a * al * klemm(2 * f - 1))
        x += w_
    return x - x0



def s_werte(b, sc, t):
    w = lambda s, nach=None: C(sc, s, nach)                 # noqa: E731
    tA, tB = w('Und die Winkel'), w('fünfundvierzig')
    t30, t60 = w('dreißig Grad spiegeln'), w('Bei sechzig')
    g = bahn(t, [(0, 50), (w('hundertachtzig Grad liegt'), 180), (w('null Grad liegt'), 0), (w('neunzig Grad bei'), 90),
                 (w('zweihundertsiebzig'), 270), (tB - 0.2, 405), (t30, 390), (t60, 420)])
    g = g % 360
    achsen(b)
    kreislinie(b)
    teil1 = 1 - ein(t, tA, 0.4)                            # Achsenpunkte
    teil2 = ein(t, tB - 0.2, 0.4)                          # Dreiecke
    # Achsenpunkte (Nutzer 13.11.: zeigen, wo die Koordinaten herkommen, und erst schreiben, wenn sie gesprochen
    # werden): Beim ersten Wert läuft eine blaue Strecke auf der x-Achse, beim zweiten eine rote auf der y-Achse;
    # die Koordinaten entstehen Teil für Teil in denselben Farben und bleiben danach klein stehen.
    PUNKTE = [  # Winkel, x, y, Zeit erster Wert, Zeit zweiter Wert
        (180, '−1', '0', w('minus eins und null'), w('null', 'minus eins und ')),
        (0, '1', '0', w('eins und null', 'P bei '), w('null', 'P bei eins und ')),
        (90, '0', '1', w('null und eins', 'neunzig Grad bei '), w('eins', 'neunzig Grad bei null und ')),
        (270, '0', '−1', w('null und minus', 'zweihundertsiebzig Grad bei '),
         w('minus eins', 'zweihundertsiebzig Grad bei null und '))]
    spaeter = []                                           # Strecken über dem Zeiger zeichnen
    for i, (gg, xs, ys, tx, ty) in enumerate(PUNKTE):
        x, y = punkt(gg)
        ende = PUNKTE[i + 1][3] - 0.6 if i + 1 < len(PUNKTE) else tA
        hell = ein(t, tx - 0.1, 0.3) * (1 - ein(t, ende, 0.4))      # Hervorhebung, solange P dort steht
        ax, ay = ein(t, tx, 0.3), ein(t, ty, 0.3)
        if hell > 0:
            spaeter.append((x, y, hell, ax, ay, glatt(p(t, tx, 0.6)), glatt(p(t, ty, 0.6))))
        a = ein(t, tx, 0.3) * teil1
        if a > 0:
            b.kreis(x, y, 8, GRUEN, alpha=a * (1 - hell))
            g_ = 26                                        # immer gleich groß (Nutzer 13.11.)
            teile = [('(', INK), (xs, COS)] + ([(' | ', INK), (ys, SIN), (')', INK)] if ay > 0 else [])
            w_ = sum(breite(s_, INTER_X, g_) for s_, _ in [('(', 0), (xs, 0), (' | ', 0), (ys, 0), (')', 0)])
            # ganz außerhalb des Kreises, nicht auf Achse, Kreis oder dem Namen P
            if gg == 0:
                lx, ly = CX + R + 14 + w_ / 2, CY - 54
            elif gg == 180:
                lx, ly = CX - R - 14 - w_ / 2, CY - 54
            else:
                lx, ly = CX + 48 + w_ / 2, y + (-34 if gg == 90 else 34)
            x0 = lx - w_ / 2
            for s_, c_ in teile:
                ww = breite(s_, INTER_X, g_)
                b.text(s_, x0 + ww / 2, ly, g_, c_, INTER_X, alpha=a if s_ not in (ys, ' | ', ')') else a * ay)
                x0 += ww
    a45 = ein(t, w('dritte Winkel'), 0.4) * (1 - ein(t, w('Nach Pythagoras'), 0.4))
    if a45 > 0:
        px45, py45 = punkt(45)
        b.linie([(px45 + 34 * math.cos(math.radians(225 + 45 * k / 12)), py45 - 34 * math.sin(math.radians(225 + 45 * k / 12)))
                 for k in range(13)], WINKEL, 5, alpha=a45)
        etikett(b, '45°', px45 - 26, py45 + 62, 22, WINKEL, a45)
    # 30°: Spiegelbild unter der x-Achse → gleichseitiges Dreieck
    sp = ein(t, t30 + 0.4, 0.6) * (1 - ein(t, t60, 0.4))
    if sp > 0:
        px, py = punkt(30)
        qx, qy = punkt(-30)
        b.poly([(CX, CY), (qx, CY), (qx, qy)], fill=WINKEL, alpha=0.10 * sp)
        b.linie([(CX, CY), (qx, qy)], INK, 4, alpha=sp)
        b.kreis(qx, qy, 8, INK, alpha=sp)
        # Begründung (Nutzer 13.11.): Winkel am Ursprung 2 · 30° = 60°, zwei Radien = 1 → gleichschenklig → beide
        # anderen Winkel (180° − 60°) : 2 = 60° → gleichseitig → senkrechte Seite 1, die x-Achse halbiert sie
        weg = 1 - ein(t, t60, 0.4)
        a60 = ein(t, w('zweimal dreißig'), 0.4) * weg * (1 - ein(t, w('Pythagoras liefert'), 0.4))
        if a60 > 0:
            n = 24
            # größerer Radius als der 30°-Bogen, Beschriftung im unteren Dreieck (Nutzer 13.11.: nicht übereinander)
            b.linie([(CX + 140 * math.cos(math.radians(-30 + 60 * k / n)), CY - 140 * math.sin(math.radians(-30 + 60 * k / n)))
                     for k in range(n + 1)], WINKEL, 5, alpha=a60)
            etikett(b, '60°', CX + 112 * math.cos(math.radians(-15)), CY + 112 * math.sin(math.radians(15)), 22, WINKEL, a60,
                    grund=False)
        ar = ein(t, w('Radien'), 0.4) * weg
        if ar > 0:
            for (x1, y1) in ((px, py), (qx, qy)):
                b.linie([(CX, CY), (x1, y1)], WINKEL, 9, alpha=0.55 * ar * (1 - ein(t, w('zwei gleich große'), 0.4)))
                etikett(b, '1', (CX + x1) / 2 - 12, (CY + y1) / 2 + (-26 if y1 < CY else 26), 26, INK, ar, grund=False)
        # dritte Seite (senkrecht von P zum Spiegelpunkt) zuerst zeichnen, dann erst die Winkel daran (Nutzer 13.11.)
        a3 = ein(t, w('Ein Dreieck mit'), 0.4) * weg
        if a3 > 0:
            f3 = glatt(p(t, w('Ein Dreieck mit'), 0.7))
            b.linie([(px, py), (px, py + (qy - py) * f3)], INK, 4, alpha=a3)
        aw = ein(t, w('für jeden'), 0.4) * weg * (1 - ein(t, w('gleichseitiges'), 0.4))
        aw0 = ein(t, w('zwei gleich große'), 0.4) * weg * (1 - ein(t, w('Pythagoras liefert'), 0.4))
        if aw0 > 0:                                        # Winkel an P und am Spiegelpunkt
            for (x1, y1), r0 in (((px, py), 210), ((qx, qy), 90)):
                pts = [(x1 + 30 * math.cos(math.radians(r0 + 60 * k / 12)), y1 - 30 * math.sin(math.radians(r0 + 60 * k / 12)))
                       for k in range(13)]
                b.linie(pts, WINKEL, 5, alpha=aw0)
                if aw > 0:
                    etikett(b, '60°', x1 + 36, y1 + (34 if y1 < CY else -34), 20, WINKEL, aw, anker='l', grund=False)
        ag = ein(t, w('gleichseitiges'), 0.5) * weg
        if ag > 0:
            b.linie([(CX, CY), (px, py), (qx, qy), (CX, CY)], WINKEL, 9, alpha=0.55 * ag)
            # Klammer rechts außen über die ganze senkrechte Seite: „1“ (Nutzer 13.11.: sonst sieht man es nicht)
            xk = CX + R + 46
            b.linie([(xk - 8, py), (xk, py), (xk, qy), (xk - 8, qy)], WINKEL, 3.5, alpha=ag)
            etikett(b, '1', xk + 14, CY - 36, 28, WINKEL, ag, anker='l', grund=False)
        hl = ein(t, w('teilt die senkrechte'), 0.4) * weg
        if hl > 0:
            b.linie([(px, CY), (qx, qy)], SIN, 8, alpha=0.45 * hl)
            for yy in ((CY + py) / 2, (CY + qy) / 2):       # Gleich-lang-Striche auf beiden Hälften
                b.linie([(px - 9, yy - 4), (px + 9, yy + 4)], INK, 3, alpha=hl)
            for yy in ((CY + py) / 2, (CY + qy) / 2):       # außerhalb des Kreises, nicht auf der Kreislinie
                etikett(b, '½', CX + R + 14, yy, 26, SIN, hl, anker='l', grund=False)
        ac3 = ein(t, w('Wurzel drei'), 0.4) * weg
        if ac3 > 0:                                        # √3/2 im oberen Dreieck, nicht auf der unteren Seite
            etikett(b, '√3 / 2', CX + 140, CY - 22, 24, COS, ac3, grund=False)
    # Linien und Dreieck
    zeig = t < w('Genauso') or t > tB - 0.2
    if zeig:
        dreieck_fuell(b, g, teil2 * (1 - ein(t, t30 + 0.2, 0.3)) + ein(t, t60 + 1.2, 0.4))
        lab_s = lab_c = ''
        if t > tB:
            lab_s = lab_c = 'x' if t < t30 else ''
        if t > w('Sinus dreißig'):
            lab_s, lab_c = ('', '') if t < t60 else ('½', '√3 / 2')    # im Spiegel-Teil eigene Beschriftung
        if t > t60 + 1.2:
            lab_s, lab_c = '√3 / 2', '½'
        strecken(b, g, a=1.0, lab_sin=lab_s, lab_cos=lab_c)
    winkel(b, g, 1.0, text=f'{int(round(g)) % 360}°')                 # Nutzer 13.11.: Bogen und Grad immer mitzeigen
    zeiger(b, g)
    for x, y, hell, ax, ay, fx, fy in spaeter:
        if x != CX:
            b.linie([(CX, CY), (CX + (x - CX) * fx, CY)], COS, 9, alpha=hell)
        if y != CY:
            b.linie([(CX, CY), (CX, CY + (y - CY) * fy)], SIN, 9, alpha=hell)
        b.kreis(x if x != CX else CX, CY, 9, COS, alpha=hell * ax)
        b.kreis(CX, y if y != CY else CY, 7 if y == CY else 9, SIN, alpha=hell * ay)
    # rechte Spalte
    zeit_zeile(b, t, w('Die Höhe ist null'), [('Höhe von P', SIN), (' = 0', INK)], 210, 32, INTER, ende=w('Genauso'))
    zeit_zeile(b, t, w('Also ist Sinus'), [('sin', SIN), (' 180° = ', INK), ('0', GRUEN)], 280, 52, ende=w('Genauso'))
    zeit_zeile(b, t, w('Minus eins ist'), [('cos', COS), (' 180° = −1', INK)], 360, 40, ende=w('Genauso'))
    zeit_zeile(b, t, w('Genauso'), [('P(', INK), ('cos α', COS), (' | ', INK), ('sin α', SIN), (')', INK)], 230, 40,
               ende=tA)
    # 45° Schritt für Schritt (Nutzer 13.11.: wie kommt man von 2x² = 1 zu √2 / 2?)
    zeit_zeile(b, t, w('dritte Winkel'), [('180° − 90° − 45° = 45°', WINKEL)], 175, 28, ende=t30)
    zeit_zeile(b, t, w('beide Katheten'), [('→ beide Katheten gleich lang: ', INK), ('x', COS), (' und ', INK), ('x', SIN)],
               220, 26, INTER, ende=t30)
    zeit_zeile(b, t, w('x Quadrat plus'), [('x²', COS), (' + ', INK), ('x²', SIN), (' = 1', INK)], 280, 34, ende=t30)
    zeit_zeile(b, t, w('zwei x Quadrat'), [('2x² = 1', INK)], 325, 30, ende=t30)
    zeit_zeile(b, t, w('Geteilt durch zwei'), [('x² = ½', INK)], 370, 30, ende=t30)
    # echte Brüche, Erweitern animiert (Nutzer 13.11.): 1/√2 · √2/√2 = √2/(√2·√2) → √2/2
    weg45 = 1 - ein(t, t30, 0.4)
    a1 = ein(t, w('Wurzel aus einem halb')) * weg45
    if a1 > 0:
        el = [('t', 'x = √½ = ', INK, 1), ('b', [('1', INK)], [('√2', INK)], 1)]
        formel(b, el, RX - formel(b, el, 0, 0, 30, messen=True) / 2, 425 + 14 * (1 - ein(t, w('Wurzel aus einem halb'))), 30, a1)
    te0, te, te3 = w('Mit Wurzel zwei'), w('erweitert'), w('Wurzel zwei durch zwei', 'erweitert')
    a2 = ein(t, te0) * weg45
    if a2 > 0:
        f3 = ein(t, te3, 0.9)
        el = [('t', 'x = ', INK, 1), ('b', [('1', INK)], [('√2', INK)], 1),
              ('t', ' · ', WINKEL, 1), ('b', [('√2', WINKEL)], [('√2', WINKEL)], 1),
              ('t', ' = ', INK, ein(t, te + 1.0)),
              ('b2', [('√2', GRUEN)], [('√2 · √2', INK)], [('2', GRUEN)], ein(t, te + 1.0), f3),
              ('t', '  ≈ 0,71', GRUEN, ein(t, te3 + 0.6))]
        el0 = [e if e[0] != 'b2' else e[:5] + (0,) for e in el]
        breite_max = formel(b, el0, 0, 0, 30, messen=True)               # fest, damit die Zeile nicht springt
        formel(b, el, RX - breite_max / 2, 510, 30, a2)
    a4 = ein(t, w('ungefähr null Komma sieben') + 0.8) * weg45
    if a4 > 0:
        el = [('t', 'sin', SIN, 1), ('t', ' 45° = ', INK, 1), ('t', 'cos', COS, 1), ('t', ' 45° = ', INK, 1),
              ('b', [('√2', INK)], [('2', INK)], 1)]
        formel(b, el, RX - formel(b, el, 0, 0, 28, messen=True) / 2, 600, 28, a4)
    ende_b = w('gleichseitiges')
    zeit_zeile(b, t, w('zweimal dreißig'), [('Winkel am Ursprung: 2 · 30° = 60°', WINKEL)], 190, 28, INTER, ende=ende_b)
    zeit_zeile(b, t, w('Radien'), [('zwei Seiten = 1', INK)], 240, 28, INTER, ende=ende_b)
    zeit_zeile(b, t, w('zwei gleich große'), [('→ zwei gleiche Winkel', INK)], 285, 28, INTER, ende=ende_b)
    zeit_zeile(b, t, w('hundertzwanzig'), [('(180° − 60°) : 2 = 60°', WINKEL)], 340, 30, ende=ende_b)
    zeit_zeile(b, t, ende_b, [('alle Winkel 60° → alle Seiten 1', WINKEL)], 190, 28, INTER, ende=t60)
    zeit_zeile(b, t, w('Sinus dreißig'), [('sin', SIN), (' 30° = ', INK), ('½', GRUEN)], 260, 46, ende=t60 + 1.2)
    zeit_zeile(b, t, w('Pythagoras liefert'), [('cos', COS), (' 30° = √(1 − ', INK), ('¼', SIN), (')', INK)], 330, 32, INTER, ende=t60 + 1.2)
    zeit_zeile(b, t, w('Wurzel drei'), [('= √3 / 2 ≈ 0,87', GRUEN)], 380, 36, ende=t60 + 1.2)
    zeit_zeile(b, t, t60 + 1.2, [('sin', SIN), (' 60° = √3 / 2', INK)], 260, 40)
    zeit_zeile(b, t, w('tauschen'), [('cos', COS), (' 60° = ½', INK)], 330, 40)


def s_vorzeichen(b, sc, t):
    w = lambda s: C(sc, s)                                  # noqa: E731
    tV = w('Vorzeichen')
    achsen(b)
    # Halbebenen tönen: oben/unten rot, rechts/links blau
    for wort, wort_ende, farbe_, ecken in (
            ('Oben ist', 'unten negativ', SIN, (0, 180)), ('unten negativ', 'Rechts ist', SIN, (180, 360)),
            ('Rechts ist', 'links negativ', COS, (-90, 90)), ('links negativ', None, COS, (90, 270))):
        a = ein(t, w(wort), 0.3) * (1 - (ein(t, w(wort_ende), 0.3) if wort_ende else ein(t, w(wort) + 1.6, 0.4)))
        if a > 0:
            g0, g1 = ecken
            pts = [(CX, CY)] + [punkt(g0 + (g1 - g0) * k / 40) for k in range(41)]
            b.poly(pts, fill=farbe_, alpha=0.13 * a)
    kreislinie(b)
    # Geist bei 30°, P bei 150°
    geist = 1 - ein(t, w('ersten Viertel') + 1.0, 0.5)
    g = bahn(t, [(0, 30), (w('hundertfünfzig') + 0.2, 150)], 1.6)
    dreieck_fuell(b, 30, 0.6 * geist)
    strecken(b, 30, a=0.35 * geist)
    zeiger(b, 30, 0.35 * geist)
    dreieck_fuell(b, g, ein(t, w('gespiegelt'), 0.4) * geist)
    strecken(b, g, lab_sin='½' if t > w('Sinus ein halb') else '', lab_cos='−√3 / 2' if t > w('Kosinus minus') else '')
    winkel(b, g, 1.0, text=f'{int(round(g))}°')
    zeiger(b, g)
    ah = ein(t, w('Gleiche Höhe'), 0.4) * geist
    if ah > 0:
        x0, y0 = punkt(150)
        x1, _ = punkt(30)
        for k in range(0, 24, 2):
            b.linie([(x0 + (x1 - x0) * k / 24, y0), (x0 + (x1 - x0) * (k + 1) / 24, y0)], SIN, 3, alpha=0.8 * ah)
    # Vorzeichen je Viertel
    for i, (gg, sc_, ss) in enumerate(((45, '+', '+'), (135, '−', '+'), (225, '−', '−'), (315, '+', '−'))):
        a = ein(t, tV + 0.25 * i, 0.4)
        if a > 0:
            x, y = punkt(gg, r=R * 1.33)
            band(b, x - 52, y - 22, x + 52, y + 22, '#ffffff', 0.92 * a, r=12)
            zeile(b, [('(', INK), (sc_, COS), (' | ', INK), (ss, SIN), (')', INK)], x, y, 30, INTER_X, alpha=a)
    zeit_zeile(b, t, w('Sinus ein halb'), [('sin', SIN), (' 150° = ½', INK)], 200, 36, ende=tV)
    zeit_zeile(b, t, w('Kosinus minus'), [('cos', COS), (' 150° = −√3 / 2', INK)], 260, 36, ende=tV)
    zeit_zeile(b, t, w('ersten Viertel'), [('Werte aus 0° bis 90° reichen', INK)], 340, 28, INTER, ende=tV)
    zeit_zeile(b, t, w('Oben ist'), [('sin', SIN), (': oben +, unten −', INK)], 230, 36)
    zeit_zeile(b, t, w('Rechts ist'), [('cos', COS), (': rechts +, links −', INK)], 300, 36)


def s_pythagoras(b, sc, t):
    w = lambda s: C(sc, s)                                  # noqa: E731
    g = 50 if t < w('jeden Winkel') else 50 + 60 * (t - w('jeden Winkel'))
    achsen(b)
    kreislinie(b)
    dreieck_fuell(b, g % 360, 1 - ein(t, w('jeden Winkel'), 0.4))
    strecken(b, g % 360, lab_sin='sin α', lab_cos='cos α')
    winkel(b, g % 360, 1.0)
    px, py = zeiger(b, g % 360)
    a1 = 1 - ein(t, w('jeden Winkel'), 0.4)
    if a1 > 0:
        etikett(b, '1', (CX + px) / 2 - 22, (CY + py) / 2 - 14, 28, INK, a1)
    zeit_zeile(b, t, w('Pythagoras sagt'), [('a²', COS), (' + ', GRAU), ('b²', SIN), (' = c²', GRAU)], 220, 34, INTER)
    zeit_zeile(b, t, w('Sinus Quadrat'), [('sin²α', SIN), (' + ', INK), ('cos²α', COS), (' = 1', INK)], 320, 52)
    zeit_zeile(b, t, w('jeden Winkel'), [('für jeden Winkel α', WINKEL)], 410, 30, INTER)


# Kurven-Szene wie der Startbildschirm der App (Nutzer 13.11.): Kreis oben links, Sinus rechts daneben, Kosinus
# darunter (Winkel nach unten); die blaue Kurve kippt danach um 90° auf die Sinus-Achsen
KX, KY, KR = 200, 215, 105
GX0, GX1 = 380, 1190                                       # Sinus: 0° … 360° waagrecht
CY0, CY1 = 392, 668                                        # Kosinus: 0° … 360° senkrecht unter dem Kreis


def gestrichelt(b, x0, y0, x1, y1, c, a=1.0, n=24, lw=2):
    for k in range(0, n, 2):
        b.linie([(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n),
                 (x0 + (x1 - x0) * (k + 1) / n, y0 + (y1 - y0) * (k + 1) / n)], c, lw, alpha=a)


def s_kurve(b, sc, t):
    w = lambda s: C(sc, s)                                  # noqa: E731
    t0, t1 = w('tragen'), w('wiederholt') - 0.2
    tU, tK, tV = w('Unter dem Kreis'), w('Kippen'), w('nach links verschoben')
    g = 360 * klemm((t - t0) / (t1 - t0))
    gx = lambda grad: GX0 + (GX1 - GX0) * grad / 360       # noqa: E731
    cyy = lambda grad: CY0 + (CY1 - CY0) * grad / 360      # noqa: E731
    achsen(b, cx=KX, cy=KY, r=KR)
    kreislinie(b, cx=KX, cy=KY, r=KR)
    # Sinus-Achsen
    b.linie([(GX0, KY), (GX1 + 30, KY)], GRAU, 3.5)
    b.poly([(GX1 + 42, KY), (GX1 + 26, KY - 7), (GX1 + 26, KY + 7)], fill=GRAU)
    b.linie([(GX0, KY + KR + 24), (GX0, KY - KR - 24)], GRAU, 3.5)
    b.poly([(GX0, KY - KR - 36), (GX0 - 7, KY - KR - 20), (GX0 + 7, KY - KR - 20)], fill=GRAU)
    for gg in (90, 180, 270, 360):
        b.linie([(gx(gg), KY - 7), (gx(gg), KY + 7)], GRAU, 3)
        dx_, dy_ = {90: (-24, 22), 180: (-26, 22), 270: (-26, -20), 360: (-26, -20)}[gg]
        etikett(b, f'{gg}°', gx(gg) + dx_, KY + dy_, 18, INK, grund=False)
    for v, s_ in ((1, '1'), (-1, '−1')):
        b.linie([(GX0 - 7, KY - v * KR), (GX0 + 7, KY - v * KR)], GRAU, 3)
        b.text(s_, GX0 - 24, KY - v * KR, 18, INK, INTER_X)
    b.text('α', GX1 + 50, KY + 22, 22, WINKEL, INTER_X, alpha=ein(t, w('Waagrecht')))
    b.text('sin α', GX0 - 46, KY - KR - 30, 22, SIN, INTER_X, alpha=ein(t, w('senkrecht der Sinus')))
    # Kosinus-Achse unter dem Kreis (Winkel nach unten), blendet beim Kippen aus
    kipp = glatt(p(t, tK, 1.8))
    ach = 1 - kipp
    if ach > 0:
        b.linie([(KX, CY0 - 10), (KX, CY1 + 20)], GRAU, 3.5, alpha=ach)
        b.poly([(KX, CY1 + 32), (KX - 7, CY1 + 16), (KX + 7, CY1 + 16)], fill=GRAU, alpha=ach)
        for gg in (90, 180, 270, 360):
            b.linie([(KX - 7, cyy(gg)), (KX + 7, cyy(gg))], GRAU, 3, alpha=ach)
            etikett(b, f'{gg}°', KX - KR - 14, cyy(gg), 18, INK, ach, anker='r', grund=False)
        b.text('α', KX + 22, CY1 + 30, 22, WINKEL, INTER_X, alpha=ach)
    # Sinus (rot) bis zum aktuellen Winkel
    n = int(200 * g / 360)
    if n > 1:
        b.linie([(gx(360 * k / 200), KY - KR * math.sin(2 * math.pi * k / 200)) for k in range(n + 1)], SIN, 6)
    # Kosinus (blau): erst unter dem Kreis, dann gekippt auf die Sinus-Achsen
    th = math.radians(90 * kipp)
    O = (KX + (GX0 - KX) * kipp, CY0 + (KY - CY0) * kipp)
    L = (CY1 - CY0) + ((GX1 - GX0) - (CY1 - CY0)) * kipp
    d = (math.sin(th) * L, math.cos(th) * L)                # Winkel-Richtung: erst nach unten, dann nach rechts
    e = (math.cos(th) * KR, -math.sin(th) * KR)             # Wert-Richtung: erst nach rechts, dann nach oben
    ort = lambda u, v: (O[0] + d[0] * u + e[0] * v, O[1] + d[1] * u + e[1] * v)   # noqa: E731
    # Querachse der Kosinus-Kurve (Nutzer 13.11.: man soll sehen, wo 0 ist): −1 … 1 am oberen Ende, dreht beim Kippen mit
    if ach > 0:
        b.linie([ort(0, -1.25), ort(0, 1.25)], GRAU, 3.5, alpha=ach)
        for v, s_ in ((1, '1'), (-1, '−1'), (0, '0')):
            x_, y_ = ort(0, v)
            b.linie([(x_, y_ - 7), (x_, y_ + 7)], GRAU, 3, alpha=ach)
            if v:
                b.text(s_, x_, y_ - 18, 18, INK, INTER_X, alpha=ach)
        x_, y_ = ort(0, 1.25)
        b.text('cos α', x_ + 30, y_, 20, COS, INTER_X, alpha=ach)
    n = int(200 * g / 360)
    if n > 1:
        b.linie([ort(k / 200, math.cos(2 * math.pi * k / 200)) for k in range(n + 1)], COS, 5)
    aL = ein(t, tU, 0.4)
    if aL > 0:
        x_, y_ = ort(0.5, -1)
        etikett(b, 'cos α', x_, y_ + 30, 22, COS, aL * klemm(2 * kipp - 1), grund=False)
    # Punkt P mit beiden Projektionen
    if t >= t0 and g < 360:
        winkel(b, g, 1.0, text='', cx=KX, cy=KY)
        px, py = punkt(g, KX, KY, KR)
        b.linie([(px, py), (px, KY)], SIN, 8)              # Nutzer 13.11.: dicker
        b.linie([(KX, KY), (px, KY)], COS, 8)
        b.linie([(KX, KY), (px, py)], INK, 3.5)
        b.kreis(px, py, 7, INK)
        gestrichelt(b, px, py, gx(g), py, SIN, 0.6, n=30)
        b.kreis(gx(g), py, 6, SIN)
        gestrichelt(b, px, py, px, cyy(g), COS, 0.6, n=30)
        b.kreis(px, cyy(g), 6, COS)
    etikett(b, 'Sinuskurve', gx(300), KY + KR + 30, 22, SIN, ein(t, w('Welle: die')) * (1 - ein(t, tV, 0.4)), grund=False)
    # Verschiebung: rote Kopie gleitet um 90° nach links auf die blaue Kurve
    av = ein(t, tV, 0.3) * (1 - ein(t, tV + 2.6, 0.6))      # Nutzer 13.11.: nach dem Ankommen bald ausblenden
    if av > 0:
        phi = 90 * glatt(p(t, tV + 0.2, 1.6))
        pts = [(gx(360 * k / 200), KY - KR * math.sin(math.radians(360 * k / 200 + phi))) for k in range(201)]
        for k in range(0, 200, 6):
            b.linie(pts[k:k + 4], SIN, 4, alpha=0.8 * av)
        y = KY - KR - 14
        b.linie([(gx(90), y), (gx(90 - phi), y)], WINKEL, 4, alpha=av)
        if phi > 5:
            b.poly([(gx(90 - phi) - 2, y), (gx(90 - phi) + 12, y - 7), (gx(90 - phi) + 12, y + 7)], fill=WINKEL, alpha=av)
        etikett(b, '90°', gx(45), y - 20, 20, WINKEL, ein(t, tV + 1.0, 0.4) * av)
    for i, wort in enumerate(('Wechselstrom', 'Schall', 'Riesenrad')):
        a = ein(t, w(wort))
        if a > 0:
            x = 460 + 260 * i
            band(b, x, 520, x + 230, 570, '#ffffff', 0.95 * a, r=14)
            b.text(wort, x + 115, 545, 26, INK, INTER_X, alpha=a)


MERK = [  # Nutzer 13.11.: x/Kosinus blau, y/Sinus rot wie im Bild
    ([('Auf dem Einheitskreis ist ', INK), ('x der Kosinus', COS)], [('und ', INK), ('y der Sinus', SIN), ('.', INK)]),
    ([('Sinus Quadrat', SIN), (' plus ', INK), ('Kosinus Quadrat', COS)], [('ist eins.', INK)]),
    ([('Die Werte im ersten Viertel reichen,', INK)], [('die Vorzeichen zeigt das Viertel,', INK)],
     [('in dem P liegt.', INK)])]


def merkzettel(b, sc, t, alle=False):
    karte(b, 640, 120, 590, 460, alpha=1.0, r=22)
    b.text('Merke', 935, 160, 30, TEAL, INTER_X)
    y = 215
    for i, zeilen in enumerate(MERK):
        start = 0 if alle else C(sc, ('Auf dem Einheitskreis', 'Sinus Quadrat', 'Die Werte')[i])
        a = ein(t, start)
        for teile in zeilen:
            if a > 0:
                zeile(b, teile, 935, y + 10 * (1 - a), 25, INTER_X, alpha=a)
            y += 36
        y += 26


def kleiner_kreis(b):
    achsen(b, cx=330, cy=CY, r=170)
    kreislinie(b, cx=330, cy=CY, r=170)
    g = 50
    a = math.radians(g)
    px, py = 330 + 170 * math.cos(a), CY - 170 * math.sin(a)
    b.linie([(330, CY), (px, CY)], COS, 7)
    b.linie([(px, CY), (px, py)], SIN, 7)
    b.linie([(330, CY), (px, py)], INK, 4)
    b.kreis(px, py, 8, INK)
    etikett(b, 'x = cos α', 342, CY + 30, 24, COS, anker='l', grund=False)
    etikett(b, 'y = sin α', 330 + math.sqrt(170 ** 2 - ((py - CY) / 2) ** 2) + 12, (CY + py) / 2, 24, SIN, anker='l', grund=False)


def s_merke(b, sc, t):
    kleiner_kreis(b)
    merkzettel(b, sc, t)


def s_schluss(b, sc, t):
    kleiner_kreis(b)
    merkzettel(b, sc, t, alle=True)
    a = ein(t, 0.1)
    if a > 0:
        band(b, 190, 604 + 10 * (1 - a), 1090, 684 + 10 * (1 - a), TEAL, 0.94 * a, r=20)
        w2 = ein(t, C(sc, 'Übung macht'), 0.5)
        b.text('Nicht sofort alles klar? Ganz normal.', 640, 644, 30, '#ffffff', INTER_X, alpha=a * (1 - klemm(w2 * 2)))
        b.text(SPRUCH, 640, 644, 32, '#ffffff', INTER_X, alpha=a * klemm(w2 * 2 - 1))


_qr = {}


def s_app(b, sc, t):
    a = ein(t, 0.05, 0.6)
    b.text('Kostenlose App', 140, 260 + 12 * (1 - a), 58, INK, INTER_X, anker='l', alpha=a)
    a2 = ein(t, C(sc, 'kostenlosen'))
    b.text('zum Einheitskreis', 140, 330 + 10 * (1 - a2), 46, TEAL, INTER_X, anker='l', alpha=a2)
    aq = ein(t, C(sc, 'Scann'))
    if aq > 0:
        if 'qr' not in _qr:
            _qr['qr'] = Image.open(QR_BILD).convert('RGBA').resize((int(260 * 2),) * 2, Image.NEAREST)
        sp = _qr['qr'].copy()
        sp.putalpha(sp.getchannel('A').point(lambda v: int(v * aq)))
        karte(b, 780, 170, 300, 300, alpha=aq, r=18)
        einfuegen(b.img, sp, 800 * 2, 190 * 2)
        b.text('QR-Code scannen', 930, 510, 30, INK, INTER_X, alpha=aq)


ZEICHNER_NEU = dict(werte=s_werte, vorzeichen=s_vorzeichen, pythagoras=s_pythagoras, kurve=s_kurve, merke=s_merke,
                    schluss=s_schluss, app=s_app)


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
ZEICHNER.update(hook=s_hook, kreis=s_kreis, orientierung=s_orientierung, warum=s_warum, **ZEICHNER_NEU)
KLAENGE = {}
MERKSAETZE = []

G.SZENEN, G.ZEICHNER, G.KLAENGE, G.MERKSAETZE = SZENEN, ZEICHNER, KLAENGE, MERKSAETZE
G.CACHE = os.path.join(HIER, 'tts_cache')

if __name__ == '__main__':
    G.main()
