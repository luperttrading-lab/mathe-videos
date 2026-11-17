#!/usr/bin/env python3
"""Standbilder zum Vorschlag „Tangens: Steigung und Winkel berechnen“ (17.11.): zeigen, was in welcher Szene gerechnet
wird, im Stil der Reihe (Baukasten aus Video 1 und 2, nur importiert). Noch kein Video, kein Ton.
Aufruf: python3 skizzen.py <ordner>  → 1_regel.png … 6_kreis.png (1600 × 900)"""
import math, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
ziel = sys.argv[1]
sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-sinus-anwendungen'))
import sinus_anwendungen as V                              # noqa: E402
import regel as G                                          # noqa: E402
from regel import INK, GRAU, INTER, INTER_X, band          # noqa: E402
from animationen import Bild, breite                       # noqa: E402
from einheitskreis import SIN, COS, WINKEL, zeile, formel, gestrichelt   # noqa: E402
from sinus_anwendungen import bogen, rechter_winkel, T, B  # noqa: E402
from PIL import Image                                      # noqa: E402

TAN = '#0f766e'                                            # wie in der App „Einheitskreis“
RX = 985                                                   # Mitte der Rechenspalte
D = 9                                                      # Strichstärke der farbigen Seiten


def f(b, el, y, g=30, x=RX):
    w = formel(b, el, 0, 0, g, messen=True)
    formel(b, el, x - w / 2, y, g, 1.0)
    return w


def z(b, teile, y, g=30, pfad=INTER_X, x=RX):
    zeile(b, teile, x, y, g, pfad)


def strich(b, el, y, g, schritt):
    w = formel(b, el, 0, 0, g, messen=True)
    x0 = RX + w / 2 + 28
    b.linie([(x0, y - 0.95 * g), (x0, y + 0.95 * g)], GRAU, 2.5)
    b.text(schritt, x0 + 0.42 * g, y, g * 0.9, GRAU, INTER_X, anker='l')


def kopf(b, nr, titel, zeit):
    b.text(f'Szene {nr} · {titel}', 60, 46, 26, INK, INTER_X, anker='l')
    b.text(zeit, 1220, 46, 22, GRAU, INTER, anker='r')
    b.linie([(60, 76), (1220, 76)], GRAU, 1.5, alpha=0.5)


def dreieck(b, A, C, Bp, r=34, hyp=INK, hyp_lw=6, hyp_a=1.0):
    b.poly([A, C, Bp], fill=WINKEL, alpha=0.08)
    b.linie([A, Bp], hyp, hyp_lw, alpha=hyp_a)
    b.linie([C, Bp], SIN, D)
    b.linie([A, C], COS, D)
    rechter_winkel(b, C[0], C[1], 90, 1.0, r=r, b1=D, b2=D)


def winkel(b, A, grad, r, text, g=30, ab=None):
    bogen(b, A[0], A[1], r, 0, grad, WINKEL, 6)
    m = math.radians(grad / 2)
    ab = ab or r + 34
    b.text(text, A[0] + ab * math.cos(m), A[1] - ab * math.sin(m), g, WINKEL, INTER_X)


def s1(b):
    kopf(b, 2, 'Was ist der Tangens?', '≈ 35 s')
    A, C, Bp = (110, 580), (510, 580), (510, 280)
    dreieck(b, A, C, Bp, hyp=GRAU, hyp_lw=4, hyp_a=0.7)
    winkel(b, A, 36.87, 70, 'α')
    b.text('Gegenkathete', C[0] + 24, 416, 28, SIN, INTER_X, anker='l')
    b.text('3', C[0] + 24, 452, 30, SIN, INTER_X, anker='l')
    b.text('Ankathete', 310, 618, 28, COS, INTER_X)
    b.text('4', 310, 654, 30, COS, INTER_X)
    b.text('Hypotenuse: wird nicht gebraucht', 270, 392, 20, GRAU, INTER, dreh=36.87)
    f(b, [T('tan α', TAN), T(' = '), B([('Gegenkathete', SIN)], [('Ankathete', COS)]), T(' = '), B([('3', SIN)], [('4', COS)]),
          T(' = 0,75')], 190, 32)
    band(b, RX - 250, 285, RX + 250, 335, TAN, 0.14, r=14)
    z(b, [('Beide Katheten, keine Hypotenuse: ', INK), ('Tangens', TAN)], 310, 26)
    z(b, [('Derselbe Wert steckt in Sinus und Kosinus:', GRAU)], 420, 21, INTER)
    f(b, [T('tan α', TAN), T(' = '), B([('sin α', SIN)], [('cos α', COS)]), T(' = '), B([('3', SIN)], [('5', INK)]), T(' : '),
          B([('4', COS)], [('5', INK)]), T(' = '), B([('3', SIN)], [('4', COS)])], 490, 30)
    z(b, [('Die Hypotenuse 5 kürzt sich weg.', GRAU)], 570, 21, INTER)


