#!/usr/bin/env python3
"""Home-Bildschirm-Symbol der Einheitskreis-App: Papiergrund mit Punktraster wie die Kopfrechnen-App, Kreis mit Achsen,
Kosinus (violett, waagrecht) und Sinus (orange, senkrecht) bei 50°, Punkt P. Keine Schrift (wäre zu klein).

Aufruf: python3 tools/icon.py (aus dem Ordner einheitskreis/)"""
import math
from PIL import Image, ImageDraw

PAPIER, INK, SIN, COS, TEAL = (246, 241, 231), (43, 45, 66), (232, 137, 12), (131, 56, 236), (15, 118, 110)


def symbol(groesse, inhalt=1.0):
    k = 4
    s = groesse * k
    img = Image.new('RGB', (s, s), PAPIER)
    d = ImageDraw.Draw(img, 'RGBA')
    schritt = s / 16
    for i in range(16):
        for j in range(16):
            x, y = (i + .5) * schritt, (j + .5) * schritt
            d.ellipse([x - s / 340, y - s / 340, x + s / 340, y + s / 340], fill=(120, 100, 70, 40))
    m = s / 2
    r = s * 0.34 * inhalt
    lw = max(2, int(s * 0.022))
    ax = r * 1.22
    d.line([m - ax, m, m + ax, m], fill=INK, width=max(2, int(s * .012)))
    d.line([m, m - ax, m, m + ax], fill=INK, width=max(2, int(s * .012)))
    w = math.radians(50)
    px, py = m + r * math.cos(w), m - r * math.sin(w)
    # Winkelbogen
    rb = r * .3
    d.pieslice([m - rb, m - rb, m + rb, m + rb], -50, 0, fill=(15, 118, 110, 50))
    d.ellipse([m - r, m - r, m + r, m + r], outline=INK, width=lw)
    d.line([m, m, px, py], fill=INK, width=int(lw * .9))
    d.line([m, m, px, m], fill=COS, width=int(lw * 1.9))
    d.line([px, m, px, py], fill=SIN, width=int(lw * 1.9))
    pr = s * .055 * inhalt
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=INK, outline=(255, 255, 255), width=int(pr * .35))
    return img.resize((groesse, groesse), Image.LANCZOS)


symbol(180).save('apple-touch-icon.png')
symbol(192).save('icon-192.png')
symbol(512).save('icon-512.png')
symbol(512, 0.82).save('icon-maskable.png')
print('Symbole geschrieben')
