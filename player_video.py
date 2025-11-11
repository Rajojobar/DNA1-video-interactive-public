from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtGui import QCursor

import numpy as np

class PlayerVideo(QWidget):
    def __init__(self, video_path, titre="sans titre", mute=False, disable_close=False, estImportant=False, position=(100,100), size=(640,480), death=-1, isFunny=False, parent=None):
        super().__init__(parent)

        self.death = death # durée de vie en ms 
        self.estDrole = isFunny
        self.Important = estImportant

        self.disable_close = disable_close
        self._allow_close = disable_close == False

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
            self.suicide.timeout.connect(self._programmatic_close)
            self.suicide.start(self.death)

        # Timer pour vérifier la souris
        if self.estDrole:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.funnyStuff)
            self.timer.start(33)


    def _programmatic_close(self):
        """Allow a programmatic close (used by internal timers) and then close."""
        self._allow_close = True
        self.close()

    def closeEvent(self, event):
        """Ignore user-initiated close events when disable_close is True.

        Programmatic closes should call _programmatic_close() to set
        _allow_close True before calling close(), which will let the
        event be accepted.
        """
        if self.disable_close and not getattr(self, "_allow_close", False):
            # ignore user close
            event.ignore()
            return
        # reset the flag — after a programmatic close we don't want
        # future closes to be auto-allowed
        self._allow_close = False
        event.accept()

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
        if self.Important:
            self.raise_()  # fenêter au premier plan
            self.activateWindow()  # focus ?
