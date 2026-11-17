# Tangens: Steigung und Winkel berechnen – Drehbuch (Entwurf 17.11., Sprechtext noch nicht freigegeben, nichts vertont)

Reihe „Mathe verstehen“ · Trigonometrie · Video 3 · für den Sohn des Nutzers (Hessen, Gymnasium, 10. Klasse), kein
Kanal, kein Abspann. Farben: Gegenkathete Rot #e63946, Ankathete Blau #3a86ff, Winkel Orange #ff9f1c, Tangens Teal
#0f766e. Sprechtext so, wie Christian ihn lesen soll (Zeilen mit „>“). Bilder: `skizzen.py` (Standbilder je Szene).

## 1 einstieg (≈ 12 s)
> Auf dem Schild steht: zwölf Prozent Steigung. Aber wie steil ist das in Grad? Und wie viel Grad sind hundert
> Prozent? Dafür brauchst du den Tangens.

Bild: Straßenschild „12 %“, dann Titel und grüne Leiste (Startbild nach dem Muster der Reihe).

## 2 regel (≈ 38 s)
> Sinus und Kosinus rechnen immer mit der Hypotenuse. Der Tangens braucht sie nicht. Er vergleicht die beiden
> Katheten: Tangens Alpha ist Gegenkathete durch Ankathete. Hier ist die Gegenkathete drei und die Ankathete vier.
> Tangens Alpha ist also drei Viertel, das sind null Komma sieben fünf. Kurz: Beide Katheten, keine Hypotenuse, also
> Tangens. Übrigens: Tangens ist auch Sinus durch Kosinus. Sinus Alpha ist drei Fünftel, Kosinus Alpha vier Fünftel.
> Beim Teilen kürzt sich die Fünf weg, und es bleiben drei Viertel.

Bild: 3-4-5-Dreieck aus Video 2, zuerst rechter Winkel und α; Hypotenuse wird grau („wird nicht gebraucht“).

## 3 turm (≈ 48 s)
> Wie hoch ist der Kirchturm? Sein Schatten reicht sechzig Meter weit, gemessen bis unter die Turmspitze. Die Sonne
> steht fünfunddreißig Grad hoch. Diesen Winkel zeigt dir eine App für den Sonnenstand. Turm und Boden bilden einen
> rechten Winkel. Die Höhe liegt gegenüber vom Fünfunddreißig-Grad-Winkel, der Schatten liegt am Winkel. Beide
> Katheten, keine Hypotenuse, also Tangens. Tangens fünfunddreißig Grad gleich Höhe durch sechzig Meter. Wir
> multiplizieren beide Seiten mit sechzig Metern. Dann ist die Höhe sechzig Meter mal Tangens fünfunddreißig Grad.
> Der Taschenrechner zeigt für Tangens fünfunddreißig Grad ungefähr null Komma sieben null null. Sechzig Meter mal
> null Komma sieben null null sind zweiundvierzig Meter.

Bild: Kirchturm, Sonne, Schatten (Nutzer 17.11.: Kirchturm, Schatten lassen, Sonnenwinkel aus der App statt
Winkelmesser – „zeitgemäße Variante“). Handy mit „Sonnenhöhe 35°“ kurz einblenden. Rechnung mit „| · 60 m“.

## 4 steigung (≈ 70 s)
> Zurück zum Schild. Zwölf Prozent Steigung heißt: Auf hundert Metern waagrecht geht es zwölf Meter nach oben. Die
> zwölf Meter sind die Gegenkathete, die hundert Meter die Ankathete. Tangens Alpha ist also zwölf durch hundert, das
> sind null Komma eins zwei. Die Steigung ist der Tangens des Winkels. Jetzt suchen wir aber den Winkel, nicht eine
> Seite. Dafür rechnest du rückwärts, mit Tangens hoch minus eins. Auf dem Taschenrechner meistens: Shift und dann
> Tangens. Achte darauf, dass er auf Grad steht: In der Anzeige steht ein D. Alpha ist Tangens hoch minus eins von
> null Komma eins zwei, ungefähr sechs Komma acht vier Grad. Und hundert Prozent? Das sind hundert Meter nach oben
> auf hundert Metern waagrecht. Beide Katheten sind gleich lang, der Tangens ist eins, und der Winkel ist
> fünfundvierzig Grad. Nicht neunzig. Bei neunzig Grad stünde eine Wand vor dir: Die waagrechte Strecke wäre null,
> und durch null kann man nicht teilen. Tangens neunzig Grad gibt es nicht.

Bild: Schild, maßstäbliches Steigungsdreieck, Taschenrechner-Karte; dann 100-m-Dreieck (45°) und Wand (90°).

## 5 gerade (≈ 30 s)
> Dasselbe gilt für eine Gerade im Koordinatensystem. Diese Gerade hat die Steigung null Komma fünf: zwei nach
> rechts, eins nach oben. Das Steigungsdreieck ist ein rechtwinkliges Dreieck, und eins durch zwei ist wieder
> Gegenkathete durch Ankathete. Die Steigung m ist also der Tangens des Steigungswinkels. Tangens hoch minus eins
> von null Komma fünf ergibt ungefähr sechsundzwanzig Komma fünf sieben Grad.

## 6 kreis (≈ 25 s)
> Und wo steckt der Tangens im Einheitskreis? Verlängere den Radius durch P, bis er die Tangente rechts am Kreis
> trifft. In diesem großen Dreieck ist die Ankathete genau eins. Die Gegenkathete ist deshalb der Tangens selbst.
> Bei fünfundvierzig Grad ist sie eins. Je näher der Winkel an neunzig Grad kommt, desto länger wird sie, ohne
> Grenze.

Bild: wie die App „Einheitskreis“ (Tangens Teal); P wandert von 40° über 45° Richtung 90°. QR der App.

## 7 merke (≈ 15 s)
> Merke: Tangens ist Gegenkathete durch Ankathete. Suchst du den Winkel, rechnest du mit Tangens hoch minus eins
> zurück. Und die Steigung ist der Tangens des Steigungswinkels.

## 8 schluss (≈ 8 s)
> Welche Kathete wohin gehört, verwechselt am Anfang jeder. Ganz normal. {SPRUCH}

{SPRUCH}: `spruch('mathe-tangens', 'schluss')` aus werkzeug/motivation.py (erst beim Bauen ziehen).

≈ 530 Wörter → ≈ 3:55 bei 2,28 Wörtern/s; ≈ 3.400 Zeichen ElevenLabs.
