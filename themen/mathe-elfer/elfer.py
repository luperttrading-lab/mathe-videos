#!/usr/bin/env python3
"""Folge 2 der Reihe „Kopfrechnen“: Der Elfer-Trick (Entwurf 06.11., Drehbuch drehbuch.md).

    ab · 11 = ab · 10 + ab = 100·a + 10·(a + b) + b      →   a | a + b | b
    43 · 11 = 473        87 · 11 = 957 (8 + 7 = 15: die 5 in die Lücke, die 1 zur 8)
    4352 · 11 = 47872    Übung 53 · 11 = 583

Baukasten aus Folge 1 (`../mathe-einmaleins/regel.py`): Ton, Zeitmarken, Kapitelkopf, App-Seite, Abspann, Rendern.
Hier stehen nur Sprechtext, Bilder und Klänge dieser Folge. Sie ersetzen die Modul-Variablen von regel.py (SZENEN,
ZEICHNER, KLAENGE, CACHE, APP_BILD, QR_BILD, MERKSAETZE), die dessen Funktionen erst beim Aufruf nachschlagen.

Aufruf wie regel.py: python3 elfer.py <ausgabe.mp4> [--nur-ton] [--bild <s>[,<s>…]]
"""
import math, os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-einmaleins'))
import regel as G                                          # noqa: E402
from regel import (INK, GRAU, HELL, CA, CB, CD, TEAL, GRUEN, INTER, INTER_X, C, band, breite, ein,  # noqa: E402
                   einblenden, einkreisen, funken, glatt, karte, klemm, mischfarbe, mitten, mix, p, schritte, spur,
                   zeile, zurueck)
from motivation import spruch                              # noqa: E402

UHR = 3                     # zweistellig mal 11: drei Sekunden (wie die App-Stufe „Mal 11“)
DENKPAUSE = 6.5             # Uhr (3 s), dann die Lösung in vier Zeilen
PAUSE = G.PAUSE
SPRUCH = spruch('mathe-elfer', 'schluss')
BRUECKE = spruch('mathe-elfer', 'bruecke')                 # „Kein Trick ohne Grund.“ (passt besser als „Klingt komplizierter …“)

SZENEN = [
    dict(id='hook', kicker='Kopfrechnen', text=(
        'Viertausenddreihundertzweiundfünfzig mal elf. Im Kopf? Mit dem Elfer-Trick klappt das für jede Zahl, '
        'Ziffer für Ziffer. Wir fangen klein an.')),
    dict(id='regel', kicker='Der Trick', text=(
        'Dreiundvierzig mal elf. Zieh die Vier und die Drei auseinander. In die Lücke kommt ihre Summe: vier plus '
        'drei gleich sieben. Ergebnis: vierhundertdreiundsiebzig.')),
    dict(id='warum', kicker='Warum klappt das?', text=(
        BRUECKE + ' Mal elf heißt: mal zehn und noch einmal die Zahl. Also vierhundertdreißig plus dreiundvierzig. '
        'Untereinander geschrieben: Vorne steht nur die Vier, hinten nur die Drei, denn darüber steht die Null. In '
        'der Mitte stehen Drei und Vier übereinander. Deshalb kommt dort ihre Summe hin.')),
    dict(id='vorsicht', kicker='Vorsicht', text=(
        'Aber Vorsicht bei siebenundachtzig mal elf. Acht plus sieben ist fünfzehn. Zwei Ziffern passen nicht in die '
        'Lücke. Also kommt nur die Fünf hinein, und die Eins wandert nach vorn: Aus der Acht wird eine Neun. '
        'Ergebnis: neunhundertsiebenundfünfzig.')),
    # Nutzerfrage 07.11. (Vorschau-Seite): Wann bekommt das Ergebnis eine Ziffer mehr? Genau dann, wenn vorne eine Neun
    # steht und eine Eins dazu wandert (zweistellig: 91 … 99). 97 statt 91: bei 91 hieße es zweimal „9 + 1 = 10“
    dict(id='neun', kicker='Vorsicht', anhang=True, text=(
        # Nutzer 07.11. zur ersten Fassung: sagen, WELCHE Eins wandert (die aus der Summe direkt hinter der Neun), und in
        # Wort und Bild zeigen, dass meist eine Ziffer dazukommt (2 → 3, 3 → 4) und wann zwei (2 → 4, 3 → 5)
        # Nutzerwahl 07.11. (Hörprobe, Satz 1): „… als die Zahl, die mit elf multipliziert wird“ – vorher war „Zahl“ falsch betont
        'Wie viele Ziffern hat das Ergebnis? Meistens eine mehr als die Zahl, die mit elf multipliziert wird: Aus zwei '
        'Ziffern werden drei, aus drei Ziffern vier. Zwei mehr gibt es nur, wenn vorne eine Neun steht und die Summe '
        'direkt dahinter zweistellig ist. '
        'Siebenundneunzig mal elf: Neun plus sieben ist sechzehn. Die Sechs kommt in die Lücke, die Eins wandert zur '
        'Neun, und aus der Neun wird eine Zehn. Ergebnis: tausendsiebenundsechzig. Aus zwei Ziffern werden vier.')),
    dict(id='gross', kicker='Große Zahlen', text=(
        'Und jetzt die große Zahl vom Anfang. Wir gehen von hinten nach vorn. Hinten bleibt die Zwei. Dann immer eine '
        'Ziffer plus ihr rechter Nachbar: fünf plus zwei gleich sieben, drei plus fünf gleich acht, vier plus drei '
        'gleich sieben. Vorne bleibt die Vier. Zusammen: siebenundvierzigtausendachthundertzweiundsiebzig.')),
    dict(id='merke', kicker='Merke', pause=DENKPAUSE, text=(
        'Merk dir: Die erste und die letzte Ziffer bleiben. Dazwischen kommt immer die Summe zweier Nachbarn. Ist eine '
        'Summe zweistellig, wandert die Eins nach vorn. Und jetzt du: dreiundfünfzig mal elf.')),
    dict(id='schluss', kicker='Merke', anhang=True, pause=1.0, text=(
        'Hat es bei dir länger als drei Sekunden gedauert? Ganz normal. Mit ein bisschen Übung schaffst du das auch '
        'so schnell. ' + SPRUCH)),
    # App-Satz und Abspann wörtlich wie in Folge 1 (gleicher Ton aus dem Cache, kostet nichts)
    dict(id='app', kicker='Merke', anhang=True, pause=2.5, text=(
        'Üben kannst du in der kostenlosen App. Den Link findest du unter dem Video.')),
    dict(id='abspann', kicker='Kopfrechnen', anhang=True, pause=G.ABSPANN, text=(
        'Noch ein Trick? Hier geht\'s weiter. Und damit du nichts verpasst: Abonnier den Kanal.')),
]

