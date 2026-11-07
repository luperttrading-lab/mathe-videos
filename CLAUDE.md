# Mathe-Videos: Kopfrechnen-Reihe und Übungs-App

Erklärvideos für einen **eigenen YouTube-Kanal** (Nutzerentscheidung 05.11., getrennt von den Gesundheits-Faktenchecks),
Reihe „Kopfrechnen“, geplant 127 Folgen (`themen/mathe-tricks/`), dazu die Übungs-App `uebung/`. Später evtl.
„Statistik leicht gemacht“; ob eigener Kanal oder zusammen mit Kopfrechnen, ist offen.

**Eigenes Repo seit 06.11.** (Nutzerentscheidung: über 100 Folgen und viele Übungen; das alte Repo hatte schon ≈ 1 GB).
Vorher Teil von `luperttrading-lab/5-Minuten-videos` (Gesundheit). Von dort kopiert (Stand a2e0836):
`werkzeug/render.py` (ElevenLabs, Dekodieren, Tonaufbereitung), `vorschau.py`, `fertig.py`, `motivation.py`,
`schriften/`, `tools/kosten.py`. Beide Fassungen entwickeln sich ab jetzt getrennt; was beide brauchen, von Hand
nachziehen.

## Aufbau
- `themen/mathe-einmaleins/` – Folge 1 „Der Zehner-Trick“: `regel.py` (Video), `animationen.py` (Zeichnen),
  `vorschaubild.py`, `youtube.md` (Titel), `tts_cache/` (Ton, eingecheckt), `bilder/` (Hand, MIT-Lizenz)
- `themen/mathe-elfer/` – Folge 2 „Der Elfer-Trick“: `elfer.py` (nutzt `regel.py` aus Folge 1 als Baukasten und bringt
  nur eigene Szenen, Klänge und Merksätze mit), `drehbuch.md`, `youtube.md`, `tts_cache/`, `bilder/` (QR `#elfer`,
  App-Bild). Stand 07.11.: Entwurf 2:48 mit Szene `neun` „Wie viele Ziffern hat das Ergebnis?“ (Nutzerwunsch: in Wort
  und Bild, Kästchen je Ziffer: meist eine mehr, 2 → 3, 3 → 4; zwei mehr nur, wenn vorne eine 9 steht und die Summe
  direkt dahinter zweistellig ist, Beispiel 97 · 11 = 1067). Satz „Meistens eine mehr als die Zahl, die mit elf
  multipliziert wird“ per Hörprobe gewählt (07.11., Satz 1; genau dieser Ton im Cache). Formulierung bleibt „… die Summe
  direkt dahinter zweistellig ist“ (Nutzer 07.11.: nicht „ab 91“, das ist ab vier Stellen falsch, 9091 · 11 = 100001).
  07.11.: „rendern“ (Nutzer), App 2.18 übt 91–99 mit.
- `themen/mathe-stilprobe/` – `vorschau.json` (Auswahl und Proben), `fertig.json` (fertige Videos)
- `themen/mathe-tricks/` – Folgenplan und Recherche der 127 Tricks
- `uebung/` – App „Kopfrechnen üben“ (GitHub Pages), Details `uebung/LIESMICH.md`
- `index.html` im Hauptordner leitet auf `uebung/` weiter

## Antworten an den Nutzer
- Kurz halten und Bilder zeigen statt viel Text (Kontaktbogen, Stichbilder, Vorher/nachher).
- **Videos nie als Datei in den Chat** (landen auf dem Handy, belegen Speicher, spielen dort stumm). Stattdessen die
  Vorschau-Seite: `python3 ../../werkzeug/vorschau.py vorschau.json vorschau` in `themen/mathe-stilprobe/`, als Artifact
  mit `{"db": {}, "comments": {}}` veröffentlichen und immer dieselbe URL aktualisieren (nur geänderte Dateien hochladen,
  Dateinamen sind je Eintrag fest); neueste Fassung oben, „zu prüfen“ / „zur Info“, je Video höchstens 16 MB (720p/12 fps).
  Urteile in der Sammlung `vorschau_urteile`. Dateien (480p, 1080p) nur, wenn der Nutzer sie ausdrücklich will.
