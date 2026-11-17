# Tangens: Steigung und Winkel berechnen – Gliederung (Vorschlag 17.11., noch nicht freigegeben)

Reihe „Mathe verstehen“ · Trigonometrie · Video 3 (Video 1 „Der Einheitskreis“, Video 2 „Wofür braucht man Sinus und
Kosinus?“). Für den Sohn des Nutzers (Hessen, Gymnasium, Klasse 10), kein Kanal, kein Abspann, keine Verweise auf
andere Videos, keine Physik-Aufgaben. Auftrag aus der Hauptsitzung 17.11.; Thema und Reihenfolge sind ein Vorschlag,
**der Nutzer hat noch nicht gewählt** (offen: Was ist im Unterricht dran, wann ist die Klassenarbeit?).
Bis zur Antwort: nichts vertont, nichts gerendert.

Stil, Stimme (Christian, eleven_v4, Tempo 1,05) und Farben wie Video 1 und 2: Gegenkathete Rot #e63946, Ankathete Blau
#3a86ff, Winkel Orange #ff9f1c, INK #2b2d42, Papier #f6f1e7; **Tangens Teal #0f766e** wie in der App. Regeln aus
`../mathe-einheitskreis/lehren.md` und den Nutzerwünschen in `../mathe-sinus-anwendungen/gliederung.md` gelten von
Anfang an (rechten Winkel zuerst zeigen, Taschenrechnerwert mit drei Nachkommastellen als Zwischenschritt,
Umformschritt „| · 20 m“ sprechen und zeigen, echte Brüche, `pruefen.py` vor jedem Clip, Betonung messen).

Ziel 3:30–4:00, höchstens 5:00 (≈ 480–550 Wörter bei 2,28 Wörtern/s).

## Was das Video Neues bringt
1. Der **Tangens** (fehlt in Video 1 und 2, Pflichtstoff): beide Katheten, keine Hypotenuse.
2. Die **Gegenrichtung**: aus zwei Seiten den Winkel (tan⁻¹ am Taschenrechner, Modus DEG). Video 1 und 2 rechnen nur
   vom Winkel zur Seite.
3. **Steigung = Tangens** (Straßenschild in Prozent, Gerade y = m · x + b: Lehrplan „Steigungswinkel einer Geraden“).

## Szenen (Vorschlag)
| # | Szene | Start | Dauer | Inhalt |
|---|---|---|---|---|
| 1 | einstieg | 0:00 | 15 s | Straßenschild „12 %“: Wie steil ist das in Grad? Und wie viel Grad sind 100 %? Startbild der Reihe. |
| 2 | regel | 0:15 | 35 s | 3-4-5-Dreieck aus Video 2: rechter Winkel, α. tan α = Gegenkathete : Ankathete = 3/4 – die Hypotenuse kommt nicht vor. Kurz: tan α = sin α : cos α (die Hypotenuse kürzt sich: (3/5) : (4/5) = 3/4). Merkform: „Beide Katheten, keine Hypotenuse: Tangens.“ |
| 3 | hoehe | 0:50 | 45 s | Vom Winkel zur Seite (wie Video 2): **Kirchturm** (Nutzer 17.11.: „Kirchturm, anderes Gebäude oder hoher Baum“), Schatten 60 m bis unter die Turmspitze, Sonne steht 35° hoch. tan 35° = Höhe / 60 m, „| · 60 m“, Taschenrechner tan 35° ≈ 0,700, Höhe ≈ 60 m · 0,700 = 42,0 m (exakt 42,012 m). |
| 4 | steigung | 1:35 | 65 s | Schild 12 %: 12 m Höhe auf 100 m waagrecht. Das ist Gegenkathete : Ankathete, also tan α = 12/100 = 0,12. **Gegenrichtung**: gesucht ist der Winkel → tan⁻¹ (Taste SHIFT/2nd + tan, Anzeige „D“ bzw. DEG): α = tan⁻¹(0,12) ≈ 6,84°. Wende: 100 % = 100 m auf 100 m, beide Katheten gleich lang, tan α = 1, α = 45° – nicht 90°. Bei 90° steht eine Wand: Ankathete 0, Teilen durch null, tan 90° gibt es nicht. |
| 5 | gerade | 2:40 | 30 s | Koordinatensystem, Gerade y = 0,5 · x + 1 mit Steigungsdreieck (2 nach rechts, 1 nach oben): m = tan α, α = tan⁻¹(0,5) ≈ 26,57°. Die Steigung m ist der Tangens des Steigungswinkels. |
| 6 | kreis | 3:10 | 25 s | Einheitskreis: Tangente bei x = 1, der Strahl durch P schneidet sie in der Höhe tan α (Ankathete = 1, darum tan α = Gegenkathete). 45° → 1; gegen 90° wächst die Strecke über jede Grenze. Daher der Name. QR der App (zeigt den Tangens). |
| 7 | merke + schluss | 3:35 | 25 s | Merkzettel (gesprochen wie geschrieben): „Tangens ist Gegenkathete durch Ankathete.“ · „Suchst du den Winkel, nimmst du tan⁻¹.“ · „Steigung ist der Tangens des Steigungswinkels.“ Motivationssatz + Spruch aus `werkzeug/motivation.py`. |

