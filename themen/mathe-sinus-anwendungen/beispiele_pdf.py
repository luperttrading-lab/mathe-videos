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


def text(x, y, t, farbe=INK, gr=20, anker='middle', fett=True):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{farbe}" font-size="{gr}" text-anchor="{anker}" font-weight="{"700" if fett else "400"}">{t}</text>'


def svg(inhalt, w=420, h=300):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" font-family="DejaVu Sans">{inhalt}</svg>'


# ---------------------------------------------------------------- Bilder
def bild_leiter():
    k = 52  # Pixel pro Meter
    wx, by = 120, 270  # Wand x, Boden y
    fx = wx + 1.71 * k
    ty = by - 4.70 * k
    s = f'<rect x="{wx - 18}" y="20" width="18" height="{by - 20}" fill="#d9d2c3"/>'
    s += f'<line x1="40" y1="{by}" x2="400" y2="{by}" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<line x1="{wx}" y1="{by}" x2="{wx}" y2="{ty}" stroke="{ROT}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{wx}" y1="{by}" x2="{fx}" y2="{by}" stroke="{BLAU}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{fx}" y1="{by}" x2="{wx}" y2="{ty}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    for i in range(1, 9):  # Sprossen
        t = i / 9
        x, y = fx + (wx - fx) * t, by + (ty - by) * t
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{INK}"/>'
    s += bogen(fx, by, 34, 110, 180)
    s += text(fx - 52, by - 14, '70°', ORANGE, 18)
    s += rechter_winkel(wx, by, 22, 0)
    s += text(wx - 30, (by + ty) / 2, 'Höhe', ROT, 18, 'end') + text(wx - 30, (by + ty) / 2 + 22, '≈ 4,70 m', ROT, 18, 'end')
    s += text((wx + fx) / 2, by + 26, '≈ 1,71 m', BLAU, 18)
    s += text((wx + fx) / 2 + 40, (by + ty) / 2 - 10, 'Leiter 5 m', INK, 18, 'start')
    return svg(s, 420, 300)


def bild_rampe():
    a = math.asin(1 / 5)
    k = 66
    x0, y0 = 20, 285
    xb, yt = x0 + 5 * math.cos(a) * k, y0 - 1 * k
    s = f'<polygon points="{x0},{y0} {xb:.1f},{y0} {xb:.1f},{yt:.1f}" fill="#e9e2d3" stroke="{INK}" stroke-width="3"/>'
    s += f'<line x1="{xb:.1f}" y1="{y0}" x2="{xb:.1f}" y2="{yt:.1f}" stroke="{ROT}" stroke-width="8" stroke-linecap="round"/>'
    s += rechter_winkel(xb, y0, 16, 90)
    s += bogen(x0, y0, 80, 0, math.degrees(a))
    s += text(x0 + 112, y0 - 6, 'α', ORANGE, 18)
    s += text(xb - 10, yt - 12, '1 m hoch', ROT, 16, 'end')
    s += text(x0 + (xb - x0) * 0.74 - 12, y0 + (yt - y0) * 0.74 - 16, '5 m lang', INK, 16, 'end')
    # Kiste auf der Rampe
    t, gr = 0.42, 30
    cx, cy = x0 + (xb - x0) * t, y0 + (yt - y0) * t
    dx, dy = math.cos(a), -math.sin(a)
    ux, uy = -math.sin(a), -math.cos(a)  # nach oben, senkrecht zur Rampe
    c1 = (cx - dx * gr / 2, cy - dy * gr / 2); c2 = (cx + dx * gr / 2, cy + dy * gr / 2)
    c3 = (c2[0] + ux * gr, c2[1] + uy * gr); c4 = (c1[0] + ux * gr, c1[1] + uy * gr)
    s += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in (c1, c2, c3, c4))}" fill="#c8a97e" stroke="{INK}" stroke-width="2.5"/>'
    # Kräftedreieck vergrößert (oben links)
    gx, gy, G = 70, 28, 150
    s += text(gx + 75, 22, 'Kräfte (vergrößert)', INK, 13, 'start', False)
    ex, ey = gx, gy + G
    bx_, by_ = gx + math.sin(a) * G * math.cos(a), gy + math.cos(a) * G * math.cos(a)
    s += pfeil(gx, gy, ex, ey, INK, 4)
    s += pfeil(gx, gy, bx_, by_, BLAU, 5)
    s += pfeil(bx_, by_, ex, ey, ROT, 5)
    s += bogen(gx, gy, 38, 270, 270 + math.degrees(a), ORANGE, 2.5)
    s += text(gx + 5, gy + 56, 'α', ORANGE, 15, 'start')
    s += text(gx - 10, gy + G / 2, '500 N', INK, 15, 'end')
    s += text(bx_ + 10, (gy + by_) / 2 + 4, '≈ 490 N', BLAU, 15, 'start')
    s += text(bx_ + 8, by_ + 16, '100 N', ROT, 15, 'start')
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
    return svg(s, 460, 300)


