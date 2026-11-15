#!/usr/bin/env python3
"""Reihe „Mathe verstehen“, Trigonometrie, Video 2: Wofür braucht man Sinus und Kosinus? (14.11., Drehbuch drehbuch.md)

Drei Anwendungen: Leiter an der Wand, Schiffskurs auf der Seekarte (beide: rechtwinkliges Dreieck), Riesenrad
(Kreisbewegung, Höhe über der Zeit). Sprechtext steht nur in drehbuch.md (Zeilen mit „>“ unter „## <n> <id>“).
Baukasten: `../mathe-einmaleins/regel.py` (Ton, Zeitmarken, Kapitelkopf, Rendern) und die Zeichenhilfen aus
`../mathe-einheitskreis/einheitskreis.py` (Formeln mit echten Brüchen, Winkel, Achsen) – beide nur importiert.

Aufruf wie regel.py: python3 sinus_anwendungen.py <ausgabe.mp4> [--nur-ton] [--bild <s>[,<s>…]]
"""
import math, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-einmaleins'))
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-einheitskreis'))
import einheitskreis as E                                  # noqa: E402  (setzt G.* für Video 1; wird unten ersetzt)
import regel as G                                          # noqa: E402
from regel import INK, GRAU, HELL, BG, TEAL, INTER, INTER_X, C, band, ein, karte   # noqa: E402
from animationen import breite, einfuegen, glatt, klemm, mischfarbe, p  # noqa: E402
from einheitskreis import SIN, COS, WINKEL, zeile, formel, etikett, gestrichelt, bahn   # noqa: E402
from motivation import spruch                              # noqa: E402
from PIL import Image                                      # noqa: E402

SPRUCH = spruch('sinus-anwendungen', 'schluss')
QR_BILD = os.path.join(HIER, 'bilder', 'qr_einheitskreis.png')   # …/mathe-videos/einheitskreis/ (Kopie aus Video 1)
STARTBILD = False                                          # startbild.py: letztes Bild des Einstiegs, P bei 50°


def szenen_aus_drehbuch():
    szenen, sc = [], None
    for z in open(os.path.join(HIER, 'drehbuch.md'), encoding='utf-8'):
        m = re.match(r'## \d+ (\w+)', z)
        if m:
            sc = dict(id=m.group(1), text='')
            szenen.append(sc)
        elif z.startswith('>') and sc is not None:
            sc['text'] = (sc['text'] + ' ' + z[1:].strip()).strip()
    return szenen


SZENEN = szenen_aus_drehbuch()
KICKER = {'einstieg': 'Wofür?', 'regel': 'Sinus oder Kosinus?', 'leiter': 'Leiter an der Wand', 'kurs': 'Schiffskurs', 'riesenrad': 'Riesenrad',
          'merke': 'Merke', 'schluss': 'Merke'}
for s in SZENEN:
    s['kicker'] = KICKER[s['id']]
    if s['id'] == 'schluss':
        s['anhang'] = True
    if s['id'] == 'riesenrad':
        s['pause'] = 2.5                                   # Karte mit QR-Code länger stehen lassen
    if s['id'] == 'leiter':
        s['pause'] = 1.6                                   # Vergleich mit dem Einheitskreis kurz stehen lassen
    if s['id'] == 'regel':
        s['pause'] = 2.2                                   # getauschte Seiten kurz stehen lassen


# ---------------------------------------------------------------- Zeichenhilfen
def bogen(b, cx, cy, r, a0, a1, c, lw, a=1.0):
    """Kreisbogen von a0 nach a1 (Grad, mathematisch: 0° rechts, gegen den Uhrzeigersinn)."""
    if a <= 0 or abs(a1 - a0) < 0.3:
        return
    n = max(2, int(abs(a1 - a0) / 3))
    b.linie([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
             for k in range(n + 1)], c, lw, alpha=a)


def rechter_winkel(b, x, y, a0, a=1.0, r=28, b1=0.0, b2=0.0):
    """Viertelbogen mit Punkt (deutsche Schulnotation); a0 = Richtung des ersten Schenkels, der zweite liegt 90° weiter.
    b1, b2: Strichbreiten der beiden Schenkel. Der Bogen sitzt in der inneren Ecke, also an der Kante der dicken
    Striche, nicht auf ihrer Mitte (Nutzer 15.11.: sonst verdeckt der rote Balken ein großes Stück des Zeichens)."""
    if a <= 0:
        return
    u1 = (math.cos(math.radians(a0)), -math.sin(math.radians(a0)))
    u2 = (math.cos(math.radians(a0 + 90)), -math.sin(math.radians(a0 + 90)))
    x, y = x + u2[0] * b1 / 2 + u1[0] * b2 / 2, y + u2[1] * b1 / 2 + u1[1] * b2 / 2
    bogen(b, x, y, r, a0, a0 + 90, INK, 2.5, a)
    m = math.radians(a0 + 45)
    b.kreis(x + 0.45 * r * math.cos(m), y - 0.45 * r * math.sin(m), 3.5, INK, alpha=a)


def strecke(b, x0, y0, x1, y1, c, lw, f=1.0, a=1.0):
    """Strecke, die von (x0, y0) aus wächst (f = 0 … 1)."""
    if f > 0 and a > 0:
        b.linie([(x0, y0), (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)], c, lw, alpha=a)


def masslinie(b, x0, y0, x1, y1, c, a=1.0, lw=2.5, t=8):
    """Maßlinie mit Querstrichen an beiden Enden."""
    if a <= 0:
        return
    b.linie([(x0, y0), (x1, y1)], c, lw, alpha=a)
    d = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / d * t, (x1 - x0) / d * t
    for x, y in ((x0, y0), (x1, y1)):
        b.linie([(x - nx, y - ny), (x + nx, y + ny)], c, lw, alpha=a)


def puls(t, start, dauer=0.7):
    return math.sin(math.pi * klemm((t - start) / dauer)) if t > start else 0.0


def zz(b, t, start, teile, x, y, g=30, pfad=INTER_X, ende=None, anker='m'):
    """Zeile blendet beim gesprochenen Wort ein (und bei `ende` wieder aus)."""
    a = ein(t, start) * (1 - (ein(t, ende, 0.4) if ende is not None else 0))
    if a > 0:
        zeile(b, teile, x, y + 12 * (1 - ein(t, start)), g, pfad, alpha=a, anker=anker)


def zf(b, t, start, el, x, y, g=30, ende=None, anker='m'):
    """Formelzeile mit echten Brüchen; el wie bei `formel`, Alpha je Teil schon eingerechnet."""
    a = ein(t, start) * (1 - (ein(t, ende, 0.4) if ende is not None else 0))
    if a > 0:
        w = formel(b, el, 0, 0, g, messen=True)
        formel(b, el, x - w / 2 if anker == 'm' else x, y + 12 * (1 - ein(t, start)), g, a)


def umformung(b, t, start, el, x, y, g, schritt, ende=None):
    """Umformungsstrich wie im Heft rechts neben einer Gleichung: „| · 5 m“ (Nutzer 15.11.: Auflösen zeigen, nicht nur
    sagen). el, x, y, g wie bei der Gleichung (zentriert bei x), schritt z. B. '· 5 m'."""
    a = ein(t, start) * (1 - (ein(t, ende, 0.4) if ende is not None else 0))
    if a > 0:
        w = formel(b, el, 0, 0, g, messen=True)
        x0 = x + w / 2 + 28
        b.linie([(x0, y - 0.95 * g), (x0, y + 0.95 * g)], GRAU, 2.5, alpha=a)   # so hoch wie der Bruch
        b.text(schritt, x0 + 0.42 * g, y, g * 0.9, GRAU, INTER_X, anker='l', alpha=a)


def T(s, c=INK, a=1.0):
    return ('t', s, c, a)


def B(z, n, a=1.0):
    return ('b', z, n, a)


def _schnitt(A, d, S1, S2):
    """Schnittpunkt des Strahls A + s·d mit der Strecke S1–S2."""
    ex_, ey_ = S2[0] - S1[0], S2[1] - S1[1]
    det = d[0] * (-ey_) - d[1] * (-ex_)
    rx, ry = S1[0] - A[0], S1[1] - A[1]
    s_ = (rx * (-ey_) - ry * (-ex_)) / det
    return A[0] + s_ * d[0], A[1] + s_ * d[1]


