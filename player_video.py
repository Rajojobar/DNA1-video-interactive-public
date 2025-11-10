from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QTimer, QUrl
import numpy as np

class VideoPlayer(QWidget):
    def __init__(self, video_path, titre="sans titre", mute=False, position=(100,100), size=(640,480), death=-1, parent=None):
        super().__init__(parent)

        self.death = death # durée de vie en ms 

        self.setWindowTitle(titre)
        x, y = position
        width, height = size
        self.setGeometry(x, y, width, height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.audio_output.setVolume(0.0 if mute else 1.0)

        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(video_path))
        self.player.mediaStatusChanged.connect(self.check_finished)
        self.player.play()

        
        # Timer pour le suicide
        if self.death > 0:
            self.suicide = QTimer(self)
            self.suicide.setSingleShot(True)
            self.suicide.timeout.connect(self.close)
            self.suicide.start(self.death)

        # Timer pour vérifier la souris
        self.timer = QTimer()
        self.timer.timeout.connect(self.funnyStuff)
        self.timer.start(33)

    def check_finished(self, status):
        from PyQt6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.close()

    def funnyStuff(self):
        if self.underMouse(): 
            screen_rect = QApplication.primaryScreen().geometry()  # OK ici
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()

            new_x = np.random.randint(10, screen_width - self.width())
            new_y = np.random.randint(10, screen_height - self.height())
            self.setGeometry(new_x, new_y, self.width(), self.height())
