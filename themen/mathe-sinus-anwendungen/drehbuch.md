# Wofür braucht man Sinus und Kosinus? – Drehbuch (Entwurf 14.11., noch keine Hörprobe)

Reihe „Mathe verstehen“ · Trigonometrie · Video 2 · für den Sohn des Nutzers (Hessen, Gymnasium, 10. Klasse), kein
Kanal, kein Abspann. Farben wie Video 1: Sinus/Höhe Rot #e63946, Kosinus/waagrecht Blau #3a86ff, Winkel Orange
#ff9f1c, Kreis/Achsen #2b2d42, Papier #f6f1e7. Sprechtext so, wie Christian ihn lesen soll.

## 1 einstieg (≈ 15 s)
> Im Einheitskreis hast du gesehen, was Sinus und Kosinus sind. Aber wofür braucht man das? Für zwei Sorten von
> Aufgaben: Längen in einem rechtwinkligen Dreieck ausrechnen. Und alles beschreiben, was sich im Kreis dreht.

Bild: Titel „Wofür braucht man Sinus und Kosinus?“, links kleines Dreieck, rechts kleiner Kreis mit drehendem P.

## 2 leiter (≈ 35 s)
> Eine Leiter ist fünf Meter lang und steht im Winkel von siebzig Grad zum Boden. Wie hoch reicht sie? Leiter, Wand
> und Boden bilden ein rechtwinkliges Dreieck. Die Leiter ist die Hypotenuse. Sinus ist Gegenkathete durch Hypotenuse,
> also ist die Höhe fünf Meter mal Sinus siebzig Grad. Das sind ungefähr vier Meter siebzig. Genauso ist der Abstand
> zur Wand fünf Meter mal Kosinus siebzig Grad, ungefähr ein Meter einundsiebzig. Es ist das Dreieck aus dem
> Einheitskreis, nur fünfmal so groß.

Bild: Wand, Boden, Leiter (Hypotenuse INK), Winkel 70° orange am Boden (erst wenn Leiter steht), Höhe rot, Abstand
blau; Rechnung als echter Bruch sin 70° = Höhe/5 m → Höhe = 5 m · sin 70° ≈ 4,70 m; dann cos. Zum Schluss schrumpft das
Dreieck auf den Einheitskreis (Hypotenuse 1).

## 3 rampe (≈ 40 s)
> Eine Kiste wiegt fünfhundert Newton. Statt sie einen Meter hochzuheben, schiebst du sie eine fünf Meter lange Rampe
> hinauf. Dann ist der Sinus des Steigungswinkels Höhe durch Länge, also ein Fünftel. Ohne Reibung brauchst du nur
> fünfhundert Newton mal ein Fünftel, also hundert Newton. Der Weg ist fünfmal so lang, die Kraft fünfmal so klein:
> die Goldene Regel der Mechanik. Den Rest der Gewichtskraft trägt die Rampe: fünfhundert Newton mal Kosinus,
> ungefähr vierhundertneunzig Newton.

Bild: Rampe (Länge 5 m INK mit Klammer, Höhe 1 m rot), Kiste, Pfeil Gewichtskraft nach
unten, zerlegt in rot (hangabwärts, 100 N) und blau (in die Rampe, ≈ 490 N), rechter Winkel als Viertelbogen mit Punkt.
sin α = 1 m / 5 m = 1/5 als echte Brüche. Offen: cos α = √(1 − 1/25) ≈ 0,98 kurz zeigen (Pythagoras aus Video 1)?

## 4 bruecke (≈ 8 s)
> Bis hier stand alles still. Jetzt dreht sich etwas, und dann brauchst du den ganzen Kreis.

## 5 riesenrad (≈ 47 s)
> Ein Riesenrad hat sechzig Meter Durchmesser, die Achse ist zweiunddreißig Meter hoch. Die Gondel ist unser Punkt P,
> nur mit Radius dreißig statt eins. Ihre Höhe ist also zweiunddreißig Meter plus dreißig Meter mal Sinus Alpha. Bei
> dreißig Grad sind das siebenundvierzig Meter, bei neunzig Grad ganz oben zweiundsechzig. Bei zweihundertzehn Grad
> wird der Sinus negativ: nur noch siebzehn Meter. Dreht sich das Rad gleichmäßig, wird die Höhe über die Zeit genau
> eine Sinuskurve. Nach jeder Runde geht alles von vorn los. Probier es in der App aus: Drück auf Play und schau zu,
> wie P kreist.

Bild: Riesenrad als Kreis mit Achsenkreuz in der Nabe (Boden 32 m tiefer), Gondel = P, rote Höhe ab Achse, Höhe
über dem Boden als Klammer; Werte 0°/30°/90°/210°/270° (Gondel unten 2 m) nacheinander; rechts entsteht die Höhenkurve
über der Zeit (Achse t in Minuten, eine Runde = 10 min), wie in Video 1 Szene `kurve`. Kurz App-Bildschirm mit Play.

## 6 generator (≈ 25 s)
> Genauso im Kraftwerk: Im Generator dreht sich ein Magnet gleichmäßig, rundherum sitzen Spulen. Die Spannung in den
> Spulen schwankt dabei fast genau wie eine Sinuskurve. Aus der Steckdose kommen fünfzig solche Schwingungen pro
> Sekunde.

Bild: drehender Stabmagnet (Pole grau/INK, Rot und Blau bleiben sin/cos vorbehalten) in einem Ring aus Spulen, daneben
die Spannungskurve; Einblendung „50 Hz = 50 Schwingungen pro Sekunde“.

## 7 merke (≈ 12 s)
> Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus Seiten aus. Und wo sich etwas gleichmäßig dreht,
> beschreiben sie, wie es sich wiederholt.

## 8 schluss (≈ 8 s)
> Klingt nach viel? Am Anfang ganz normal. Rechne die Leiter einfach selbst einmal nach. Das kann jeder lernen.

(Spruch aus `werkzeug/motivation.py`, Thema `sinus-anwendungen`: „Das kann jeder lernen.“)

Hinweis Generator: Im Kraftwerk dreht sich der Magnet (Polrad), die Spulen stehen; das Schulmodell „Spule dreht im
Magnetfeld“ ist physikalisch gleichwertig. Netzspannung ist nicht exakt sinusförmig (Oberschwingungen) → „fast genau“.
