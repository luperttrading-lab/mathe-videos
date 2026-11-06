# YouTube: Zehner-Trick

- **YouTube-Link (nur Test):** https://youtu.be/prkKe_iExIU auf dem Testkanal „Volumen Trader“ (Nutzer 06.11.). Nach dem
  Hochladen auf den Mathe-Kanal: neuen Link in `uebung/aufgaben.js` (Feld `video`) eintragen, `APP_VERSION` hochzählen.
  QR-Code und Beschreibung bleiben gleich (sie zeigen auf die App, nicht auf das Video).
- **Titel** (Nutzerwahl 05.11.): Zehner-Trick: großes Einmaleins im Kopf – 16 · 18 in 4 Sekunden
- **Vorschaubild:** `vorschaubild_zehner.png` (1280 × 720, Reihen-Stil „Papier mit Teal-Leiste“, `vorschaubild.py`)
- **Video:** 1080p-Master nicht eingecheckt, neu rendern mit `python3 regel.py <ziel>.mp4` (Ton aus `tts_cache/`, kostenlos)
- **Zielgruppe** (Nutzerentscheidung 06.11.): „Nein, nicht speziell für Kinder“ (Jugendliche ab 13 und Erwachsene). Titel
  geprüft: keine Wörter wie „Grundschule“, „Klasse“, „für Kinder“.
- **Beschreibung, Zeile 2, und angepinnter Kommentar** (Nutzer 06.11.): „Kostenlose App zum Üben →
  https://luperttrading-lab.github.io/mathe-videos/uebung/#zehner“ (nackte Adresse, YouTube macht sie klickbar).
- **Nach dem Hochladen:** YouTube-Adresse in `uebung/aufgaben.js` (Feld `video`) eintragen, `APP_VERSION` hochzählen.

## Beschreibung (06.11., Kapitelzeiten aus dem Render vom 06.11., 3:19)

```text
16 · 18 im Kopf in 4 Sekunden? Mit dem Zehner-Trick klappt das immer für zwei Zahlen von 11 bis 19 – ganz ohne Taschenrechner.
Kostenlose App zum Üben → https://luperttrading-lab.github.io/mathe-videos/uebung/#zehner

So geht der Zehner-Trick:
1. Eine Einerziffer zur anderen Zahl addieren: 16 + 8 = 24
2. Eine Null anhängen: 240
3. Die Einerziffern malnehmen und dazuzählen: 6 · 8 = 48, also 240 + 48 = 288

Damit rechnest du das große Einmaleins im Kopf. Ein Kopfrechen-Trick zum Multiplizieren, den du in wenigen Minuten lernst.

Kapitel:
0:00 16 · 18 im Kopf in 4 Sekunden?
0:10 Der Trick: drei Schritte
0:41 Warum klappt das?
1:19 Andersherum
1:39 Sonderfall: Einer ergeben zusammen 10
2:07 Vorsicht bei 15 · 14
2:26 Merke: die drei Schritte und deine Übung

Wie schnell warst du bei 13 · 14? Schreib deine Zeit in die Kommentare.
Mehr Kopfrechen-Tricks: Kanal abonnieren.

#Kopfrechnen #großesEinmaleins #Mathe
```

Kapitelzeiten = Szenenanfänge aus `regel.py` (aufgerundet auf volle Sekunden): regel 9,9 s, warum 40,9 s, andersrum 78,5 s,
sonderfall 98,8 s, vorsicht 127,0 s, merke 145,5 s. Bei jedem neuen Render prüfen.
