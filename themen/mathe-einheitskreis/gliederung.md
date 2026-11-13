# Einheitskreis – Gliederung (Vorschlag 13.11., noch nicht freigegeben)

Ziel ≈ 4:35 plus 8 s Abspann, ≈ 600 Wörter (Tempo 1,05 ≈ 2,28 Wörter/s).
Farben: Sinus Rot #e63946 (senkrecht), Kosinus Blau #3a86ff (waagrecht), Winkel/Bogen Orange #ff9f1c,
Kreis/Achsen INK #2b2d42, Papier #f6f1e7.

| # | Szene | Zeit | Wörter | Inhalt |
|---|---|---|---|---|
| 1 | hook | 0:00–0:15 | 30 | „Sinus von 180 Grad: null oder minus eins?“ (häufigster Fehler laut Kommentaren) – am Einheitskreis in einer Sekunde ablesbar |
| 2 | kreis | 0:15–0:35 | 45 | Radius 1, Mittelpunkt im Ursprung, Winkel ab positiver x-Achse gegen den Uhrzeigersinn |
| 3 | warum | 0:35–1:20 | 100 | Lot → rechtwinkliges Dreieck, Hypotenuse 1 → cos α = x, sin α = y; Merkhilfe „c vor s, x vor y“; ab 90° kein Dreieck mehr → dann *legt man fest*: cos und sin sind die Koordinaten |
| 4 | werte | 1:20–2:25 | 150 | 0/90/180/270° ablesen (Auflösung Hook: sin 180° = 0); 45°: halbes Quadrat, x = y, 2x² = 1 → √2/2; 30°/60°: halbes gleichseitiges Dreieck → ½ und √3/2 |
| 5 | vorzeichen | 2:25–3:00 | 80 | Spiegeln: 150° → (−√3/2; ½); Vorzeichen in den vier Quadranten |
| 6 | pythagoras | 3:00–3:20 | 45 | sin²α + cos²α = 1 – Pythagoras im Dreieck mit Hypotenuse 1 |
| 7 | kurve | 3:20–3:55 | 80 | Kreis links, Höhe nach rechts abtragen → Sinuskurve live; Kosinus = dieselbe Kurve, um 90° verschoben; wofür: Schwingungen, Drehungen |
| 8 | merke + schluss | 3:55–4:15 | 45 | Merkzettel (gesprochen wie geschrieben), Motivationssatz + Spruch |
| 9 | app | 4:15–4:25 | 20 | Satz zur kostenlosen App, QR …/einheitskreis/ |
| 10 | abspann | 4:25–4:35 (+8 s) | 25 | wie in der Reihe |

Nicht drin (Vorschlag eigene Folgen): Bogenmaß, Tangens.

Recherche (6 meistgesehene deutsche Videos, 151 Tsd.–1,6 Mio. Aufrufe, Stand 13.11.): keines leitet 30/45/60° her,
keines zeigt sin² + cos² = 1 am Kreis, keines Kreis und Kurve nebeneinander live, zwei tun so, als folge sin = y
für alle Winkel aus dem Dreieck (in Wahrheit Definition). Häufigste Hänger: sin 180° = −1, sin/cos vertauscht,
„woher kommen die Werte für 30/45/60°?“, „wozu das Ganze?“.

App-Abgleich (Info App-Sitzung 13.11.): App 0.2 nutzt dieselben Farben, dazu Tangens #0f766e. App liegt bis zur
Abnahme auf Zweig `einheitskreis`; QR auf …/einheitskreis/ funktioniert erst danach. Zeichencode zum Abgleich der
Optik: `einheitskreis/kreis.js` (zeichneKreis, zeichneKurven). Das Video bleibt beim Python-Baukasten regel.py und
übernimmt nur Farben und Strichbild.

## Entscheidungen des Nutzers (13.11.)
- Erstmal **kein YouTube-Kanal**: Das Video ist für den Sohn des Nutzers. Falls später veröffentlicht, dann auf einem
  eigenen Kanal zum Mathelernen (nicht Kopfrechnen).
- Name der Reihe: **„Mathe verstehen“**, Thema **Trigonometrie**.
- Sohn: 10. Klasse (13.11.).
- Bogenmaß: eigenes Video. Tangens: weglassen. Abspann: weglassen. 480p-Datei für den Sohn: ja.
- Vorschau-Seite nur für dieses Video (Nutzer 13.11.: die alten Kopfrechnen-Links nicht mehr zeigen): [Einheitskreis · Vorschau](https://claude.ai/artifact/2zRnaGCW6fr3xH48QPsMXc), Slug `101dceed-779d-4835-8c36-388133b01b8f`, `vorschau.json` hier.
- Notiz zur Hörprobe (13.11.): 180° per Drehung zeigen, beschriften statt nur reden, Sinus von P senkrecht nach unten, Zahlen 1/−1 außerhalb des Kreises → Szenen 1–3 animiert.
- App ist live (13.11., App 0.8): https://luperttrading-lab.github.io/mathe-videos/einheitskreis/ – der QR-Code im Video zeigt dorthin.
- Nutzer 13.11.: Wenn das Video fertig ist, `lehren.md` als Gestaltungsregeln in die CLAUDE.md übernehmen (für alle
  künftigen Videos und Apps).
- Damit offen: Abspann mit Abo-Aufruf (ohne Kanal sinnlos), Titel und Vorschaubild erst bei Veröffentlichung.
