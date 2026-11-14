#!/usr/bin/env python3
"""Betonung messen (Muster: ../mathe-einmaleins/betonung_messen.py): je Silbe Dauer, Tonhöhe (Praat) und Lautstärke aus
dem Rohton von ElevenLabs, Silbengrenzen aus den Zeitmarken je Zeichen. Anlass 14.11.: „fehlende Seiten“ im Merksatz
lag auf „fehlende“ statt auf „Seiten“ (Nutzer). Braucht `pip install praat-parselmouth`.

Aufruf: python3 betonung.py            (misst alle FASSUNGEN; neue Texte werden dabei vertont und kosten Zeichen)"""
import os, re, subprocess, sys, tempfile

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.argv = sys.argv[:1]
import numpy as np                                         # noqa: E402
import parselmouth                                         # noqa: E402
import sinus_anwendungen as V                              # noqa: E402
import regel as G                                          # noqa: E402

REST = (' Und wo sich etwas gleichmäßig dreht, beschreiben sie die Bewegung: beim Riesenrad, beim Windrad, beim Pedal am '
        'Fahrrad.')
FASSUNGEN = {
    'alt': 'Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus fehlende Seiten aus.' + REST,
    'gross': 'Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus fehlende SEITEN aus.' + REST,
    'artikel': 'Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus die fehlenden Seiten aus.' + REST,
    'artikel_gross': 'Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus die fehlenden SEITEN aus.' + REST,
    'laengen': 'Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus die Längen der Seiten aus.' + REST,
    # Messung 14.11.: Der Satzakzent liegt immer auf „Sinus und Kosinus“, alles danach ist tief und flach; in „alt“ ragt
    # nur „fehlende“ heraus (131 Hz, 78 dB gegen „Seiten“ 93 Hz, 74 dB). Großschreibung hilft nicht. Umgestellt steht
    # „die fehlenden Seiten“ am Satzende im Fokus.
    'umgestellt': 'Merke: Mit Sinus und Kosinus rechnest du im rechtwinkligen Dreieck die fehlenden Seiten aus.' + REST,
    'umgestellt_ohne': 'Merke: Mit Sinus und Kosinus rechnest du im rechtwinkligen Dreieck fehlende Seiten aus.' + REST,
}
SILBEN = {'fehlende': ['feh', 'len', 'de'], 'fehlenden': ['feh', 'len', 'den'], 'seiten': ['Sei', 'ten']}


def messen(text):
    mp3, al = G.R.tts_eleven(text, G.CFG, G.CACHE)
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    wav = os.path.join(tempfile.gettempdir(), 'betonung.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '44100', wav], check=True)
    snd = parselmouth.Sound(wav)
    pitch = snd.to_pitch(time_step=0.005, pitch_floor=70, pitch_ceiling=300)
    inten = snd.to_intensity(time_step=0.005)
    pt, pf = pitch.xs(), pitch.selected_array['frequency']
    it, iv = inten.xs(), inten.values[0]
    skala = len(st) / len(text)
    aus = {}
    for m in re.finditer(r'fehlenden?|Seiten|SEITEN', text):
        wort, a0, k = m.group(0), m.start(), 0
        for sil in SILBEN[wort.lower()]:
            i0, i1 = int(round((a0 + k) * skala)), int(round((a0 + k + len(sil)) * skala)) - 1
            t0, t1 = st[i0], en[min(i1, len(en) - 1)]
            f = pf[(pt >= t0) & (pt < t1)]
            f = f[f > 0]
            db = iv[(it >= t0) & (it < t1)]
            aus[sil] = dict(ms=round((t1 - t0) * 1000), hz=round(float(np.median(f))) if len(f) else None,
                            hz_max=round(float(f.max())) if len(f) else None, db=round(float(db.max()), 1) if len(db) else None)
            k += len(sil)
    return aus


if __name__ == '__main__':
    for name, text in FASSUNGEN.items():
        w = messen(text)
        zeile = f'{name:14s} ' + ' | '.join(f"{s}: {x['ms']} ms, {x['hz']} Hz (max {x['hz_max']}), {x['db']} dB" for s, x in w.items())
        if 'feh' in w:
            feh, sei = w['feh'], w['Sei']
            ht = 12 * np.log2(sei['hz_max'] / feh['hz_max']) if sei['hz_max'] and feh['hz_max'] else float('nan')
            zeile += f"  →  Sei−feh: {ht:+.1f} Halbtöne, {sei['db'] - feh['db']:+.1f} dB"
        print(zeile)


def woerter(text, von='rechnest', bis='aus.'):
    """Je Wort zwischen `von` und `bis`: Dauer, höchste Tonhöhe, Lautstärke – zeigt, wo der Satzakzent liegt."""
    mp3, al = G.R.tts_eleven(text, G.CFG, G.CACHE)
    st, en = al['character_start_times_seconds'], al['character_end_times_seconds']
    wav = os.path.join(tempfile.gettempdir(), 'betonung.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '44100', wav], check=True)
    snd = parselmouth.Sound(wav)
    pitch = snd.to_pitch(time_step=0.005, pitch_floor=70, pitch_ceiling=300)
    inten = snd.to_intensity(time_step=0.005)
    pt, pf = pitch.xs(), pitch.selected_array['frequency']
    it, iv = inten.xs(), inten.values[0]
    skala = len(st) / len(text)
    a, b = text.index(von), text.index(bis) + len(bis)
    aus = []
    for m in re.finditer(r'\S+', text[a:b]):
        i0, i1 = int(round((a + m.start()) * skala)), int(round((a + m.end()) * skala)) - 1
        t0, t1 = st[i0], en[min(i1, len(en) - 1)]
        f = pf[(pt >= t0) & (pt < t1)]
        f = f[f > 0]
        db = iv[(it >= t0) & (it < t1)]
        aus.append((m.group(0), round((t1 - t0) * 1000), round(float(f.max())) if len(f) else 0, round(float(db.max()), 1)))
    return aus
