# Audio Converter

Prosta aplikacja okienkowa do konwersji plików audio z użyciem Python, PyQt5 i FFmpeg.

## Funkcje

- Wybór pliku audio przez okno dialogowe.
- Konwersja do MP3, WAV, OGG, FLAC, M4A, AAC i WMA.
- Wybór bitrate dla formatów stratnych.
- Wybór katalogu docelowego.
- Automatyczne dodawanie numeru do nazwy, gdy plik wyjściowy już istnieje.
- Konwersja w osobnym wątku, bez blokowania interfejsu.

## Wymagania

- Python 3 z obsługą PyQt5.
- Pakiety z `requirements.txt`.
- FFmpeg w lokalizacji `ffmpeg/bin/ffmpeg.exe` (obecna implementacja korzysta ze ścieżki Windows).

## Uruchomienie (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python audio_converter.py
```

Uruchamiaj program z katalogu głównego projektu, aby prawidłowo odnaleźć FFmpeg.

## Użycie

1. Wybierz plik audio.
2. Ustaw format docelowy i ewentualnie bitrate.
3. Wybierz katalog zapisu.
4. Kliknij **KONWERTUJ**. Gotowy plik możesz znaleźć przyciskiem otwarcia folderu.

Więcej informacji: [obsługiwane formaty](docs/FORMATS.md) i [rozwiązywanie problemów](docs/TROUBLESHOOTING.md).