MERKSAETZE = [  # (Nummer, Farbe, Zeilen auf dem Merkzettel = genau der gesprochene Satz, Stichwort)
    ('1', CB, ['Die erste und die letzte', 'Ziffer bleiben'], 'Die erste'),
    ('2', TEAL, ['Dazwischen kommt immer die', 'Summe zweier Nachbarn'], 'Dazwischen'),
    ('3', CD, ['Ist eine Summe zweistellig,', 'wandert die Eins nach vorn'], 'Ist eine Summe')]


# ---------------------------------------------------------------- Bühne für zweistellige Zahlen (Trick, Vorsicht)
X2, YT2, G2 = 400, 175, 112                                # Aufgabe oben links
YR2, PP2, YL2 = 410, 104, 292                              # Ergebniszeile, Abstand der drei Plätze, Summe darüber


def oben2(b, t, za, zb, kreise, alpha=1.0):
    """Aufgabe „ab · 11“, a orange, b violett; kreise = [(i, von, bis)]: Ziffer i eingekreist."""
    teile = [(za, CA), (zb, CB), (' · 11', INK)]
    cs = mitten(teile, X2, G2)
    for i, von, bis in kreise:
        einkreisen(b, teile[i][0], cs[i], YT2, G2, teile[i][1], ein(t, von, 0.3) * (1 - ein(t, bis, 0.3)) * alpha)
    zeile(b, teile, X2, YT2, G2, INTER_X, alpha=alpha)
    return cs


def luecke(b, t, von, bis, rot=None):
    """Leerer Platz zwischen den beiden Ziffern, pocht kurz, wenn er genannt wird; rot = (von, bis): rot getönt
    (zu klein für zwei Ziffern)."""
    a = ein(t, von, 0.35) * (1 - ein(t, bis, 0.3))
    if a > 0:
        s = 1 + 0.08 * math.sin(math.pi * p(t, von, 0.6))
        w, h = 0.66 * PP2 * s, 0.95 * G2 * s
        r = ein(t, rot[0], 0.3) * (1 - ein(t, rot[1], 0.3)) if rot else 0.0
        band(b, X2 - w / 2, YR2 - h / 2, X2 + w / 2, YR2 + h / 2, mischfarbe(HELL, '#f4c7cb', r), 0.95 * a, r=14)


def auseinander(b, t, cs, za, zb, t_flug, x_a, x_b, farbe_a=None, farbe_b=None, alpha_a=1.0):
    """Die beiden Ziffern wandern von der Aufgabe nach unten auf die äußeren Plätze."""
    f = glatt(p(t, t_flug, 0.9))
    if f <= 0:
        return
    for s, c, x0, x1, seite, a in ((za, farbe_a or CA, cs[0], x_a, -1, alpha_a), (zb, farbe_b or CB, cs[1], x_b, 1, 1.0)):
        b.text(s, mix(x0, x1, f) + seite * 40 * math.sin(math.pi * f), mix(YT2, YR2, f), G2, c, INTER_X,
               alpha=klemm(f * 3) * a)


def s_hook(b, sc, t):
    q = zurueck(p(t, 0.0, 0.7))
    tz, tk = C(sc, 'Ziffer für'), C(sc, 'Im Kopf')
    hops = [math.sin(math.pi * p(t, tz + 0.16 * i, 0.38)) for i in range(4)]   # „Ziffer für Ziffer“: jede hüpft kurz
    teile = [(z, mischfarbe(INK, TEAL, h)) for z, h in zip('4352', hops)] + [(' · ', INK), ('11', CB), (' = ?', GRAU)]
    eff = {i: dict(dy=-20 * h) for i, h in enumerate(hops)}
    eff[6] = dict(skala=1 + 0.12 * math.sin(math.pi * p(t, tk, 0.5)))
    zeile(b, teile, 640, 270, 150 * (0.6 + 0.4 * q), INTER_X, alpha=klemm(q * 2), effekte=eff)
    qn = zurueck(p(t, C(sc, 'Elfer-Trick'), 0.45))        # Name des Tricks als Band, wie in Folge 1
    if qn > 0:
        an = klemm(qn * 2)
        hw = (breite('Der Elfer-Trick', INTER_X, 44) + 90) / 2
        band(b, 640 - hw * qn, 450 - 43 * qn, 640 + hw * qn, 450 + 43 * qn, TEAL, 0.95 * an, r=16)
        b.text('Der Elfer-Trick', 640, 450, 44, '#ffffff', INTER_X, skala=max(qn, 0.01), alpha=an)
    einblenden(b, [('Erst mal: ', GRAU), ('43 · 11', INK)], 640, 590, 40, t, C(sc, 'klein'))