def hinweis_gegenueber(b, t, t0, A, w0, w1, seite, rb=48, c=SIN, dauer=2.8, ab=None, pfeil=WINKEL):
    """Nutzer 15.11.: zeigen, dass die Gegenkathete dem Winkel GEGENÜBER liegt. Der Winkelbogen leuchtet auf, ein
    gestrichelter oranger Pfeil läuft vom Winkel quer durchs Dreieck zur gegenüberliegenden Seite, die dann leuchtet.
    w0, w1: Schenkel des Winkels in Grad (mathematisch), seite: die beiden Endpunkte der Gegenkathete; ab: Abstand vom
    Scheitel, an dem der Pfeil beginnt (hinter der Gradzahl, die auf der Winkelhalbierenden steht)."""
    if t < t0 or t > t0 + dauer + 0.6:
        return
    a = 1 - ein(t, t0 + dauer, 0.5)
    bogen(b, A[0], A[1], rb, w0, w1, pfeil, 14, 0.35 * puls(t, t0, 0.9) * a)
    m = math.radians((w0 + w1) / 2)
    d = (math.cos(m), -math.sin(m))
    Q = _schnitt(A, d, *seite)
    L = math.hypot(Q[0] - A[0], Q[1] - A[1])
    s0, s1 = (ab if ab is not None else rb + 10), L - 12
    f = glatt(p(t, t0 + 0.25, 0.8))
    if f > 0 and s1 > s0:
        e = s0 + (s1 - s0) * f
        gestrichelt(b, A[0] + d[0] * s0, A[1] + d[1] * s0, A[0] + d[0] * e, A[1] + d[1] * e, pfeil, a,
                    n=max(4, int((e - s0) / 9)), lw=3.5)
        hx, hy = A[0] + d[0] * (e + 6), A[1] + d[1] * (e + 6)
        nx, ny = -d[1], d[0]
        b.poly([(hx + d[0] * 6, hy + d[1] * 6), (hx - d[0] * 10 + nx * 8, hy - d[1] * 10 + ny * 8),
                (hx - d[0] * 10 - nx * 8, hy - d[1] * 10 - ny * 8)], fill=pfeil, alpha=a)
    hl = math.sin(math.pi * klemm((t - (t0 + 0.9)) / 1.8))
    if hl > 0:
        b.linie(list(seite), c, 24, alpha=0.30 * hl * a)


def hinweis_anliegend(b, t, t0, A, B, w0, w1, rb=48, c=COS, dauer=2.6):
    """Nutzer 15.11.: zeigen, dass die Ankathete AM Winkel liegt: Der Winkelbogen leuchtet auf, ein Leuchten läuft vom
    Scheitel des Winkels an der Ankathete entlang (A = Scheitel, B = anderes Ende)."""
    if t < t0 or t > t0 + dauer + 0.6:
        return
    a = 1 - ein(t, t0 + dauer, 0.5)
    bogen(b, A[0], A[1], rb, w0, w1, WINKEL, 14, 0.35 * puls(t, t0, 0.9) * a)
    b.kreis(A[0], A[1], 13, WINKEL, alpha=0.45 * puls(t, t0, 0.9) * a)
    f = glatt(p(t, t0 + 0.2, 1.0))
    if f > 0:
        b.linie([A, (A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f)], c, 24, alpha=0.30 * a)


def hypotenuse_leuchtet(b, t, t0, A, B, dauer=1.6):
    """Wie im Einheitskreis-Video: Die Hypotenuse leuchtet kurz auf."""
    hl = math.sin(math.pi * klemm((t - t0) / dauer))
    if hl > 0:
        b.linie([A, B], WINKEL, 14, alpha=0.35 * hl)


def etikett_teile(b, teile, x, y, g, a, anker='m'):
    """Beschriftung aus mehreren Farben ohne Papierfeld; anker m, l oder r."""
    if a <= 0:
        return
    w = sum(breite(s_, INTER_X, g) for s_, _ in teile)
    x0 = x - w / 2 if anker == 'm' else (x if anker == 'l' else x - w)
    zeile(b, teile, x0, y, g, INTER_X, alpha=a, anker='l')


def zahlenstrahl(b, x0, x1, y, a, punkte):
    """Zahlenstrahl mit hervorgehobenem Bereich 0 … 1; punkte = [(wert, farbe, name, alpha), …] mit Namen über dem Punkt."""
    if a <= 0:
        return
    b.linie([(x0 - 46, y), (x1 + 46, y)], GRAU, 2.5, alpha=a)
    b.linie([(x0, y), (x1, y)], TEAL, 7, alpha=0.45 * a)
    for v, s_ in ((0, '0'), (1, '1')):
        x = x0 + (x1 - x0) * v
        b.linie([(x, y - 10), (x, y + 10)], INK, 3, alpha=a)
        b.text(s_, x, y + 28, 24, INK, INTER_X, alpha=a)
    for wert, c, name, al in punkte:
        x = x0 + (x1 - x0) * wert
        b.kreis(x, y, 9, c, alpha=a * al)
        b.text(name, x, y - 28, 22, c, INTER_X, alpha=a * al)


def leiste(b, a=1.0):
    band(b, 0, 640, 1280, 720, TEAL, a, r=0)
    b.text('MATHE VERSTEHEN', 60, 680, 30, '#ffffff', INTER_X, anker='l', alpha=a)
    b.text('TRIGONOMETRIE', 1220, 680, 30, '#ffffff', INTER_X, anker='r', alpha=a)


# ---------------------------------------------------------------- 1 Einstieg (Startbild entsteht)
def s_einstieg(b, sc, t):
    tW, tZ = C(sc, 'wofür'), C(sc, 'zwei Sorten')
    tD, tK = C(sc, 'rechtwinkligen Dreieck'), C(sc, 'im Kreis dreht')
    if STARTBILD:
        t = 1e6
    f = glatt(p(t, tZ, 1.1))                               # Kreis wandert nach rechts, das Dreieck nach links
    r = 140
    cx, cy = 640 + 260 * f, 400 + 25 * f
    g = 50.0 if STARTBILD else 50 + 80 * max(0.0, t - tK)
    a0 = ein(t, 0.1, 0.5)
    b.text('Der Einheitskreis', 640, 150, 30, GRAU, INTER_X, alpha=a0 * (1 - ein(t, tW - 0.3, 0.3)))
    E.achsen(b, a0, cx=cx, cy=cy, r=r)
    E.kreislinie(b, glatt(p(t, 0.2, 0.9)), a0, cx=cx, cy=cy, r=r)
    px, py = E.punkt(g, cx, cy, r)
    ap = ein(t, 0.9, 0.4)
    if ap > 0:
        E.winkel(b, g % 360, ap, text='', cx=cx, cy=cy)
        b.linie([(cx, cy), (px, cy)], COS, 10, alpha=ap)
        b.linie([(px, cy), (px, py)], SIN, 10, alpha=ap)
        b.linie([(cx, cy), (px, py)], INK, 5, alpha=ap)
        b.kreis(px, py, 12, INK, alpha=ap)
        al = ein(t, 1.3, 0.4) * (1 - ein(t, tZ - 0.3, 0.3))  # Rückblick auf Video 1: was die Strecken sind
        ym = (py + cy) / 2
        etikett(b, 'sin α', cx + math.sqrt(r * r - (ym - cy) ** 2) + 14, ym, 26, SIN, al, anker='l', grund=False)
        etikett(b, 'cos α', (cx + px) / 2, cy + 30, 26, COS, al, grund=False)
    # Dreieck: startet deckungsgleich im Kreis (P bei 50°) und wächst nach links heraus
    if f > 0:
        q0 = [(640, 400), (640 + r * math.cos(math.radians(50)), 400), E.punkt(50, 640, 400, r)]
        q1 = [(170, 590), (430, 590), (430, 590 - 260 * math.tan(math.radians(50)))]
        A_, B_, C_ = [(u[0] + (v[0] - u[0]) * f, u[1] + (v[1] - u[1]) * f) for u, v in zip(q0, q1)]
        b.poly([A_, B_, C_], fill=WINKEL, alpha=0.10 * f)
        bogen(b, A_[0], A_[1], 48 + 22 * f, 0, 50, WINKEL, 5 + 2 * f, f)
        b.linie([A_, B_], COS, 10, alpha=f)
        b.linie([B_, C_], SIN, 10, alpha=f)
        b.linie([A_, C_], INK, 5 + f, alpha=f)
        rechter_winkel(b, B_[0], B_[1], 90, ein(t, tD, 0.4), r=34, b1=10, b2=10)
    b.text('Wofür braucht man', 640, 56 + 12 * (1 - ein(t, tW)), 44, INK, INTER_X, alpha=ein(t, tW))
    a2 = ein(t, tW + 0.35)
    zeile(b, [('Sinus', SIN), (' und ', INK), ('Kosinus', COS), ('?', INK)], 640, 112 + 12 * (1 - a2), 58, INTER_X, alpha=a2)
    aD, aK = ein(t, tD), ein(t, tK)
    zeile(b, [('Dreieck: ', INK), ('Längen ausrechnen', GRAU)], 300, 192 + 8 * (1 - aD), 26, INTER_X, alpha=aD)
    zeile(b, [('Kreis: ', INK), ('was sich dreht', GRAU)], 900, 192 + 8 * (1 - aK), 26, INTER_X, alpha=aK)
    leiste(b, ein(t, 0.2, 0.5))


# ---------------------------------------------------------------- 2 Regel: Sinus gegenüber, Kosinus am Winkel
RA, RC, RB = (130, 590), (530, 590), (530, 290)            # 3-4-5-Dreieck: α bei A, rechter Winkel bei C
RX_ = 1005                                                 # Mitte der rechten Spalte
ALPHA_R = math.degrees(math.atan2(300, 400))               # 36,87°