def s2(b):
    kopf(b, 3, 'Vom Winkel zur Seite: Wie hoch ist der Kirchturm?', '≈ 45 s')
    A, C, Bp = (110, 580), (510, 580), (510, 300)             # 60 m = 400 px, 42 m = 280 px → 35°
    b.linie([(60, 580 + D / 2 + 2), (680, 580 + D / 2 + 2)], GRAU, 3)   # Boden
    ux, uy = 400 / math.hypot(400, 280), -280 / math.hypot(400, 280)
    S = (Bp[0] + 190 * ux, Bp[1] + 190 * uy)
    gestrichelt(b, A[0], A[1], S[0] - 34 * ux, S[1] - 34 * uy, WINKEL, 1.0, n=30, lw=3)
    b.kreis(S[0], S[1], 26, '#ffbe0b')
    b.text('Sonne', S[0], S[1] - 44, 20, GRAU, INTER)
    b.poly([A, C, Bp], fill=WINKEL, alpha=0.08)
    # Kirchturm: 9 m breit, Mauer 26 m, Helm bis 42 m; die Höhe wird in der Turmmitte gemessen
    ty = 580 - 26 * 400 / 60
    b.poly([(480, 580), (540, 580), (540, ty), (480, ty)], fill='#d9d2c3', outline=INK, lw=3)
    b.poly([(474, ty), (546, ty), Bp], fill='#8d99ae', outline=INK, lw=3)
    b.poly([(498, ty + 26), (522, ty + 26), (522, ty + 62), (498, ty + 62)], fill=INK, alpha=0.55)   # Schallfenster
    b.linie([C, Bp], SIN, D)
    b.linie([A, C], COS, D)
    rechter_winkel(b, C[0], C[1], 90, 1.0, r=30, b1=D, b2=D)
    winkel(b, A, 35, 80, '35°', 28, ab=128)
    b.text('Höhe = ?', 562, 440, 28, SIN, INTER_X, anker='l')
    b.text('gegenüber vom Winkel', 562, 474, 18, GRAU, INTER, anker='l')
    b.text('Schatten = 60 m', 290, 622, 28, COS, INTER_X)
    b.text('am Winkel · bis unter die Turmspitze', 290, 654, 18, GRAU, INTER)
    g, x = 30, 1010
    el = [T('tan 35°', TAN), T(' = '), B([('Höhe', SIN)], [('60 m', COS)])]
    w = f(b, el, 170, g, x)
    x0 = x + w / 2 + 28
    b.linie([(x0, 170 - 0.95 * g), (x0, 170 + 0.95 * g)], GRAU, 2.5)
    b.text('· 60 m', x0 + 0.42 * g, 170, g * 0.9, GRAU, INTER_X, anker='l')
    f(b, [T('Höhe', SIN), T(' = '), T('60 m', COS), T(' · '), T('tan 35°', TAN)], 270, g, x)
    z(b, [('Taschenrechner:', GRAU)], 350, 21, INTER, x)
    f(b, [T('tan 35°', TAN), T(' ≈ 0,700')], 392, g, x)
    band(b, x - 225, 532, x + 225, 592, TAN, 0.14, r=14)
    f(b, [T('Höhe', SIN), T(' ≈ '), T('60 m', COS), T(' · 0,700 = '), T('42,0 m', SIN)], 562, g, x)


