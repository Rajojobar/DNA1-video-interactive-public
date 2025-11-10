import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
import OpenGL.GL as gl


class OpenGLRenderWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shader_program = None
        self.vao = None
        self.vertex_count = 0
        self.bg_color = [0.1, 0.1, 0.1]

    def initializeGL(self):
        """Initialize OpenGL settings and shaders."""
        gl.glClearColor(*self.bg_color, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        self.shader_program = QOpenGLShaderProgram()
        self.shader_program.addShaderFromSourceCode(
            QOpenGLShader.Vertex,
            """
            #version 330
            layout(location = 0) in vec3 position;
            layout(location = 1) in vec3 color;
            out vec3 vertexColor;
            
            void main() {
                gl_Position = vec4(position, 1.0);
                vertexColor = color;
            }
            """
        )
        self.shader_program.addShaderFromSourceCode(
            QOpenGLShader.Fragment,
            """
            #version 330
            in vec3 vertexColor;
            out vec4 FragColor;
            
            void main() {
                FragColor = vec4(vertexColor, 1.0);
            }
            """
        )
        self.shader_program.link()
        
        # Create a simple triangle
        vertices = np.array([
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.0,  0.5, 0.0
        ], dtype=np.float32)
        
        colors = np.array([
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ], dtype=np.float32)
        
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        
        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 12, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        
        cbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, cbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, colors.nbytes, colors, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 12, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)
        
        self.vertex_count = 3

    def resizeGL(self, w, h):
        """Handle widget resize."""
        gl.glViewport(0, 0, w, h)

    def paintGL(self):
        """Render the scene."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        self.shader_program.bind()
        gl.glBindVertexArray(self.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertex_count)
        self.shader_program.release()

    def change_background_color(self):
        """Change background to random color."""
        self.bg_color = [random.random(), random.random(), random.random()]
        gl.glClearColor(*self.bg_color, 1.0)
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL Random Color Background")
        self.setGeometry(100, 100, 800, 600)
        
        self.gl_widget = OpenGLRenderWidget()
        self.setCentralWidget(self.gl_widget)
        
        # Timer to change color every 500ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.gl_widget.change_background_color)
        self.timer.start(500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