def s_regel(b, sc, t):
    """Nutzer 15.11.: „Das Allerwichtigste: Sinus gegenüber vom Winkel, Kosinus am Winkel“ – eigene Szene vor den
    Beispielen. Die Seiten bekommen ihren Namen nur aus der Lage zu α; am Ende wandert α in die andere Ecke und die
    Rollen tauschen (Vorbereitung auf den Schiffskurs: nicht waagrecht/senkrecht entscheidet, sondern der Winkel)."""
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    tW, tH, tGK = w('wo der Winkel'), w('Gegenüber vom rechten'), w('Gegenüber von Alpha')
    tS, tAn, tAK = w('Für sie brauchst'), w('An Alpha liegen'), w('und die Ankathete')
    tK, tKurz, tKg = w('Für die Ankathete'), w('Kurz:'), w('Kathete am Winkel')
    tT, tPl = w('Sitzt Alpha'), w('die Plätze')
    A, Cc, Bp = RA, RC, RB
    f = glatt(p(t, tT + 0.4, 1.4))                         # Tausch: α wandert von A nach B
    fG, fA = glatt(p(t, tGK + 0.6, 0.6)), glatt(p(t, tAK, 0.6))
    # Dreieck, rechter Winkel
    a0 = ein(t, 0.1, 0.5)
    b.poly([A, Cc, Bp], fill=WINKEL, alpha=0.08 * a0)
    c_bc = mischfarbe(mischfarbe(INK, SIN, fG), COS, f)    # erst schwarz, dann rot (gegenüber), nach dem Tausch blau
    c_ac = mischfarbe(mischfarbe(INK, COS, fA), SIN, f)
    w_bc, w_ac = 5 + 4 * fG, 5 + 4 * fA
    b.linie([Cc, Bp], c_bc, w_bc, alpha=a0)
    b.linie([A, Cc], c_ac, w_ac, alpha=a0)
    b.linie([A, Bp], INK, 6, alpha=a0)
    rechter_winkel(b, Cc[0], Cc[1], 90, a0, r=34, b1=w_bc, b2=w_ac)
    # Winkel α: erst bei A, beim Tausch bei B
    aw = ein(t, tW, 0.4)
    bogen(b, A[0], A[1], 70, 0, ALPHA_R, WINKEL, 6, aw * (1 - f))
    m = math.radians(ALPHA_R / 2)
    b.text('α', A[0] + 104 * math.cos(m), A[1] - 104 * math.sin(m), 32, WINKEL, INTER_X, alpha=aw * (1 - f))
    w0B = 180 + ALPHA_R
    bogen(b, Bp[0], Bp[1], 70, w0B, 270, WINKEL, 6, f)
    mB = math.radians((w0B + 270) / 2)
    b.text('α', Bp[0] + 100 * math.cos(mB), Bp[1] - 100 * math.sin(mB), 32, WINKEL, INTER_X, alpha=f)
    # Hypotenuse: gegenüber vom rechten Winkel (schwarzer Pfeil), Name gedreht entlang der Seite
    hinweis_gegenueber(b, t, tH, Cc, 90, 180, (A, Bp), rb=34, c=INK, ab=56, pfeil=INK, dauer=2.4)
    aH = ein(t, tH + 0.9)
    ux, uy = (Bp[0] - A[0]) / 500, (Bp[1] - A[1]) / 500
    nx, ny = uy, -ux                                       # Normale nach links oben (außerhalb)
    mx_, my_ = (A[0] + Bp[0]) / 2, (A[1] + Bp[1]) / 2
    b.text('Hypotenuse', mx_ + nx * 28, my_ + ny * 28, 28, INK, INTER_X, alpha=aH, dreh=ALPHA_R)
    b.text('gegenüber vom rechten Winkel', mx_ + nx * 60, my_ + ny * 60, 18, GRAU, INTER_X, alpha=aH * (1 - ein(t, tAn, 0.4)),
           dreh=ALPHA_R)
    # Gegenkathete: gegenüber von α (oranger Pfeil), wird rot
    hinweis_gegenueber(b, t, tGK, A, 0, ALPHA_R, (Cc, Bp), rb=70, ab=130, dauer=2.6)
    aG = ein(t, tGK + 0.8)
    for txt, gr, dy, c, al in (('Gegenkathete', 28, -14, SIN, aG * (1 - f)), ('gegenüber von α', 20, 20, GRAU, aG * (1 - f)),
                               ('Ankathete', 28, -14, COS, f), ('an α', 20, 20, GRAU, f)):
        etikett(b, txt, Cc[0] + 22, (Cc[1] + Bp[1]) / 2 + dy, gr, c, al, anker='l', grund=False)
    # An α liegen zwei Seiten: die Hypotenuse und die Ankathete
    hypotenuse_leuchtet(b, t, tAn + 0.5, A, Bp, 1.4)
    hinweis_anliegend(b, t, tAK, A, Cc, 0, ALPHA_R, rb=70, dauer=2.4)
    aA = ein(t, tAK + 0.6)
    for txt, gr, dy, c, al in (('Ankathete', 28, 34, COS, aA * (1 - f)), ('an α', 20, 64, GRAU, aA * (1 - f)),
                               ('Gegenkathete', 28, 34, SIN, f), ('gegenüber von α', 20, 64, GRAU, f)):
        etikett(b, txt, (A[0] + Cc[0]) / 2, A[1] + dy, gr, c, al, grund=False)
    # nach dem Tausch: Pfeil von der neuen Ecke zur neuen Gegenkathete (unten)
    hinweis_gegenueber(b, t, tT + 1.6, Bp, w0B, 270, (A, Cc), rb=70, ab=124, dauer=2.4)
    # rechte Spalte: die Regel
    zz(b, t, 0.2, [('Sinus', SIN), (' oder ', INK), ('Kosinus', COS), ('?', INK)], RX_, 150, 44)
    zz(b, t, tW, [('Das entscheidet die Lage zum Winkel ', GRAU), ('α', WINKEL), ('.', GRAU)], RX_, 204, 22, INTER)
    for y, t0 in ((262, tS), (392, tK)):
        hl = puls(t, tKurz + (0 if y == 262 else 1.6), 1.2)
        if hl > 0:
            band(b, RX_ - 235, y - 25, RX_ + 235, y + 25, TEAL, 0.14 * hl, r=14)
    zz(b, t, tS, [('Kathete gegenüber', SIN), ('  →  ', GRAU), ('Sinus', SIN)], RX_, 262, 32)
    zz(b, t, tS + 0.6, [('Gegenkathete', SIN), (' = Hypotenuse · ', INK), ('sin α', SIN)], RX_, 310, 26)
    zz(b, t, tK, [('Kathete am Winkel', COS), ('  →  ', GRAU), ('Kosinus', COS)], RX_, 392, 32)
    zz(b, t, tK + 0.6, [('Ankathete', COS), (' = Hypotenuse · ', INK), ('cos α', COS)], RX_, 440, 26)
    zz(b, t, tT + 0.4, [('α', WINKEL), (' in der anderen Ecke: Rot und Blau tauschen', INK)], RX_, 530, 23)
    zz(b, t, tPl, [('Es zählt die Lage zum Winkel,', GRAU)], RX_, 570, 20, INTER)
    zz(b, t, tPl, [('nicht waagrecht oder senkrecht.', GRAU)], RX_, 598, 20, INTER)


# ---------------------------------------------------------------- 3 Leiter an der Wand
LM = 96                                                    # Bildpunkte je Meter
FX, FY = 170, 610                                          # Leiterfuß (wie der Ursprung im Einheitskreis)
WX = FX + 5 * math.cos(math.radians(70)) * LM              # Wand
TY = FY - 5 * math.sin(math.radians(70)) * LM              # oberes Ende der Leiter
LX = 920                                                   # Mitte der Rechenspalte


