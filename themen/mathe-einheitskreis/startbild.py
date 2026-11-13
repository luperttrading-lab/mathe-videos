#!/usr/bin/env python3
"""Startbild (Titelkarte und Vorschaubild) für das Einheitskreis-Video, Reihe „Mathe verstehen“ – Entwürfe 13.11.
Aufruf: python3 startbild.py <ordner>  → startbild_welle.png, startbild_riesenrad.png (1920 × 1080)"""
import math, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, '..', 'mathe-einmaleins')); sys.argv += [] 
import regel as G
from regel import INK, GRAU, TEAL, band, INTER, INTER_X
from animationen import Bild, zeile
from PIL import Image
SIN, COS, WINKEL = '#e63946', '#3a86ff', '#ff9f1c'


def leiste(b):
    band(b, 0, 640, 1280, 720, TEAL, 1.0, r=0)
    b.text('MATHE VERSTEHEN', 60, 680, 30, '#ffffff', INTER_X, anker='l')
    b.text('TRIGONOMETRIE', 1220, 680, 30, '#ffffff', INTER_X, anker='r')


def kreis(b, cx, cy, r, grad, lw=6, speichen=0):
    for k in range(speichen):
        a = 2 * math.pi * k / speichen
        b.linie([(cx, cy), (cx + r * math.cos(a), cy - r * math.sin(a))], '#c9c2b4', 3)
    b.linie([(cx - 1.25 * r, cy), (cx + 1.25 * r, cy)], GRAU, 4)
    b.linie([(cx, cy + 1.25 * r), (cx, cy - 1.25 * r)], GRAU, 4)
    n = 240
    b.linie([(cx + r * math.cos(2 * math.pi * k / n), cy - r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)], INK, lw)
    a = math.radians(grad)
    px, py = cx + r * math.cos(a), cy - r * math.sin(a)
    b.linie([(cx + 60 * math.cos(math.radians(grad * k / 30)), cy - 60 * math.sin(math.radians(grad * k / 30))) for k in range(31)],
            WINKEL, 7)
    b.linie([(cx, cy), (px, cy)], COS, 12)
    b.linie([(px, cy), (px, py)], SIN, 12)
    b.linie([(cx, cy), (px, py)], INK, 6)
    return px, py


def welle(ordner):
    b = Bild(G.grund())
    cx, cy, r = 280, 390, 180
    px, py = kreis(b, cx, cy, r, 50)
    b.kreis(px, py, 14, INK)
    # Sinuswelle startet auf der Höhe von P (gleiche Amplitude wie der Kreis)
    x0, x1 = 540, 1240
    pts = [(x0 + (x1 - x0) * k / 200, cy - r * math.sin(math.radians(50 + 360 * k / 200))) for k in range(201)]
    for k in range(0, 20, 2):
        b.linie([(px + (x0 - px) * k / 20, py), (px + (x0 - px) * (k + 1) / 20, py)], SIN, 3, alpha=0.7)
    b.linie(pts, SIN, 8)
    b.kreis(x0, py, 10, SIN)
    b.text('Der Einheitskreis', 640, 80, 64, INK, INTER_X)
    zeile(b, [('Sinus', SIN), (' und ', INK), ('Kosinus', COS), (' verstehen', INK)], 640, 145, 36, INTER_X)
    leiste(b)
    b.img.resize((1920, 1080), Image.LANCZOS).save(os.path.join(ordner, 'startbild_welle.png'))


def riesenrad(ordner):
    b = Bild(G.grund())
    cx, cy, r = 360, 330, 230
    px, py = kreis(b, cx, cy, r, 30, lw=8, speichen=12)
    # Gondel hängt am Punkt
    b.linie([(px, py), (px, py + 26)], INK, 4)
    b.d.rounded_rectangle([(px - 34) * 2, (py + 26) * 2, (px + 34) * 2, (py + 80) * 2], radius=24, fill='#ff9f1c')
    b.kreis(px, py, 12, INK)
    # Ständer
    b.linie([(cx, cy), (cx - 140, 630)], INK, 8)
    b.linie([(cx, cy), (cx + 140, 630)], INK, 8)
    b.text('Wie hoch ist', 1000, 170, 64, INK, INTER_X)
    b.text('die Gondel?', 1000, 245, 64, INK, INTER_X)
    b.text('Der Einheitskreis', 1000, 350, 36, INK, INTER_X)
    zeile(b, [('Sinus', SIN), (' und ', INK), ('Kosinus', COS), (' verstehen', INK)], 1000, 400, 32, INTER_X)
    leiste(b)
    b.img.resize((1920, 1080), Image.LANCZOS).save(os.path.join(ordner, 'startbild_riesenrad.png'))


if __name__ == '__main__':
    o = sys.argv[1] if len(sys.argv) > 1 else HIER
    welle(o); riesenrad(o)
