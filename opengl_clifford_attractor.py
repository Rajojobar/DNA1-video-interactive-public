from PyQt6 import QtOpenGL
from OpenGL import GL
import numpy as np
from random import randint

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

class CliffordAttractorShader1(QtOpenGL.QOpenGLWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        self._width = 300
        self._height = 300
        self.points = [(0.1, 0.1)]
        self.a = -1.3
        self.b = -1.3
        self.c = -1.8
        self.d = -1.9
        self.scale = 100.0  # scale to make the attractor visible in 300x300

        # prepopulate some points so there's something to draw immediately
        for _ in range(1):
             self.add_new_point()

    def get_last_y(self):
        return self.points[-1][1]
    
    def get_last_x(self):
        return self.points[-1][0]
        
    def calculate_next_color(self, color):
        # slightly fade the color so older points appear darker
        r = max(0, int(color[0]) - 1)
        g = max(0, int(color[1]) - 2)
        b = max(0, int(color[2]) - 1)
        # return (255, 255, 255)
        return (r, g, b)
    
    def add_new_point(self):
        next_x = np.sin(self.a * self.get_last_y()) + self.c * np.cos(self.a * self.get_last_x())
        next_y = np.sin(self.b * self.get_last_x()) + self.d * np.cos(self.b * self.get_last_y())

        self.points.append((next_x, next_y))
        if len(self.points) > 100000:
            self.points.pop(0)
    
    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w: int, h: int):
        # set viewport and an orthographic projection that maps coordinates to pixel space
        self._width = w
        self._height = h
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # top-left origin to match typical UI coordinates (y increases downward)
        GL.glOrtho(0, w, h, 0, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def paintGL(self):
        # Ajout d'un nouveau point à chaque frame
        self.add_new_point()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glPointSize(randint(1, 5))
        # draw all points between glBegin/glEnd so OpenGL actually renders them
        GL.glBegin(GL.GL_POINTS)
        couleur = (255, 255, 255)
        # iterate from newest to oldest so the fading color works naturally
        for i in range(len(self.points)-1, -1, -1):
            couleur = self.calculate_next_color(couleur)
            GL.glColor3ub(couleur[0], couleur[1], couleur[2])
            # mise à l'échelle pour mieux voir l'attracteur
            x_upscaled = self.points[i][0] * self.scale
            y_upscaled = self.points[i][1] * self.scale
            # centrage dans la fenêtre
            x_centered = x_upscaled + (self._width / 2.0)
            y_centered = y_upscaled + (self._height / 2.0)
            GL.glVertex2f(x_centered, y_centered)
        GL.glEnd()

        # Request a new frame to be rendered
        self.update()

    # def resizeGL(self, w: int, h: int):
    #     GL.glViewport(0, 0, w, h)   


class CliffordAttractorShader2(QtOpenGL.QOpenGLWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 200)
        self._width = 300
        self._height = 300
        self.points = [(0.1, 0.1)]
        self.a = -1.3
        self.b = -1.3
        self.c = -1.8
        self.d = -1.9
        self.scale = 100.0  # scale to make the attractor visible in 300x300

        # prepopulate some points so there's something to draw immediately
        # for _ in range(10000):
        #      self.add_new_point()

    def get_last_y(self):
        return self.points[-1][1]
    
    def get_last_x(self):
        return self.points[-1][0]
        
    def calculate_next_color(self, color):
        # slightly fade the color so older points appear darker
        # r = max(0, int(color[0]) - 1)
        # g = max(0, int(color[1]) - 2)
        # b = max(0, int(color[2]) - 1)
        return (255, 255, 255)
        # return (r, g, b)
    
    def add_new_point(self):
        next_x = np.sin(self.a * self.get_last_y()) + self.c * np.cos(self.a * self.get_last_x())
        next_y = np.sin(self.b * self.get_last_x()) + self.d * np.cos(self.b * self.get_last_y())

        self.points.append((next_x, next_y))
    
    def initializeGL(self):
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w: int, h: int):
        # set viewport and an orthographic projection that maps coordinates to pixel space
        self._width = w
        self._height = h
        GL.glViewport(0, 0, w, h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        # top-left origin to match typical UI coordinates (y increases downward)
        GL.glOrtho(0, w, h, 0, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def paintGL(self):
        # Ajout d'un nouveau point à chaque frame
        self.add_new_point()

        # GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glPointSize(1)
        # draw all points between glBegin/glEnd so OpenGL actually renders them
        GL.glBegin(GL.GL_POINTS)
        couleur = (255, 255, 255)
        # iterate from newest to oldest so the fading color works naturally
        for i in range(len(self.points)-1, -1, -1):
            couleur = self.calculate_next_color(couleur)
            GL.glColor3ub(couleur[0], couleur[1], couleur[2])
            # mise à l'échelle pour mieux voir l'attracteur
            x_upscaled = self.points[i][0] * self.scale
            y_upscaled = self.points[i][1] * self.scale
            # centrage dans la fenêtre
            x_centered = x_upscaled + (self._width / 2.0)
            y_centered = y_upscaled + (self._height / 2.0)
            GL.glVertex2f(x_centered, y_centered)
        GL.glEnd()

        # Request a new frame to be rendered
        self.update()
