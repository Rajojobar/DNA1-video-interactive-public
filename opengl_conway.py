import sys
from PyQt6 import QtOpenGL
from OpenGL import GL
import numpy as np
from random import randint
from PyQt6.QtWidgets import QApplication


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

class ConwaySimulation(QtOpenGL.QOpenGLWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 300)
        self._width = 300
        self._height = 300

        self.matrice = np.zeros((300, 300), dtype=int)

        self.scale = 89.0  # scale to make the attractor visible in 300x300

        self.reset()
    
    def reset(self):
        self.matrice = np.zeros((300, 300), dtype=int)
        self.matrice[149, 299] = 1
        self.matrice[151, 299] = 1
        self.matrice[150, 299] = 1

    def calculate_next_color(self, color):
        # slightly fade the color so older points appear darker
        r = max(0, int(color[0]) - 1)
        g = max(0, int(color[1]) - 2)
        b = max(0, int(color[2]) - 1)
        # return (255, 255, 255)
        return (r, g, b)
    
    def calculate_next_state(self, x, y):
        # Count live neighbors
        total = (
            self.matrice[(x-1) % 300, (y-1) % 300] + self.matrice[(x-1) % 300, y % 300] + self.matrice[(x-1) % 300, (y+1) % 300] +
            self.matrice[x % 300, (y-1) % 300] +                                     self.matrice[x % 300, (y+1) % 300] +
            self.matrice[(x+1) % 300, (y-1) % 300] + self.matrice[(x+1) % 300, y % 300] + self.matrice[(x+1) % 300, (y+1) % 300]
        )
        if self.matrice[x, y] == 1:
            if total < 2 or total > 3:
                return 0
            else:
                return 1
        else:
            if total == 3:
                return 1
            else:
                return 0

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

        GL.glPointSize(randint(1, 5))

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        # draw all points between glBegin/glEnd so OpenGL actually renders them
        GL.glBegin(GL.GL_POINTS)
        
        couleur = (255, 255, 255)
        # iterate from newest to oldest so the fading color works naturally
        
        nouvelle_matrice = np.copy(self.matrice)
        
        for i in range(len(self.matrice)-1):
            for j in range(len(self.matrice)-1):

                if self.matrice[i, j] == 1:
                    couleur = self.calculate_next_color(couleur)
                    GL.glColor3ub(couleur[0], couleur[1], couleur[2])
                    GL.glVertex2f(i, j)

                nouvelle_valeur = self.calculate_next_state(i, j)
                nouvelle_matrice[i, j] = nouvelle_valeur

        GL.glEnd()
        self.matrice = nouvelle_matrice
        # Request a new frame to be rendered
        self.update()


if __name__ == "__main__":
    from player_opengl import PlayerOpenGl

    app = QApplication(sys.argv)

    player = PlayerOpenGl(ConwaySimulation)

    player.show()
    sys.exit(app.exec())