def schild(b, x, y, s, text):
    pts = [(x, y - s), (x + 0.92 * s, y + 0.6 * s), (x - 0.92 * s, y + 0.6 * s)]
    b.poly(pts, fill='#ffffff', outline='#d62828', lw=10)
    b.poly([(x - 0.42 * s, y + 0.36 * s), (x + 0.42 * s, y + 0.36 * s), (x + 0.42 * s, y + 0.12 * s)], fill=INK)
    b.text(text, x, y - 0.1 * s, 0.3 * s, INK, INTER_X)


def s3(b):
    kopf(b, 4, 'Von den Seiten zum Winkel: 12 % Steigung', '≈ 40 s')
    schild(b, 190, 250, 110, '12 %')
    A, C, Bp = (80, 560), (640, 560), (640, 560 - 67.2)       # maßstäblich: 100 m = 560 px, 12 m = 67,2 px
    dreieck(b, A, C, Bp, r=22)
    bogen(b, A[0], A[1], 150, 0, 6.84, WINKEL, 6)
    b.text('α = ?', A[0] + 250, A[1] - 78, 28, WINKEL, INTER_X)
    b.text('12 m', C[0] + 22, 526, 28, SIN, INTER_X, anker='l')
    b.text('100 m waagrecht', 360, 602, 28, COS, INTER_X)
    b.text('maßstäblich gezeichnet', 360, 636, 18, GRAU, INTER)
    b.text('12 % heißt: 12 m Höhe', 330, 226, 22, INK, INTER_X, anker='l')
    b.text('auf 100 m waagrecht', 330, 258, 22, INK, INTER_X, anker='l')
    x = 1010
    f(b, [T('tan α', TAN), T(' = '), B([('12 m', SIN)], [('100 m', COS)]), T(' = 0,12')], 170, 30, x)
    z(b, [('Gesucht ist der Winkel: rückwärts rechnen', GRAU)], 262, 20, INTER, x)
    f(b, [T('α', WINKEL), T(' = '), T('tan⁻¹', TAN), T('(0,12)')], 318, 30, x)
    band(b, x - 170, 372, x + 170, 472, '#ffffff', 0.9, r=14)
    z(b, [('Taschenrechner', GRAU)], 396, 19, INTER, x)
    z(b, [('SHIFT', INK), ('  +  ', GRAU), ('tan', TAN)], 428, 24, INTER_X, x)
    z(b, [('Anzeige „D“ oder „DEG“ (Grad)', GRAU)], 456, 17, INTER, x)
    band(b, x - 130, 512, x + 130, 572, TAN, 0.14, r=14)
    f(b, [T('α', WINKEL), T(' ≈ '), T('6,84°', WINKEL)], 542, 32, x)


def s4(b):
    kopf(b, 4, 'Die Wende: 100 % sind 45°, nicht 90°', '≈ 25 s')
    A, C, Bp = (90, 580), (400, 580), (400, 270)
    dreieck(b, A, C, Bp)
    winkel(b, A, 45, 70, '45°', 28, ab=112)
    b.text('100 m', C[0] + 22, 425, 28, SIN, INTER_X, anker='l')
    b.text('100 m', 245, 620, 28, COS, INTER_X)
    b.text('100 %', 245, 220, 34, INK, INTER_X)
    # 90°: die Wand
    wx = 620
    b.linie([(wx - 60, 580 + D / 2 + 2), (wx + 70, 580 + D / 2 + 2)], GRAU, 3)
    b.linie([(wx, 580), (wx, 270)], SIN, D)
    b.text('90°', wx, 220, 34, INK, INTER_X)
    b.text('Wand', wx + 22, 425, 24, SIN, INTER_X, anker='l')
    b.text('waagrecht: 0 m', wx, 620, 22, COS, INTER_X)
    x = 1000
    f(b, [T('tan α', TAN), T(' = '), B([('100 m', SIN)], [('100 m', COS)]), T(' = 1')], 160, 30, x)
    f(b, [T('α', WINKEL), T(' = '), T('tan⁻¹', TAN), T('(1) = '), T('45°', WINKEL)], 250, 30, x)
    for i, (pz, gr) in enumerate((('12 %', '6,84°'), ('50 %', '26,57°'), ('100 %', '45°'), ('200 %', '63,43°'))):
        y = 330 + 38 * i
        b.text(pz, x - 40, y, 24, INK, INTER_X, anker='r')
        b.text('→', x, y, 24, GRAU, INTER_X)
        b.text(gr, x + 40, y, 24, WINKEL, INTER_X, anker='l')
    band(b, x - 215, 498, x + 215, 606, '#ffffff', 0.9, r=14)
    f(b, [T('tan 90°', TAN), T(' = '), B([('Höhe', SIN)], [('0 m', COS)])], 536, 26, x)
    z(b, [('Teilen durch null: tan 90° gibt es nicht.', INK)], 586, 19, INTER_X, x)