def s_leiter(b, sc, t):
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    tL, tW_, tH = w('fünf Meter lang'), w('siebzig Grad'), w('Wie hoch')
    tD, tHy, tG = w('rechtwinkliges Dreieck'), w('Die Leiter liegt gegenüber'), w('Gegenkathete durch')
    tGg, tGgW, tMs = w('Die Höhe an der Wand'), w('gegenüber vom Siebzig'), w('Kathete gegenüber')
    tA, tM, tT1 = w('also Sinus siebzig'), w('Dann ist die Höhe'), w('Der Taschenrechner')
    tU1 = w('multiplizieren beide Seiten')
    tW1, tZ01, tKa = w('ungefähr null Komma neun'), w('zwischen null und eins'), w('eine Kathete ist')
    tR1, tE1 = w('Fünf Meter mal null Komma'), w('sind vier Meter siebzig')
    tK, tB, tT2 = w('Und der Abstand zur Wand'), w('Der Abstand ist also'), w('Kosinus siebzig Grad ist')
    tAnW, tMk = w('am Siebzig-Grad-Winkel an'), w('Kathete am Winkel')
    tRW = w('Wand und Boden bilden')                       # Nutzer 15.11.: zuerst sagen und zeigen, wo der rechte Winkel ist
    tW2, tE2 = w('ungefähr null Komma drei'), w('das ergibt ein Meter')
    tEK = w('Es ist das Dreieck')
    tHy1, tAk = w('Hypotenuse'), w('Ankathete durch')
    # Wand und Boden
    a0 = ein(t, 0.0, 0.4)
    band(b, WX, 120, WX + 28, FY, '#d9d2c3', a0, r=0)
    b.linie([(50, FY), (560, FY)], INK, 3.5, alpha=a0)
    # Dreiecksfläche, rechter Winkel
    aD = ein(t, tD, 0.5)
    b.poly([(FX, FY), (WX, FY), (WX, TY)], fill=WINKEL, alpha=0.10 * aD)
    aRW = ein(t, tRW + 0.4, 0.4)
    hl = puls(t, tRW + 0.2, 1.8)                           # Wand und Boden leuchten an der Ecke auf
    if hl > 0:
        b.linie([(WX - 150, FY), (WX, FY), (WX, FY - 150)], INK, 16, alpha=0.18 * hl)
    rechter_winkel(b, WX, FY, 90, aRW, r=28 + 10 * puls(t, tRW + 0.5, 1.0),
                   b1=8, b2=3.5 + 4.5 * glatt(p(t, tK, 0.7)))   # erst Bodenlinie, dann blaue Strecke
    # Höhe (rot, an der Wand) und Abstand (blau, am Boden)
    strecke(b, WX, FY, WX, TY, SIN, 8 + 4 * puls(t, tMs), glatt(p(t, tGg, 0.7)))
    strecke(b, FX, FY, WX, FY, COS, 8 + 4 * puls(t, tMk), glatt(p(t, tK, 0.7)))
    # Leiter: wird angelehnt (wächst vom Fuß aus), mit Sprossen
    fl = glatt(p(t, 0.25, 1.0))
    strecke(b, FX, FY, WX, TY, INK, 6, fl)
    dx, dy = math.cos(math.radians(70)), -math.sin(math.radians(70))
    for k in range(1, 10):
        if fl * 10 >= k:
            x, y = FX + (WX - FX) * k / 10, FY + (TY - FY) * k / 10
            b.linie([(x + 9 * dy, y - 9 * dx), (x - 9 * dy, y + 9 * dx)], INK, 3)
    E.winkel(b, 70 * glatt(p(t, tW_, 0.8)), ein(t, tW_, 0.3), text='70°' if t > tW_ + 0.6 else '', cx=FX, cy=FY)
    # Wo liegt was? (Nutzer 15.11.) Hypotenuse leuchtet, Gegenkathete gegenüber vom Winkel, Ankathete am Winkel
    hypotenuse_leuchtet(b, t, tHy1, (FX, FY), (WX, TY))
    hinweis_gegenueber(b, t, tHy, (WX, FY), 90, 180, ((FX, FY), (WX, TY)), rb=28, c=INK, ab=40, pfeil=INK, dauer=2.4)
    hinweis_gegenueber(b, t, tGgW, (FX, FY), 0, 70, ((WX, FY), (WX, TY)), ab=114)
    hinweis_anliegend(b, t, tAnW, (FX, FY), (WX, FY), 0, 70)
    # Beschriftungen neben den Strecken, nie darauf
    aHy = ein(t, tHy)
    etikett(b, 'Hypotenuse', 232, 352 - 30 * aHy, 22, INK, aHy, anker='r', grund=False)
    etikett(b, '5 m', 232, 352 + 6 * aHy, 28, INK, ein(t, tL), anker='r', grund=False)
    aF = ein(t, tH) * (1 - ein(t, tGg, 0.3))               # Frage: wie hoch?
    nah = ein(t, tGg + 0.7, 0.4)                           # Maßlinie weicht der roten Strecke, die Schrift rückt heran
    masslinie(b, WX + 54, FY, WX + 54, TY, SIN, ein(t, tH) * (1 - nah), lw=2.5)
    etikett(b, '?', WX + 84, (FY + TY) / 2, 44, SIN, aF, grund=False)
    lx = WX + 70 - 26 * nah
    aG = ein(t, tGg) * (1 - ein(t, tE1, 0.3))
    etikett(b, 'Höhe', lx, (FY + TY) / 2 - 14, 28, SIN, aG, anker='l', grund=False)
    aGK = ein(t, tGgW + 0.6) * (1 - ein(t, tE1, 0.3))
    etikett(b, 'Gegenkathete', lx, (FY + TY) / 2 + 20, 20, SIN, aGK, anker='l', grund=False)
    etikett_teile(b, [('gegenüber vom Winkel', GRAU), (' → ', GRAU), ('Sinus', SIN)], lx, (FY + TY) / 2 + 46, 18,
                  ein(t, tMs) * (1 - ein(t, tE1, 0.3)), anker='l')
    etikett(b, '≈ 4,70 m', lx, (FY + TY) / 2, 30, SIN, ein(t, tE1 + 0.3), anker='l', grund=False)
    aAn = ein(t, tK) * (1 - ein(t, tE2, 0.3))
    etikett(b, 'Abstand (Ankathete)', (FX + WX) / 2, FY + 34, 20, COS, aAn, grund=False)
    etikett_teile(b, [('am Winkel', GRAU), (' → ', GRAU), ('Kosinus', COS)], (FX + WX) / 2, FY + 58, 18,
                  ein(t, tMk) * (1 - ein(t, tE2, 0.3)))
    etikett(b, '≈ 1,71 m', (FX + WX) / 2, FY + 36, 28, COS, ein(t, tE2 + 0.3), grund=False)
    # rechts zuerst, was gegeben und gesucht ist; dann die Rechnung Zeile für Zeile; am Ende der Einheitskreis
    vor = tG - 0.4
    zz(b, t, tL, [('Leiter: ', GRAU), ('5 m', INK)], LX, 250, 34, ende=vor)
    zz(b, t, tW_, [('Winkel: ', GRAU), ('70°', WINKEL)], LX, 312, 34, ende=vor)
    zz(b, t, tH, [('Höhe: ', GRAU), ('?', SIN)], LX, 374, 34, ende=vor)
    # Teil 1 (Sinus): Herleitung, Zahlenwert vom Taschenrechner, Ergebnis. Teil 2 (Kosinus) ab tK: Die Herleitung
    # weicht, das Ergebnis rückt nach oben, darunter derselbe Weg für den Abstand. Der Zahlenstrahl bleibt stehen.
    weg, g = tEK, 30
    zf(b, t, tG, [T('sin α', SIN), T(' = '), B([('Gegenkathete', SIN)], [('Hypotenuse', INK)])], LX, 150, g, tK - 0.2)
    el_s = [T('sin 70°', SIN), T(' = '), B([('Höhe', SIN)], [('5 m', INK)])]
    zf(b, t, tA, el_s, LX, 236, g, tK - 0.2)
    umformung(b, t, tU1, el_s, LX, 236, g, '· 5 m', tK - 0.2)
    zf(b, t, tM, [T('Höhe', SIN), T(' = 5 m · '), T('sin 70°', SIN)], LX, 316, g, tK - 0.2)
    zf(b, t, tT1, [T('Taschenrechner:  ', GRAU), T('sin 70°', SIN), T(' ≈ ', INK, ein(t, tW1)), T('0,940', SIN, ein(t, tW1))],
       LX, 372, 26, tK - 0.2)
    hoch = glatt(p(t, tK, 0.7))
    e1 = ein(t, tE1)
    zf(b, t, tR1, [T('Höhe', SIN), T(' ≈ 5 m · '), T('0,940', SIN), T(' = ', INK, e1), T('4,70 m', SIN, e1)],
       LX, 430 - 280 * hoch, g, weg)
    el_c = [T('cos 70°', COS), T(' = '), B([('Abstand', COS)], [('5 m', INK)])]
    zf(b, t, max(tK + 0.7, tAk), el_c, LX, 236, g, weg)
    umformung(b, t, tB, el_c, LX, 236, g, '· 5 m', weg)
    zf(b, t, tB, [T('Abstand', COS), T(' = 5 m · '), T('cos 70°', COS)], LX, 316, g, weg)
    zf(b, t, tT2, [T('Taschenrechner:  ', GRAU), T('cos 70°', COS), T(' ≈ ', INK, ein(t, tW2)), T('0,342', COS, ein(t, tW2))],
       LX, 372, 26, weg)
    e2 = ein(t, tE2)
    zf(b, t, tW2 + 1.2, [T('Abstand', COS), T(' ≈ 5 m · '), T('0,342', COS), T(' = ', INK, e2), T('1,71 m', COS, e2)], LX, 430, g, weg)
    aZ = ein(t, tZ01 - 0.3) * (1 - ein(t, weg, 0.4))
    zahlenstrahl(b, 700, 1140, 510, aZ, [(0.940, SIN, 'sin 70°', 1.0), (0.342, COS, 'cos 70°', ein(t, tW2))])
    zz(b, t, tZ01, [('im rechtwinkligen Dreieck: ', GRAU), ('immer zwischen 0 und 1', TEAL)], LX, 576, 24, ende=weg)
    zz(b, t, w('Strecken sind nie'), [('Strecken sind nie negativ,', GRAU)], LX, 614, 21, INTER, ende=weg)
    zz(b, t, tKa, [('eine Kathete ist immer kürzer als die Hypotenuse.', GRAU)], LX, 644, 21, INTER, ende=weg)
    # Vergleich: dasselbe Dreieck im Einheitskreis (Hypotenuse 1), mal 5
    aE = ein(t, tEK + 0.3, 0.6)
    if aE > 0:
        cx, cy, r = 800, 430, 150
        zz(b, t, tEK + 0.3, [('Das Dreieck aus dem Einheitskreis,', INK)], LX, 122, 28)
        zz(b, t, w('nur fünfmal'), [('nur fünfmal so groß', TEAL)], LX, 162, 28)
        E.achsen(b, aE, cx=cx, cy=cy, r=r)
        E.kreislinie(b, 1.0, aE, cx=cx, cy=cy, r=r)
        px, py = E.punkt(70, cx, cy, r)
        viertel = [(cx, cy)] + [E.punkt(90 * k / 30, cx, cy, r) for k in range(31)]
        b.poly(viertel, fill=TEAL, alpha=0.10 * aE)          # erstes Viertel: beide Werte zwischen 0 und 1
        b.poly([(cx, cy), (px, cy), (px, py)], fill=WINKEL, alpha=0.10 * aE)
        # 70° ist zu schmal für eine Zahl im Winkel (steht rechts); Bogen klein, damit er den rechten Winkel nicht berührt
        bogen(b, cx, cy, 26, 0, 70, WINKEL, 5, aE)
        rechter_winkel(b, px, cy, 90, aE, r=16, b1=8, b2=8)
        b.linie([(cx, cy), (px, cy)], COS, 8, alpha=aE)
        b.linie([(px, cy), (px, py)], SIN, 8, alpha=aE)
        b.linie([(cx, cy), (px, py)], INK, 4, alpha=aE)
        b.kreis(px, py, 9, INK, alpha=aE)
        x = 1128
        zz(b, t, tEK + 0.5, [('Winkel ', INK), ('70°', WINKEL), (', Radius 1', INK)], x, 268, 24)
        zz(b, t, tEK + 0.8, [('sin 70° ≈ 0,940', SIN)], x, 346, 26)
        zz(b, t, w('nur fünfmal') + 0.3, [('mal 5: ', INK), ('≈ 4,70 m', SIN)], x, 386, 26)
        zz(b, t, tEK + 1.1, [('cos 70° ≈ 0,342', COS)], x, 468, 26)
        zz(b, t, w('nur fünfmal') + 0.6, [('mal 5: ', INK), ('≈ 1,71 m', COS)], x, 508, 26)
        zz(b, t, w('nur fünfmal') + 1.0, [('erstes Viertel:', TEAL)], x, 574, 20)
        zz(b, t, w('nur fünfmal') + 1.0, [('beide Werte zwischen 0 und 1', TEAL)], x, 600, 20)


