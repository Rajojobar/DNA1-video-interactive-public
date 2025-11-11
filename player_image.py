from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import QTimer, Qt
import numpy as np

class PlayerImage(QWidget):
    def __init__(self, image_path, titre="sans titre", fullscreen=False, position=(100,100), size=(640,480), death=-1, isFunny=False, parent=None):
        super().__init__(parent)

        self.death = death
        self.estDrole = isFunny

        self.setWindowTitle(titre)
        x, y = position
        width, height = size
        self.setGeometry(x, y, width, height)

        # Simple image display
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)


        # pour récupérer les événements de la souris m^ quand rien n'est cliqué
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
                
        layout.addWidget(self.label)
        self.setLayout(layout)

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.label.setText("Image not found")
        else:
            pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.label.setPixmap(pixmap)

        # Timer for auto-close
        if self.death > 0:
            self.suicide = QTimer(self)
            self.suicide.setSingleShot(True)
            self.suicide.timeout.connect(self.close)
            self.suicide.start(self.death)

        # Timer for mouse tracking
        if self.estDrole:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.funnyStuff)
            self.timer.start(33)

    def funnyStuff(self):
        cursor_pos = QCursor.pos()
        global_geom = self.frameGeometry()

        if global_geom.contains(cursor_pos):
            screen_rect = QApplication.primaryScreen().geometry()
            screen_width = screen_rect.width()
            screen_height = screen_rect.height()

            w = self.width()
            h = self.height()

            max_x = screen_width - w - 10
            max_y = screen_height - h - 10

            new_x = int(np.random.randint(10, max(max_x + 1, 11)))
            new_y = int(np.random.randint(10, max(max_y + 1, 11)))

            self.move(new_x, new_y)
        self.raise_()
        self.activateWindow()
