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

Bild: **Wand rechts, Leiterfuß links** (Nutzer 14.11.: dann öffnet sich der Winkel wie im ersten Quadranten des
Einheitskreises, nicht im zweiten), Boden, Leiter (Hypotenuse INK), Winkel 70° orange am Boden (erst wenn Leiter steht), Höhe rot, Abstand
blau; Rechnung als echter Bruch sin 70° = Höhe/5 m → Höhe = 5 m · sin 70° ≈ 4,70 m; dann cos. Zum Schluss schrumpft das
Dreieck auf den Einheitskreis (Hypotenuse 1).

## 3 kurs (≈ 40 s) – mit Seekarte (Nutzer 14.11.: „mit Karte, nicht nur mit Dreieck“)
> Ein Schiff fährt vom Hafen zehn Kilometer auf Kurs sechzig Grad zu einer Insel. Wie weit liegt die Insel östlich
> und wie weit nördlich vom Hafen? Auf See misst man den Kurs von Norden aus, im Uhrzeigersinn. Geh auf der Karte vom
> Hafen erst nach Norden, dann nach Osten: wieder ein rechtwinkliges Dreieck. Die Strecke nach Osten liegt dem Winkel
> gegenüber, also zehn Kilometer mal Sinus sechzig Grad, ungefähr acht Komma sieben Kilometer. Die Strecke nach Norden
> liegt am Winkel an: zehn Kilometer mal Kosinus sechzig Grad, genau fünf Kilometer. Achtung: Hier gehört der Sinus
> zur waagrechten Strecke, weil der Winkel an der Nordlinie liegt.

Bild: Seekarte wie im Auswahlblatt (`beispiele_pdf.py`, `bild_karte`): oben Norden, Kilometergitter (1 Kästchen =
1 km), Kompassrose, Maßstab, Festland mit Hafen unten links, Insel mit Leuchtturm. Schiff fährt die Strecke ab
(10 km INK), Kurswinkel 60° orange ab der Nordlinie; dann Nordstrecke blau (Ankathete, 5 km), Oststrecke rot
(Gegenkathete, ≈ 8,66 km), rechter Winkel als Viertelbogen mit Punkt. Farbe folgt der Funktion (Sinus rot, Kosinus
blau), nicht der Richtung – das ist die Pointe. Zum Schluss Kästchen abzählen: 5 hoch, knapp 9 nach rechts.
Gesprochen „acht Komma sieben“, eingeblendet ≈ 8,66 km.

## 4 bruecke (≈ 7 s)
> Bis hier hat ein Dreieck gereicht. Jetzt dreht sich etwas, und dann brauchst du den ganzen Kreis.

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

## 6 merke (≈ 12 s)
> Merke: Im rechtwinkligen Dreieck rechnest du mit Sinus und Kosinus Seiten aus. Und wo sich etwas gleichmäßig dreht,
> beschreiben sie, wie es sich wiederholt.

## 7 schluss (≈ 8 s)
> Klingt nach viel? Am Anfang ganz normal. Rechne die Leiter einfach selbst einmal nach. Das kann jeder lernen.

(Spruch aus `werkzeug/motivation.py`, Thema `sinus-anwendungen`: „Das kann jeder lernen.“)

Gestrichen (Nutzer 14.11.: „keine Physik-Aufgabe“): Rampe (Goldene Regel), Generator, Ballwurf.
Alternativen ohne Physik im Auswahlblatt `beispiele.pdf`: Skipiste (statt Leiter), Tageslänge in Frankfurt (zweites
Kreis-Beispiel, nur ungefähr sinusförmig: Sinuskurve bis zu 24 min daneben).
