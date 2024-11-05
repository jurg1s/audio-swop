import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import QFontDatabase
from datetime import datetime

class FFMpegThread(QThread):
    progress = pyqtSignal()

    def __init__(self, video_other_path, video_with_audio_path, output_directory, audio_shift):
        super().__init__()
        self.video_other_path = video_other_path
        self.video_with_audio_path = video_with_audio_path
        self.output_directory = output_directory
        self.audio_shift = audio_shift

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_video_path = os.path.join(self.output_directory, f"output_video_{timestamp}.mp4")
        os.system(f"ffmpeg -itsoffset {self.audio_shift} -i '{self.video_other_path}' -i '{self.video_with_audio_path}' -c:v copy -map 0:v:0 -map 1:a:0 -shortest '{output_video_path}'")
        self.progress.emit()

class AudioSwopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.video_with_audio_path = ""
        self.video_other_path = ""
        self.output_directory = ""
        self.audio_shift = "0"

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Swop")
        self.setGeometry(100, 100, 500, 460)

        layout = QVBoxLayout()

        self.label_instruction = QLabel("Select the video file with desired audio, the video to replace audio, and the directory to save the output.")
        self.label_instruction.setWordWrap(True)
        layout.addWidget(self.label_instruction)

        self.button_video_with_audio = QPushButton("Select Video with Desired Audio ⇢")
        self.button_video_with_audio.clicked.connect(self.select_video_with_audio)
        layout.addWidget(self.button_video_with_audio)

        self.label_video_with_audio = QLabel("<span style='color:red;'>*</span> No file selected")
        layout.addWidget(self.label_video_with_audio)

        self.button_video_other = QPushButton("Select Video to Replace Audio ⇠")
        self.button_video_other.clicked.connect(self.select_video_other)
        layout.addWidget(self.button_video_other)

        self.label_video_other = QLabel("<span style='color:red;'>*</span> No file selected")
        layout.addWidget(self.label_video_other)

        self.button_output_directory = QPushButton("Select Directory to Save Output Video ↓")
        self.button_output_directory.clicked.connect(self.select_output_directory)
        layout.addWidget(self.button_output_directory)

        self.label_output_directory = QLabel("<span style='color:red;'>*</span> No directory selected")   
        layout.addWidget(self.label_output_directory)

        self.label_audio_shift = QLabel("Enter audio shift in seconds (positive for forward, negative for backward):")
        layout.addWidget(self.label_audio_shift)

        self.input_audio_shift = QLineEdit()
        self.input_audio_shift.setPlaceholderText("0")
        layout.addWidget(self.input_audio_shift)

        # Spinner setup
        self.spinner_label = QLabel(self)
        spinner_path = os.path.join(os.path.dirname(__file__), 'spinner.gif')
        self.spinner_movie = QMovie(spinner_path)
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.spinner_label)
        self.spinner_label.setVisible(False)

        # Replacing label setup
        self.replacing_label = QLabel("Replacing")
        self.replacing_label.setAlignment(Qt.AlignCenter)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.replacing_label.setFont(fixed_font)
        layout.addWidget(self.replacing_label)
        self.replacing_label.setVisible(False)

        layout.addStretch()

        self.start_button = QPushButton("Start Process")
        self.start_button.clicked.connect(self.start_process)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        # Timer for animating dots
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_replacing_label)
        self.dot_count = 0

    def select_video_with_audio(self):
        self.video_with_audio_path, _ = QFileDialog.getOpenFileName(self, "Select Video with Desired Audio", "", "Video files (*.mp4 *.avi *.mov *.mkv)")
        if self.video_with_audio_path:
            self.label_video_with_audio.setText(f"<span style='color:gray;'>Selected: {self.video_with_audio_path}</span>")

    def select_video_other(self):
        self.video_other_path, _ = QFileDialog.getOpenFileName(self, "Select Video to Replace Audio", "", "Video files (*.mp4 *.avi *.mov *.mkv)")
        if self.video_other_path:
            self.label_video_other.setText(f"<span style='color:gray;'>Selected: {self.video_other_path}</span>")

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Select Directory to Save Output Video")
        if self.output_directory:
            self.label_output_directory.setText(f"<span style='color:gray;'>Selected: {self.output_directory}</span>")

    def start_process(self):
        if not self.video_with_audio_path or not self.video_other_path or not self.output_directory:
            QMessageBox.critical(self, "Error", "Please select all required files and directory.")
            return

        self.audio_shift = self.input_audio_shift.text()

        # Disable button
        self.start_button.setEnabled(False)

        # Start the spinner animation
        self.spinner_label.setVisible(True)
        self.spinner_movie.start()

       # Start the replacing label animation
        self.replacing_label.setVisible(True)
        self.timer.start(100)  # Increase the speed of the animation

        self.ffmpeg_thread = FFMpegThread(self.video_other_path, self.video_with_audio_path, self.output_directory, self.audio_shift)
        self.ffmpeg_thread.progress.connect(self.on_process_complete)
        self.ffmpeg_thread.start()

    def update_replacing_label(self):
        self.dot_count = (self.dot_count + 1) % 4
        dots = '.' * self.dot_count
        self.replacing_label.setText(f"Replacing{dots:<3}")

    def on_process_complete(self):
        # Stop the spinner animation
        self.spinner_movie.stop()
        self.spinner_label.setVisible(False)

        # Stop the replacing label animation
        self.timer.stop()
        self.replacing_label.setVisible(False)

        # Enable button
        self.start_button.setEnabled(True)

        QMessageBox.information(self, "Process Complete", "Audio replaced successfully!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioSwopApp()
    ex.show()
    sys.exit(app.exec_())