# ---------------------------------------------------------------- 3 Schiffskurs auf der Seekarte
SEE, GITTER, LAND, UFER = '#e3eef5', '#c3d5e2', '#eadfbf', '#b4a57c'
MX0, MY0, MX1, MY1 = 50, 92, 640, 650                      # Kartenrand
KM = 46                                                    # Bildpunkte je Kilometer (1 Kästchen = 1 km)
HX, HY = 160, 530                                          # Hafen
ZX, ZY = HX + 10 * math.sin(math.radians(60)) * KM, HY - 10 * math.cos(math.radians(60)) * KM   # Insel (Ziel)
KX = 958                                                   # Mitte der Rechenspalte


def bezier(p0, p1, p2, p3, n=24):
    return [tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b_ + 3 * (1 - u) * u * u * c + u ** 3 * d
                  for a, b_, c, d in zip(p0, p1, p2, p3)) for u in (k / n for k in range(n + 1))]


KUESTE = bezier((MX0, 474), (95, 474), (128, 494), (HX, HY)) + bezier((HX, HY), (194, 564), (236, 604), (300, MY1))[1:]


def seekarte(b, a=1.0):
    """Oben Norden, 1 Kästchen = 1 km: Festland mit Hafen unten links, Insel mit Leuchtturm am Ziel."""
    if a <= 0:
        return
    band(b, MX0, MY0, MX1, MY1, SEE, a, r=0)
    k = -2
    while HX + KM * k < MX1:
        b.linie([(HX + KM * k, MY0), (HX + KM * k, MY1)], GITTER, 1.2, alpha=a)
        k += 1
    k = -2
    while HY - KM * k > MY0:
        b.linie([(MX0, HY - KM * k), (MX1, HY - KM * k)], GITTER, 1.2, alpha=a)
        k += 1
    b.poly(KUESTE + [(MX0, MY1)], fill=LAND, alpha=a)
    b.linie(KUESTE, UFER, 2.5, alpha=a)
    b.text('Hafen', 104, 604, 22, INK, INTER_X, alpha=a)
    # Insel mit Leuchtturm
    ix, iy = 598, 266
    b.d.ellipse([(ix - 37) * 2, (iy - 27) * 2, (ix + 37) * 2, (iy + 27) * 2], fill=G.farbe(UFER, 255 * a))
    b.d.ellipse([(ix - 35) * 2, (iy - 25) * 2, (ix + 35) * 2, (iy + 25) * 2], fill=G.farbe(LAND, 255 * a))
    b.poly([(ix + 2, iy + 8), (ix + 14, iy + 8), (ix + 11, iy - 16), (ix + 5, iy - 16)], fill='#ffffff', outline=INK, lw=1.5, alpha=a)
    band(b, ix + 4, iy - 23, ix + 12, iy - 16, INK, a, r=1)
    b.text('Insel', ix, iy - 44, 22, INK, INTER_X, alpha=a)
    # Kompassrose
    cx, cy = 96, 146
    b.kreis(cx, cy, 25.5, INK, alpha=a)
    b.kreis(cx, cy, 23.5, '#ffffff', alpha=a)
    b.poly([(cx, cy - 20), (cx - 7, cy), (cx + 7, cy)], fill=INK, alpha=a)
    b.poly([(cx, cy + 20), (cx - 7, cy), (cx + 7, cy)], fill='#ffffff', outline=INK, lw=1.2, alpha=a)
    b.text('N', cx, cy - 39, 20, INK, INTER_X, alpha=a)
    # Maßstab: 5 km
    sx, sy = 372, 628
    b.linie([(sx, sy), (sx + 5 * KM, sy)], INK, 3, alpha=a)
    for k in range(6):
        b.linie([(sx + KM * k, sy - 6), (sx + KM * k, sy + 6)], INK, 2.5, alpha=a)
    b.text('0', sx, sy - 20, 18, INK, INTER, alpha=a)
    b.text('5 km', sx + 5 * KM, sy - 20, 18, INK, INTER, alpha=a)
    b.linie([(MX0, MY0), (MX1, MY0), (MX1, MY1), (MX0, MY1), (MX0, MY0)], INK, 2.5, alpha=a)


def schiff(b, x, y, a=1.0):
    """Schiff von oben, Bug in Fahrtrichtung (Kurs 60°)."""
    if a <= 0:
        return
    dx, dy = math.sin(math.radians(60)), -math.cos(math.radians(60))
    q = lambda u, v: (x + u * dx - v * dy, y + u * dy + v * dx)   # noqa: E731
    b.poly([q(-22, -9), q(8, -9), q(24, 0), q(8, 9), q(-22, 9)], fill='#ffffff', outline=INK, lw=2.5, alpha=a)
    b.poly([q(-12, -5), q(0, -5), q(0, 5), q(-12, 5)], fill=INK, alpha=a)


