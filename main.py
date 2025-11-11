import sys
from functools import partial
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from player_video import PlayerVideo
from player_opengl import PlayerOpenGl
from player_image import PlayerImage
from compteur import Compteur

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # keep references so Qt windows are not garbage-collected
    windows = []

    # Generated
    def show_instance(cls, *args, **kwargs):
        inst = cls(*args, **kwargs)
        windows.append(inst)
        inst.show()
        return inst
    
    def show_instance_fullscreen(cls, *args, **kwargs):
        inst = cls(*args, **kwargs)
        windows.append(inst)
        inst.showFullScreen()
        return inst
    
    # Generated
    def schedule(callable_obj, delay_ms):
        QTimer.singleShot(delay_ms, callable_obj)

    # Début du film (titre)
    schedule(partial(show_instance_fullscreen, PlayerImage, "src/titre.png", size=(1920,1080), titre="Titre", death=20000), 0)
    
    schedule(partial(show_instance, Compteur, death=999999, isFunny=True), 11000)
    schedule(partial(show_instance, PlayerVideo, "src/rush_1.mp4", isFunny=True, mute=True), 15000)

    from opengl_clifford_attractor import CliffordAttractorShader as Clifford0
    schedule(
        partial(
            show_instance,
            PlayerOpenGl,
            Clifford0,
            titre="Clifford Attractor 1",
            position=(800, 500),
            death=200000,
            isFunny=True,
        ),
        12000,
    )

    sys.exit(app.exec())
