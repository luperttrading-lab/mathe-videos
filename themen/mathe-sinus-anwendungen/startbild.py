#!/usr/bin/env python3
"""Startbild (Titelkarte) für „Wofür braucht man Sinus und Kosinus?“: das letzte Bild des Einstiegs, P bei 50°.
Muster: ../mathe-einheitskreis/startbild.py. Aufruf: python3 startbild.py [ordner]  → startbild.png (1920 × 1080)"""
import os, sys

HIER = os.path.dirname(os.path.abspath(__file__))
ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HIER, 'bilder')
sys.argv = sys.argv[:1]
sys.path.insert(0, HIER)
import sinus_anwendungen as V                              # noqa: E402
import regel as G                                          # noqa: E402
from animationen import Bild                               # noqa: E402
from PIL import Image                                      # noqa: E402

G.ton_und_zeitplan()                                       # Zeitmarken aus dem Ton-Cache (kostet nichts)
V.STARTBILD = True
b = Bild(G.grund())
V.s_einstieg(b, V.SZENEN[0], 0.0)
b.img.resize((1920, 1080), Image.LANCZOS).save(os.path.join(ziel, 'startbild.png'))
print(os.path.join(ziel, 'startbild.png'))