def s_kurs(b, sc, t):
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    tS, tK0, tI, tQ = w('fährt vom Hafen'), w('zehn Kilometer'), w('zu einer Insel'), w('Wie weit liegt')
    tN, tU = w('von Norden aus'), w('im Uhrzeigersinn')
    tGN, tGO, tR = w('erst nach Norden'), w('dann nach Osten'), w('wieder ein rechtwinkliges')
    tGg, tO1, tT1 = w('gegenüber'), w('zehn Kilometer mal Sinus'), w('Sinus sechzig Grad ist')
    tW1, tZ01, tO2 = w('ungefähr null Komma acht'), w('wieder ein Wert'), w('Das ergibt ungefähr')
    tAn, tN1, tT2 = w('liegt am Kurswinkel an'), w('zehn Kilometer mal Kosinus'), w('Kosinus sechzig Grad ist')
    tHyK, tMs, tMk, tZaehlt = w('Die Fahrstrecke ist'), w('Kathete gegenüber'), w('Kathete am'), w('Es zählt nicht')
    tW2, tN2 = w('genau null Komma fünf'), w('also fünf Kilometer')
    tAch = w('Achtung')
    seekarte(b, ein(t, 0.0, 0.4))
    ex, ey = HX, ZY                                        # Ecke mit dem rechten Winkel
    aR = ein(t, tR, 0.5)
    b.poly([(HX, HY), (ex, ey), (ZX, ZY)], fill=WINKEL, alpha=0.14 * aR)
    # Nordlinie (gestrichelt), erst wenn vom Kurs die Rede ist
    aN = ein(t, tN, 0.4)
    if aN > 0:
        gestrichelt(b, HX, HY, HX, ZY - 46, GRAU, aN, n=22, lw=2.5)
    # Fahrstrecke und Schiff
    fs = glatt(p(t, tS, max(1.5, tI + 0.4 - tS)))
    strecke(b, HX, HY, ZX, ZY, INK, 5, fs)
    # Nord- und Oststrecke
    strecke(b, HX, HY, ex, ey, COS, 8 + 4 * puls(t, tMk), glatt(p(t, tGN, 0.8)))
    strecke(b, ex, ey, ZX, ZY, SIN, 8 + 4 * puls(t, tMs) + 4 * puls(t, tAch + 0.6), glatt(p(t, tGO, 0.9)))
    rechter_winkel(b, ex, ey, 270, aR, r=28 + 10 * puls(t, tR + 0.3, 1.0), b1=8, b2=8)
    # Wo liegt was? (Nutzer 15.11.) wie bei der Leiter
    hypotenuse_leuchtet(b, t, tHyK, (HX, HY), (ZX, ZY))
    hinweis_gegenueber(b, t, tGg, (HX, HY), 30, 90, ((ex, ey), (ZX, ZY)), rb=62, ab=124)
    hinweis_anliegend(b, t, tAn, (HX, HY), (ex, ey), 30, 90, rb=62)
    # Kurswinkel: von der Nordlinie im Uhrzeigersinn bis zur Fahrstrecke
    fu = glatt(p(t, tU, 1.0))
    bogen(b, HX, HY, 62, 90, 90 - 60 * fu, WINKEL, 5 + 3 * puls(t, tAch + 0.2), ein(t, tU, 0.2))
    etikett(b, '60°', HX + 100 * math.cos(math.radians(62)), HY - 100 * math.sin(math.radians(62)), 24, WINKEL,
            ein(t, tU + 0.8), grund=False)
    b.kreis(HX, HY, 7, INK, alpha=ein(t, tS - 0.2, 0.3))
    b.kreis(ZX, ZY, 7, INK, alpha=ein(t, tI + 0.3, 0.3))
    schiff(b, HX + (ZX - HX) * fs, HY + (ZY - HY) * fs, ein(t, tS - 0.3, 0.3) * (1 - ein(t, tGN - 0.5, 0.4)))
    # Beschriftungen neben den Strecken
    etikett(b, '10 km', HX + (ZX - HX) * 0.56 + 22, HY + (ZY - HY) * 0.56 + 34, 24, INK, ein(t, tI + 0.4), anker='l', grund=False)
    etikett(b, 'Hypotenuse', HX + (ZX - HX) * 0.56 + 22, HY + (ZY - HY) * 0.56 + 60, 18, INK, ein(t, tHyK + 0.3), anker='l', grund=False)
    etikett_teile(b, [('gegenüber vom Winkel', GRAU), (' → ', GRAU), ('Sinus', SIN)], (ex + ZX) / 2, ey - 52, 18,
                  ein(t, tMs) * (1 - ein(t, tO2 + 0.6, 0.4)))
    aKw = ein(t, tMk) * (1 - ein(t, tN2, 0.4))
    # links neben der Nordstrecke ist kein Platz (Kartenrand, Küste): innen rechts daneben, unter dem rechten Winkel
    etikett_teile(b, [('am Winkel', GRAU), (' → ', GRAU), ('Kosinus', COS)], HX + 14, ey + 62, 18, aKw, anker='l')
    aNo = ein(t, tGN + 0.5)
    hoch = 14 * ein(t, tN2)
    etikett(b, 'Norden', HX - 14, (HY + ey) / 2 - hoch, 22, COS, aNo, anker='r', grund=False)
    etikett(b, '5 km', HX - 14, (HY + ey) / 2 + 16, 24, COS, ein(t, tN2 + 0.2), anker='r', grund=False)
    aO = ein(t, tGO + 0.6)
    if t < tO2:
        etikett(b, 'Osten', (ex + ZX) / 2, ey - 26, 22, SIN, aO, grund=False)
    else:
        zeile(b, [('Osten ', SIN), ('≈ 8,66 km', SIN)], (ex + ZX) / 2, ey - 26, 24, INTER_X, alphas=[1, ein(t, tO2 + 0.6)])
    # Rechnung rechts
    zz(b, t, tK0, [('Kurs ', INK), ('60°', WINKEL), (' · Strecke 10 km', INK)], KX, 128, 28)
    zz(b, t, tQ, [('Wie weit nach Osten? Wie weit nach Norden?', GRAU)], KX, 174, 21, INTER, ende=tAn - 0.2)
    # Teil 1 (Osten, Sinus), Teil 2 (Norden, Kosinus) ab tAn: wie bei der Leiter rückt das Ergebnis nach oben
    g, weg1 = 28, tAn - 0.2
    el_o = [T('sin 60°', SIN), T(' = '), B([('Osten', SIN)], [('10 km', INK)])]
    zf(b, t, tGg, el_o, KX, 250, g, weg1)
    umformung(b, t, tO1, el_o, KX, 250, g, '· 10 km', weg1)
    zf(b, t, tO1, [T('Osten', SIN), T(' = 10 km · '), T('sin 60°', SIN)], KX, 326, g, weg1)
    zf(b, t, tT1, [T('Taschenrechner:  ', GRAU), T('sin 60°', SIN), T(' ≈ ', INK, ein(t, tW1)), T('0,866', SIN, ein(t, tW1))],
       KX, 378, 24, weg1)
    hoch = glatt(p(t, tAn, 0.7))
    o2 = ein(t, tO2 + 0.6)
    zf(b, t, tO2, [T('Osten', SIN), T(' ≈ 10 km · '), T('0,866', SIN), T(' = ', INK, o2), T('8,66 km', SIN, o2)], KX, 432 - 248 * hoch, g)
    el_n = [T('cos 60°', COS), T(' = '), B([('Norden', COS)], [('10 km', INK)])]
    zf(b, t, tAn + 0.7, el_n, KX, 258, g)                  # erst, wenn die Zeile oben ist
    umformung(b, t, tN1, el_n, KX, 258, g, '· 10 km')
    zf(b, t, tN1, [T('Norden', COS), T(' = 10 km · '), T('cos 60°', COS)], KX, 332, g)
    zf(b, t, tT2, [T('cos 60°', COS), T(' = ', INK, ein(t, tW2)), T('0,5', COS, ein(t, tW2)), T('  (genau)', GRAU, ein(t, tW2))], KX, 382, 24)
    n2 = ein(t, tN2)
    zf(b, t, tW2 + 0.9, [T('Norden', COS), T(' = 10 km · '), T('0,5', COS), T(' = ', INK, n2), T('5 km', COS, n2)], KX, 432, g)
    zahlenstrahl(b, 740, 1180, 512, ein(t, tZ01 - 0.3), [(0.866, SIN, 'sin 60°', 1.0), (0.5, COS, 'cos 60°', ein(t, tW2))])
    aA = ein(t, tAch)
    if aA > 0:
        band(b, 662, 566 + 10 * (1 - aA), 1254, 652 + 10 * (1 - aA), TEAL, 0.94 * aA, r=18)
        b.text('Achtung: Der Sinus gehört hier zur waagrechten Strecke.', KX, 592 + 10 * (1 - aA), 19, '#ffffff', INTER_X, alpha=aA)
        a2 = ein(t, tZaehlt)
        b.text('Es zählt nur, wo die Seite zum Winkel liegt.', KX, 626 + 10 * (1 - aA), 19, '#ffffff', INTER_X, alpha=aA * a2)


# ---------------------------------------------------------------- 4 Riesenrad
PM = 8                                                     # Bildpunkte je Meter
BODEN = 630
NX, NY, RR = 350, BODEN - 32 * PM, 30 * PM                 # Nabe (Achse 32 m hoch), Radius 30 m
QX = 950                                                   # Mitte der Rechenspalte
ZX0, ZX1 = 720, 1230                                       # Höhe über der Zeit: zwei Runden
GONDEL = '#b7b0a2'
_qr = {}


def rad(b, g, a=1.0, unsere=0.0):
    """Riesenrad, um g Grad gedreht; `unsere` hebt die Gondel bei g hervor (Punkt P)."""
    if a <= 0:
        return
    for s_ in (-1, 1):
        b.linie([(NX, NY), (NX + 112 * s_, BODEN)], GRAU, 6, alpha=a)
    ecken = [(NX + RR * math.cos(math.radians(g + 30 * k)), NY - RR * math.sin(math.radians(g + 30 * k))) for k in range(12)]
    for x, y in ecken:
        b.linie([(NX, NY), (x, y)], HELL, 2.5, alpha=a)
    E.kreislinie(b, 1.0, a, cx=NX, cy=NY, r=RR)
    for k, (x, y) in enumerate(ecken):
        if k or unsere < 1:
            b.kreis(x, y, 9, GONDEL, alpha=a)
    b.kreis(NX, NY, 10, INK, alpha=a)
    if unsere > 0:
        b.kreis(ecken[0][0], ecken[0][1], 9 + 3 * unsere, INK, alpha=a * unsere)


def rad_winkel(sc, t):
    """Stellung unserer Gondel in Grad (darf über 360 hinauslaufen)."""
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    tJ, tP = w('Jetzt dreht'), w('Die Gondel ist')
    t30, t90, t210 = w('Bei dreißig Grad'), w('Bei neunzig Grad'), w('Bei zweihundertzehn')
    tD, tC0, tC1 = w('Dreht sich das Rad'), w('dann ergibt die Höhe'), w('Probier es') + 0.4
    v = 40.0
    if t <= tJ:
        return 10 - v * (tP - tJ)
    if t <= tP:
        return 10 - v * (tP - t)
    if t < t30 - 0.3:
        u = klemm((t - tP) / 2.0)
        return 10 + 40 * (1 - (1 - u) ** 2)                # läuft weich bei 50° aus
    if t < tD:
        return bahn(t, [(0, 50), (t30 - 0.3, 30), (t90 - 0.3, 90), (t210 - 0.3, 210)], 1.2)
    if t < tC0:
        return 210 + 150 * glatt(p(t, tD, max(0.8, tC0 - tD - 0.1)))
    return 360 + 720 * klemm((t - tC0) / (tC1 - tC0))      # zwei Runden, gleichmäßig


