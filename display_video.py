import cv2
import glfw
import OpenGL.GL as gl

def main(video_path):

    source = cv2.VideoCapture(video_path)
    if not source.isOpened():
        raise IOError("Vidéo existe pas ou impossible à ouvrir")

    vid_width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = source.get(cv2.CAP_PROP_FPS) or 30

    # --- Taille écran ---
    if not glfw.init():
        raise Exception("Échec initialisation GLFW")
    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    screen_w, screen_h = mode.size.width, mode.size.height

    # --- Adapter taille vidéo ---
    scale = min(screen_w / vid_width, screen_h / vid_height, 1.0)
    win_w, win_h = int(vid_width * scale), int(vid_height * scale)

    # --- Créer la fenêtre ---
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
    window = glfw.create_window(win_w, win_h, "Video OpenGL", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Échec création fenêtre GLFW")
    glfw.make_context_current(window)

    # --- Config OpenGL ---
    gl.glEnable(gl.GL_TEXTURE_2D)
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    # --- Boucle principale ---
    while not glfw.window_should_close(window):
        ret, frame = source.read()
        if not ret:
            break  # Fin de la vidéo

        # Conversion OpenCV BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 0)  # Y inversé pour OpenGL

        # Envoyer frame à OpenGL
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGB,
            frame.shape[1], frame.shape[0],
            0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, frame
        )

        # Effacer l’écran
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Dessiner un quad plein écran
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0, 0); gl.glVertex2f(-1, -1)
        gl.glTexCoord2f(1, 0); gl.glVertex2f(1, -1)
        gl.glTexCoord2f(1, 1); gl.glVertex2f(1, 1)
        gl.glTexCoord2f(0, 1); gl.glVertex2f(-1, 1)
        gl.glEnd()

        glfw.swap_buffers(window)
        glfw.poll_events()
        glfw.wait_events_timeout(1 / fps)

    # --- Nettoyage ---
    source.release()
    glfw.terminate()


if __name__ == "__main__":
    main("src/video.mp4")
