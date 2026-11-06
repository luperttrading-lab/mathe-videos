#!/usr/bin/env python3
"""Home-Bildschirm-Symbol (Nutzerwahl 06.11., Symbol 2 „wie Vorschaubild“): Papiergrund mit feinem Punktraster, oben
„16·18“ in den Videofarben, unten die grüne Leiste mit „= ?“ – wie Vorschaubild und App-Kopf.

Kein Name des Tricks im Symbol: Die App enthält später alle Tricks, und auf dem Home-Bildschirm wäre Schrift in dieser
Größe nicht lesbar. Der Name unter dem Symbol kommt aus manifest.webmanifest (short_name „Kopfrechnen“).

Aufruf: python3 tools/icon.py (aus dem Ordner uebung/)"""
import subprocess
from PIL import Image, ImageDraw, ImageFont


def fc(n):
    return subprocess.check_output(['fc-match', '-f', '%{file}', n]).decode()


F = fc('Inter:extrabold')
PAPIER, INK, TEAL, OR, VI = (246, 241, 231), (43, 45, 66), (15, 118, 110), (232, 137, 12), (131, 56, 236)


def symbol(groesse, inhalt=1.0):
    """inhalt < 1 rückt Schrift zur Mitte (maskierbares Symbol: alles Wichtige im inneren Kreis)."""
    k = 4
    s = groesse * k
    img = Image.new('RGB', (s, s), PAPIER)
    d = ImageDraw.Draw(img, 'RGBA')
    schritt = s / 16
    for i in range(16):
        for j in range(16):
            x, y = (i + .5) * schritt, (j + .5) * schritt
            d.ellipse([x - s / 340, y - s / 340, x + s / 340, y + s / 340], fill=(120, 100, 70, 40))
    leiste = s * (0.5 + 0.16 * inhalt)                    # Oberkante der grünen Leiste
    d.rectangle([0, leiste, s, s], fill=TEAL)
    f = ImageFont.truetype(F, int(s * 0.29 * inhalt))
    teile = [('1', INK), ('6', OR), ('·', INK), ('1', INK), ('8', VI)]
    breite = sum(d.textlength(t, font=f) for t, _ in teile)
    x, y = (s - breite) / 2, s * (0.5 - 0.12 * inhalt)
    for t, c in teile:
        d.text((x, y), t, font=f, fill=c, anchor='lm')
        x += d.textlength(t, font=f)
    d.text((s / 2, (leiste + s) / 2), '= ?', font=ImageFont.truetype(F, int(s * 0.2 * inhalt)),
           fill=(255, 255, 255), anchor='mm')
    return img.resize((groesse, groesse), Image.LANCZOS)


symbol(180).save('apple-touch-icon.png')
symbol(192).save('icon-192.png')
symbol(512).save('icon-512.png')
symbol(512, 0.8).save('icon-maskable.png')
print('Symbole geschrieben')