def s_riesenrad(b, sc, t):
    w = lambda s_, nach=None: C(sc, s_, nach)               # noqa: E731
    tJ, t60, t32, tP, tR30 = w('Jetzt dreht'), w('sechzig Meter Durchmesser'), w('zweiunddreißig Meter über'), w('Die Gondel ist'), w('Radius dreißig')
    tUe, tHo = w('Über der Achse'), w('Ihre Höhe')
    t30, t90, t210 = w('Bei dreißig Grad'), w('Bei neunzig Grad'), w('Bei zweihundertzehn')
    tD, tC0, tC1, tApp = w('Dreht sich das Rad'), w('dann ergibt die Höhe'), w('Probier es') + 0.4, w('Probier es')
    tDr, tGeg, tMs = w('Auch hier steckt'), w('Die Höhe über der Achse'), w('Kathete gegenüber')
    g = rad_winkel(sc, t)
    gm = g % 360
    kurve = ein(t, tD, 0.5)                                # Rechnung weg, Kurve her
    # Boden, Achshöhe
    b.linie([(24, BODEN), (640, BODEN)], INK, 3.5)
    a32 = ein(t, t32)
    masslinie(b, 62, BODEN, 62, NY, GRAU, a32)
    b.text('32 m', 38, (BODEN + NY) / 2, 22, GRAU, INTER_X, alpha=a32, dreh=90)
    if a32 > 0:
        gestrichelt(b, 62, NY, NX + RR + 34, NY, GRAU, a32, n=44, lw=2)
    a60 = ein(t, t60) * (1 - ein(t, tP - 0.3, 0.4))
    masslinie(b, NX - RR, NY - RR - 22, NX + RR, NY - RR - 22, GRAU, a60)
    etikett(b, '60 m', NX, NY - RR - 44, 22, GRAU, a60, grund=False)
    aP = ein(t, tP, 0.4)
    rad(b, g, 1.0, aP)
    px, py = E.punkt(g, NX, NY, RR)
    # feste Stellen mit ihrer Höhe (bleiben stehen)
    for grad, tt, s_, ox, oy in ((30, t30, '47 m', 46, -16), (90, t90, '62 m', 52, -28), (210, t210, '17 m', -34, 32)):
        am = ein(t, w({30: 'siebenundvierzig', 90: 'zweiundsechzig', 210: 'siebzehn'}[grad]), 0.4) * (1 - 0.0 * kurve)
        if am > 0:
            x, y = E.punkt(grad, NX, NY, RR)
            b.kreis(x, y, 7, TEAL, alpha=am)
            etikett(b, s_, x + ox, y + oy, 24, TEAL, am, grund=False)
    # Einmal (Nutzer 15.11.): das Dreieck im Rad – Winkel an der Achse, rechter Winkel, Gegenkathete gegenüber
    aT = ein(t, tDr, 0.4) * (1 - ein(t, t30 - 0.5, 0.4))
    if aT > 0:
        b.poly([(NX, NY), (px, NY), (px, py)], fill=WINKEL, alpha=0.12 * aT)
        rechter_winkel(b, px, NY, 90, aT, r=20 + 8 * puls(t, tDr + 0.6, 1.0), b1=8, b2=2)
        hypotenuse_leuchtet(b, t, tDr + 0.3, (NX, NY), (px, py), 1.4)
        hinweis_gegenueber(b, t, tGeg + 0.6, (NX, NY), 0, gm, ((px, NY), (px, py)), dauer=2.6, ab=102)
        # wie im Einheitskreis-Video: der Name steht gedreht entlang der Hypotenuse (statt „30 m“, solange das Dreieck da ist)
        m = math.radians(gm)
        b.text('Hypotenuse = 30 m', (NX + px) / 2 - 22 * math.sin(m), (NY + py) / 2 - 22 * math.cos(m), 20, INK, INTER_X,
               alpha=aT * ein(t, tDr + 0.3, 0.4), dreh=gm)
    zz(b, t, tMs, [('Kathete gegenüber', SIN), ('  →  ', GRAU), ('Sinus', SIN)], QX, 96, 24, ende=t30 - 0.5)
    # Zeiger, Winkel, Höhe über der Achse (rot)
    aU = ein(t, tDr - 0.2, 0.4)
    if aP > 0:
        b.linie([(NX, NY), (px, py)], INK, 4, alpha=aP)
    if aU > 0:
        name = 'α' if t < t30 else ('' if t > tD else f'{int(round(gm))}°' if abs(gm - round(gm / 30) * 30) < 0.5 else '')
        E.winkel(b, gm, aU, text=name, cx=NX, cy=NY)
        unten = min(NY, py) if py < NY else NY
        if abs(py - NY) > 2:
            gestrichelt(b, px, BODEN, px, max(NY, py) if py > NY else NY, GRAU, 0.8 * aU, n=int(max(4, abs(BODEN - max(NY, py)) / 9)), lw=2)
        b.linie([(px, NY), (px, py)], SIN, 8, alpha=aU)
    if aP > 0:
        b.kreis(px, py, 12, INK, alpha=aP)
        if t < tD:
            dx = 26 if px >= NX - 2 else -26
            b.text('P', px + dx, py + (-24 if py <= NY + 1 else 26), 28, INK, INTER_X, alpha=aP * (1 - ein(t, t30 - 0.4, 0.3)))
    a30 = ein(t, tR30) * (1 - ein(t, tDr, 0.3))             # danach steht „Hypotenuse = 30 m“ entlang des Radius
    if a30 > 0:
        m = math.radians(gm)
        etikett(b, '30 m', (NX + px) / 2 - 30 * math.sin(m), (NY + py) / 2 - 30 * math.cos(m), 22, INK, a30, grund=False)
    # rechts zuerst, was gegeben ist; dann die Rechnung
    vor = tDr - 0.4
    zz(b, t, 0.2, [('Bis hier: ein Dreieck', GRAU)], QX, 150, 28, ende=vor)
    zz(b, t, w('ganzen Kreis'), [('Jetzt: der ganze Kreis', TEAL)], QX, 198, 32, ende=vor)
    zz(b, t, t60, [('Durchmesser: ', GRAU), ('60 m', INK)], QX, 300, 30, ende=vor)
    zz(b, t, t32, [('Achse: ', GRAU), ('32 m über dem Boden', INK)], QX, 352, 30, ende=vor)
    zz(b, t, tP, [('Gondel = Punkt ', GRAU), ('P', INK)], QX, 404, 30, ende=vor)
    zz(b, t, tR30, [('Radius: ', GRAU), ('30 m', INK), (' statt 1', GRAU)], QX, 456, 30, ende=vor)
    weg = tD
    zz(b, t, tUe, [('über der Achse: ', INK), ('30 m · sin α', SIN)], QX, 138, 28, ende=weg)
    yH = 196 - 104 * kurve                                 # die Formel wandert nach oben und bleibt stehen
    aH = ein(t, tHo)
    if aH > 0:
        zeile(b, [('Höhe', INK), (' = 32 m + ', INK), ('30 m · sin α', SIN)], QX + 35 * kurve, yH + 12 * (1 - aH), 32 - 6 * kurve, INTER_X, alpha=aH)
    zz(b, t, t30, [('Höhe in Metern:', GRAU)], 660, 262, 21, INTER, ende=weg, anker='l')
    halb = lambda c=SIN: B([('1', c)], [('2', c)])          # noqa: E731
    r1, r2 = ein(t, w('zweiunddreißig plus fünfzehn')), ein(t, w('siebenundvierzig'))
    zf(b, t, t30, [T('30°:  ', WINKEL), T('32 + 30 · '), halb(), T(' = 32 + 15', INK, r1), T(' = 47', INK, r2)], 660, 322, 27, weg, 'l')
    r3 = ein(t, w('zweiundsechzig'))
    zf(b, t, t90, [T('90°:  ', WINKEL), T('32 + 30 · '), T('1', SIN), T(' = 62', INK, r3)], 660, 410, 27, weg, 'l')
    r4, r5 = ein(t, w('zweiunddreißig minus fünfzehn')), ein(t, w('siebzehn'))
    zf(b, t, w('minus ein halb'), [T('210°:  ', WINKEL), T('32 + 30 · ('), T('−', SIN), halb(), T(')'), T(' = 32 − 15', INK, r4),
                                   T(' = 17', INK, r5)], 660, 498, 27, weg, 'l')
    zz(b, t, w('minus ein halb') + 0.9, [('negativ: Die Gondel hängt unter der Achse.', GRAU)], 660, 558, 20, INTER, ende=weg, anker='l')
    # Höhe über der Zeit
    if kurve > 0:
        b.linie([(640, BODEN), (ZX1 + 26, BODEN)], GRAU, 3.5, alpha=kurve)
        b.poly([(ZX1 + 38, BODEN), (ZX1 + 22, BODEN - 7), (ZX1 + 22, BODEN + 7)], fill=GRAU, alpha=kurve)
        b.linie([(ZX0, BODEN + 8), (ZX0, NY - RR - 26)], GRAU, 3.5, alpha=kurve)
        b.poly([(ZX0, NY - RR - 38), (ZX0 - 7, NY - RR - 22), (ZX0 + 7, NY - RR - 22)], fill=GRAU, alpha=kurve)
        for h in (32, 62):
            y = BODEN - h * PM
            b.linie([(ZX0 - 7, y), (ZX0 + 7, y)], GRAU, 3, alpha=kurve)
            b.text(f'{h} m', ZX0 - 14, y - (14 if h == 32 else 0), 18, INK, INTER_X, anker='r', alpha=kurve)
        b.text('0', ZX0 - 14, BODEN + 20, 18, INK, INTER_X, anker='r', alpha=kurve)
        b.text('Höhe', ZX0 - 14, NY - RR - 34, 20, INK, INTER_X, anker='r', alpha=kurve)
        b.text('Zeit', ZX1 + 14, BODEN - 22, 20, INK, INTER_X, alpha=kurve)
        gestrichelt(b, ZX0, NY, ZX1 + 20, NY, GRAU, 0.7 * kurve, n=56, lw=2)
        for k, s_ in ((1, '1 Runde'), (2, '2 Runden')):
            x = ZX0 + (ZX1 - ZX0) * k / 2
            b.linie([(x, BODEN - 7), (x, BODEN + 7)], GRAU, 3, alpha=kurve)
            b.text(s_, x, BODEN + 24, 18, INK, INTER_X, anker='m' if k == 1 else 'r', alpha=kurve)
        f = klemm((t - tC0) / (tC1 - tC0))
        n = int(240 * f)
        if n > 1:
            b.linie([(ZX0 + (ZX1 - ZX0) * k / 240, BODEN - PM * (32 + 30 * math.sin(4 * math.pi * k / 240))) for k in range(n + 1)], SIN, 6)
        if 0 < f < 1:
            kx = ZX0 + (ZX1 - ZX0) * f
            gestrichelt(b, px, py, kx, py, SIN, 0.6, n=40)
            b.kreis(kx, py, 7, SIN)
    # App: Karte mit QR-Code und Play-Zeichen
    aA = ein(t, tApp + 0.2, 0.6)
    if aA > 0:
        band(b, 652, 66, 1280, 690, BG, 0.72 * aA, r=0)
        karte(b, 880, 150, 340, 420, alpha=aA, r=22)
        b.text('Einheitskreis-App', 1050, 190, 28, INK, INTER_X, alpha=aA)
        if 'qr' not in _qr:
            _qr['qr'] = Image.open(QR_BILD).convert('RGBA').resize((int(210 * 2),) * 2, Image.NEAREST)
        sp = _qr['qr'].copy()
        sp.putalpha(sp.getchannel('A').point(lambda v: int(v * aA)))
        einfuegen(b.img, sp, 945 * 2, 222 * 2)
        aPl = ein(t, w('Drück auf Play'))
        b.kreis(948, 500, 30, TEAL, alpha=aA * aPl)
        b.poly([(938, 484), (938, 516), (964, 500)], fill='#ffffff', alpha=aA * aPl)
        b.text('Play: P kreist', 1092, 500, 28, INK, INTER_X, alpha=aA * aPl)


