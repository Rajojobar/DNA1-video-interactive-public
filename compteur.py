import sys
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QGridLayout, QLabel
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtGui import QCursor
import numpy as np

class Compteur(QWidget):
    def __init__(self, position=(200,500), size=(100,50), death=-1, isFunny=True,  parent=None):
        super().__init__(parent)
        self.setWindowTitle('Compte à rebours')

        x, y = position
        width, height = size
        self.setGeometry(x, y, width, height)

        self.death = death
        self.estDrole = isFunny
        self.elapsed_time = 0  # Track elapsed time in milliseconds

        self.listFile = QListWidget()
        self.remaining_time_label = QLabel('STARTING...')
        self.startBtn = QPushButton('Start')
        self.endBtn = QPushButton('Please stop!')

        layout = QGridLayout()

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)

        layout.addWidget(self.remaining_time_label, 1, 0, 1, 2)
        layout.addWidget(self.startBtn, 2, 0)
        layout.addWidget(self.endBtn, 2, 1)

        self.startBtn.setDisabled(True)

        self.startTimer()
        # self.startBtn.clicked.connect(self.startTimer)
        # self.endBtn.clicked.connect(self.endTimer)

        # Timer suicide 
        if self.death > 0:
            self.suicide = QTimer(self)
            self.suicide.setSingleShot(True)
            self.suicide.timeout.connect(self.close)
            self.suicide.start(self.death)

        # Timer for mouse tracking
        if self.estDrole:
            self.tracking = QTimer(self)
            self.tracking.timeout.connect(self.funnyStuff)
            self.tracking.start(33)
            self.setMouseTracking(True)
            self.label.setMouseTracking(True)

        self.setLayout(layout)

    def showTime(self):
        current_time = QDateTime.currentDateTime()
        # formatted_time = current_time.toString('hh:mm:ss')
        # self.label.setText(formatted_time)

        # Update remaining time if death is set
        if self.death > 0:
            remaining_time = max(0, self.death - self.elapsed_time)
            remaining_seconds = remaining_time // 1000
            self.remaining_time_label.setText(f'Remaining: {remaining_seconds} seconds')
            self.elapsed_time += 1000  # Increment elapsed time

    def startTimer(self):
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    # def endTimer(self):
    #     self.timer.stop()
    #     self.startBtn.setEnabled(True)
    #     self.endBtn.setEnabled(False)

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Compteur(death=10000)  # Set death time in milliseconds (e.g., 10000 ms = 10 seconds)
    form.show()
    sys.exit(app.exec())