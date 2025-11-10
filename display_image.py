import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np

class openGLImage1:
    def __init__(self, image_path):
        if not glfw.init():
            raise Exception("GLFW init failed")

        self.window = glfw.create_window(800, 600, "Display Image", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window creation failed")

        glfw.make_context_current(self.window)
        self.image_path = image_path
        
def main():

    # Charger l'image avec Pillow
    img = Image.open("img/ciel.png").convert("RGBA")
    img_data = np.array(img)

    # Créer une texture OpenGL
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Boucle d'affichage
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Dessin d’un rectangle plein (l’image)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, -1)
        glTexCoord2f(1, 0); glVertex2f(1, -1)
        glTexCoord2f(1, 1); glVertex2f(1, 1)
        glTexCoord2f(0, 1); glVertex2f(-1, 1)
        glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
