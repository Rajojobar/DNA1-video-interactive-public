import sys
from functools import partial
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from player_video import PlayerVideo
from player_opengl import PlayerOpenGl
from player_image import PlayerImage
from compteur import Compteur
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

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
    
    def play_audio(file_path, volume=50):
        audio_output = QAudioOutput()
        audio_output.setVolume(volume / 100)  # Volume between 0.0 and 1.0

        # Ensure the audio output is not muted
        audio_output.setMuted(False)

        media_player = QMediaPlayer()
        media_player.setAudioOutput(audio_output)
        media_player.setSource(QUrl.fromLocalFile(file_path))
        
        # Keep a reference to prevent garbage collection
        windows.append(media_player)
        windows.append(audio_output)
        
        media_player.play()
        return media_player

    # Generated
    def schedule(callable_obj, delay_ms):
        QTimer.singleShot(delay_ms, callable_obj)



    # Début du film (titre) Durée : 30 secondes
    schedule(partial(show_instance_fullscreen, PlayerImage, "src/titre.png", size=(1920,1080), titre="Titre", death=30000), 0)
    
    # Début de mla bande son à 8 secondes
    schedule(partial(play_audio, "src/audio1.mp3", volume=70), 8000)

    # Création du compteur à 8 secondes 
    schedule(partial(show_instance, Compteur, death=999999, isFunny=True), 8000)
    
    # OpenGL Clifford Attractor 1 à 20 secondes Termine à 40 secondes
    from opengl_clifford_attractor import CliffordAttractorShader as Clifford0
    schedule(
        partial(
            show_instance,
            PlayerOpenGl,
            Clifford0,
            titre="Chaos Attractor 1",
            position=(800, 500),
            death=200000,
            isFunny=True,
        ),
        20000,
    )

    # Vidéo rush 1 à 29 secondes
    schedule(partial(show_instance, PlayerVideo, "src/rush_1.mp4", isFunny=True, mute=True), 24000)

    # Vidéo rush 2 à 29 secondes
    schedule(partial(show_instance, PlayerVideo, "src/rush_2.mp4", size=(900,1440), isFunny=True, mute=False), 30000)


    sys.exit(app.exec())
