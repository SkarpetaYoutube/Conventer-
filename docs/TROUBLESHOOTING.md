# Rozwiązywanie problemów

## Program nie uruchamia się

Sprawdź wersję Pythona i zainstaluj zależności:

```powershell
python -m pip install -r requirements.txt
```

Jeżeli pojawia się `ModuleNotFoundError: No module named 'PyQt5'`, uruchom instalację przez tę samą wersję Pythona, którą uruchamiasz aplikację.

## FFmpeg nie został znaleziony

Aktualny kod szuka pliku `ffmpeg/bin/ffmpeg.exe` względem **bieżącego katalogu roboczego**. Otwórz terminal w katalogu projektu, sprawdź obecność pliku i uruchom `python audio_converter.py`.

## Konwersja zakończyła się błędem

Sprawdź, czy wejściowy plik audio jest poprawny, docelowy folder jest zapisywalny i czy używana wersja FFmpeg obsługuje wybrany koder. Szczegóły błędu FFmpeg pojawiają się w statusie aplikacji.

## Nie mogę znaleźć wyniku

Plik trafia do folderu wskazanego w aplikacji. Jeśli plik o tej samej nazwie już istnieje, nowy dostaje numerowany sufiks, np. `nagranie_1.mp3`.

## Linux i macOS

Interfejs jest oparty na PyQt5, ale ścieżka do FFmpeg w aktualnym kodzie jest ustawiona na `ffmpeg.exe`. Konwersja na tych systemach wymaga dostosowania tej ścieżki; sam FFmpeg z systemowego PATH obecnie nie jest automatycznie wykrywany.