# ---------------------------------------------------------------- 5 Merke, 6 Schluss
def merkbilder(b):
    """Links klein: das Dreieck (Leiter) und der Kreis (Riesenrad)."""
    ax, ay, bx, cy_ = 110, 316, 270, 316 - 160 * math.tan(math.radians(50))
    b.poly([(ax, ay), (bx, ay), (bx, cy_)], fill=WINKEL, alpha=0.10)
    bogen(b, ax, ay, 44, 0, 50, WINKEL, 5)
    b.linie([(ax, ay), (bx, ay)], COS, 8)
    b.linie([(bx, ay), (bx, cy_)], SIN, 8)
    b.linie([(ax, ay), (bx, cy_)], INK, 4)
    rechter_winkel(b, bx, ay, 90, r=24, b1=8, b2=8)
    b.text('α', ax + 66, ay - 22, 22, WINKEL, INTER_X)
    etikett(b, 'Gegenkathete', bx + 16, (ay + cy_) / 2, 20, SIN, anker='l', grund=False)
    etikett(b, 'Ankathete', (ax + bx) / 2, ay + 26, 20, COS, grund=False)
    etikett(b, 'Hypotenuse', (ax + bx) / 2 - 22, (ay + cy_) / 2 - 26, 20, INK, anker='r', grund=False)
    cx, cy, r = 250, 508, 108
    b.linie([(cx - r - 26, cy), (cx + r + 26, cy)], GRAU, 2.5)
    E.kreislinie(b, cx=cx, cy=cy, r=r)
    px, py = E.punkt(50, cx, cy, r)
    bogen(b, cx, cy, 28, 0, 50, WINKEL, 5)                # klein: zwischen Bogen und rechtem Winkel steht α
    rechter_winkel(b, px, cy, 90, 0.8, r=16, b1=8, b2=2.5)   # Nutzer 15.11.: rechten Winkel leicht andeuten
    b.linie([(px, cy), (px, py)], SIN, 8)
    b.linie([(cx, cy), (px, py)], INK, 4)
    b.kreis(px, py, 9, INK)
    b.kreis(cx, cy, 6, INK)
    b.text('α', cx + 39, cy - 19, 22, WINKEL, INTER_X)
    etikett(b, 'Radius', (cx + px) / 2 - 24, (cy + py) / 2 - 24, 20, INK, anker='r', grund=False)
    etikett(b, 'Radius · sin α', cx + r + 16, (cy + py) / 2, 20, SIN, anker='l', grund=False)


def merkzettel(b, sc, t, alle=False):
    karte(b, 600, 96, 640, 480, alpha=1.0, r=22)
    mx = 920
    b.text('Merke', mx, 128, 28, TEAL, INTER_X)
    st = (lambda s_: 0) if alle else (lambda s_: C(sc, s_))  # noqa: E731
    t1, t2 = st('Mit Sinus'), st('Für die Kathete')          # Merksatz 1 vom Nutzer 15.11. abgenommen; Satz 2 neu (15.11.)
    a1, a2, aU = ein(t, t1), ein(t, t2), ein(t, st('Und wo sich'))
    a3 = [ein(t, st(s_)) for s_ in ('beim Riesenrad', 'beim Windrad', 'beim Pedal')]
    g = 22
    zeile(b, [('Mit ', INK), ('Sinus', SIN), (' und ', INK), ('Kosinus', COS), (' rechnest du im', INK)], mx, 168 + 10 * (1 - a1),
          g, INTER_X, alpha=a1)
    zeile(b, [('rechtwinkligen Dreieck die fehlenden Seiten aus.', INK)], mx, 198 + 10 * (1 - a1), g, INTER_X, alpha=a1)
    zeile(b, [('Für die Kathete ', INK), ('gegenüber', SIN), (' vom Winkel brauchst du', INK)],
          mx, 242 + 10 * (1 - a2), g, INTER_X, alpha=a2)
    zeile(b, [('den ', INK), ('Sinus', SIN), (', für die Kathete ', INK), ('am Winkel', COS), (' den ', INK), ('Kosinus', COS), ('.', INK)],
          mx, 272 + 10 * (1 - a2), g, INTER_X, alpha=a2)
    aF = ein(t, t2 + (0 if alle else 1.0))
    zeile(b, [('Gegenkathete', SIN), (' = Hypotenuse · ', INK), ('sin α', SIN)], mx, 318 + 10 * (1 - aF), 26, INTER_X, alpha=aF)
    zeile(b, [('Ankathete', COS), (' = Hypotenuse · ', INK), ('cos α', COS)], mx, 356 + 10 * (1 - aF), 26, INTER_X, alpha=aF)
    b.linie([(640, 394), (1200, 394)], HELL, 2, alpha=aU)
    b.text('Und wo sich etwas gleichmäßig dreht,', mx, 428 + 10 * (1 - aU), g, INK, INTER_X, alpha=aU)
    b.text('beschreiben sie die Bewegung:', mx, 458 + 10 * (1 - aU), g, INK, INTER_X, alpha=aU)
    # Nutzer 15.11.: keine allgemeine Formel „Höhe = Höhe der Achse + Radius · sin α“ – im Video nie so gezeigt, verwirrt
    zeile(b, [('beim Riesenrad, ', INK), ('beim Windrad,', INK)], mx, 500, g, INTER_X, alphas=a3[:2])
    zeile(b, [('beim Pedal am Fahrrad.', INK)], mx, 530, g, INTER_X, alphas=a3[2:])


def s_merke(b, sc, t):
    merkbilder(b)
    merkzettel(b, sc, t)


def s_schluss(b, sc, t):
    merkbilder(b)
    merkzettel(b, sc, t, alle=True)
    a = ein(t, 0.1)
    if a > 0:
        band(b, 190, 622 + 10 * (1 - a), 1090, 688 + 10 * (1 - a), TEAL, 0.96 * a, r=20)
        w1, w2 = ein(t, C(sc, 'Rechne die Leiter'), 0.5), ein(t, C(sc, 'Das kann jeder'), 0.5)
        b.text('Klingt nach viel? Am Anfang ganz normal.', 640, 655, 28, '#ffffff', INTER_X, alpha=a * (1 - klemm(w1 * 2)))
        b.text('Rechne die Leiter einfach selbst einmal nach.', 640, 655, 28, '#ffffff', INTER_X,
               alpha=a * klemm(w1 * 2 - 1) * (1 - klemm(w2 * 2)))
        b.text(SPRUCH, 640, 655, 30, '#ffffff', INTER_X, alpha=a * klemm(w2 * 2 - 1))


ZEICHNER = dict(einstieg=s_einstieg, regel=s_regel, leiter=s_leiter, kurs=s_kurs, riesenrad=s_riesenrad, merke=s_merke, schluss=s_schluss)
KLAENGE = {}                                               # Geräusche sparsam: keine
MERKSAETZE = []

G.SZENEN, G.ZEICHNER, G.KLAENGE, G.MERKSAETZE = SZENEN, ZEICHNER, KLAENGE, MERKSAETZE
_rahmen = E._rahmen                                        # der ursprüngliche Kapitelkopf aus regel.py


def rahmen(b, i, tl, t):
    if SZENEN[i]['id'] != 'einstieg':                      # Startbild ohne Kapitelkopf
        _rahmen(b, i, tl, t)


G.rahmen = rahmen
G.CACHE = os.path.join(HIER, 'tts_cache')

if __name__ == '__main__':
    G.main()
