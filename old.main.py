import glfw, OpenGL.GL as gl, subprocess, sys

class GLWindow:
    def __init__(self, title, script):
        self.script = script
        self.window = glfw.create_window(640, 480, title, None, None)
        glfw.set_key_callback(self.window, self.on_key)
        self.running = True

    def on_key(self, win, key, scancode, action, mods):
        if action == glfw.PRESS:
            print(  f"Key pressed: {key}" )
            if key == glfw.KEY_Q:
                self.running = False
            elif key == glfw.KEY_N:
                windows.append(GLWindow("New GL Window", "opengl-bezier.py"))

    def render(self):
        glfw.make_context_current(self.window)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        subprocess.run([sys.executable, self.script])
        glfw.swap_buffers(self.window)

if not glfw.init():
    raise Exception("GLFW init failed")

windows = [
    GLWindow("Fenêtre Bézier", "opengl-bezier.py"),
    GLWindow("Fenêtre Demo", "render.py"),
    GLWindow("Oh lala", "ciel.py")
]

while windows:
    for w in windows[:]:
        if glfw.window_should_close(w.window) or not w.running:
            glfw.destroy_window(w.window)
            windows.remove(w)
        else:
            w.render()
    glfw.poll_events()

glfw.terminate()
