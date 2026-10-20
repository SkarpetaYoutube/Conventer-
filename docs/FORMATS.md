# Formaty audio

Program przyjmuje pliki wybrane w oknie dialogowym: MP3, WAV, OGG, FLAC, M4A, AAC, WMA, AIFF i OPUS (o ile lokalny FFmpeg potrafi je odczytać).

| Format wyjściowy | Koder FFmpeg | Bitrate z interfejsu |
| --- | --- | --- |
| MP3 | libmp3lame | Tak |
| WAV | pcm_s16le | Nie |
| OGG | libvorbis | Tak |
| FLAC | flac | Nie |
| M4A | aac | Tak |
| AAC | aac | Tak |
| WMA | wmav2 | Tak |

## Uwagi

- Dostępne wartości bitrate to 128k, 192k, 256k i 320k.
- Zwiększenie bitrate nie przywróci jakości utraconej we wcześniejszej kompresji.
- Format WAV i FLAC nie korzysta z wyboru bitrate.
- Wynik jest zapisywany w wybranym folderze; jeśli nazwa już istnieje, aplikacja dodaje sufiks `_1`, `_2` itd.
- Faktyczna obsługa kodeków zależy od używanej kompilacji FFmpeg.
