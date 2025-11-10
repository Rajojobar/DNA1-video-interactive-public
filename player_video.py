from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QCursor

import numpy as np

class PlayerVideo(QWidget):
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

        self.setMouseTracking(True)
        self.video_widget.setMouseTracking(True)
        # Cache screen geometry for efficiency )
        self.screen_rect = QApplication.primaryScreen().geometry()


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
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.funnyStuff)
        self.timer.start(33)

    def check_finished(self, status):
        from PyQt6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.close()

    def funnyStuff(self):
        cursor_pos = QCursor.pos() # position de la souris
        global_geom = self.frameGeometry()

        if global_geom.contains(cursor_pos):
            # Refresh screen geometry in case of multi-monitor or resolution changes
            screen_rect = QApplication.primaryScreen().geometry()
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()

            w = self.width()
            h = self.height()

            max_x = screen_width - w - 10
            max_y = screen_height - h - 10

            if max_x <= 10:
                new_x = 10
            else:
                new_x = int(np.random.randint(10, max_x + 1))

            if max_y <= 10:
                new_y = 10
            else:
                new_y = int(np.random.randint(10, max_y + 1))

            self.move(new_x, new_y)
            self.raise_()  # fenêter au premier plan
            self.activateWindow()  # focus ?
