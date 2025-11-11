import sys
from PyQt6.QtWidgets import QApplication
from player_video import PlayerVideo

# from opengl_random_color import RandomColorShader


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Exemple : lancer plusieurs vidéos en même temps
    player1 = PlayerVideo("src/video.mp4", mute=True)
    player2 = PlayerVideo("src/video.mp4", mute=True)
    player1.show()
    player2.show()

    # player3 = PlayerOpenGl(RandomColorShader, titre="OpenGL Random Color", death=5000)
    # player3.show()

    # from opengl_clifford_attractor import CliffordAttractorShader as Clifford0
    # player4 = PlayerOpenGl(Clifford0, titre="Clifford Attractor 1", death=200000)
    # player4.show()


    # player4 = rajojoQtWidget(titre="Rajojo Qt Widget", death=15000)
    # player4.show() 
    
