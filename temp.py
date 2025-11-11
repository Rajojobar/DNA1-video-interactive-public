# /home/rajojo/Bureau/generation images/projet-video/main.py
import sys
import traceback
import multiprocessing
import importlib
from multiprocessing import Process


def _run_player_video(source, mute=False):
    # runs in a separate process; any exception will exit the process only
    try:
        from PyQt6.QtWidgets import QApplication
        from player_video import PlayerVideo

        app = QApplication([])
        player = PlayerVideo(source, mute=mute)
        player.show()
        app.exec()
    except Exception:
        traceback.print_exc()
    finally:
        # ensure the process exits cleanly
        sys.exit(0)


def _run_player_opengl(shader_module, shader_class, titre=None, death=None):
    # shader_module: e.g. "opengl_aizawa_attractor"
    # shader_class: e.g. "AizawaAttractorShader"
    try:
        from PyQt6.QtWidgets import QApplication
        PlayerOpenGl = None

        # import shader class dynamically
        shader_mod = importlib.import_module(shader_module)
        shader_cls = getattr(shader_mod, shader_class)

        # import PlayerOpenGl
        player_mod = importlib.import_module("player_opengl")
        PlayerOpenGl = getattr(player_mod, "PlayerOpenGl")

        app = QApplication([])
        player = PlayerOpenGl(shader_cls, titre=titre, death=death)
        player.show()
        app.exec()
    except Exception:
        traceback.print_exc()
    finally:
        sys.exit(0)


if __name__ == "__main__":
    # Ensure spawn start method for cross-platform safety
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        # already set
        pass

    processes = []

    # Example: start multiple windows in independent processes.
    # Each process runs its own QApplication and will exit on error without
    # killing the other windows.
    #
    # Uncomment or add more processes as needed.

    # Video players (each in its own process)
    # p1 = Process(target=_run_player_video, args=("src/video1.mp4",), kwargs={"mute": True})
    # p2 = Process(target=_run_player_video, args=("src/video2.mp4",), kwargs={"mute": True})
    # processes.extend([p1, p2])

    # OpenGL players
    p3 = Process(
        target=_run_player_opengl,
        args=("opengl_aizawa_attractor", "AizawaAttractorShader"),
        kwargs={"titre": "OpenGL Aizawa", "death": 10000},
    )
    processes.append(p3)

    # start all processes
    for p in processes:
        p.start()

    try:
        # wait for all children to finish
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        # attempt graceful shutdown on Ctrl+C
        for p in processes:
            if p.is_alive():
                p.terminate()
        for p in processes:
            p.join()