def s_regel(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(zieh='Zieh', vier='die Vier', drei='die Drei', aus='auseinander', luecke='Lücke',
                                         plus='vier plus', sieben='gleich sieben', erg='Ergebnis',
                                         z473='vierhundert').items()}
    cs = oben2(b, t, '4', '3', [(0, T['vier'], T['aus'] + 0.5), (1, T['drei'], T['aus'] + 0.5)])
    luecke(b, t, T['luecke'], T['sieben'] + 0.3)
    kompakt = glatt(p(t, T['z473'], 0.5))                  # zum Schluss rücken die Ziffern zur Zahl zusammen
    ziel = mitten([('4', INK), ('7', INK), ('3', INK)], X2, G2)
    gruen = p(t, T['z473'], 0.4)
    auseinander(b, t, cs, '4', '3', T['aus'], mix(X2 - PP2, ziel[0], kompakt), mix(X2 + PP2, ziel[2], kompakt),
                mischfarbe(CA, GRUEN, gruen), mischfarbe(CB, GRUEN, gruen))
    al = ein(t, T['plus']) * (1 - ein(t, T['sieben'] + 0.2, 0.3))   # „4 + 3“ über der Lücke, die 7 fällt hinein
    if al > 0:
        zeile(b, [('4', CA), (' + ', INK), ('3', CB)], X2, YL2 + 10 * (1 - ein(t, T['plus'])), 46, INTER_X, alpha=al)
    f7 = p(t, T['sieben'], 0.55)
    if f7 > 0:
        g7 = glatt(f7)
        b.text('7', mix(X2, ziel[1], kompakt), mix(YL2, YR2, g7), mix(46, G2, g7) * (1 + 0.1 * math.sin(math.pi * f7)),
               mischfarbe(TEAL, GRUEN, gruen), INTER_X, alpha=klemm(f7 * 4))
    funken(b, t, T['z473'] + 0.1, X2, YR2, r0=80, r1=200)
    zeilen = [dict(nr='1', farbe=CB, titel='Ziffern auseinander', t_titel=T['zieh'], t_rech=T['aus'] + 0.4,
                   teile=[('4', CA), ('  _  ', GRAU), ('3', CB)], aktiv=(T['zieh'], T['luecke'])),
              dict(nr='2', farbe=TEAL, titel='Summe in die Lücke', t_titel=T['luecke'], t_rech=T['sieben'] + 0.3,
                   teile=[('4', CA), (' + ', INK), ('3', CB), (' = ', INK), ('7', TEAL)],
                   aktiv=(T['luecke'], T['z473']))]
    schritte(b, t, 780, 170, 440, zeilen, ([('43 · 11 = ', INK), ('473', GRUEN)], T['z473']),
             alpha=ein(t, T['zieh'] - 0.4, 0.4))


def s_warum(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(zehn='mal zehn', einmal='noch einmal', z430='vierhundertdreißig',
                                         unter='Untereinander', vorne='Vorne', hinten='hinten nur', null='Null',
                                         mitte='In der', summe='Summe').items()}
    T['z43'] = C(sc, 'dreiundvierzig', 'plus')
    a0, a1, a2 = ein(t, 0.1), ein(t, T['zehn']), ein(t, T['einmal'])
    zeile(b, [('43 · 11', INK), (' = ', GRAU), ('43 · 10', INK), (' + ', GRAU), ('43', INK)], 640, 150, 54, INTER_X,
          effekte={0: dict(alpha=a0), 1: dict(alpha=a1), 2: dict(alpha=a1), 3: dict(alpha=a2), 4: dict(alpha=a2)})
    PP, g, y1, y2, y3 = 88, 100, 290, 392, 516
    xs = [640 + (k - 1) * PP for k in range(3)]
    # Spalten nacheinander hinterlegen: vorne, hinten, Mitte (die Mitte bleibt)
    for k, c, von, bis in ((0, CA, T['vorne'], T['hinten']), (2, CB, T['hinten'], T['mitte']),
                           (1, TEAL, T['mitte'], 1e9)):
        a = ein(t, von, 0.3) * (1 - ein(t, bis, 0.3))
        band(b, xs[k] - PP / 2 + 6, y1 - 62, xs[k] + PP / 2 - 6, y2 + 54, c, 0.14 * a, r=16)
    einkreisen(b, '0', xs[2], y1, g, GRAU, ein(t, T['null'], 0.3) * (1 - ein(t, T['mitte'], 0.3)))
    for k, (s, c) in enumerate((('4', CA), ('3', CB), ('0', GRAU))):
        einblenden(b, [(s, c)], xs[k], y1, g, t, T['z430'] + 0.08 * k)
    for k, (s, c) in ((1, ('4', CA)), (2, ('3', CB))):
        einblenden(b, [(s, c)], xs[k], y2, g, t, T['z43'] + 0.08 * k)
    einblenden(b, [('+', INK)], xs[0] - PP + 6, y2, g, t, T['z43'])
    au = ein(t, T['unter'], 0.6)
    if au > 0:
        b.linie([(xs[0] - PP - 30, y2 + 62), (mix(xs[0] - PP - 30, xs[2] + PP / 2 + 10, au), y2 + 62)], INK, 5)
    tg = T['summe'] + 0.7                                  # alles fertig: Ergebnis grün
    gruen = p(t, tg, 0.4)
    for k, (s, c, ts) in enumerate((('4', CA, T['vorne'] + 0.4), ('7', TEAL, T['summe']), ('3', CB, T['hinten'] + 0.4))):
        einblenden(b, [(s, mischfarbe(c, GRUEN, gruen))], xs[k], y3, g, t, ts)
    einblenden(b, [('3', CB), (' + ', INK), ('4', CA), (' = ', INK), ('7', TEAL)], xs[1], 610, 38, t, T['mitte'] + 0.6)
    funken(b, t, tg, xs[1], y3, r0=70, r1=190)


