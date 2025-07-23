# ui/window.py

import tkinter as tk
from pynput import mouse, keyboard
import threading

class TrackingWindow:
    def __init__(self, tracker, config):
        self.tracker = tracker
        self.config = config
        self.root = tk.Tk()
        self.root.title("Haxball Tracker MVP")
        self.root.geometry("400x200")
        self.running = True

        # Estado y feedback
        self.status_var = tk.StringVar()
        self.status_var.set("Esperando tecla...")

        # Interfaz simple
        tk.Label(self.root, text="Estado del Tracker:").pack(pady=10)
        tk.Label(self.root, textvariable=self.status_var, fg="lime", font=("Arial", 14)).pack()
        tk.Button(self.root, text="Cerrar", command=self.close).pack(pady=20)

        # Listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.handle_key)
        self.mouse_listener = mouse.Listener(on_click=self.handle_mouse)

    def run(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.root.mainloop()

    def close(self):
        self.running = False
        self.tracker.stop()
        self.root.destroy()

    def handle_key(self, key):
        try:
            k = key.char.upper() if hasattr(key, 'char') and key.char else str(key).upper()
        except:
            k = str(key)

        bindings = self.config["key_bindings"]

        if k == bindings["start_tracking"]:
            self.tracker.start()
            self.status_var.set("Grabando...")

        elif k == bindings["stop_tracking"]:
            self.tracker.stop()
            self.status_var.set("Detenido.")

        elif k == bindings["log_goal"]:
            self.tracker.log_event("gol")

        elif k == bindings["log_assist"]:
            self.tracker.log_event("asistencia")

        elif k == bindings["log_error"]:
            self.tracker.log_event("error")

        elif k == bindings["log_touch"]:
            self.tracker.log_event("toque")

    def handle_mouse(self, x, y, button, pressed):
        if pressed and self.tracker.tracking:
            pos = (int(x), int(y))
            self.tracker.update_position(pos)
