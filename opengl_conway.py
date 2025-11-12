import sys
from PyQt6 import QtOpenGL
from OpenGL import GL
import numpy as np
from random import randint, choice
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
        self.resize(290, 250)
        # self._width = 300
        # self._height = 300

        self.game_width = 100
        self.game_height = 100

        self.strongColor = choice([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1)])
        self.matrice = np.zeros((300, 300), dtype=int)
        self.puissanceCouleur = randint(70,150)
        
        self.countIterations = 0
        self.reset()
        
    def reset(self):
        self.matrice = np.zeros((self.game_width, self.game_height), dtype=int)
        # self.matrice[149, 299] = 1
        # self.matrice[151, 299] = 1
        # self.matrice[150, 298] = 1
        self.strongColor = choice([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 0, 1)])
        self.puissanceCouleur = randint(70,200)

        for _ in range(self.game_width * self.game_height // 10):
            self.matrice[randint(0, self.game_width-1), randint(0, self.game_height-1)] = 1

    def calculate_next_color(self, color):
        base = randint(0, 255)
        
        # slightly fade the color so older points appear darker
        r = max(0, int(base) - self.strongColor[0]*self.puissanceCouleur)
        g = max(0, int(base) - self.strongColor[1]*self.puissanceCouleur)
        b = max(0, int(base) - self.strongColor[2]*self.puissanceCouleur)
        # return (255, 255, 255)
        return (r, g, b)
    
    def calculate_next_state(self, x, y):
        # Count live neighbors
        total = (
            self.matrice[(x-1) % self.game_width, (y-1) % self.game_height] + self.matrice[(x-1) % self.game_width, y % self.game_height] + self.matrice[(x-1) % self.game_width, (y+1) % self.game_height] +
            self.matrice[x % self.game_width, (y-1) % self.game_height] + self.matrice[x % self.game_width, (y+1) % self.game_height] +
            self.matrice[(x+1) % self.game_width, (y-1) % self.game_height] + self.matrice[(x+1) % self.game_width, y % self.game_height] + self.matrice[(x+1) % self.game_width, (y+1) % self.game_height]
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

        GL.glPointSize(randint(2,6))

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        # draw all points between glBegin/glEnd so OpenGL actually renders them
        GL.glBegin(GL.GL_POINTS)
        
        couleur = (255, 255, 255)
        # iterate from newest to oldest so the fading color works naturally
        
        nouvelle_matrice = np.copy(self.matrice)
        
        for i in range(self.game_width-1):
            for j in range(self.game_height-1):

                if self.matrice[i, j] == 1:
                    couleur = self.calculate_next_color(couleur)
                    GL.glColor3ub(couleur[0], couleur[1], couleur[2])
                    upscaled_x = int(i * (self._width / self.game_width))
                    upscaled_y = int(j * (self._height / self.game_height))
                    GL.glVertex2f(upscaled_x, upscaled_y)
                    #GL.glVertex2f(i, j)

                nouvelle_valeur = self.calculate_next_state(i, j)
                nouvelle_matrice[i, j] = nouvelle_valeur

        GL.glEnd()
        self.matrice = nouvelle_matrice
        # Request a new frame to be rendered
  
        self.update()

        self.countIterations += 1

        if self.countIterations >= 70:
            self.countIterations = 0
            self.reset()


if __name__ == "__main__":
    from player_opengl import PlayerOpenGl

    app = QApplication(sys.argv)

    player = PlayerOpenGl(ConwaySimulation, titre="Conway")

    player.show()
    sys.exit(app.exec())