# YouTube: Elfer-Trick

- **Platzhalter (nur Test, 06.11.):** https://youtu.be/lrJzCcwyrrw (Testkanal „Volumen Trader“, 10 s „Video folgt demnächst“).
  Wird durch das echte Video ersetzt: neuer Link, dann Abspann von Folge 1 umstellen und Platzhalter löschen.
- **Vorschaubild:** `vorschaubild_elfer.png` (4352 · 11 = ?, Reihen-Stil)
- **Fünfer-Trick, Platzhalter (nur Test):** https://youtu.be/tccoRox8Tyk
- **Video:** 1080p-Master nicht eingecheckt, neu rendern mit `python3 elfer.py <ziel>.mp4` (Ton aus `tts_cache/`, kostenlos).
  Render vom 07.11.: 2:49.
- **Zielgruppe:** „Nein, nicht speziell für Kinder“ (wie Folge 1).
- **Nach dem Hochladen:** YouTube-Adresse in `uebung/aufgaben.js` (Elfer, Feld `video`) eintragen, `APP_VERSION` hochzählen;
  im Abspann von Folge 1 den Platzhalter durch das echte Video ersetzen.

## Titel (Vorschläge 07.11., noch nicht gewählt)

YouTube-Suchvorschläge am 07.11.: „große zahlen im kopf multiplizieren“, „schnell im kopf multiplizieren“, „kopfrechnen
trick multiplizieren“, „mit 11 multiplizieren“ (nur mit einem Kanalnamen davor); „elfer trick“ und „mal 11“ führen zu
anderen Themen (Fußball, Kartenspiel, Hausnummern).

1. Elfer-Trick: große Zahlen im Kopf multiplizieren – 4352 · 11 Ziffer für Ziffer
2. Elfer-Trick: mit 11 multiplizieren im Kopf – 4352 · 11 ganz einfach
3. Elfer-Trick: Kopfrechnen Trick zum Multiplizieren – jede Zahl mal 11

## Beschreibung (07.11., Kapitelzeiten aus dem Render vom 07.11., 2:49)

```text
4352 · 11 im Kopf? Mit dem Elfer-Trick multiplizierst du jede Zahl mit 11 – Ziffer für Ziffer, ganz ohne Taschenrechner.
Kostenlose App zum Üben → https://luperttrading-lab.github.io/mathe-videos/uebung/#elfer

So geht der Elfer-Trick:
1. Die erste und die letzte Ziffer bleiben.
2. Dazwischen kommt immer die Summe zweier Nachbarn.
3. Ist eine Summe zweistellig, wandert die Eins nach vorn.
Beispiele: 43 · 11 = 473, 87 · 11 = 957, 97 · 11 = 1067

Kapitel:
0:00 4352 · 11 im Kopf?
0:10 Der Trick: 43 · 11
0:23 Warum klappt das?
0:45 Vorsicht bei 87 · 11
1:02 Wie viele Ziffern hat das Ergebnis?
1:34 Große Zahlen: 4352 · 11
1:57 Merke und deine Übung

Wie schnell warst du bei 53 · 11? Schreib deine Zeit in die Kommentare.
Mehr Kopfrechen-Tricks: Kanal abonnieren.

#Kopfrechnen #Mathe #KopfrechnenTrick
```

Kapitelzeiten = Szenenanfänge aus `elfer.py` (aufgerundet): regel 10,4 s, warum 22,6 s, vorsicht 44,3 s, neun 61,6 s,
gross 93,7 s, merke 116,7 s. Bei jedem neuen Render prüfen.

## Tags und KI-Angabe

- **Tags:** Kopfrechnen, Kopfrechnen Trick, im Kopf multiplizieren, große Zahlen im Kopf multiplizieren, mit 11 multiplizieren,
  Elfer-Trick, Mathe Trick, schneller rechnen
- **„Verwendung von KI“:** Ja (Sprecherstimme synthetisch, ElevenLabs), wie Folge 1.

## Abspann in YouTube Studio

- Elemente erst ab **2:34** (Szene `abspann` beginnt bei 153,6 s), sonst verdecken sie die App-Seite mit dem QR-Code.
  Ende 2:49, also 15 s Abspann (YouTube: 5–20 s).
