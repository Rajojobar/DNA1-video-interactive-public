from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QCursor
import numpy as np
import sys

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

        # self.gl_widget = GLWidget(fragment_shader_source=shader, parent=self)
        # layout.addWidget(self.gl_widget)

        gl_window = classe_gl_window()
        if not hasattr(gl_window, 'winId'):  # Basic check for QWindow
            raise TypeError("classe_gl_window() must return a QWindow instance")
        gl_widget = QWidget.createWindowContainer(gl_window, self)
        # gl_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # pour récupérer les événements de la souris m^ quand rien n'est cliqué
        self.setMouseTracking(True)
        gl_widget.setMouseTracking(True)

        layout.addWidget(gl_widget)

        # Cache screen geometry for efficiency )
        self.screen_rect = QApplication.primaryScreen().geometry()

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