def s_vorsicht(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(mal='mal elf', plus='Acht plus', z15='fünfzehn', zwei='Zwei Ziffern',
                                         fuenf='nur die Fünf', eins='die Eins wandert', acht='Aus der Acht',
                                         z957='neunhundert').items()}
    cs = oben2(b, t, '8', '7', [])
    luecke(b, t, T['mal'] + 0.5, T['fuenf'] + 0.5, rot=(T['zwei'], T['fuenf']))   # rot: zu klein für die 15
    kompakt = glatt(p(t, T['z957'], 0.5))
    ziel = mitten([('9', INK), ('5', INK), ('7', INK)], X2, G2)
    gruen = p(t, T['z957'], 0.4)
    f9 = p(t, T['acht'] + 0.25, 0.5)                       # aus der 8 wird eine 9
    x8 = mix(X2 - PP2, ziel[0], kompakt)
    auseinander(b, t, cs, '8', '7', T['mal'], x8, mix(X2 + PP2, ziel[2], kompakt),
                mischfarbe(CA, GRUEN, gruen), mischfarbe(CB, GRUEN, gruen), alpha_a=1 - klemm(f9 * 3))
    if f9 > 0:                                             # die 8 blendet aus, die 9 springt auf
        b.text('9', x8, YR2, G2 * (0.7 + 0.3 * zurueck(f9)), mischfarbe(CD, GRUEN, gruen), INTER_X, alpha=klemm(f9 * 3))
    # „8 + 7 = 15“ steht über der Lücke. Die 15 passt nicht hinein (Nutzer-Bild 06.11.: in der Reihe las sie sich wie
    # „8157“): nur die 5 fällt in die Lücke, die 1 springt zur 8
    lab = [('8', CA), (' + ', INK), ('7', CB), (' = ', INK), ('1', CD), ('5', CD)]
    lx = mitten(lab, X2, 46)
    a_lab = ein(t, T['plus'])
    a_rest = a_lab * (1 - ein(t, T['fuenf'], 0.3))
    for i in range(4):
        b.text(lab[i][0], lx[i], YL2 + 10 * (1 - a_lab), 46, lab[i][1], INTER_X, alpha=a_rest)
    a15 = ein(t, T['z15'], 0.3)
    zittern = 5 * math.sin(2 * math.pi * 4 * (t - T['zwei'])) * (1 - p(t, T['zwei'], 0.9)) if t > T['zwei'] else 0.0
    puls = 1 + 0.15 * math.sin(math.pi * p(t, T['zwei'], 0.5))
    g5 = glatt(p(t, T['fuenf'], 0.55))
    b.text('5', mix(mix(lx[5] + zittern, X2, g5), ziel[1], kompakt), mix(YL2, YR2, g5), mix(46 * puls, G2, g5),
           mischfarbe(mischfarbe(CD, TEAL, g5), GRUEN, gruen), INTER_X, alpha=a15)
    f1 = glatt(p(t, T['eins'], 0.7))
    rein = glatt(p(t, T['acht'], 0.35))
    z1 = (X2 - PP2, YR2 - 98)                              # über der 8

    def ort1(tt):
        ff = glatt(p(tt, T['eins'], 0.7))
        return None if not 0 < ff < 1 else (mix(lx[4], z1[0], ff), mix(YL2, z1[1], ff) - 40 * math.sin(math.pi * ff))
    spur(b, ort1, t, CD)
    b.text('1', mix(lx[4] + zittern, z1[0], f1), mix(YL2, z1[1], f1) - 40 * math.sin(math.pi * f1) + 60 * rein,
           mix(46 * puls, 64, f1), CD, INTER_X, alpha=a15 * (1 - rein))
    funken(b, t, T['z957'] + 0.1, X2, YR2, r0=80, r1=200)
    zeilen = [dict(nr='1', farbe=TEAL, titel='Summe in die Lücke', t_titel=T['plus'], t_rech=T['z15'] + 0.3,
                   teile=[('8', CA), (' + ', INK), ('7', CB), (' = ', INK), ('15', CD)], aktiv=(T['plus'], T['eins'])),
              dict(nr='2', farbe=CD, titel='Die Eins wandert nach vorn', t_titel=T['eins'], t_rech=T['acht'] + 0.5,
                   teile=[('8', CA), (' + ', INK), ('1', CD), (' = ', INK), ('9', CD)], aktiv=(T['eins'], T['z957']))]
    schritte(b, t, 780, 170, 440, zeilen, ([('87 · 11 = ', INK), ('957', GRUEN)], T['z957']),
             alpha=ein(t, T['plus'] - 0.4, 0.4))             # Karte erst mit ihrer ersten Zeile