- **Aufbau jeder Antwort** (Nutzerwunsch 05.11.): oben kurz, was gemacht wurde. **Am Ende**, in dieser Reihenfolge:
  1. Bilder und Dateien erst jetzt schicken (`SendUserFile`), nicht mitten im Text.
  2. **„Deine Aufgabe: …“** – jede offene Entscheidung oder Abnahme als kurzer Arbeitsauftrag: Link, Ort auf der Seite,
     Zahl der Stellen. Nie nur „bitte abnehmen“. Nichts offen: kein Aufgabenblock.
  3. Die drei festen Links (unten) als beschriftete Liste, jeden **genau einmal**; der Arbeitsauftrag verweist darauf
     („Auswahl-Seite, Link unten“).
  4. Kostenzeile: `python3 tools/kosten.py` ausführen, Ausgabe wörtlich als letzte Zeile.
- **Jeder offene Punkt mit eigenem Link:** Vergleichsbilder als Eintrag auf die Vorschau-Seite (Standbild als kurzes
  Video, „passt“ = übernehmen). Nie ein Kürzel („Variante D“) ohne Bild und Link. Reine Textentscheidungen (z. B. Titel)
  direkt im Chat als nummerierte Liste.
- Jede Internetadresse als klickbarer Markdown-Link.
- **Feste Links** (Nutzerwunsch 05.11. abends: das fertige Video nicht zwischen den Proben suchen müssen):
  - **Fertige Videos:** [Kopfrechnen · fertige Videos](https://claude.ai/artifact/KtWyuT3JFmgu3yVphKcAH4) – nur die
    abgenommenen Fassungen mit YouTube-Titel (Kopieren-Knopf) und Vorschaubild. Nach jeder Abnahme `fertig.json` in
    `themen/mathe-stilprobe/` nachziehen, `python3 ../../werkzeug/fertig.py fertig.json <ordner>`, mit `publish_files`
    auf Slug `98f5e798-15cf-46ab-8792-8c95d9d0393f` (nur geänderte Dateien, alte entfernen).
  - **Auswahl und Proben:** [Mathe-Videos · Vorschau](https://claude.ai/artifact/PVisw26MxXcVy1NJngcMFu)
    (Slug `b62baf34-57b9-4814-be87-966add9566f8`)
  - **App:** [Kopfrechnen üben](https://luperttrading-lab.github.io/mathe-videos/uebung/)
- `vorschau.json` und `fertig.json` zeigen auf Videos im Scratchpad der Sitzung, die sie gerendert hat. In einer neuen
  Sitzung sind die Dateien weg: neu rendern (Ton aus dem Cache kostet nichts) und Pfade anpassen.

## Zugänge (Cloud-Umgebung „Standard“)
- `ELEVENLABS_API_KEY`: vorhanden. Creator-Plan, 125.526 Zeichen pro Monat; ein neuer Satz kostet ≈ 40–60 Zeichen.
- Schlüssel nie ausgeben, nie in Dateien oder den Chat. Das Repo ist öffentlich: keine Schlüssel, keine Stimmproben des
  Nutzers (geklonte Stimme „Lupert“) einchecken. MP4 und WAV nie committen (lassen sich aus Code und Ton-Cache neu
  rendern), Transkripte fremder Videos nie einchecken.
- App-Tests brauchen einen Klon von `luperttrading-lab/wuerfel` (Sprachmodell Vosk, die App lädt es von
  `luperttrading-lab.github.io/wuerfel/sprache/`), Pfad über `WUERFEL=…` (Standard `/home/user/luperttrading-lab/wuerfel`).

## Stimme und Ton
- ElevenLabs „Christian – Warm and Captivating“ (`NBqeXKdZHweef6y0B67V`), Modell `eleven_v4`, **Tempo 1,05**
  (≈ 4,14 Silben/s; bei 1,00 langsamer als alle gemessenen deutschen Erklärvideos).
- Tonaufbereitung in `werkzeug/render.py` (Rauschunterdrückung, De-Esser, lineare Verstärkung auf −16 LUFS).
- Antworten (JSON mit Audio und Zeitmarken) in `tts_cache/` einchecken, dann kosten Neu-Renders nichts.

## Mathe-Videos (Format ohne Ampel)
- Vorlage: `themen/mathe-einmaleins/regel.py` (Bilder ganz per Code, Formeln nie per KI-Bild; Einblendungen hängen an
  gesprochenen Wörtern).
- **Am Schluss immer ein Motivationssatz** (Nutzerwunsch 04.11.), z. B. nach einer Übung: „Länger als vier Sekunden? Ganz
  normal. Mit ein bisschen Übung schaffst du das auch.“ plus ein **wechselnder Spruch** („Das ist kein Hexenwerk.“, „Das
  ist keine Raketenwissenschaft.“ …) aus `werkzeug/motivation.py` (`spruch(thema, 'schluss')`; `'bruecke'` für Übergänge).
  Ein Thema behält seinen Spruch, neue Themen bekommen den seltensten. Sprüche gern ergänzen.
- **Zu jedem Mathe-Video eine Übung** in der App `uebung/` (Nutzerwunsch 04.11.: 10 Aufgaben, tippen oder sprechen,
  richtig gezählt, Ø-Zeit). **Eine App mit vielen Übungen, nicht viele Apps** (06.11.: ein Symbol auf dem Handy, ein
  Sprachmodell-Download, ein Update-Mechanismus). Startseite der App im Stil des Vorschaubilds (Nutzerwahl 06.11.: Aufgabe groß mit „= ?“, grüne Leiste
  mit dem Namen des Tricks darüber). App-Symbol wie das Vorschaubild (Nutzerwahl 06.11.: „16·18“, grüne Leiste mit „= ?“,
  `uebung/tools/icon.py`); Name unter dem Symbol „Kopfrechnen“, kein Trickname und keine Nummer, weil die App alle Tricks
  enthält. Ob die Tricks nummeriert werden („Trick 1“), entscheidet der Nutzer nach Sichtung der ganzen Serie.
  Neue Übung in `uebung/aufgaben.js`, `APP_VERSION` hochzählen,
  `node uebung/tests/uebung.mjs` muss „Alles grün“ melden.
  Stand 06.11. abends: App 2.17 mit zwei Übungen (Zehner, Elfer), Trick wählen über den Namen in der grünen Leiste.
  Elfer-Stufen: Zweistellig 3 s, Summe unter 10 3 s, Die Eins wandert 4 s, Dreistellig 6 s (nur tippen). Seit 2.18 (07.11.)
  mit 91 … 99 wie im Video (97 · 11 = 1067), Sprache bis 1099.
- **Zielgruppe: Jugendliche ab 13 und Erwachsene, „nicht speziell für Kinder“** (Nutzerentscheidung 06.11.): Kanal und
  jedes Video in YouTube Studio so einstellen; nur dann gibt es Abspann, Infokarten und Kommentare. Die Einstellung muss
  zum Inhalt passen (Kinder = unter 13, US-Gesetz COPPA): keine Wörter wie „Grundschule“, „Klasse 4“, „für Kinder“ in
  Titel, Beschreibung und Schlagwörtern, keine Kinderansprache, keine Zeichentrickfiguren, Beispiele aus dem Alltag.
  „Großes Einmaleins“ als Suchwort bleibt. Der Haken versteckt nichts: Kinder dürfen weiter zuschauen.
- **Vernetzung Video ↔ App, Bezahlmodell** (Nutzer 06.11., Übersicht `strategie/video_app_vernetzung.pdf`, Quelltext
  daneben als HTML): Video zuerst, kein App-Hinweis am Anfang oder in der Mitte; ein Satz vor dem Abspann („Üben kannst du in
  der kostenlosen App. Den Link findest du unter dem Video.“, Nutzer 06.11.: nicht „zehn Aufgaben“, kostenlos ist die App), QR-Code neben dem Handy auf derselben Seite für Fernseh-Zuschauer (Nutzer 06.11.: nicht zusätzlich im Abspann, sonst kommt die App doppelt; Seite 2,5 s länger zum Scannen); Link zur Übung in der Beschreibung
  (Zeile 2) und im angepinnten Kommentar. Die App führt zurück: „▶ Video zum Trick“, „Nächster Trick“ = erst Video, dann
  Übung. Später gratis die Übung je Video, bezahlt Mischtraining/Statistik. **Bezahlen erst nach einem Umzug** (jetzt
  Testphase auf GitHub Pages, öffentlich: eine Bezahlsperre im Browser ist umgehbar). Abspann und Infokarten gibt es
  nicht bei „für Kinder gemacht“. Gebaut 06.11.: App 2.12 („▶ Video“ an der Trick-Karte, „Nächster Trick“ nach
  der Runde, Direktlink `#zehner`, Feld `video` in `aufgaben.js` nach dem Hochladen füllen); im Video Szene `app` vor dem
  Abspann (Handy mit `bilder/app_start.png`) mit QR-Code `bilder/qr_zehner.png` daneben; der Abspann bleibt ohne App. Je neue Folge:
  eigenen QR-Code (`segno`, Adresse `…/uebung/#<kurz>`) und App-Bild erzeugen.
- **Ziel vier Sekunden** (Nutzerentscheidung 05.11.): Video und App-Stufe „Alle Zahlen“ sagen „in vier Sekunden“ (Uhr
  `UHR = 4` in `regel.py`), „Einer ergeben 10“ und „Mal 11“ drei, „Quadrate“ vier (`ziel` je Stufe in
  `uebung/aufgaben.js`). Grund: Drei Sekunden mit Rechnen frustrieren; die meistgesehenen Videos nennen 3–5 s.
- **Name des Tricks** (Nutzerwahl 05.11.): kurzer Name („Der Zehner-Trick“), im Einstieg gesprochen („Mit dem
  Zehner-Trick klappt das immer für zwei Zahlen von elf bis neunzehn.“, Nutzerwahl 06.11.: sagt, was „das“ ist;
  „zwischen zehn und zwanzig“ verworfen, viele lesen es als 10 bis 20) und als Band unter der Aufgabe eingeblendet,
  sobald die Lösung steht. Kein eigenes Startbild vor dem Einstieg; oben links bleibt „Kopfrechnen“ als Name der Reihe.
- **YouTube-Vorschaubild der Reihe** (Nutzerwahl 05.11.: ein Design für alle Folgen): Stil „Papier mit Teal-Leiste
  unten“ aus `themen/mathe-einmaleins/vorschaubild.py` (`papier`): Aufgabe groß mit „= ?“, Einer orange und violett wie
  im Video, unten die grüne Leiste mit Name des Tricks links und „KOPFRECHNEN“ rechts. Je Folge nur Aufgabe und Name in
  `FOLGEN` ändern, keine Uhr. Fertig: `vorschaubild_zehner.png`.
- **YouTube-Titel nach Suchbegriffen** (Nutzerwunsch 05.11.): vorher die YouTube-Suchvorschläge abfragen
  (`https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=de&gl=de&q=…`; zeigt, was gesucht wird,
  nicht wie oft). Stand 05.11.: „großes Einmaleins“ (Tricks, im Kopf rechnen), „im Kopf multiplizieren“, „Kopfrechnen
  Trick multiplizieren“; niemand sucht „malnehmen“ oder eine konkrete Aufgabe. Aufbau (Nutzerwahl 05.11.): Name des
  Tricks vorn, dann ein Suchwort, dann das Beispiel mit dem Versprechen, z. B. „Zehner-Trick: großes Einmaleins im
  Kopf – 16 · 18 in 4 Sekunden“. Titel je Folge in `youtube.md`.
- **Endbildschirm** (Nutzerwahl 05.11., Szene `abspann` in `regel.py`): nach dem Motivationssatz gesprochen „Noch ein
  Trick? Hier geht's weiter. Und damit du nichts verpasst: Abonnier den Kanal.“ („Trick“ nur einmal) (für jede Folge
  gleich, kein bestimmtes Video ankündigen), dann `ABSPANN` = 8 s still. Bild: „Noch ein Trick?“, zwei Flächen für
  Video-Empfehlungen, Knopf „Abonnieren“; YouTube Studio legt die Elemente darauf, das Abo-Element (Kanalbild) rechts
  neben den Knopf auf freie Fläche (nur letzte 5–20 s, nicht bei „für Kinder gemacht“). Abo-Zeile: gezeichneter Knopf
  „Abonnieren“, auf den beim Wort „Abonnier“ eine Emoji-Hand „👆“ (`zeigehand`, `HAND_BILD` =
  `bilder/hand_fluent_3d_mittelhell.png`, Microsoft Fluent Emoji, MIT-Lizenz) schräg von links unten tippt (Klang
  `klick`, Spitze ≈ 0,16) und eine Tipp-Welle auslöst. Farben (`ABO_STIL = ('weiss', 'gruen')`): vorher weiß mit grünem
  Rand und grüner Schrift, nach dem Tippen kräftig grün mit weißem „✓ Abonniert“, Tipp-Welle weiß. Finger statt
  Mauszeiger: YouTube läuft vor allem auf Handy und Fernseher.
- **Erst rendern, wenn der Nutzer freigibt** (Nutzer 05.11.): Änderungen an einer Stelle als kurzen Clip nur dieser
  Stelle zeigen (Bilder per `G.bild(t)` in 4 Prozessen, Ton aus der WAV von `--nur-ton`), das ganze Video erst nach
  ausdrücklicher Freigabe („rendern“) neu rendern.
- **Geprüft und verworfen** (Nutzerentscheidung 04.11.): Abweichungs-Kreuz (tecmath/vedisch, Probe `kreuz_probe.py`) –
  unser Flächenmodell mit „Andersherum“ erklärt es besser. Recherche der meistgesehenen Videos zum Trick: kein anderer
  Rechenweg, nur andere Darstellungen.
- **Nichts Falsches behaupten, auch nicht vereinfacht** (Nutzer 07.11.): Nicht jeden Sonderfall erklären, aber eine
  Regel muss immer stimmen. Lieber die allgemeingültige Formulierung (Elfer: „die Summe direkt dahinter“, die wandernde
  Eins steckt darin) als eine einfachere, die Sonderfälle falsch macht („ab 91“ scheitert an 9091 · 11 = 100001).
- **„multiplizieren“ statt „malnehmen“** in neuen Folgen (Nutzer 07.11.: „malnehmen“ klingt nach Grundschule,
  Zielgruppe ab 13). Folge 1 bleibt, wie sie abgenommen ist.
- **Merksätze so sprechen, wie sie dastehen** (Nutzerwunsch 04.11.): keine Kurzformen („Einer rüber“), die man nur
  lesend versteht; der Merkzettel zeigt genau die gesprochenen Sätze.
- **Geräusche sparsam** (Nutzer 04.11.): kein „Plopp“; Glöckchen nur zusammen mit den Funken an den grünen
  Endergebnissen. Klicks der Sprachausgabe in Pausen dämpft `entknacksen` in `regel.py`, dazu Tiefpass 12 kHz.
  Vorschau-Ton direkt aus der WAV kodieren (`-map 1:a`, AAC 160k), nicht AAC aus AAC.
- **Keine künstlichen Pausen in den Ton schneiden** (Messung 04.11.): Christian pausiert an Satzenden selbst
  200–500 ms, die Zeitmarken sind nur auf ≈ 40 ms genau, Schnitte landeten im Wort.
- **Ausliefern:** 1080p für den Upload (AAC 192k), 720p für Vorschau- und Fertig-Seite, 480p zum Verschicken:
  `ffmpeg -i video.mp4 -vf "fps=15,scale=854:480:flags=lanczos" -c:v libx264 -preset slow -crf 30 -tune stillimage
  -profile:v main -pix_fmt yuv420p -c:a aac -b:a 64k -ac 1 -movflags +faststart video_480p.mp4`
