from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import QTimer
import numpy as np
import sys

from shader_render import GLWidget

class PlayerOpenGl(QWidget):
    ### Ce composant requiert de récupérer un argument correspondant à la classe de shader qu'il va afficher
    def __init__(self, classe_gl_window, titre="sans titre", position=(100,100), size=(640,480), death=-1, parent=None):
        super().__init__(parent)
        
        self.death = death # durée de vie en ms 

        self.setWindowTitle(titre)
        x, y = position
        width, height = size
        self.setGeometry(x, y, width, height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.gl_widget = GLWidget(fragment_shader_source=shader, parent=self)
        layout.addWidget(self.gl_widget)

        # Encapsule la fenêtre OpenGL donnée dans un QWidget
        gl_window = gl_window_class()
        gl_widget = QWidget.createWindowContainer(gl_window, self)
        gl_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        layout.addWidget(gl_widget)

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
        # from PyQt6.QtMultimedia import QMediaPlayer
        # if status == QMediaPlayer.MediaStatus.EndOfMedia:
        #     self.close()
        pass

    def funnyStuff(self):
        if self.underMouse(): 
            screen_rect = QApplication.primaryScreen().geometry()  # OK ici
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()

            new_x = np.random.randint(10, screen_width - self.width())
            new_y = np.random.randint(10, screen_height - self.height())
            self.setGeometry(new_x, new_y, self.width(), self.height())