def kaestchen(b, x, y, n, c, alpha=1.0, k=26, abstand=7):
    """n Kästchen nebeneinander ab x (linke Kante), Mitte y: eine Ziffer = ein Kästchen. Gibt die rechte Kante zurück."""
    for i in range(n):
        band(b, x + i * (k + abstand), y - k / 2, x + i * (k + abstand) + k, y + k / 2, c, alpha, r=6)
    return x + n * (k + abstand) - abstand


def stellen(b, x, y, n, m, c, alpha, k=26):
    """„n Kästchen → m Kästchen“ ab x: so viele Ziffern hat die Zahl, so viele das Ergebnis."""
    x1 = kaestchen(b, x, y, n, GRAU, 0.55 * alpha, k)
    b.text('→', x1 + 30, y, k * 1.2, GRAU, INTER_X, alpha=alpha)
    return kaestchen(b, x1 + 60, y, m, c, alpha, k)


def s_neun(b, sc, t):
    """Wie viele Ziffern hat das Ergebnis? Meist eine mehr als die Zahl (2 → 3, 3 → 4), zwei mehr genau dann, wenn vorne
    eine 9 steht und die Summe direkt dahinter zweistellig ist (mit wandernder Eins von weiter hinten): dann wird aus der
    9 eine 10. Zweistellig ab 91, dreistellig ab 910, vierstellig ab 9091 (x · 11 ≥ 10^(n+1)). Beispiel 97 · 11 = 1067."""
    T = {k: C(sc, w) for k, w in dict(r1='Aus zwei Ziffern', r2='aus drei Ziffern', r3='Zwei mehr', s97='Siebenundneunzig',
                                         mal='mal elf', plus='Neun plus', z16='sechzehn', sechs='Die Sechs',
                                         eins='die Eins wandert', zehn='aus der Neun', z='tausend').items()}
    T['ende'] = C(sc, 'Aus zwei Ziffern', 'tausend')
    # Teil 1: Übersicht in Wort und Bild, verschwindet bei „Siebenundneunzig“
    aA = ein(t, 0.05) * (1 - ein(t, T['s97'] - 0.35, 0.4))
    if aA > 0:
        karte(b, 170, 140, 940, 420, aA)
        b.text('WIE VIELE ZIFFERN HAT DAS ERGEBNIS?', 210, 180, 22, GRAU, INTER_X, anker='l', alpha=aA)
        zeilen_ = [(T['r1'], [('43 · 11 = ', INK), ('473', GRUEN)], 2, 3, TEAL, 'meistens eine mehr'),
                   (T['r2'], [('352 · 11 = ', INK), ('3872', GRUEN)], 3, 4, TEAL, 'meistens eine mehr'),
                   (T['r3'], [('9', CA), (' vorne, Summe dahinter', INK)], 2, 4, CD, 'zwei mehr')]
        for k, (tz, links, n, m, c, wort) in enumerate(zeilen_):
            a = ein(t, tz) * aA
            if a <= 0:
                continue
            y = 262 + k * 104 + 12 * (1 - ein(t, tz))
            if k == 2:                                     # dritte Zeile hinterlegt: der Sonderfall
                band(b, 186, y - 46, 1094, y + 46, CD, 0.07 * a, r=16)
                zeile(b, links, 210, y - 14, 36, INTER_X, alpha=a, anker='l')
                b.text('zweistellig', 210, y + 24, 36, CD, INTER_X, anker='l', alpha=a)
            else:
                zeile(b, links, 210, y, 46, INTER_X, alpha=a, anker='l')
            stellen(b, 690, y - 12, n, m, c, a)
            b.text(f'{n} → {m} Ziffern · {wort}', 690, y + 26, 22, c if k == 2 else GRAU, INTER_X, anker='l', alpha=a)
    # Teil 2: das Beispiel 97 · 11
    aE = ein(t, T['s97'] - 0.1, 0.4)
    if aE <= 0:
        return
    cs = oben2(b, t, '9', '7', [], alpha=aE)
    luecke(b, t, T['mal'] + 0.5, T['sechs'] + 0.5)
    kompakt = glatt(p(t, T['z'], 0.5))
    ziel = mitten([('10', INK), ('6', INK), ('7', INK)], X2, G2)
    gruen = p(t, T['z'], 0.4)
    f10 = p(t, T['zehn'] + 0.25, 0.5)                      # aus der 9 wird eine 10 (zwei Ziffern, rechtsbündig am Platz)
    w9, w10 = breite('9', INTER_X, G2), breite('10', INTER_X, G2)
    x9 = mix(X2 - PP2, ziel[0], kompakt)
    x10 = mix(X2 - PP2 - (w10 - w9) / 2 - 8, ziel[0], kompakt)
    auseinander(b, t, cs, '9', '7', T['mal'], x9, mix(X2 + PP2, ziel[2], kompakt),
                mischfarbe(CA, GRUEN, gruen), mischfarbe(CB, GRUEN, gruen), alpha_a=1 - klemm(f10 * 3))
    if f10 > 0:
        b.text('10', x10, YR2, G2 * (0.7 + 0.3 * zurueck(f10)), mischfarbe(CD, GRUEN, gruen), INTER_X, alpha=klemm(f10 * 3))
    lab = [('9', CA), (' + ', INK), ('7', CB), (' = ', INK), ('1', CD), ('6', CD)]
    lx = mitten(lab, X2, 46)
    a_lab = ein(t, T['plus'])
    a_rest = a_lab * (1 - ein(t, T['sechs'], 0.3))
    for i in range(4):
        b.text(lab[i][0], lx[i], YL2 + 10 * (1 - a_lab), 46, lab[i][1], INTER_X, alpha=a_rest)
    a16 = ein(t, T['z16'], 0.3)
    g6 = glatt(p(t, T['sechs'], 0.55))
    b.text('6', mix(mix(lx[5], X2, g6), ziel[1], kompakt), mix(YL2, YR2, g6), mix(46, G2, g6),
           mischfarbe(mischfarbe(CD, TEAL, g6), GRUEN, gruen), INTER_X, alpha=a16)
    f1 = glatt(p(t, T['eins'], 0.7))
    rein = glatt(p(t, T['zehn'], 0.35))
    z1 = (X2 - PP2, YR2 - 98)                              # über der 9

    def ort1(tt):
        ff = glatt(p(tt, T['eins'], 0.7))
        return None if not 0 < ff < 1 else (mix(lx[4], z1[0], ff), mix(YL2, z1[1], ff) - 40 * math.sin(math.pi * ff))
    spur(b, ort1, t, CD)
    b.text('1', mix(lx[4], z1[0], f1), mix(YL2, z1[1], f1) - 40 * math.sin(math.pi * f1) + 60 * rein,
           mix(46, 64, f1), CD, INTER_X, alpha=a16 * (1 - rein))
    funken(b, t, T['z'] + 0.1, X2, YR2, r0=80, r1=200)
    am = ein(t, T['ende'], 0.4)                             # „Aus zwei Ziffern werden vier“: 10 rot unterstrichen, Kästchen
    if am > 0:
        ox, oy, w, h = G.tinte('10', G2)
        cx, cy = ziel[0] + ox, YR2 + oy
        b.linie([(cx - w / 2, cy + h / 2 + 14), (cx - w / 2 + w * am, cy + h / 2 + 14)], CD, 7)
        breit = 2 * 33 - 7 + 60 + 4 * 33 - 7               # Breite von „▢▢ → ▢▢▢▢“
        stellen(b, X2 - breit / 2, YR2 + 112 + 10 * (1 - am), 2, 4, CD, am)
        b.text('Aus 2 Ziffern werden 4', X2, YR2 + 156 + 10 * (1 - am), 26, CD, INTER_X, alpha=am)
    zeilen = [dict(nr='1', farbe=TEAL, titel='Summe in die Lücke', t_titel=T['plus'], t_rech=T['z16'] + 0.3,
                   teile=[('9', CA), (' + ', INK), ('7', CB), (' = ', INK), ('16', CD)], aktiv=(T['plus'], T['eins'])),
              dict(nr='2', farbe=CD, titel='Die Eins wandert zur Neun', t_titel=T['eins'], t_rech=T['zehn'] + 0.5,
                   teile=[('9', CA), (' + ', INK), ('1', CD), (' = ', INK), ('10', CD)], aktiv=(T['eins'], T['z']))]
    schritte(b, t, 780, 170, 440, zeilen, ([('97 · 11 = ', INK), ('1067', GRUEN)], T['z']),
             alpha=ein(t, T['plus'] - 0.4, 0.4))