def bild_generator():
    cx, cy = 100, 150
    s = f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{GRAU}" stroke-width="3"/>'
    for wkl in (90, 270):
        x, y = cx + 80 * math.cos(math.radians(wkl)), cy - 80 * math.sin(math.radians(wkl))
        s += f'<rect x="{x - 22:.1f}" y="{y - 12:.1f}" width="44" height="24" rx="5" fill="#b87333" stroke="{INK}" stroke-width="2"/>'
    s += text(cx, cy - 98, 'Spule', INK, 15) + text(cx, cy + 112, 'Spule', INK, 15)
    rot = 30
    for farbe, sgn, lab in (('#555a70', 1, 'N'), ('#c9cbd4', -1, 'S')):
        x1, y1 = cx + sgn * 50 * math.cos(math.radians(rot)), cy - sgn * 50 * math.sin(math.radians(rot))
        s += f'<line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{farbe}" stroke-width="22"/>'
        s += text(x1 * 0.75 + cx * 0.25, y1 * 0.75 + cy * 0.25 + 6, lab, 'white' if lab == 'N' else INK, 16)
    s += bogen(cx, cy, 60, 120, 200, INK, 2)
    s += text(cx - 66, cy - 66, 'dreht', INK, 13, 'middle', False)
    x0, w, ym = 225, 180, 150
    s += f'<line x1="{x0}" y1="{ym}" x2="{x0 + w + 6}" y2="{ym}" stroke="{INK}" stroke-width="2"/><line x1="{x0}" y1="60" x2="{x0}" y2="240" stroke="{INK}" stroke-width="2"/>'
    pts = [f'{x0 + i / 100 * w:.1f},{ym - 70 * math.sin(2 * math.pi * 2 * i / 100):.1f}' for i in range(101)]
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GRUEN}" stroke-width="4"/>'
    s += text(x0 + w, 262, 'Zeit →', INK, 13, 'end', False) + text(x0 + 6, 54, 'Spannung', INK, 13, 'start', False)
    return svg(s, 420, 290)


def bild_wurf():
    k = 11
    x0, y0 = 120, 250
    a = math.radians(30)
    vx, vy = 20 * math.cos(a) * k, 20 * math.sin(a) * k
    s = f'<line x1="20" y1="{y0}" x2="400" y2="{y0}" stroke="{INK}" stroke-width="3.5"/>'
    s += f'<line x1="{x0 + vx:.1f}" y1="{y0}" x2="{x0 + vx:.1f}" y2="{y0 - vy:.1f}" stroke="{ROT}" stroke-width="2" stroke-dasharray="4 4"/>'
    s += f'<line x1="{x0}" y1="{y0 - vy:.1f}" x2="{x0 + vx:.1f}" y2="{y0 - vy:.1f}" stroke="{BLAU}" stroke-width="2" stroke-dasharray="4 4"/>'
    s += pfeil(x0, y0, x0 + vx, y0, BLAU, 6)
    s += pfeil(x0, y0, x0, y0 - vy, ROT, 6)
    s += pfeil(x0, y0, x0 + vx, y0 - vy, INK, 5)
    s += bogen(x0, y0, 56, 0, 30)
    s += text(x0 + 66, y0 - 10, '30°', ORANGE, 16, 'start')
    s += text(x0 + vx / 2 + 6, y0 - vy / 2 - 22, '20 m/s', INK, 17, 'end')
    s += text(x0 + vx / 2, y0 + 26, '≈ 17,3 m/s vorwärts', BLAU, 16)
    s += text(x0 - 12, y0 - vy / 2, '10 m/s', ROT, 16, 'end') + text(x0 - 12, y0 - vy / 2 + 20, 'hoch', ROT, 16, 'end')
    s += f'<circle cx="{x0 - 12}" cy="{y0 - 10}" r="9" fill="{INK}"/>'
    return svg(s, 420, 290)


