# Gestaltungsregeln für Erklärvideos und Lern-Apps

Gelernt am Einheitskreis-Video (13./14.11., `themen/mathe-einheitskreis/`). Nutzer 14.11.: „Egal in welchen Videos, ich
hab immer die gleichen Ansprüche, das gleiche Vorgehen.“ Gilt deshalb für **jedes** Erklärvideo und jede App, nicht nur
für Mathe. Vor dem ersten Clip lesen, vor jedem Clip gegen diese Liste prüfen – nicht erst, wenn der Nutzer es findet.

## 1 Vorgehen
1. Kurz recherchieren, was die meistgesehenen Videos zum Thema erklären und wo Zuschauer hängen bleiben (Kommentare).
2. Gliederung mit Sekundenangaben vorschlagen, offene Fragen als nummerierte Liste – erst danach Drehbuch.
3. Drehbuch lesen lassen, dann Hörprobe (Ton kostet Zeichen; Text vorher abstimmen).
4. Szene für Szene als kurzen Clip zeigen, ganzes Video erst nach „rendern“.
5. Eigene Vorschau-Seite je Video, im Chat immer nur der Link, der gerade gebraucht wird, Linkname mit „Video“.
6. Wenn der Nutzer eine Stelle bemängelt: dieselbe Art Fehler im **ganzen** Video suchen und mitbeheben.
7. Länge: Verständnis geht vor der Zielzeit, aber jede Verlängerung offen nennen (neue Länge in Minuten).

## 2 Inhalt: nichts Falsches, nichts unbegründet
- Jede Aussage muss allgemein stimmen. Beispiel: nicht „Das Dreieck gibt es nur zwischen 0° und 90°“ (es gibt auch
  bei 140° ein Dreieck), sondern „Im rechtwinkligen Dreieck liegt α zwischen 0° und 90°; wird α größer, ist der Winkel im
  Dreieck nicht mehr α. Deshalb legt man fest …“.
- Nichts behaupten, was sich zeigen lässt: „gleichseitig“, „gleich lang“, „ist die Hälfte“ immer mit Grund
  (Winkelsumme, gleichschenklig, Symmetrie) – gesprochen und im Bild.
- Rechenwege lückenlos, ein Schritt pro Zeile: 2x² = 1 → x² = 1/2 → x = √½ = 1/√2 → mit √2 erweitern → √2/2.
- Text logisch prüfen: Aufzählungen ohne Dopplung (jedes Viertel genau einmal), Übergänge, die stimmen
  („in den anderen Vierteln“ nur, wenn es wirklich andere sind).
- Alltagsbeispiele auf Richtigkeit prüfen und vorsichtig formulieren („solche Wellen stecken im Schall“, nicht „Schall
  ist eine Sinuswelle“).

## 3 Aufbau des Videos
- Starker Anfang: animiertes Startbild mit gesprochenem Titel und einem Satz, was man lernt – keine leere Seite mit
  einer Frage. Typische Fehler (z. B. „sin 180° ≠ −1“) als Hinweis an der passenden Stelle, nicht als Einstieg.
- Grundbegriff zuerst deutlich zeigen (Radius 1 als Zirkel, der den Kreis zeichnet, nicht als Strich auf der Achse).
- Orientierung geben (wo liegen 0°, 90°, 180°, 270° und typische Winkel in jedem Viertel).
- Am Schluss ein Merkzettel, der die Zusammenhänge als Gleichungen zusammenführt (P(x | y) = P(cos α | sin α),
  sin²α + cos²α = 1) und Ergebnisse als Tabelle zeigt – gesprochen wird, was dasteht.

## 4 Bild: Herkunft zeigen, Schritt für Schritt
- Jeder gesprochene Schritt erscheint im Bild, genau beim Wort, nicht vorher.
- Herkunft zeigen statt benennen: Werte mit Strecken und gestrichelten Linien auf die Achsen tragen, Wert für Wert beim
  Sprechen; Kurven aus der Bewegung entstehen lassen; Zusammenhänge animieren (Kurve kippen, Kopie verschieben).
- Nichts einzeichnen, bevor es existiert (Winkel an einer Seite erst, wenn die Seite da ist; Dreieck erst, wenn der
  Punkt angekommen ist).
- Hilfsobjekte (gestrichelte Kopien, Pfeile) nach ihrem Zweck bald wieder ausblenden.
- Rechenschritte lange genug stehen lassen: Pausen nur an echten Sprechpausen verlängern (`pause_nach` je Szene in
  `regel.py`), nie ins Wort schneiden.
- Schrift, die Buchstabe für Buchstabe erscheint, hat von Anfang an ihren festen Platz (sonst springt sie).

## 5 Deutlichkeit
- Wichtige Strecken dick (≈ 8), überall gleich dick, auch in kleinen Nebenbildern; Achsen ≈ 3,5.
- Jedes Diagramm hat beide Achsen mit 0 und Skala, auch gedrehte oder zusätzliche Diagramme.
- Winkel immer mit Bogen und Gradzahl, wenn sich etwas dreht oder ein Winkel genannt wird.
- Gleiche Größe = gleiche Farbe überall, auch in Formeln, Tabellen und im Merkzettel (Einheitskreis: x/cos/Ankathete
  blau, y/sin/Gegenkathete rot, Winkel orange; in x² + x² = 1 ein x blau, ein x rot).

## 6 Beschriftungen und Typografie
- Keine Zahl und kein Wort auf einer Linie, Kreislinie, Kurve oder Achse, wo es vermeidbar ist: daneben in freien
  Raum, dann ohne Papierfeld. Keine Überlappung mit anderen Beschriftungen oder Achsenzahlen (1, −1, Gradzahlen).
- Gleiche Art Beschriftung immer gleich groß. Bei schmalen Winkeln kleiner und weiter außen. Beschriftungen von
  Winkelbögen weichen den Achsen aus.
- Längen eindeutig zeigen (Klammer über die ganze Seite mit „1“), nicht mit einer Zahl, die man für eine Achsenzahl hält.
- Brüche immer übereinander (echter Bruchstrich), nie mit Schrägstrich oder als ½-Zeichen – auch in kleinen
  Beschriftungen und bei sin = Gegenkathete / Hypotenuse. Ausnahme: kleine Brüche unter einer Wurzel (√½).
- Koordinaten wie im Mathe-Satz: Trennstrich als eigener Strich, so hoch und kräftig wie die Klammern; Abstände nach
  der sichtbaren Tinte, nicht nach Zeichenbreiten (sonst klebt „1)“, während „(0“ Luft hat): innen an Klammern
  ≈ 0,10 em, Tinte bis Strichmitte ≈ 0,26 em (`satz()` in `themen/mathe-einheitskreis/einheitskreis.py`).
- Winkelbögen ohne Pfeilspitze; rechter Winkel als Viertelbogen mit Punkt (deutsche Schulnotation).

## 7 Eigene Kontrolle vor dem Zeigen
- Automatische Prüfung jedes Clips: `werkzeug/beschriftung_pruefen.py` (rendert alle 0,5 s ohne Text, misst Linien
  unter jeder Beschriftung, auch gedrehter, und Überlappungen). Nur bewegte Linien dürfen kurz über eine Zahl streichen.
  Das Skript ist auf das Einheitskreis-Video zugeschnitten; für ein neues Video den Import anpassen.
- Kontaktbogen über alle Szenen und vergrößerte Ausschnitte für Typografie (Klammern, Brüche, Abstände) – im
  Gesamtbild fallen 2–3 Bildpunkte nicht auf. Stichproben allein reichen nicht.