Summe ≈ 4:00.

## Offene Entscheidungen für den Nutzer
1. Thema und Reihenfolge der Reihe (3 Tangens · 4 Sinussatz · 5 Kosinussatz · 6 Bogenmaß · 7 Sinus-/Kosinusfunktion ·
   8 fakultativ a · sin(b · x + c)); Unterrichtsstand und Termin der Klassenarbeit.
2. Beispiel in Szene 3: **Schatten** (Vorschlag: stimmt ohne Zusatz) oder **Turm mit Winkelmesser** (klassische
   Schulbuchaufgabe, braucht aber die Augenhöhe: 20 m · tan 35° + 1,60 m = 15,6 m, ≈ 10 s länger).
3. Szene 5 (Gerade) behalten (Lehrplan) oder streichen (dann ≈ 3:30).

## Geprüft (17.11.)
- Gerechnet (Python): tan⁻¹(0,12) = 6,843° (zum Vergleich sin⁻¹(0,12) = 6,892°: der Unterschied zwischen „100 m
  waagrecht“ und „100 m Straße“ ist klein, aber da; im Video „auf 100 m waagrecht“ sagen und so zeichnen).
  tan 35° = 0,7002 → 20 m · 0,700 = 14,0 m (exakt 14,004 m). tan⁻¹(0,5) = 26,565° → 26,57°. tan⁻¹(1) = 45°.
  tan 30° = √3/3 = 0,5774, tan 60° = √3 = 1,7321, tan 89° = 57,29, tan 89,9° = 572,96.
  Probe mit Video 2: 4,70 m / 1,71 m = 2,749 ≈ tan 70° = 2,747.
- Straßenschild (Zeichen 110): Prozent = Höhenunterschied : waagrechte Strecke, 100 % = 45° – per Websuche bestätigt,
  aber nur populäre Quellen (bussgeldkatalog.org, OpenStreetMap-Wiki), keine amtliche Fundstelle gefunden.
- **Rollstuhlrampe weggelassen**: „höchstens 6 % nach DIN 18040-1“ wird meist so genannt, die Websuche fand aber
  widersprüchliche Angaben zu Länge und Ausnahmen und keinen Normtext. Nicht ins Video, solange unbelegt.
- Negative Steigungen und Winkel über 90° kommen nicht vor (tan⁻¹ liefert dann negative Winkel); das Video behauptet
  nichts dazu.
- Lehrplan Hessen (Abgleich der Video-2-Sitzung, hier nicht erneut geprüft): 10.4 nennt tan als Längenverhältnis und
  „Steigungswinkel einer Geraden“ als Pflicht, Tangens**funktion** fakultativ.

## Bausteine
`regel.py` (Folge 1) als Baukasten, Zeichenhilfen aus `einheitskreis.py` und `sinus_anwendungen.py` nur importieren
(`rechter_winkel`, `hinweis_gegenueber`, `hinweis_anliegend`, `umformung`, `zz`, `zf`, `B`, `T`); `pruefen.py` und
`startbild.py` kopieren und anpassen. Ordner der Videos 1 und 2 und `einheitskreis/` (App) nicht ändern.
Eigene Vorschau-Seite erst mit dem ersten Clip anlegen (eine Veröffentlichung je Runde, vorher ankündigen).

## Skizzen (17.11.)
Nutzer 17.11.: „noch mal mit ein paar Bildern, die wir als Grafiken verwenden würden, dass ich sehe, was gerechnet
wird“, bevor das Video gebaut wird. `skizzen.py <ordner>` zeichnet sechs Standbilder (Regel, Mast, 12 %, 100 % = 45°,
Gerade, Einheitskreis) mit dem Baukasten der Reihe; an den Nutzer geschickt, Antwort offen.
Nutzer 17.11.: **Kirchturm** statt Fahnenmast; **Schatten lassen**; „lieber in der App dann den Sonnenwinkel berechnen
lassen, das ist aktuell die zeitgemäße Variante“ – verstanden als: die 35° kommen aus einer Sonnenstand-App auf dem Handy
statt vom Winkelmesser (Deutung, beim Nutzer rückgefragt). `drehbuch.md` als Entwurf geschrieben, nicht vertont.