def bild_kurs():
    k = 20
    x0, y0 = 90, 250
    a = math.radians(60)
    ox, ny = 10 * math.sin(a) * k, 10 * math.cos(a) * k
    s = pfeil(x0, y0, x0, 40, GRAU, 2.5) + text(x0, 32, 'N', INK, 18)
    s += pfeil(x0, y0, 400, y0, GRAU, 2.5) + text(392, y0 + 24, 'O', INK, 18)
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + ox:.1f}" y2="{y0}" stroke="{BLAU}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{x0 + ox:.1f}" y1="{y0}" x2="{x0 + ox:.1f}" y2="{y0 - ny:.1f}" stroke="{ROT}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0 + ox:.1f}" y2="{y0 - ny:.1f}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    s += bogen(x0, y0, 60, 30, 90)
    s += text(x0 + 80 * math.cos(math.radians(66)), y0 - 80 * math.sin(math.radians(66)), '60°', ORANGE, 16, 'start')
    s += rechter_winkel(x0 + ox, y0, 18, 90)
    s += text(x0 + ox / 2, y0 + 28, 'Osten ≈ 8,66 km', BLAU, 16)
    s += text(x0 + ox + 12, y0 - ny / 2 + 6, 'Norden 5 km', ROT, 16, 'start')
    s += text(x0 + ox / 2 + 14, y0 - ny / 2 + 26, '10 km', INK, 17, 'start')
    return svg(s, 420, 290)


# ---------------------------------------------------------------- Formeln (MathML, echte Brüche)
def bruch(z, n):
    return f'<mfrac><mrow>{z}</mrow><mrow>{n}</mrow></mfrac>'


def m(inhalt):
    import re
    inhalt = re.sub(r'<mi>(m|N|s|km|Hz)</mi>', r'<mspace width="0.17em"/><mi mathvariant="normal">\1</mi>', inhalt)
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
         pfiff='Es ist genau das Dreieck aus dem Einheitskreis – nur fünfmal so groß. Deshalb „mal 5“.'),
    dict(nr=2, titel='Kiste auf der Rampe', bereich='Physik: Goldene Regel der Mechanik', dauer='≈ 40 s',
         typ='Dreieck', lehrplan='Physik Kl. 10 (Hessen): „Arbeit und Energie … Goldene Regel der Mechanik“', drin=True,
         bild=bild_rampe(),
         frage='Eine Kiste hat 500 N Gewichtskraft (etwa 50 kg). Statt sie 1 m hochzuheben, schiebst du sie eine 5 m lange Rampe hinauf. Wie viel Kraft brauchst du?',
         erkl='Die Gewichtskraft zeigt senkrecht nach unten. Auf der Rampe teilt sie sich in zwei Teile: einen, der die Kiste '
              'die Rampe hinunterzieht (den musst du halten), und einen, der sie in die Rampe drückt (den trägt die Rampe). '
              'Reibung lassen wir weg.',
         rechnung=[m(f'<mi>sin</mi>{al}<mo>=</mo>{bruch(r("1 m"), "<mn>5</mn><mi>m</mi>")}<mo>=</mo>{bruch("<mn>1</mn>", "<mn>5</mn>")}'
                     f'<mspace width="1em"/><mo>⇒</mo><mspace width="1em"/>{t("Kraft hangabwärts")}<mo>=</mo><mn>500</mn><mi>N</mi><mo>·</mo>{bruch("<mn>1</mn>", "<mn>5</mn>")}<mo>=</mo>'
                     f'<mn style="color:{ROT}">100</mn><mi style="color:{ROT}">N</mi>'),
                   m(f'<mi>cos</mi>{al}<mo>=</mo><msqrt><mn>1</mn><mo>−</mo><msup><mrow><mo>(</mo>{bruch("<mn>1</mn>", "<mn>5</mn>")}<mo>)</mo></mrow><mn>2</mn></msup></msqrt>'
                     f'<mo>=</mo><msqrt>{bruch("<mn>24</mn>", "<mn>25</mn>")}</msqrt><mo>≈</mo><mn>0,98</mn>'
                     f'<mspace width="1em"/><mo>⇒</mo><mspace width="1em"/>{t("Druck auf die Rampe")}<mo>≈</mo><mn>500</mn><mi>N</mi><mo>·</mo><mn>0,98</mn><mo>=</mo>'
                     f'<mn style="color:{BLAU}">490</mn><mi style="color:{BLAU}">N</mi>')],
         pfiff='Goldene Regel: Der Weg ist 5-mal so lang, die Kraft 5-mal so klein. Arbeit bleibt gleich: 100 N · 5 m = 500 N · 1 m. '
               'Und cos α kommt aus sin² α + cos² α = 1 – dem Pythagoras aus dem Einheitskreis-Video.'),
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
    dict(nr=4, titel='Strom aus dem Generator', bereich='Physik: Energieversorgung', dauer='≈ 25 s',
         typ='Kreis', lehrplan='Physik Kl. 10 (Hessen): „Generator, Motor“, „Energieversorgung“', drin=True,
         bild=bild_generator(),
         frage='Warum heißt es Wechselstrom – und was hat das mit dem Sinus zu tun?',
         erkl='Im Generator dreht sich ein Magnet gleichmäßig, um ihn herum sitzen Spulen (im Schulmodell dreht sich die Spule im '
              'Magnetfeld – das wirkt genauso). Die Spannung in den Spulen steigt, fällt, wird negativ und steigt wieder: '
              'fast genau wie eine Sinuskurve, weil sich alles im Kreis dreht.',
         rechnung=[m(f'<mn>50</mn><mi>Hz</mi><mo>=</mo><mn>50</mn>{t(" Schwingungen pro Sekunde")}<mspace width="1em"/><mo>⇒</mo>'
                     f'<mspace width="1em"/>{t("eine Schwingung dauert\u00a0")}{bruch("<mn>1</mn>", "<mn>50</mn>")}<mi>s</mi><mo>=</mo><mn>0,02</mn><mi>s</mi>')],
         pfiff='Hier wird nichts ausgerechnet – das Beispiel zeigt, dass Sinuskurven aus jeder Steckdose kommen.'),
    dict(nr=5, titel='Ballwurf', bereich='Sport', dauer='≈ 30 s',
         typ='Dreieck', lehrplan='Würfe kommen in Hessen erst in der Oberstufe – Vorgriff', drin=False,
         bild=bild_wurf(),
         frage='Ein Ball wird mit 20 m/s unter 30° abgeworfen. Wie schnell fliegt er vorwärts, wie schnell nach oben?',
         erkl='Die Geschwindigkeit ist ein Pfeil schräg nach oben. Man zerlegt ihn in einen waagrechten und einen senkrechten Teil – '
              'das gibt wieder ein rechtwinkliges Dreieck.',
         rechnung=[m(f'{b("vorwärts")}<mo>=</mo><mn>20</mn><mo>·</mo><mi>cos</mi><mn>30°</mn><mo>≈</mo><mn>17,3</mn>{t(" m/s")}'
                     f'<mspace width="1.4em"/>{r("hoch")}<mo>=</mo><mn>20</mn><mo>·</mo><mi>sin</mi><mn>30°</mn><mo>=</mo><mn>20</mn><mo>·</mo>{bruch("<mn>1</mn>", "<mn>2</mn>")}<mo>=</mo><mn>10</mn>{t(" m/s")}')],
         pfiff='sin 30° = ½ kennst du schon aus dem Einheitskreis-Video.'),
    dict(nr=6, titel='Schiffskurs', bereich='Navigation', dauer='≈ 25 s',
         typ='Dreieck', lehrplan='nicht ausdrücklich im Lehrplan – klassische Schulbuch-Aufgabe', drin=False,
         bild=bild_kurs(),
         frage='Ein Schiff fährt 10 km auf Kurs 60°. Wie weit ist es nach Osten und nach Norden gekommen?',
         erkl='Achtung, Falle: Ein Kurs wird von Norden aus im Uhrzeigersinn gemessen – anders als im Einheitskreis. '
              'Deshalb tauschen Sinus und Kosinus hier die Rollen.',
         rechnung=[m(f'{b("Osten")}<mo>=</mo><mn>10</mn><mo>·</mo><mi>sin</mi><mn>60°</mn><mo>≈</mo><mn>8,66</mn><mi>km</mi>'
                     f'<mspace width="1.4em"/>{r("Norden")}<mo>=</mo><mn>10</mn><mo>·</mo><mi>cos</mi><mn>60°</mn><mo>=</mo><mn>5</mn><mi>km</mi>')],
         pfiff='Gut, um zu üben: Nie „waagrecht = Kosinus“ auswendig lernen, sondern immer schauen, wo der Winkel liegt.'),
]


