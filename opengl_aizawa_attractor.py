# opengl_aizawa_attractor.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import numpy as np

points = [(0.1, 0.1)]

def add_point(point):
    points.append(point)
    if len(points) > 10000:
        points.pop(0)
    
def calculate_next_color():
    return (255,255,255)

def next_point(x, y, a=-1.3, b=-1.3, c=-1.8, d=-1.9):
    # x_next = x + (z - b) * x - d * y
    # y_next = y + d * x + (z - b) * y
    # z_next = z + c + a * z - (z**3) / 3 - (x**2 + y**2) * (1 + e * z) + f * z * x**3
    next_x = np.sin(a * y) + c * np.cos(a * x)
    next_y = np.sin(b * x) + d * np.cos(b * y)
    return next_x, next_y

def draw_points():
    glBegin(GL_POINTS)
    for (x, y) in points:
        glColor3ub(*calculate_next_color())
        glVertex2f(x * 0.1, y * 0.1)
    glEnd()

if __name__ == "__main__":
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(1.0)
    x, y = 0.1, 0.1
    for _ in range(10000):
        x, y = next_point(x, y)
        add_point((x, y))
    draw_points()