def s_gross(b, sc, t):
    T = {k: C(sc, w) for k, w in dict(start='große Zahl', richtung='von hinten', hinten='Hinten bleibt',
                                         p1='fünf plus zwei', e1='gleich sieben', p2='drei plus fünf', e2='gleich acht',
                                         p3='vier plus drei', vorne='Vorne bleibt', zus='Zusammen',
                                         z='siebenundvierzigtausend').items()}
    T['e3'] = C(sc, 'gleich sieben', 'vier plus drei')
    PP, g, yo, yl, yu = 92, 100, 168, 270, 384
    w_mal = breite(' · 11', INTER_X, g)
    links = 640 - (4 * PP + w_mal) / 2
    xo = [links + PP / 2 + i * PP for i in range(4)]       # Ziffern der Aufgabe
    xu = [links + PP / 2 + (k - 0.5) * PP for k in range(5)]   # Ergebnis: jede Ziffer unter ihrem Nachbarpaar
    a0 = ein(t, 0.05)
    gruen = p(t, T['z'], 0.4)
    kompakt = glatt(p(t, T['zus'], 0.5))
    ziel = mitten([(z, INK) for z in '47872'], 640, g)
    unten = glatt(p(t, T['z'] + 1.0, 0.8))                 # zum Schluss eine Gleichung: „4352 · 11 = 47872“
    zl = [(z, INK) for z in '4352'] + [(' · 11', INK), (' = ', INK)] + [(z, GRUEN) for z in '47872']
    zx, ys, gs = mitten(zl, 640, 76), 360, 76

    def lage(j, x, y, gg):
        return mix(x, zx[j], unten), mix(y, ys, unten), mix(gg, gs, unten)
    # Paare (und die Enden) hinterlegen, solange sie dran sind
    abschnitte = [((3, 3), CB, T['hinten'], T['p1']), ((2, 3), TEAL, T['p1'], T['p2']), ((1, 2), TEAL, T['p2'], T['p3']),
                  ((0, 1), TEAL, T['p3'], T['vorne']), ((0, 0), CA, T['vorne'], T['zus'])]
    for (i, j), c, von, bis in abschnitte:
        a = ein(t, von, 0.3) * (1 - ein(t, bis, 0.3))
        band(b, xo[i] - PP / 2 + 4, yo - 60, xo[j] + PP / 2 - 4, yo + 60, c, 0.15 * a, r=16)
    for i, z in enumerate('4352'):
        x_, y_, g_ = lage(i, xo[i], yo, g)
        b.text(z, x_, y_, g_, INK, INTER_X, alpha=a0)
    x_, y_, g_ = lage(4, links + 4 * PP + w_mal / 2, yo, g)
    b.text(' · 11', x_, y_, g_, INK, INTER_X, alpha=a0)
    b.text(' = ', zx[5], ys, gs, INK, INTER_X, alpha=unten)
    # „von hinten nach vorn“: Pfeil unter dem Ergebnis
    ar = ein(t, T['richtung']) * (1 - ein(t, T['zus'], 0.4))
    if ar > 0:
        ya = yu + 78
        b.linie([(xu[4] + 20, ya), (xu[0] - 10, ya)], GRAU, 4, alpha=ar)
        b.linie([(xu[0] + 8, ya - 12), (xu[0] - 10, ya), (xu[0] + 8, ya + 12)], GRAU, 4, alpha=ar)
        b.text('von hinten nach vorn', 640, ya + 34, 24, GRAU, INTER_X, alpha=ar)
    # Summen der Paare: klein über dem Platz, dann fällt das Ergebnis hinein
    paare = [(3, '5', '2', '7', T['p1'], T['e1']), (2, '3', '5', '8', T['p2'], T['e2']), (1, '4', '3', '7', T['p3'], T['e3'])]
    for k, za, zb, s, tp, te in paare:
        al = ein(t, tp) * (1 - ein(t, te + 0.2, 0.3))
        if al > 0:
            zeile(b, [(za, INK), (' + ', GRAU), (zb, INK)], xu[k], yl + 8 * (1 - ein(t, tp)), 40, INTER_X, alpha=al)
        f = p(t, te, 0.5)
        if f > 0:
            gf = glatt(f)
            x_, y_, g_ = lage(6 + k, mix(xu[k], ziel[k], kompakt), mix(yl, yu, gf), mix(40, g, gf))
            b.text(s, x_, y_, g_, mischfarbe(TEAL, GRUEN, gruen), INTER_X, alpha=klemm(f * 4))
    for k, i, s, c, ts in ((4, 3, '2', CB, T['hinten']), (0, 0, '4', CA, T['vorne'])):   # die Enden rutschen herunter
        f = glatt(p(t, ts + 0.3, 0.7))
        if f > 0:
            x_, y_, g_ = lage(6 + k, mix(mix(xo[i], xu[k], f), ziel[k], kompakt), mix(yo, yu, f), g)
            b.text(s, x_, y_, g_, mischfarbe(c, GRUEN, gruen), INTER_X, alpha=klemm(f * 3))
    funken(b, t, T['z'] + 0.05, 640, yu, r0=90, r1=260)


