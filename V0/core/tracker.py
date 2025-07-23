from pynput import keyboard
from threading import Thread

class HaxballTracker:
    def __init__(self, config):
        self.config = config
        self.tracking = False
        self.position_log = []
        self.event_log = []
        self.start_time = None
        self.listener = None

    def start(self):
        self.tracking = True
        self.start_time = time.time()
        self.position_log.clear()
        self.event_log.clear()
        print("[TRACKER] Iniciado.")

        # Iniciar listener en hilo aparte
        self.listener = Thread(target=self._start_keyboard_listener, daemon=True)
        self.listener.start()

    def stop(self):
        self.tracking = False
        print("[TRACKER] Detenido. Eventos registrados:", len(self.event_log))

    def _start_keyboard_listener(self):
        def on_press(key):
            if self.tracking:
                try:
                    self.log_event(f"KEY_DOWN:{key.char}")
                except AttributeError:
                    self.log_event(f"KEY_DOWN:{key.name}")

        def on_release(key):
            if not self.tracking:
                return False  # Detiene listener
            try:
                self.log_event(f"KEY_UP:{key.char}")
            except AttributeError:
                self.log_event(f"KEY_UP:{key.name}")

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def update_position(self, position):
        if self.tracking:
            timestamp = time.time() - self.start_time
            self.position_log.append((timestamp, position))

    def log_event(self, event_type):
        if self.tracking:
            timestamp = time.time() - self.start_time
            self.event_log.append((timestamp, event_type))
            print(f"[EVENTO] {event_type.upper()} @ {timestamp:.2f}s")