def s5(b):
    kopf(b, 5, 'Steigung einer Geraden', '≈ 30 s')
    ox, oy, e = 150, 560, 78                                  # Ursprung, Einheit
    for k in range(0, 7):
        b.linie([(ox + k * e, oy), (ox + k * e, oy - 5.2 * e)], GRAU, 1, alpha=0.3)
    for k in range(0, 6):
        b.linie([(ox, oy - k * e), (ox + 6.3 * e, oy - k * e)], GRAU, 1, alpha=0.3)
    b.linie([(ox - 30, oy), (ox + 6.5 * e, oy)], INK, 3.5)
    b.linie([(ox, oy + 30), (ox, oy - 5.4 * e)], INK, 3.5)
    b.text('x', ox + 6.5 * e + 16, oy, 24, INK, INTER_X)
    b.text('y', ox, oy - 5.4 * e - 18, 24, INK, INTER_X)
    b.text('0', ox - 18, oy + 22, 20, INK, INTER_X)
    for k in range(1, 7):
        b.text(str(k), ox + k * e, oy + 22, 20, INK, INTER_X)
    for k in range(1, 6):
        b.text(str(k), ox - 26, oy - k * e, 20, INK, INTER_X)
    P = lambda x_, y_: (ox + x_ * e, oy - y_ * e)             # noqa: E731
    A, C, Bp = P(2, 2), P(4, 2), P(4, 3)
    b.poly([A, C, Bp], fill=WINKEL, alpha=0.10)
    b.linie([P(0, 1), P(6.2, 4.1)], INK, 6)
    b.linie([C, Bp], SIN, D)
    b.linie([A, C], COS, D)
    rechter_winkel(b, C[0], C[1], 90, 1.0, r=22, b1=D, b2=D)
    bogen(b, A[0], A[1], 62, 0, 26.57, WINKEL, 6)
    b.text('α', A[0] + 88, A[1] - 19, 26, WINKEL, INTER_X)
    b.text('1', C[0] + 20, (C[1] + Bp[1]) / 2, 28, SIN, INTER_X, anker='l')
    b.text('2', (A[0] + C[0]) / 2, A[1] + 30, 28, COS, INTER_X)
    b.text('y = 0,5 · x + 1', P(4.6, 4.25)[0], P(4.6, 4.25)[1], 26, INK, INTER_X, anker='r')
    x = 1010
    f(b, [T('m = '), B([('1', SIN)], [('2', COS)]), T(' = 0,5')], 170, 30, x)
    band(b, x - 200, 245, x + 200, 299, TAN, 0.14, r=14)
    f(b, [T('m = '), T('tan α', TAN)], 272, 32, x)
    z(b, [('Die Steigung ist der Tangens', GRAU)], 336, 20, INTER, x)
    z(b, [('des Steigungswinkels.', GRAU)], 364, 20, INTER, x)
    f(b, [T('α', WINKEL), T(' = '), T('tan⁻¹', TAN), T('(0,5)')], 440, 30, x)
    f(b, [T('α', WINKEL), T(' ≈ '), T('26,57°', WINKEL)], 510, 32, x)