def s_merke(b, sc, t):
    tdu = C(sc, 'Und jetzt du')
    te = sc['dauer'] + 0.2                                 # Denkpause mit Uhr, dann die Lösung
    zeiten = [te + UHR + 0.2, te + UHR + 0.8, te + UHR + 1.4, te + UHR + 2.1]
    G.merkkarte(b, sc, t, nochmal=[(zeiten[i], zeiten[i + 1]) for i in range(3)])
    ab = 1 - ein(t, tdu, 0.35)                             # Beispiel 87 · 11 neben den Merksätzen
    mitten_y, y = [], 200
    for _, _, z, _ in MERKSAETZE:
        mitten_y.append(y + 15 + 22 + 22 * (len(z) - 1))
        y += 30 + 44 * len(z)

    def nummer(teile, yy, i, a, g=38):
        xk = 960 - sum(breite(s_, INTER_X, g) for s_, _ in teile) / 2 - 30
        b.kreis(xk, yy, 17, MERKSAETZE[i][1], alpha=a)
        b.text(MERKSAETZE[i][0], xk, yy, 19, '#ffffff', INTER_X, alpha=a)
    if ab > 0:
        karte(b, 700, 130, 490, 450, ab)
        b.text('BEISPIEL  87 · 11', 730, 168, 22, GRAU, INTER_X, anker='l', alpha=ab)
        bsp = [[('8', CA), ('  _  ', GRAU), ('7', CB)], [('8 + 7 = ', INK), ('15', TEAL)],
               [('8 + ', INK), ('1', CD), (' = ', INK), ('9', CD)]]
        for i, teile in enumerate(bsp):
            tl = C(sc, MERKSAETZE[i][3]) + 0.2
            ai = ein(t, tl) * ab
            if ai > 0:
                yy = mitten_y[i] + 16 * (1 - ein(t, tl))
                zeile(b, teile, 960, yy, 38, INTER_X, alpha=ai)
                nummer(teile, yy, i, ai)
        t957 = C(sc, 'nach vorn') + 0.3
        a957 = ein(t, t957) * ab
        if a957 > 0:
            zeile(b, [('= ', INK), ('957', GRUEN)], 960, 530 + 16 * (1 - ein(t, t957)), 56, INTER_X, alpha=a957)
    a = ein(t, tdu + 0.3)
    karte(b, 700, 130, 490, 450, a)
    if a <= 0:
        return
    b.text('UND JETZT DU', 730, 168, 22, GRAU, INTER_X, anker='l', alpha=a)
    zeile(b, [('5', CA), ('3', CB), (' · 11', INK), (' = ?', GRAU)], 945, 245, 64, INTER_X, alpha=a)
    au = ein(t, te, 0.3) * (1 - ein(t, te + UHR, 0.3))
    G.uhr(b, 945, 400, 62, (t - te) / UHR, alpha=au * a, sek=UHR)
    loes = [[('5', CA), ('  _  ', GRAU), ('3', CB)], [('5 + 3 = ', INK), ('8', TEAL)],
            [('8 < 10: ', INK), ('nichts wandert', GRAU)]]
    for i, teile in enumerate(loes):
        y, g = 335 + i * 62, (38 if i < 2 else 32)
        einblenden(b, teile, 960, y, g, t, zeiten[i])
        ai = ein(t, zeiten[i])
        if ai > 0:
            nummer(teile, y + 16 * (1 - ai), i, ai, g)
    einblenden(b, [('= ', INK), ('583', GRUEN)], 960, 530, 56, t, zeiten[3])
    funken(b, t, zeiten[3] + 0.15, mitten([('= ', INK), ('583', GRUEN)], 960, 56)[1], 530, r0=60, r1=170, fy=0.6)


