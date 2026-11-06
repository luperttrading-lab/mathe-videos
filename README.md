# Mathe-Videos

Erklärvideos zum Kopfrechnen (eigener YouTube-Kanal, Reihe „Kopfrechnen“) und die Übungs-App dazu.

- **App:** https://luperttrading-lab.github.io/mathe-videos/uebung/ (iPhone: *Teilen → Zum Home-Bildschirm*)
- **Folge 1 „Der Zehner-Trick“:** `themen/mathe-einmaleins/` – Video ganz per Code (`regel.py`), Ton ElevenLabs mit Zeitmarken
- **Folgenplan (127 Tricks):** `themen/mathe-tricks/`
- Ablauf und Regeln: `CLAUDE.md`

Voraussetzungen: Python 3 mit Pillow und numpy, ffmpeg; für neuen Ton `ELEVENLABS_API_KEY` in der Umgebung
(vorhandene Sätze kommen aus `tts_cache/` und kosten nichts).

    cd themen/mathe-einmaleins
    python3 regel.py video.mp4 --nur-ton        # Ton und Länge
    python3 regel.py video.mp4 --bild 5,60      # Kontrollbilder
    python3 regel.py video.mp4                  # ganzes Video (≈ 5 min Rechenzeit)

Herkunft: bis 06.11.2026 Teil von `luperttrading-lab/5-Minuten-videos` (Gesundheits-Faktenchecks).
