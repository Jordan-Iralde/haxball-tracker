# main.py
import keyboard
from core.tracker import HaxballTracker
from ui.window import TrackingWindow
from config.settings import config

if __name__ == "__main__":
    # Crear instancia del tracker con config
    tracker = HaxballTracker(config)

    # 2. Asignar teclas
    keyboard.add_hotkey("F5", tracker.start)
    keyboard.add_hotkey("F6", tracker.stop)

    # Lanzar ventana principal de tracking
    app = TrackingWindow(tracker, config)
    app.run()
    # 1. Instanciar tracker
