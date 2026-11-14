# Wofür braucht man Sinus und Kosinus? – Gliederung (Vorschlag 14.11., noch nicht freigegeben)

Reihe „Mathe verstehen“ · Trigonometrie · Video 2 (Video 1: „Der Einheitskreis“, themen/mathe-einheitskreis/).
Für den Sohn des Nutzers (10. Klasse), kein Kanal, kein Abspann (übernommen aus Video 1, gliederung.md 13.11.).
Stil, Stimme, Farben wie Video 1: Sinus/Höhe Rot #e63946, Kosinus/waagrecht Blau #3a86ff, Winkel Orange #ff9f1c,
INK #2b2d42, Papier #f6f1e7. Regeln aus ../mathe-einheitskreis/lehren.md gelten.

Ziel ≈ 2:45–3:05, ≈ 380–440 Wörter (Tempo 1,05 ≈ 2,28 Wörter/s).

## Lehrplan-Abgleich (14.11.)
- Bayern Gymnasium (LehrplanPLUS): rechtwinkliges Dreieck in **M9 7.1** (ca. 9 Std., „Anwendungsaufgaben z. B. aus
  der Physik oder aus dem Vermessungswesen“), Einheitskreis 0–360° schon in M9 7.2. **M10 Kap. 3 „Sinus- und
  Kosinusfunktion“** (ca. 17 Std.): Bogenmaß, Graphen, a · sin(b · (x + c)) + d mit Amplitude und Periode,
  „realitätsbezogene Problemstellungen zu periodischen Vorgängen graphisch und rechnerisch“. Konkrete Beispiele nennt
  der Lehrplan nicht.
- **Sohn: Hessen, Gymnasium (Nutzer 14.11.)** – maßgeblich. Hessischer Lehrplan Mathematik, gymnasialer
  Bildungsgang 5–13 (kultus.hessen.de, g9-mathematik.pdf), **Jahrgangsstufe 10, „10.4 Trigonometrie und
  trigonometrische Funktionen“, 24 Std.**: alles in Klasse 10 – sin/cos/tan als Längenverhältnisse im rechtwinkligen
  Dreieck, Einheitskreis 0–360°, sin² + cos² = 1, „Anwendungen aus Technik, Physik und ebener und räumlicher
  Geometrie“, Sinus-/Kosinussatz, Steigungswinkel einer Geraden; „Sinus- und Kosinusfunktion: Definition über den
  Einheitskreis bzw. über die senkrechte Projektion einer Kreisbewegung“, Periodizität, „Beispiele periodischer
  Zusammenhänge (z. B. Modelle einfacher zyklischer Prozesse aus den Natur-, Wirtschafts- oder Sozialwissenschaften)“.
  **Fakultativ**: allgemeine a sin(bx + c), Tangensfunktion, Vermessung/Triangulation.
- Folgerung: Beide Teile (Dreieck und Kreis) sind in Hessen Klasse-10-Stoff, die Aufteilung passt. Riesenrad =
  wörtlich „senkrechte Projektion einer Kreisbewegung“. Weil a sin(bx + c) nur fakultativ ist: im Riesenrad Höhen über
  Einheitskreis-Winkel ausrechnen (Höhe = Achse + 30 · sin), die Formel h(t) höchstens zeigen, nicht ins Zentrum.

## Stand 14.11. mittags: Video gebaut
Nutzer 14.11.: erst „das, was in Mathe und Physik dran kommt in Klasse 10“, dann **„keine Physik-Aufgabe“** und
**„die Schiffsaufgabe mit Karte, nicht nur mit Dreieck“**; Leiter mit **Wand rechts** (Winkel im ersten Quadranten);
schließlich **„bau das Video so, wie du es jetzt am besten findest“** → Auswahl Leiter, Schiffskurs, Riesenrad und
ganzes Video gerendert (3:10, 430 Wörter). Physik Hessen Klasse 10 (Lehrplan Physik, g9-physik.pdf) wäre: Arbeit und
Energie (Goldene Regel, Generator), Radioaktivität, Energieversorgung – Rampe, Generator und Ballwurf gestrichen.

| # | Szene | Start | Dauer | Inhalt | Bezug Mathe Klasse 10 Hessen |
|---|---|---|---|---|---|
| – | einstieg | 0:00 | 15 s | Startbild entsteht: Einheitskreis aus Video 1, Dreieck löst sich heraus, P kreist | – |
| 1 | leiter | 0:16 | 44 s | 5-m-Leiter, 70°, Wand rechts: Höhe 5 m · sin 70° ≈ 4,70 m, Abstand 5 m · cos 70° ≈ 1,71 m; Einheitskreis mal 5 | „Anwendungen aus Technik“ |
| 2 | kurs | 1:01 | 45 s | Seekarte mit km-Gitter: 10 km auf Kurs 60° → Osten 10 km · sin 60° ≈ 8,7 km, Norden 10 km · cos 60° = 5 km | „Berechnungen in Dreiecken“ |
| 3 | riesenrad | 1:46 | 56 s | Höhe = 32 m + 30 m · sin α: 30° → 47 m, 90° → 62 m, 210° → 17 m; Höhe über der Zeit = Sinuskurve; QR der App | „senkrechte Projektion einer Kreisbewegung“ |
| 4 | merke + schluss | 2:45 | 22 s | Merkzettel (gesprochen wie geschrieben), Motivationssatz + Spruch „Das kann jeder lernen.“ | – |

Dateien: `sinus_anwendungen.py` (Video; Baukasten regel.py und Zeichenhilfen aus einheitskreis.py nur importiert),
`drehbuch.md` (Sprechtext), `startbild.py` → `bilder/startbild.png`, `pruefen.py` (Beschriftungs-Check, muss außer
den Texten auf den grünen Bändern leer bleiben), `tts_cache/` (Ton, 1.139 Zeichen berechnet), `beispiele_pdf.py` →
`beispiele.pdf` (Auswahlblatt mit den Alternativen Skipiste und Tageslänge), `vorschau.json` (eigene Vorschau-Seite).
Vorschau-Seite: [Sinus-Anwendungen-Video · Vorschau](https://claude.ai/artifact/Rr7NxyPfPvNJSXyf89sZ7W), Slug
`c936b41e-56df-414b-a0c6-0a264d78df29` (Artifact mit {"db": {}, "comments": {}}). Kein Abspann, kein Kanal, keine Geräusche. Offen: Abnahme durch den Nutzer; Verweis in Video 1 auf Video 2 (Vorschlag,
nicht eingebaut).

## Zahlen (nachgerechnet 14.11.)
5 · sin 70° = 4,698 → 4,70 m; 5 · cos 70° = 1,710 → 1,71 m; 20 · cos 30° = 17,32; 20 · sin 30° = 10;
Skipiste: 900 · sin 20° = 307,8 → 308 m; 900 · cos 20° = 845,7 → 846 m.
Tageslänge Frankfurt (50,11° N, NOAA-Formeln, Horizont −0,833°): 21.6. 16 h 23 min, 21.12. 8 h 03 min (Dezember-Wert
per Quelle bestätigt: wetterdienst.de 8 h 03 min 25 s); Modell 12,2 h + 4,2 h · sin(360° · (Tage seit 21.3.)/365):
21.4. 14 h 20 min statt 14 h 08 min, größte Abweichung 24 min (Ende Oktober).
Riesenrad 32 + 30 · sin α: 0° 32, 30° 47, 90° 62, 210° 17, 270° 2.
