import os
import sys
import subprocess
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                             QFileDialog, QComboBox, QVBoxLayout, QWidget,
                             QProgressBar, QGroupBox, QHBoxLayout)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Dodaj ffmpeg do PATH
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(PROJECT_DIR, "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_path


class ConversionThread(QThread):
    """Wątek do konwersji w tle"""
    finished = pyqtSignal(str)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_file, output_format, output_dir, bitrate):
        super().__init__()
        self.input_file = input_file
        self.output_format = output_format
        self.output_dir = output_dir
        self.bitrate = bitrate

    def run(self):
        try:
            self.progress.emit("Przygotowuję konwersję...")

            # Przygotuj nazwę pliku wyjściowego
            base_name = os.path.basename(self.input_file).rsplit('.', 1)[0]
            output_file = os.path.join(self.output_dir, f"{base_name}.{self.output_format}")

            # Sprawdź czy plik już istnieje
            if os.path.exists(output_file):
                counter = 1
                while os.path.exists(output_file):
                    output_file = os.path.join(self.output_dir, f"{base_name}_{counter}.{self.output_format}")
                    counter += 1

            self.progress.emit(f"Konwertuję do {self.output_format.upper()}...")

            # Ścieżka do FFmpeg
            ffmpeg_exe = os.path.join(ffmpeg_path, "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg")
            if not os.path.isfile(ffmpeg_exe):
                ffmpeg_exe = shutil.which("ffmpeg")
            if not ffmpeg_exe:
                raise FileNotFoundError("Nie znaleziono FFmpeg. Zainstaluj FFmpeg lub umieść go w ffmpeg/bin.")

            # Komenda FFmpeg
            command = [ffmpeg_exe, '-i', self.input_file]

            # Dodaj parametry w zależności od formatu
            if self.output_format == 'mp3':
                command.extend(['-acodec', 'libmp3lame', '-ab', self.bitrate])
            elif self.output_format == 'aac' or self.output_format == 'm4a':
                command.extend(['-acodec', 'aac', '-ab', self.bitrate])
            elif self.output_format == 'ogg':
                command.extend(['-acodec', 'libvorbis', '-ab', self.bitrate])
            elif self.output_format == 'wav':
                command.extend(['-acodec', 'pcm_s16le'])
            elif self.output_format == 'flac':
                command.extend(['-acodec', 'flac'])
            elif self.output_format == 'wma':
                command.extend(['-acodec', 'wmav2', '-ab', self.bitrate])

            # Dodaj plik wyjściowy i nadpisanie
            command.extend(['-y', output_file])

            # Wykonaj konwersję
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            if process.returncode == 0:
                self.progress.emit("Gotowe!")
                self.finished.emit(output_file)
            else:
                self.error.emit(f"FFmpeg error: {process.stderr}")

        except Exception as e:
            self.error.emit(f"Błąd: {str(e)}")


class AudioConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.output_dir = os.getcwd()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Converter')
        self.setGeometry(100, 100, 700, 500)

        # Widget główny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tytuł
        title = QLabel('🎵 AUDIO CONVERTER')
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 20px;")
        layout.addWidget(title)

        # Sekcja wyboru pliku
        file_group = QGroupBox("Plik wejściowy")
        file_layout = QVBoxLayout()

        self.btn_select = QPushButton('📁 Wybierz plik audio')
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_select.clicked.connect(self.select_file)
        file_layout.addWidget(self.btn_select)

        self.label_file = QLabel('Nie wybrano pliku')
        self.label_file.setStyleSheet("padding: 10px; color: #7f8c8d;")
        file_layout.addWidget(self.label_file)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Sekcja ustawień konwersji
        settings_group = QGroupBox("Ustawienia konwersji")
        settings_layout = QVBoxLayout()

        # Format wyjściowy
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('Format wyjściowy:'))

        self.combo_format = QComboBox()
        self.combo_format.addItems([
            'mp3 - MP3 (najpopularniejszy)',
            'wav - WAV (bez strat)',
            'ogg - OGG Vorbis',
            'flac - FLAC (bez strat)',
            'm4a - M4A (AAC)',
            'aac - AAC',
            'wma - Windows Media Audio'
        ])
        format_layout.addWidget(self.combo_format)
        settings_layout.addLayout(format_layout)

        # Bitrate (dla formatów stratnych)
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel('Jakość (bitrate):'))

        self.combo_bitrate = QComboBox()
        self.combo_bitrate.addItems([
            '128k - Niska jakość',
            '192k - Średnia jakość',
            '256k - Dobra jakość',
            '320k - Najwyższa jakość'
        ])
        self.combo_bitrate.setCurrentIndex(1)  # Domyślnie 192k
        bitrate_layout.addWidget(self.combo_bitrate)
        settings_layout.addLayout(bitrate_layout)

        # Folder wyjściowy
        output_layout = QHBoxLayout()
        self.btn_output_dir = QPushButton('📂 Wybierz folder docelowy')
        self.btn_output_dir.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.btn_output_dir)

        self.label_output = QLabel(f'Zapisze do: {self.output_dir}')
        self.label_output.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        output_layout.addWidget(self.label_output)
        settings_layout.addLayout(output_layout)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Przycisk konwersji
        self.btn_convert = QPushButton('🔄 KONWERTUJ')
        self.btn_convert.setEnabled(False)
        self.btn_convert.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.btn_convert.clicked.connect(self.start_conversion)
        layout.addWidget(self.btn_convert)

        # Status
        self.label_status = QLabel('Gotowy do pracy')
        self.label_status.setStyleSheet("padding: 10px; color: #27ae60; font-weight: bold;")
        layout.addWidget(self.label_status)

        # Pasek postępu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Przycisk otwórz folder
        self.btn_open_folder = QPushButton('📁 Otwórz folder z plikiem')
        self.btn_open_folder.setEnabled(False)
        self.btn_open_folder.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.btn_open_folder.clicked.connect(self.open_output_folder)
        layout.addWidget(self.btn_open_folder)

        central_widget.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik audio",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma *.aiff *.opus)"
        )
        if file_path:
            self.input_file = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            self.label_file.setText(f'✅ {file_name} ({file_size:.2f} MB)')
            self.btn_convert.setEnabled(True)

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Wybierz folder docelowy")
        if dir_path:
            self.output_dir = dir_path
            self.label_output.setText(f'Zapisze do: {self.output_dir}')

    def start_conversion(self):
        if not self.input_file:
            return

        # Wyciągnij format i bitrate
        output_format = self.combo_format.currentText().split(' - ')[0]
        bitrate = self.combo_bitrate.currentText().split(' - ')[0]

        # Wyłącz przyciski
        self.btn_open_folder.setEnabled(False)
        self.btn_convert.setEnabled(False)
        self.btn_select.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Nieokreślony postęp

        # Uruchom konwersję w wątku
        self.thread = ConversionThread(self.input_file, output_format, self.output_dir, bitrate)
        self.thread.progress.connect(self.update_status)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.error.connect(self.conversion_error)
        self.thread.start()

    def update_status(self, message):
        self.label_status.setText(message)

    def conversion_finished(self, output_file):
        self.label_status.setText(f'✅ Gotowe! Zapisano: {os.path.basename(output_file)}')
        self.progress_bar.setVisible(False)
        self.btn_convert.setEnabled(True)
        self.btn_select.setEnabled(True)
        self.btn_open_folder.setEnabled(True)
        self.last_output_file = output_file

    def conversion_error(self, error_message):
        self.btn_open_folder.setEnabled(False)
        self.label_status.setText(f'❌ {error_message}')
        self.progress_bar.setVisible(False)
        self.btn_convert.setEnabled(True)
        self.btn_select.setEnabled(True)

    def open_output_folder(self):
        if hasattr(self, 'last_output_file'):
            # Otwórz folder i zaznacz plik
            if sys.platform == 'win32':
                os.startfile(os.path.dirname(self.last_output_file))
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(["open", os.path.dirname(self.last_output_file)])
            else:  # Linux
                subprocess.Popen(["xdg-open", os.path.dirname(self.last_output_file)])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioConverterApp()
    window.show()
    sys.exit(app.exec_())






