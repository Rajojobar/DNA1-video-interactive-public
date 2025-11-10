from PyQt6 import QtOpenGL, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from OpenGL import GL
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
import sys
import random

class RandomColorShader(QtOpenGL.QOpenGLWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        
    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        # Generate random color
        r, g, b = random.random(), random.random(), random.random()
        GL.glClearColor(r, g, b, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Request a new frame to be rendered
        self.update()

    # def resizeGL(self, w: int, h: int):
    #     GL.glViewport(0, 0, w, h)   
   