def s_schluss(b, sc, t):
    """Übung mit Lösung bleibt stehen, darunter der Motivationssatz."""
    m = next(x for x in SZENEN if x['id'] == 'merke')
    s_merke(b, m, m['dauer'] + 30)
    a = ein(t, 0.1)
    if a > 0:
        band(b, 190, 604 + 10 * (1 - a), 1090, 684 + 10 * (1 - a), TEAL, 0.94 * a, r=20)
        w = ein(t, C(sc, 'Mit ein bisschen'), 0.5)        # erst aus-, dann einblenden: nie zwei Texte übereinander
        b.text('Länger als drei Sekunden? Ganz normal.', 640, 644, 30, '#ffffff', INTER_X, alpha=a * (1 - klemm(w * 2)))
        b.text('Mit ein bisschen Übung schaffst du das auch.', 640, 628, 25, '#ffffff', INTER, alpha=a * klemm(w * 2 - 1))
        a2 = ein(t, C(sc, SPRUCH))
        b.text(SPRUCH, 640, 660 + 10 * (1 - a), 32, '#ffffff', INTER_X, alpha=a * a2, skala=0.85 + 0.15 * zurueck(a2))


KLAENGE = {  # sparsam wie in Folge 1: Luftzug bei Flügen, Glöckchen nur mit den Funken an grünen Ergebnissen
    'regel': [('auseinander', 'wusch', 0), ('gleich sieben', 'wusch', 0), ('vierhundert', 'ding', 0.1)],
    'warum': [('Summe', 'ding', 0.7)],
    'vorsicht': [('mal elf', 'wusch', 0), ('Zwei Ziffern', 'tief', 0), ('die Eins wandert', 'wusch', 0),
                 ('neunhundert', 'ding', 0.1)],
    'neun': [('mal elf', 'wusch', 0), ('die Eins wandert', 'wusch', 0), ('tausend', 'ding', 0.1)],   # wie Vorsicht
    'gross': [('siebenundvierzigtausend', 'ding', 0.05)],
    'merke': [('#ende', 'tick', 0.2 + k) for k in range(UHR)] + [('#ende', 'ding', 0.2 + UHR + 2.1)],
    'abspann': [('Abonnier', 'klick', 0.2)],
}

ZEICHNER = {'hook': s_hook, 'regel': s_regel, 'warum': s_warum, 'vorsicht': s_vorsicht, 'neun': s_neun, 'gross': s_gross,
            'merke': s_merke, 'schluss': s_schluss, 'app': G.s_app, 'abspann': G.s_abspann}

# Bausteine von Folge 1 auf diese Folge umstellen
G.SZENEN, G.ZEICHNER, G.KLAENGE, G.MERKSAETZE = SZENEN, ZEICHNER, KLAENGE, MERKSAETZE
G.CACHE = os.path.join(HIER, 'tts_cache')
G.QR_BILD = os.path.join(HIER, 'bilder', 'qr_elfer.png')   # https://luperttrading-lab.github.io/mathe-videos/uebung/#elfer
_app = os.path.join(HIER, 'bilder', 'app_start.png')        # App-Bild mit der Elfer-Übung, sobald es die Übung gibt
G.APP_BILD = _app if os.path.exists(_app) else G.APP_BILD

if __name__ == '__main__':
    G.main()
