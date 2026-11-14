"""Auswahlblatt: Beispiele für das Video „Wofür braucht man Sinus und Kosinus?“ als PDF.

Aufruf: python3 beispiele_pdf.py  →  beispiele.pdf (HTML mit SVG-Bildern, gedruckt mit Chromium/Playwright).
"""
import math
from pathlib import Path

HIER = Path(__file__).resolve().parent
SCHRIFT = (HIER / '../../werkzeug/schriften/Kalam-Bold.ttf').resolve()
ROT, BLAU, ORANGE, INK, PAPIER, GRUEN = '#e63946', '#3a86ff', '#ff9f1c', '#2b2d42', '#f6f1e7', '#0f766e'
GRAU = '#8d8f9e'


def bogen(cx, cy, r, a0, a1, farbe=ORANGE, w=3):
    """Winkelbogen in SVG-Koordinaten (y nach unten), Winkel mathematisch (gegen den Uhrzeigersinn)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    gross = 1 if (a1 - a0) % 360 > 180 else 0
    return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 {gross} 0 {x1:.1f},{y1:.1f}" fill="none" stroke="{farbe}" stroke-width="{w}"/>'


def rechter_winkel(cx, cy, r, a0):
    """Viertelbogen mit Punkt (deutsche Schulnotation), a0 = Richtung des ersten Schenkels."""
    m = math.radians(a0 + 45)
    return bogen(cx, cy, r, a0, a0 + 90, INK, 2) + \
        f'<circle cx="{cx + r * 0.5 * math.cos(m):.1f}" cy="{cy - r * 0.5 * math.sin(m):.1f}" r="2.6" fill="{INK}"/>'


def pfeil(x0, y0, x1, y1, farbe, w=5):
    d = math.atan2(y1 - y0, x1 - x0)
    s = 14
    p1 = (x1 - s * math.cos(d - 0.45), y1 - s * math.sin(d - 0.45))
    p2 = (x1 - s * math.cos(d + 0.45), y1 - s * math.sin(d + 0.45))
    xe, ye = x1 - 0.7 * s * math.cos(d), y1 - 0.7 * s * math.sin(d)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{xe:.1f}" y2="{ye:.1f}" stroke="{farbe}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x1:.1f},{y1:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{farbe}"/>')


def text(x, y, t, farbe=INK, gr=20, anker='middle', fett=True, hof=None):
    """hof: Farbe eines Randes um die Schrift (für Beschriftungen auf der Karte, über dem Gitter)."""
    rand = f' paint-order="stroke" stroke="{hof}" stroke-width="5" stroke-linejoin="round"' if hof else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{farbe}" font-size="{gr}" text-anchor="{anker}" '
            f'font-weight="{"700" if fett else "400"}"{rand}>{t}</text>')


def svg(inhalt, w=420, h=300):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">{inhalt}</svg>'


# ---------------------------------------------------------------- Bilder
def bild_leiter():
    """Wand rechts, Leiterfuß links: der Winkel öffnet sich wie im ersten Quadranten des Einheitskreises."""
    k = 52  # Pixel pro Meter
    fx, by = 150, 270  # Leiterfuß x, Boden y
    wx = fx + 1.71 * k
    ty = by - 4.70 * k
    s = f'<rect x="{wx:.1f}" y="14" width="18" height="{by - 14}" fill="#d9d2c3"/>'
    s += f'<line x1="30" y1="{by}" x2="400" y2="{by}" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<line x1="{wx:.1f}" y1="{by}" x2="{wx:.1f}" y2="{ty:.1f}" stroke="{ROT}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{fx}" y1="{by}" x2="{wx:.1f}" y2="{by}" stroke="{BLAU}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{fx}" y1="{by}" x2="{wx:.1f}" y2="{ty:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    for i in range(1, 9):  # Sprossen
        t = i / 9
        s += f'<circle cx="{fx + (wx - fx) * t:.1f}" cy="{by + (ty - by) * t:.1f}" r="3" fill="{INK}"/>'
    s += bogen(fx, by, 34, 0, 70)
    s += text(fx + 47, by - 26, '70°', ORANGE, 17)
    s += rechter_winkel(wx, by, 20, 90)
    s += text(wx + 30, (by + ty) / 2, 'Höhe', ROT, 18, 'start') + text(wx + 30, (by + ty) / 2 + 22, '≈ 4,70 m', ROT, 18, 'start')
    s += text((wx + fx) / 2, by + 26, '≈ 1,71 m', BLAU, 18)
    s += text((wx + fx) / 2 - 36, (by + ty) / 2 - 10, 'Leiter 5 m', INK, 18, 'end')
    return svg(s, 420, 300)


def bild_riesenrad():
    k = 3.5
    ax, by = 200, 290
    ay = by - 32 * k
    r = 30 * k
    s = f'<line x1="20" y1="{by}" x2="300" y2="{by}" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<line x1="{ax - 40}" y1="{by}" x2="{ax}" y2="{ay}" stroke="{GRAU}" stroke-width="4"/><line x1="{ax + 40}" y1="{by}" x2="{ax}" y2="{ay}" stroke="{GRAU}" stroke-width="4"/>'
    s += f'<circle cx="{ax}" cy="{ay}" r="{r}" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<line x1="{ax - r - 14}" y1="{ay}" x2="{ax + r + 14}" y2="{ay}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 5"/>'
    for wkl, dx, dy in ((30, 12, -4), (90, 12, -8), (210, -12, 6)):
        gx, gy = ax + r * math.cos(math.radians(wkl)), ay - r * math.sin(math.radians(wkl))
        s += f'<line x1="{gx:.1f}" y1="{ay}" x2="{gx:.1f}" y2="{gy:.1f}" stroke="{ROT}" stroke-width="6" stroke-linecap="round"/>'
        s += f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="7" fill="{INK}"/>'
        s += text(gx + dx, gy + dy, f'{wkl}°', ORANGE, 15, 'start' if dx > 0 else 'end')
    s += bogen(ax, ay, 30, 0, 30)
    s += f'<circle cx="{ax}" cy="{ay}" r="4" fill="{INK}"/>'
    # Achshöhe als Maß links neben dem Rad
    mx = ax - r - 40
    s += f'<line x1="{mx}" y1="{ay}" x2="{mx}" y2="{by}" stroke="{GRAU}" stroke-width="2"/><line x1="{mx - 6}" y1="{ay}" x2="{mx + 6}" y2="{ay}" stroke="{GRAU}" stroke-width="2"/>'
    s += text(mx - 6, (ay + by) / 2 + 30, '32 m', GRAU, 14, 'end')
    s += text(ax + r * 0.35, ay + 18, 'r = 30 m', INK, 13, 'start', False)
    x0, w, y0 = 350, 96, 285
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + w + 6}" y2="{y0}" stroke="{INK}" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="50" stroke="{INK}" stroke-width="2"/>'
    pts = []
    for i in range(101):
        t = i / 100 * 20
        hm = 32 - 30 * math.cos(2 * math.pi * t / 10)
        pts.append(f'{x0 + t / 20 * w:.1f},{y0 - hm * 3.5:.1f}')
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ROT}" stroke-width="4"/>'
    s += text(x0 + w, y0 + 18, 'Zeit', INK, 13, 'end', False) + text(x0 + 4, 44, 'Höhe', INK, 13, 'start', False)
    return svg(s, 460, 312)


def bild_karte():
    """Seekarte: oben Norden, 1 Kästchen = 1 km. Hafen → Insel, 10 km auf Kurs 60°."""
    k = 30  # Pixel pro Kilometer
    hx, hy = 100, 270  # Hafen
    zx, zy = hx + 10 * math.sin(math.radians(60)) * k, hy - 10 * math.cos(math.radians(60)) * k  # Ziel
    see, gitter, land, ufer = '#e3eef5', '#c3d5e2', '#eadfbf', '#b4a57c'
    s = f'<rect x="10" y="10" width="440" height="330" fill="{see}"/>'
    for i in range(1, 15):
        s += f'<line x1="{10 + 30 * i}" y1="10" x2="{10 + 30 * i}" y2="340" stroke="{gitter}" stroke-width="1"/>'
    for j in range(1, 11):
        s += f'<line x1="10" y1="{30 * j}" x2="450" y2="{30 * j}" stroke="{gitter}" stroke-width="1"/>'
    # Festland unten links, der Hafen liegt an der Küste
    s += (f'<path d="M10,236 C40,236 78,246 {hx},{hy} C122,292 150,318 196,340 L10,340 Z" fill="{land}" stroke="{ufer}" stroke-width="2"/>')
    s += text(24, 312, 'Hafen', INK, 16, 'start')
    # Insel am Ziel mit Leuchtturm
    s += f'<ellipse cx="{zx + 40:.1f}" cy="{zy - 26:.1f}" rx="34" ry="22" fill="{land}" stroke="{ufer}" stroke-width="2"/>'
    lx, ly = zx + 46, zy - 22
    s += f'<polygon points="{lx - 5:.1f},{ly:.1f} {lx + 5:.1f},{ly:.1f} {lx + 3:.1f},{ly - 18:.1f} {lx - 3:.1f},{ly - 18:.1f}" fill="white" stroke="{INK}" stroke-width="1.5"/>'
    s += f'<rect x="{lx - 4:.1f}" y="{ly - 24:.1f}" width="8" height="6" fill="{INK}"/>'
    s += text(zx + 40, zy - 56, 'Insel', INK, 16, 'middle', True, see)
    # Dreieck: erst nach Norden (am Winkel, blau), dann nach Osten (gegenüber vom Winkel, rot)
    s += f'<line x1="{hx}" y1="{hy}" x2="{hx}" y2="{zy:.1f}" stroke="{BLAU}" stroke-width="7" stroke-linecap="round"/>'
    s += f'<line x1="{hx}" y1="{zy:.1f}" x2="{zx:.1f}" y2="{zy:.1f}" stroke="{ROT}" stroke-width="7" stroke-linecap="round"/>'
    s += f'<line x1="{hx}" y1="{hy}" x2="{zx:.1f}" y2="{zy:.1f}" stroke="{INK}" stroke-width="4.5" stroke-linecap="round"/>'
    s += rechter_winkel(hx, zy, 20, 270)
    s += bogen(hx, hy, 50, 30, 90)
    s += text(hx + 68 * math.cos(math.radians(63)), hy - 68 * math.sin(math.radians(63)) + 6, '60°', ORANGE, 16, 'middle', True, see)
    # Schiff auf dem Kurs (Draufsicht), bei 42 % der Strecke
    sx, sy = hx + (zx - hx) * 0.42, hy + (zy - hy) * 0.42
    s += (f'<g transform="translate({sx:.1f},{sy:.1f}) rotate(-30)"><polygon points="-17,-7 7,-7 19,0 7,7 -17,7" fill="white" stroke="{INK}" stroke-width="2.2"/>'
          f'<rect x="-9" y="-3.5" width="9" height="7" fill="{INK}"/></g>')
    s += f'<circle cx="{hx}" cy="{hy}" r="6" fill="{INK}"/><circle cx="{zx:.1f}" cy="{zy:.1f}" r="6" fill="{INK}"/>'
    s += text(hx - 10, (hy + zy) / 2 - 6, 'Norden', BLAU, 16, 'end', True, see) + text(hx - 10, (hy + zy) / 2 + 14, '5 km', BLAU, 16, 'end', True, see)
    s += text((hx + zx) / 2, zy - 13, 'Osten ≈ 8,66 km', ROT, 16, 'middle', True, see)
    s += text(hx + (zx - hx) * 0.72 + 6, hy + (zy - hy) * 0.72 + 30, '10 km', INK, 16, 'start', True, see)
    # Kompassrose oben links
    cx, cy = 46, 62
    s += f'<circle cx="{cx}" cy="{cy}" r="20" fill="white" stroke="{INK}" stroke-width="1.5"/>'
    s += f'<polygon points="{cx},{cy - 17} {cx - 6},{cy} {cx + 6},{cy}" fill="{INK}"/><polygon points="{cx},{cy + 17} {cx - 6},{cy} {cx + 6},{cy}" fill="white" stroke="{INK}" stroke-width="1.2"/>'
    s += text(cx, cy - 25, 'N', INK, 15, 'middle', True, see)
    # Maßstab unten rechts: 5 km
    mx, my = 280, 322
    s += f'<line x1="{mx}" y1="{my}" x2="{mx + 150}" y2="{my}" stroke="{INK}" stroke-width="3"/>'
    for i in range(6):
        s += f'<line x1="{mx + 30 * i}" y1="{my - 5}" x2="{mx + 30 * i}" y2="{my + 5}" stroke="{INK}" stroke-width="2"/>'
    s += text(mx, my - 10, '0', INK, 13, 'middle', False, see) + text(mx + 150, my - 10, '5 km', INK, 13, 'middle', False, see)
    s += f'<rect x="10" y="10" width="440" height="330" fill="none" stroke="{INK}" stroke-width="2"/>'
    return svg(s, 460, 350)


def bild_piste():
    k = 0.4  # Pixel pro Meter
    x0, y0 = 40, 250
    a = math.radians(20)
    xb, yt = x0 + 900 * math.cos(a) * k, y0 - 900 * math.sin(a) * k
    s = f'<polygon points="{x0},{y0} {xb:.1f},{y0} {xb:.1f},{yt:.1f}" fill="white" stroke="{INK}" stroke-width="1.5"/>'
    s += f'<line x1="{x0}" y1="{y0}" x2="{xb:.1f}" y2="{y0}" stroke="{BLAU}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{xb:.1f}" y1="{y0}" x2="{xb:.1f}" y2="{yt:.1f}" stroke="{ROT}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{x0}" y1="{y0}" x2="{xb:.1f}" y2="{yt:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    s += rechter_winkel(xb, y0, 18, 90)
    s += bogen(x0, y0, 84, 0, 20)
    s += text(x0 + 112, y0 - 13, '20°', ORANGE, 16)
    s += text((x0 + xb) / 2 - 22, (y0 + yt) / 2 - 22, 'Piste 900 m', INK, 17)
    s += text(xb + 12, (y0 + yt) / 2, '≈ 308 m', ROT, 17, 'start') + text(xb + 12, (y0 + yt) / 2 + 20, 'tiefer', ROT, 15, 'start', False)
    s += text((x0 + xb) / 2, y0 + 26, '≈ 846 m auf der Karte', BLAU, 17)
    # Skifahrer als Punkt mit Fahrtrichtung
    px, py = x0 + (xb - x0) * 0.8, y0 + (yt - y0) * 0.8
    s += f'<circle cx="{px - 4:.1f}" cy="{py - 10:.1f}" r="7" fill="{INK}"/>'
    return svg(s, 480, 290)


def tageslaenge(n, breite=50.11):
    """Stunden zwischen Sonnenauf- und -untergang am Tag n (0 = 1. Januar 2026), Frankfurt am Main.

    Sonnenstand nach den NOAA-Näherungsformeln, Horizont −0,833° (Lichtbrechung und Sonnenradius).
    """
    T = (2461041.5 + n + 0.5 - 2451545) / 36525
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360
    M = math.radians(357.52911 + T * (35999.05029 - 0.0001537 * T))
    C = (math.sin(M) * (1.914602 - T * (0.004817 + 0.000014 * T)) + math.sin(2 * M) * (0.019993 - 0.000101 * T)
         + math.sin(3 * M) * 0.000289)
    Om = math.radians(125.04 - 1934.136 * T)
    lam = math.radians(L0 + C - 0.00569 - 0.00478 * math.sin(Om))
    eps = math.radians(23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - 0.001813 * T))) / 60) / 60 + 0.00256 * math.cos(Om))
    d = math.asin(math.sin(eps) * math.sin(lam))
    p = math.radians(breite)
    return 2 * math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(p) * math.cos(d)) - math.tan(p) * math.tan(d))) / 15


def bild_tageslaenge():
    """Tageslänge übers Jahr; die Hochachse ist zwischen 0 und 6 h unterbrochen (Zickzack), damit man den Unterschied sieht."""
    x0, y0, w, kh = 52, 292, 365, 22  # 1 px pro Tag, 22 px pro Stunde oberhalb von 6 h

    def y(h):
        return y0 - 30 - (h - 6) * kh

    s = f'<line x1="{x0}" y1="{y0}" x2="{x0 + w + 10}" y2="{y0}" stroke="{INK}" stroke-width="2.5"/>'
    s += f'<polyline points="{x0},{y0} {x0},{y0 - 8} {x0 - 6},{y0 - 12} {x0 + 6},{y0 - 18} {x0},{y0 - 22} {x0},22" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    s += text(x0 - 9, y0 + 5, '0 h', INK, 13, 'end', False)
    for h in (8, 12, 16):
        s += f'<line x1="{x0 - 5}" y1="{y(h)}" x2="{x0}" y2="{y(h)}" stroke="{INK}" stroke-width="2"/>' + text(x0 - 9, y(h) + 5, f'{h} h', INK, 13, 'end', False)
    n = 0
    for name, tage in zip('JFMAMJJASOND', (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)):
        s += f'<line x1="{x0 + n}" y1="{y0}" x2="{x0 + n}" y2="{y0 + 5}" stroke="{INK}" stroke-width="1.5"/>'
        s += text(x0 + n + tage / 2, y0 + 19, name, INK, 13, 'middle', False)
        n += tage
    echt = [tageslaenge(i) for i in range(365)]
    modell = [12.2 + 4.2 * math.sin(2 * math.pi * (i - 79) / 365) for i in range(365)]
    s += f'<polyline points="{" ".join(f"{x0 + i},{y(v):.1f}" for i, v in enumerate(modell))}" fill="none" stroke="{ROT}" stroke-width="3" stroke-dasharray="7 5"/>'
    s += f'<polyline points="{" ".join(f"{x0 + i},{y(v):.1f}" for i, v in enumerate(echt))}" fill="none" stroke="{INK}" stroke-width="3"/>'
    s += text(x0 + 171, y(16.4) - 10, '21. Juni: 16 h 23 min', INK, 13)
    s += text(x0 + 354, y(8.05) + 24, '21. Dez.: 8 h 03 min', INK, 13, 'end')
    s += f'<line x1="{x0 + 120}" y1="{y(9.4)}" x2="{x0 + 150}" y2="{y(9.4)}" stroke="{INK}" stroke-width="3"/>' + text(x0 + 156, y(9.4) + 5, 'wirklich', INK, 13, 'start', False)
    s += f'<line x1="{x0 + 120}" y1="{y(8.4)}" x2="{x0 + 150}" y2="{y(8.4)}" stroke="{ROT}" stroke-width="3" stroke-dasharray="7 5"/>' + text(x0 + 156, y(8.4) + 5, 'Sinuskurve', ROT, 13, 'start', False)
    return svg(s, 440, 320)


# ---------------------------------------------------------------- Formeln (MathML, echte Brüche)
def bruch(z, n):
    return f'<mfrac><mrow>{z}</mrow><mrow>{n}</mrow></mfrac>'


def m(inhalt):
    import re
    inhalt = re.sub(r'<mi>(m|N|s|h|km|Hz)</mi>', r'<mspace width="0.17em"/><mi mathvariant="normal">\1</mi>', inhalt)
    inhalt = re.sub(r'<mi( style="[^"]*")?>(m|N)</mi>', r'<mspace width="0.17em"/><mi mathvariant="normal"\1>\2</mi>', inhalt)
    inhalt = re.sub(r'<mi>(sin|cos)</mi>', r'<mi>\1</mi><mspace width="0.2em"/>', inhalt)
    inhalt = inhalt.replace('<mtext> Schwingungen', '<mtext>\u00a0Schwingungen').replace('<mtext> m/s', '<mtext>\u00a0m/s')
    return f'<math display="block"><mrow>{inhalt}</mrow></math>'


def r(t):
    return f'<mi mathvariant="normal" style="color:{ROT}">{t}</mi>'


def b(t):
    return f'<mi mathvariant="normal" style="color:{BLAU}">{t}</mi>'


def t(x):
    return f'<mtext>{x}</mtext>'


al = f'<mi style="color:{ORANGE}">α</mi>'

BEISPIELE = [
    dict(nr=1, titel='Leiter an der Wand', bereich='Bau & Handwerk', dauer='≈ 35 s',
         typ='Dreieck', lehrplan='Mathe Kl. 10 (Hessen): „Anwendungen aus Technik, Physik …“', drin=True,
         bild=bild_leiter(),
         frage='Eine 5 m lange Leiter lehnt im Winkel von 70° an der Wand. Wie hoch reicht sie – und wie weit steht sie von der Wand weg?',
         erkl='Leiter, Wand und Boden bilden ein rechtwinkliges Dreieck. Die Leiter ist die längste Seite (Hypotenuse). '
              'Die Wandhöhe liegt dem 70°-Winkel gegenüber (Gegenkathete), der Abstand am Boden liegt am Winkel an (Ankathete).',
         rechnung=[m(f'<mi>sin</mi><mn>70°</mn><mo>=</mo>{bruch(r("Höhe"), "<mn>5</mn><mi>m</mi>")}<mspace width="1em"/><mo>⇒</mo>'
                     f'<mspace width="1em"/>{r("Höhe")}<mo>=</mo><mn>5</mn><mi>m</mi><mo>·</mo><mi>sin</mi><mn>70°</mn><mo>≈</mo><mn>4,70</mn><mi>m</mi>'),
                   m(f'<mi>cos</mi><mn>70°</mn><mo>=</mo>{bruch(b("Abstand"), "<mn>5</mn><mi>m</mi>")}<mspace width="1em"/><mo>⇒</mo>'
                     f'<mspace width="1em"/>{b("Abstand")}<mo>=</mo><mn>5</mn><mi>m</mi><mo>·</mo><mi>cos</mi><mn>70°</mn><mo>≈</mo><mn>1,71</mn><mi>m</mi>')],
         pfiff='Es ist genau das Dreieck aus dem Einheitskreis – nur fünfmal so groß, deshalb „mal 5“. Der Leiterfuß ist der '
               'Mittelpunkt, die Leiter der Radius, und der Winkel liegt im ersten Viertel.'),
    dict(nr=2, titel='Schiffskurs auf der Seekarte', bereich='Navigation & Geografie', dauer='≈ 40 s',
         typ='Dreieck', lehrplan='Mathe Kl. 10 (Hessen): „Berechnungen in Dreiecken“, „cos α = sin (90° − α)“', drin=True,
         bild=bild_karte(), breit=True,
         frage='Ein Schiff fährt vom Hafen 10 km auf Kurs 60° zur Insel. Wie weit liegt die Insel östlich und wie weit nördlich vom Hafen?',
         erkl='Auf der Seekarte ist oben Norden, ein Kästchen ist 1 km breit. Einen Kurs misst man von Norden aus im Uhrzeigersinn. '
              'Geh in Gedanken vom Hafen erst nach Norden, dann nach Osten: Das gibt ein rechtwinkliges Dreieck, die Fahrstrecke ist '
              'die längste Seite. Die Oststrecke liegt dem Winkel gegenüber (Sinus), die Nordstrecke liegt am Winkel an (Kosinus).',
         rechnung=[m(f'<mi>sin</mi><mn>60°</mn><mo>=</mo>{bruch(r("Osten"), "<mn>10</mn><mi>km</mi>")}<mspace width="1em"/><mo>⇒</mo>'
                     f'<mspace width="1em"/>{r("Osten")}<mo>=</mo><mn>10</mn><mi>km</mi><mo>·</mo><mi>sin</mi><mn>60°</mn><mo>≈</mo><mn>8,66</mn><mi>km</mi>'),
                   m(f'<mi>cos</mi><mn>60°</mn><mo>=</mo>{bruch(b("Norden"), "<mn>10</mn><mi>km</mi>")}<mspace width="1em"/><mo>⇒</mo>'
                     f'<mspace width="1em"/>{b("Norden")}<mo>=</mo><mn>10</mn><mi>km</mi><mo>·</mo><mi>cos</mi><mn>60°</mn><mo>=</mo><mn>5</mn><mi>km</mi>')],
         pfiff='Zähl auf der Karte nach: 5 Kästchen nach oben, knapp 9 nach rechts. Achtung, Falle: Hier gehört der Sinus zur '
               'waagrechten Strecke, weil der Winkel an der Nordlinie liegt. Wer lieber wie im Einheitskreis rechnet: Kurs 60° heißt '
               '30° über der Ost-Richtung, also 10 · cos 30° ≈ 8,66 und 10 · sin 30° = 5. Dasselbe Ergebnis.'),
    dict(nr=3, titel='Gondel im Riesenrad', bereich='Technik & Freizeit', dauer='≈ 47 s',
         typ='Kreis', lehrplan='Mathe Kl. 10 (Hessen): Sinusfunktion als „senkrechte Projektion einer Kreisbewegung“', drin=True,
         bild=bild_riesenrad(),
         frage='Ein Riesenrad hat 60 m Durchmesser, die Achse ist 32 m hoch. Wie hoch ist deine Gondel bei 30°, 90° und 210°?',
         erkl='Die Gondel ist der Punkt P aus dem Einheitskreis – nur mit Radius 30 m statt 1, und der Kreis hängt 32 m über dem Boden. '
              'Den Winkel misst man wie im Einheitskreis von „3 Uhr“ aus gegen den Uhrzeigersinn.',
         rechnung=[m(f'<mi>Höhe</mi><mo>=</mo><mn>32</mn><mi>m</mi><mo>+</mo><mn>30</mn><mi>m</mi><mo>·</mo>{r("sin")}{al}'),
                   m(f'<mn>30°</mn><mo>:</mo><mn>32</mn><mo>+</mo><mn>30</mn><mo>·</mo>{bruch("<mn>1</mn>", "<mn>2</mn>")}<mo>=</mo><mn>47</mn><mi>m</mi>'
                     f'<mspace width="1.4em"/><mn>90°</mn><mo>:</mo><mn>32</mn><mo>+</mo><mn>30</mn><mo>·</mo><mn>1</mn><mo>=</mo><mn>62</mn><mi>m</mi>'
                     f'<mspace width="1.4em"/><mn>210°</mn><mo>:</mo><mn>32</mn><mo>+</mo><mn>30</mn><mo>·</mo><mrow><mo>(</mo><mo>−</mo>{bruch("<mn>1</mn>", "<mn>2</mn>")}<mo>)</mo></mrow><mo>=</mo><mn>17</mn><mi>m</mi>')],
         pfiff='Unter der Achse wird der Sinus negativ – die Gondel ist dann tiefer als 32 m. Dreht das Rad gleichmäßig, '
               'wird die Höhe über die Zeit eine Sinuskurve, die sich jede Runde wiederholt (Play-Knopf in der App!).'),
    dict(nr=4, titel='Skipiste', bereich='Sport & Berge', dauer='≈ 30 s',
         typ='Dreieck', lehrplan='Mathe Kl. 10 (Hessen): „Berechnungen in Dreiecken“ – könnte die Leiter ersetzen', drin=False,
         bild=bild_piste(),
         frage='Eine Piste ist 900 m lang und gleichmäßig 20° steil. Wie viele Höhenmeter fährst du hinunter – und wie lang ist die Piste auf der Landkarte?',
         erkl='Piste, Höhenunterschied und die waagrechte Strecke bilden ein rechtwinkliges Dreieck. Eine Landkarte zeigt alles von oben: '
              'Dort sieht man nur die waagrechte Strecke, und die ist kürzer als die Piste.',
         rechnung=[m(f'{r("Höhe")}<mo>=</mo><mn>900</mn><mi>m</mi><mo>·</mo><mi>sin</mi><mn>20°</mn><mo>≈</mo><mn>308</mn><mi>m</mi>'
                     f'<mspace width="1.6em"/>{b("Karte")}<mo>=</mo><mn>900</mn><mi>m</mi><mo>·</mo><mi>cos</mi><mn>20°</mn><mo>≈</mo><mn>846</mn><mi>m</mi>')],
         pfiff='Gleiche Rechnung wie bei der Leiter, nur mit anderen Zahlen. Eines von beiden reicht im Video.'),
    dict(nr=5, titel='Wie lang ist der Tag?', bereich='Natur & Jahreszeiten', dauer='≈ 30 s',
         typ='Kreis', lehrplan='Mathe Kl. 10 (Hessen): „Beispiele periodischer Zusammenhänge … aus den Naturwissenschaften“', drin=False,
         bild=bild_tageslaenge(),
         frage='In Frankfurt dauert der längste Tag etwa 16 h 23 min, der kürzeste etwa 8 h 03 min. Wie lang ist der Tag am 21. April?',
         erkl='Die Tageslänge schwankt übers Jahr um den Mittelwert 12,2 h, und zwar um 4,2 h nach oben und nach unten. Das sieht aus '
              'wie eine Sinuskurve: Ein Punkt läuft in einem Jahr einmal um den Kreis, Start am 21. März. Am 21. April sind 31 Tage vergangen.',
         rechnung=[m(f'{al}<mo>=</mo><mn>360°</mn><mo>·</mo>{bruch("<mn>31</mn>", "<mn>365</mn>")}<mo>≈</mo><mn>30,6°</mn>'
                     f'<mspace width="1em"/><mo>⇒</mo><mspace width="1em"/><mn>12,2</mn><mi>h</mi><mo>+</mo><mn>4,2</mn><mi>h</mi><mo>·</mo><mi>sin</mi><mn>30,6°</mn><mo>≈</mo><mn>14,3</mn><mi>h</mi>')],
         pfiff='Ehrlich gesagt: Das stimmt nur ungefähr. Wirklich sind es am 21. April rund 14 h 08 min, die Sinuskurve liefert 14 h 20 min. '
               'Im Herbst liegt sie bis zu 24 Minuten daneben. Für eine grobe Schätzung reicht sie, genau ist sie nicht.'),
]


def seite(bsp):
    marke = ('<span class="marke ja">im Video-Vorschlag</span>' if bsp['drin']
             else '<span class="marke nein">Alternative</span>')
    return f'''
<section class="bsp">
  <div class="kopf"><span class="nr">{bsp["nr"]}</span><h2>{bsp["titel"]}</h2>{marke}</div>
  <div class="meta">{bsp["bereich"]} · Typ: <b>{bsp["typ"]}</b> · im Video {bsp["dauer"]}<br><i>{bsp["lehrplan"]}</i></div>
  <div class="zeile">
    <div class="bild{" breit" if bsp.get("breit") else ""}">{bsp["bild"]}</div>
    <div class="txt"><p class="frage">{bsp["frage"]}</p><p>{bsp["erkl"]}</p></div>
  </div>
  <div class="rechnung">{"".join(bsp["rechnung"])}</div>
  <p class="pfiff">💡 {bsp["pfiff"]}</p>
  <div class="wahl">☐ will ich im Video &nbsp;&nbsp; ☐ lieber nicht</div>
</section>'''


def html():
    seiten = ''.join(seite(x) for x in BEISPIELE)
    return f'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Kalam; src: url("file://{SCHRIFT}"); }}
@page {{ size: A4; margin: 14mm 14mm 12mm 14mm; }}
body {{ font-family: "DejaVu Sans", sans-serif; color: {INK}; font-size: 10.5pt; line-height: 1.38; }}
h1 {{ font-family: Kalam; font-size: 25pt; margin: 0 0 2mm; }}
.leiste {{ background: {GRUEN}; color: white; font-weight: 700; letter-spacing: .08em; padding: 2mm 4mm; font-size: 9pt; border-radius: 2mm; display: inline-block; }}
.intro {{ background: {PAPIER}; border-radius: 3mm; padding: 4mm 5mm; margin: 4mm 0; }}
.intro b.r {{ color: {ROT}; }} .intro b.b {{ color: {BLAU}; }} .intro b.o {{ color: {ORANGE}; }}
.bsp {{ break-inside: avoid; border: 1.5px solid #ddd6c6; border-radius: 3mm; padding: 4mm 5mm; margin: 0 0 5mm; }}
.kopf {{ display: flex; align-items: center; gap: 3mm; }}
.nr {{ background: {INK}; color: white; border-radius: 50%; width: 9mm; height: 9mm; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13pt; }}
h2 {{ font-family: Kalam; font-size: 18pt; margin: 0; flex: 1; }}
.marke {{ font-size: 8.5pt; font-weight: 700; padding: 1mm 2.5mm; border-radius: 2mm; }}
.marke.ja {{ background: #d7efe9; color: {GRUEN}; }} .marke.nein {{ background: #eee; color: #666; }}
.meta {{ font-size: 8.8pt; color: #555; margin: 1mm 0 2mm; }}
.zeile {{ display: flex; gap: 4mm; align-items: flex-start; }}
.bild svg {{ width: 82mm; height: auto; }}
.bild.breit svg {{ width: 98mm; }}
.txt {{ flex: 1; }} .frage {{ font-weight: 700; margin-top: 0; }}
.rechnung {{ background: {PAPIER}; border-radius: 2mm; padding: 1mm 3mm; font-size: 12pt; }}
.rechnung math {{ margin: 2mm 0; }}
.pfiff {{ margin: 2mm 0 1mm; }}
.wahl {{ font-size: 11pt; margin-top: 2mm; }}
.umbruch {{ break-before: page; }}
</style></head><body>
<span class="leiste">MATHE VERSTEHEN · TRIGONOMETRIE · VIDEO 2</span>
<h1>Wofür braucht man Sinus und Kosinus?</h1>
<div class="intro">
Fast alles läuft auf <b>zwei Sorten Aufgaben</b> hinaus:
<b>Dreieck</b> – in einem rechtwinkligen Dreieck fehlende Seiten ausrechnen (Bau, Karten, Wege), und
<b>Kreis</b> – beschreiben, was sich gleichmäßig dreht und deshalb immer wiederholt (Riesenrad, Jahreszeiten).
Farben wie im Einheitskreis-Video: <b class="r">Sinus rot</b> (die Seite gegenüber vom Winkel),
<b class="b">Kosinus blau</b> (die Seite am Winkel), <b class="o">Winkel orange</b>.<br><br>
<b>Zum Aussuchen:</b> Das Video soll 2–3 Minuten lang sein, also <b>3 Beispiele</b>, höchstens 4. Nr. 1–3 sind der Vorschlag
(Mathe Klasse 10 in Hessen, ohne Physik), Nr. 4–5 sind Alternativen. Einfach ankreuzen.
</div>
{seiten}
</body></html>'''


if __name__ == '__main__':
    import subprocess
    quelle = HIER / 'beispiele.html'
    quelle.write_text(html(), encoding='utf-8')
    js = (f"const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('{quelle.as_uri()}');await p.waitForTimeout(500);"
          f"await p.pdf({{path:'{HIER / 'beispiele.pdf'}',format:'A4',printBackground:true,"
          f"margin:{{top:'14mm',bottom:'12mm',left:'14mm',right:'14mm'}}}});await b.close();}})();")
    subprocess.run(['node', '-e', js], check=True)
    quelle.unlink()
    print('beispiele.pdf geschrieben')