def s6(b):
    kopf(b, 6, 'Der Tangens am Einheitskreis', '≈ 25 s')
    cx, cy, r, w = 300, 400, 210, 40
    b.linie([(cx - r - 45, cy), (cx + r + 70, cy)], INK, 3.5)
    b.linie([(cx, cy + r + 45), (cx, cy - r - 45)], INK, 3.5)
    n = 120
    b.linie([(cx + r * math.cos(2 * math.pi * k / n), cy - r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)], INK, 4)
    b.linie([(cx + r, cy + r + 40), (cx + r, cy - r - 50)], TAN, 2.5, alpha=0.6)      # Tangente x = 1
    co, si, ta = math.cos(math.radians(w)), math.sin(math.radians(w)), math.tan(math.radians(w))
    Pp, Tt = (cx + r * co, cy - r * si), (cx + r, cy - r * ta)
    b.poly([(cx, cy), (cx + r, cy), Tt], fill=WINKEL, alpha=0.08)
    b.linie([(cx, cy), Pp], INK, 5)
    gestrichelt(b, Pp[0], Pp[1], Tt[0], Tt[1], INK, 1.0, n=8, lw=3)
    b.linie([(Pp[0], cy), Pp], SIN, D)
    b.linie([(cx, cy), (Pp[0], cy)], COS, D)
    b.linie([(cx + r, cy), Tt], TAN, D)
    b.kreis(Pp[0], Pp[1], 9, INK)
    b.kreis(Tt[0], Tt[1], 9, TAN)
    bogen(b, cx, cy, 58, 0, w, WINKEL, 6)
    b.text('α', cx + 84 * math.cos(math.radians(w / 2)), cy - 84 * math.sin(math.radians(w / 2)), 26, WINKEL, INTER_X)
    b.text('P', Pp[0] - 28, Pp[1] - 14, 24, INK, INTER_X)
    b.text('tan α', cx + r + 20, cy - r * ta / 2, 28, TAN, INTER_X, anker='l')
    b.text('1', cx + r + 16, cy + 24, 22, INK, INTER_X)
    b.text('Tangente', cx + r + 14, cy + r + 24, 20, TAN, INTER, anker='l')
    b.text('sin α', Pp[0] - 14, cy - r * si / 2 + 22, 20, SIN, INTER_X, anker='r')
    b.text('cos α', cx + r * co / 2, cy + 26, 20, COS, INTER_X)
    x = 1000
    z(b, [('Großes Dreieck: Ankathete = 1', INK)], 160, 24, INTER_X, x)
    f(b, [T('tan α', TAN), T(' = '), B([('Gegenkathete', TAN)], [('1', INK)])], 232, 28, x)
    z(b, [('Die grüne Strecke ', GRAU), ('ist', INK), (' der Tangens.', GRAU)], 310, 21, INTER, x)
    for i, (a_, v) in enumerate((('0°', '0'), ('45°', '1'), ('60°', '≈ 1,732'), ('89°', '≈ 57,29'), ('90°', 'gibt es nicht'))):
        y = 372 + 38 * i
        b.text('tan ' + a_, x - 24, y, 24, TAN, INTER_X, anker='r')
        b.text(v, x + 6, y, 24, INK, INTER_X, anker='l')
    z(b, [('Gegen 90° wächst sie über jede Grenze.', GRAU)], 584, 20, INTER, x)


if __name__ == '__main__':
    G.ton_und_zeitplan()                                   # Baukasten erwartet den Zeitplan (Ton aus dem Cache)
    os.makedirs(ziel, exist_ok=True)
    for name, fn in (('1_regel', s1), ('2_hoehe', s2), ('3_steigung', s3), ('4_hundert', s4), ('5_gerade', s5), ('6_kreis', s6)):
        b = Bild(G.grund())
        fn(b)
        b.img.convert('RGB').resize((1600, 900), Image.LANCZOS).save(os.path.join(ziel, name + '.png'))
        print(name)
