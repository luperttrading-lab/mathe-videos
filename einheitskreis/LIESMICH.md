# Einheitskreis – Web-App

Nutzerwunsch 13.11.2026: „erst eine App … Startbildschirm, dann den Einheitskreis, den man per Hand drehen kann oder
Sinus und Kosinus verstellt … alles auf einen Bildschirm, Handy-App.“ Erklärvideo vielleicht später.

**Adresse nach Abnahme:** https://luperttrading-lab.github.io/mathe-videos/einheitskreis/ (eigene App, eigenes Symbol;
„Kopfrechnen“ wäre der falsche Name für ein Trigonometrie-Werkzeug). Bis zur Abnahme nur als Vorschau-Artifact
(Slug `18ad2432-58ac-4411-acae-c3f12ae7e7da`) und auf dem Zweig `einheitskreis`, nicht auf `main`.

- **Start:** Punkt kreist, zeichnet die Sinuswelle (nach rechts) und die Kosinuswelle (nach unten), Knopf „Los“.
  Direktlink zur Hauptansicht: `#kreis`.
- **Hauptansicht ohne Scrollen:** Kreis (Punkt P ziehen, Tippen irgendwo im Kreisfeld setzt den Winkel), darunter die
  abgewickelten Kurven über 0 … 2π (auch dort ziehen), unten Regler θ, sin, cos mit Werten. Sinus rot #e63946 (senkrecht),
  Kosinus blau #3a86ff (waagrecht), Winkel orange #ff9f1c (gemeinsam mit dem Erklärvideo, 13.11.), Tangens grün (Zusatz, Schalter „tan“).
- **sin² + cos² = 1:** Der Sinus-Regler hält die Kreishälfte rechts/links (Kosinus = ±√(1 − sin²) mit dem bisherigen
  Vorzeichen), der Kosinus-Regler hält oben/unten. Während man schiebt, zeigt ein blasser zweiter Punkt die andere Lösung.
- **Exakte Werte** nur an Vielfachen von 30° und 45° (½, √2/2, √3/2, √3/3, √3; tan bei 90°/270° „nicht definiert“),
  Bogenmaß als π-Bruch; sonst drei Nachkommastellen bzw. Grad mit einer Stelle. „Einrasten“ (an, abschaltbar): Kreis
  und Kurven ±3°, θ-Regler ±2°, sin/cos-Regler ±0,02 um besondere Werte.
- **Für ein späteres Video:** `kreis.js` zeichnet nur aus dem Winkel (`zeichneKreis(ctx, rahmen, grad, opt)`,
  `zeichneKurven(…)`), ohne Bedienung; Bilder für ein Video ließen sich per Playwright Winkel für Winkel abgreifen.
- **Update:** Skill app-update-iphone (Netz zuerst, `APP_VERSION`, Prüfung beim Öffnen und Zurückholen, Tipp auf
  „Version …“). Cache `einheitskreis`, löscht nur eigene Caches; localStorage `einheitskreis.*`.
- **Tests:** `node einheitskreis/tests/einheitskreis.mjs [bildordner]` muss „Alles grün“ melden (exakte Werte gegen
  Math.sin/cos/tan, fünf Hochformate ohne Scrollen, Touch-Ziehen, Halbseiten-Regel, Einrasten, Update-Tipp).
- Symbol: `python3 tools/icon.py` im Ordner `einheitskreis/`.

**v0.3 (Nutzer 13.11.):** eigene App „Einheitskreis“ bestätigt, Startbildschirm bei jedem Öffnen, Einrasten an.
Startanimation langsamer (eine Umdrehung in 9 s). Einrasten nur noch im Winkel, ±1,5° (vorher rasteten die sin-/cos-Regler
im Wert ±0,02 ein, nahe sin = 1 sind das ±11,5°: „der Winkel springt“). Werte von sin, cos (und tan) direkt an den
Strecken im Kreis. Kurvenbild höher (21 % der Bildhöhe), Kreis etwas kleiner und mit und ohne Tangens gleich groß.

**v0.4 (Nutzer 13.11.: „beim Drehen soll nichts springen“, Beschriftung „sin ½“ vom Kreis durchgestrichen):** Beim
Ziehen folgt P dem Finger genau; erst beim Loslassen gleitet er in 0,16 s zum besonderen Winkel, wenn er höchstens 2°
daneben liegt (gilt für Kreis, Kurvenbild und alle drei Regler). Kleine Striche am Kreis zeigen die besonderen Winkel.
Beschriftungen mit Papier-Rand (lesbar über Linien), sin-Beschriftung auf der Seite mit mehr Platz.