def seite(bsp):
    marke = ('<span class="marke ja">im Video-Vorschlag</span>' if bsp['drin']
             else '<span class="marke nein">Alternative</span>')
    return f'''
<section class="bsp">
  <div class="kopf"><span class="nr">{bsp["nr"]}</span><h2>{bsp["titel"]}</h2>{marke}</div>
  <div class="meta">{bsp["bereich"]} · Typ: <b>{bsp["typ"]}</b> · im Video {bsp["dauer"]}<br><i>{bsp["lehrplan"]}</i></div>
  <div class="zeile">
    <div class="bild">{bsp["bild"]}</div>
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
<b>Dreieck</b> – in einem rechtwinkligen Dreieck fehlende Seiten ausrechnen (Bau, Kräfte, Wege), und
<b>Kreis</b> – beschreiben, was sich gleichmäßig dreht und deshalb immer wiederholt (Riesenrad, Strom).
Farben wie im Einheitskreis-Video: <b class="r">Sinus / senkrecht rot</b>, <b class="b">Kosinus / waagrecht blau</b>,
<b class="o">Winkel orange</b>.<br><br>
<b>Zum Aussuchen:</b> Das Video soll 2–3 Minuten lang sein, also <b>3–4 Beispiele</b>. Nr. 1–4 sind der Vorschlag
(alles Stoff aus Mathe oder Physik Klasse 10 in Hessen), Nr. 5–6 sind Alternativen. Einfach ankreuzen.
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
