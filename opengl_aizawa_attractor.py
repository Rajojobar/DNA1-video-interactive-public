from PyQt6 import QtOpenGL, QtGui, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from OpenGL import GL
from PyQt6.QtCore import Qt
import sys

# def draw_points():
#     glBegin(GL_POINTS)
#     for (x, y) in points:
#         glColor3ub(*calculate_next_color())
#         glVertex2f(x * 0.1, y * 0.1)
#     glEnd()

# if __name__ == "__main__":
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     glPointSize(1.0)
#     x, y = 0.1, 0.1
#     for _ in range(10000):
#         x, y = next_point(x, y)
#         add_point((x, y))
#     draw_points()

class AizawaAttractorShader(QtOpenGL.QOpenGLWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        self.points = [(0.1, 0.1)]
        self.a = -1.3
        self.b = -1.3
        self.c = -1.8
        self.d = -1.9

    def get_last_y(self):
        return self.points[-1][1]
    
    def get_last_x(self):
        return self.points[-1][0]
        
    def calculate_next_color(self):
        return (255,255,255)
    
    def add_new_point(self):
        next_x = np.sin(self.a * self.get_last_y) + self.c * np.cos(self.a * self.get_last_x)
        next_y = np.sin(self.b * self.get_last_x) + self.d * np.cos(self.b * self.get_last_y)

        points.append((next_x, next_y))
        if len(points) > 10000:
            points.pop(0)
    
    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glPointSize(1.0)
        
        for point in self.points.reverse():
            GL.glColor3ub(self.calculate_next_color())
            GL.glVertex2f(point[0] * 0.1, point[1] * 0.1)
        # Request a new frame to be rendered
        self.update()

    # def resizeGL(self, w: int, h: int):
    #     GL.glViewport(0, 0, w, h)   