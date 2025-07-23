import cv2
import numpy as np
import keyboard
import pyautogui
import time
import math
import json
from datetime import datetime

class HaxballTracker:
    def __init__(self, min_dist=5):
        self.tracking = False
        self.positions = []
        self.events = []
        self.opacity = 0.5
        self.show_heatmap = False
        self.min_dist = min_dist
        self.screen_width, self.screen_height = pyautogui.size()
        self.player_pos = None
        self.player_speed = 5  # Velocidad de movimiento
        self.game_window = None  # Para mantener la referencia a la ventana del juego
        self.key_bindings = {
            "start_tracking": {"key": "F5", "label": "Iniciar Tracking"},
            "stop_tracking": {"key": "F6", "label": "Detener Tracking"},
            "log_touch": {"key": ";", "label": "Toque Balón"},
            "log_goal": {"key": "G", "label": "Gol Propio"},
            "log_assist": {"key": "A", "label": "Asistencia"},
            "log_error": {"key": "E", "label": "Error Propio"},
            "increase_opacity": {"key": "+", "label": "Subir Opacidad"},
            "decrease_opacity": {"key": "-", "label": "Bajar Opacidad"},
            "toggle_heatmap": {"key": "H", "label": "Mostrar Heatmap"},
        }
        self.setup_key_bindings()
        
        # Crear una imagen de fondo semitransparente
        self.background = np.zeros((self.screen_height, self.screen_width, 3), dtype=np.uint8)
        self.setup_key_bindings()

    def setup_key_bindings(self):
        kb = keyboard.add_hotkey
        kb(self.key_bindings["start_tracking"]["key"], self.start_tracking)
        kb(self.key_bindings["stop_tracking"]["key"], self.stop_tracking)
        kb(self.key_bindings["log_touch"]["key"], self.log_event, args=("touch",))
        kb(self.key_bindings["log_goal"]["key"], self.log_event, args=("goal",))
        kb(self.key_bindings["log_assist"]["key"], self.log_event, args=("assist",))
        kb(self.key_bindings["log_error"]["key"], self.log_event, args=("error",))
        kb(self.key_bindings["increase_opacity"]["key"], self.increase_opacity)
        kb(self.key_bindings["decrease_opacity"]["key"], self.decrease_opacity)
        kb(self.key_bindings["toggle_heatmap"]["key"], self.toggle_heatmap)
        
        # Configurar teclas TGHF para movimiento
        keyboard.on_press_key('t', lambda e: self.move_player(0, -self.player_speed))
        keyboard.on_press_key('g', lambda e: self.move_player(0, self.player_speed))
        keyboard.on_press_key('f', lambda e: self.move_player(-self.player_speed, 0))
        keyboard.on_press_key('h', lambda e: self.move_player(self.player_speed, 0))
        
        # Configurar teclas para dejar de mover
        keyboard.on_release_key('t', lambda e: self.stop_moving())
        keyboard.on_release_key('g', lambda e: self.stop_moving())
        keyboard.on_release_key('f', lambda e: self.stop_moving())
        keyboard.on_release_key('h', lambda e: self.stop_moving())
        keyboard.on_release_key('a', lambda e: self.stop_moving())
        keyboard.on_release_key('d', lambda e: self.stop_moving())

    def start_tracking(self):
        self.tracking = True
        self.positions.clear()
        self.events.clear()
        print("Iniciando tracking...")
        # Establecer posición inicial del jugador
        x, y = pyautogui.position()
        self.player_pos = {"x": x, "y": y}
        print(f"Posición inicial: {self.player_pos}")

    def stop_tracking(self):
        self.tracking = False
        print("Deteniendo tracking...")
        self.save_tracking_data()

    def log_event(self, event_type):
        if not self.tracking:
            return
        x, y = pyautogui.position()
        self.events.append({"type": event_type, "timestamp": time.time(), "position": {"x": x, "y": y}})
        print(f"Evento {event_type} en ({x},{y})")

    def move_player(self, dx, dy):
        if not self.tracking or self.player_pos is None:
            return
            
        # Actualizar posición del jugador
        self.player_pos["x"] = int(self.player_pos["x"] + dx)
        self.player_pos["y"] = int(self.player_pos["y"] + dy)
        
        # Asegurarse de que la posición esté dentro de los límites de la pantalla
        self.player_pos["x"] = max(0, min(self.screen_width - 1, self.player_pos["x"]))
        self.player_pos["y"] = max(0, min(self.screen_height - 1, self.player_pos["y"]))
        
        # Actualizar posición
        self.update_position(self.player_pos["x"], self.player_pos["y"])
        
    def stop_moving(self):
        # No hace nada, solo para mantener la consistencia
        pass

    def update_position(self, x, y):
        if not self.tracking:
            return
            
        if self.positions:
            last = self.positions[-1]
            dist = math.hypot(x - last["x"], y - last["y"])
            if dist < self.min_dist:
                return  # Ignorar posiciones muy cercanas para evitar saturación
                
        self.positions.append({"x": x, "y": y, "timestamp": time.time()})

    def increase_opacity(self):
        self.opacity = min(1.0, self.opacity + 0.1)
        print(f"Opacidad ajustada a: {self.opacity:.1f}")

    def decrease_opacity(self):
        self.opacity = max(0.1, self.opacity - 0.1)
        print(f"Opacidad ajustada a: {self.opacity:.1f}")

    def toggle_heatmap(self):
        self.show_heatmap = not self.show_heatmap
        print(f"Heatmap {'activado' if self.show_heatmap else 'desactivado'}")

    def save_tracking_data(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {"positions": self.positions, "events": self.events, "metadata": {"screen_width": self.screen_width, "screen_height": self.screen_height, "timestamp": ts}}
        with open(f"tracking_data_{ts}.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"Datos guardados en tracking_data_{ts}.json")

def main():
    tracker = HaxballTracker(min_dist=5)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Cambiar a MP4 para mejor compatibilidad
    out = cv2.VideoWriter(f"haxball_{datetime.now():%Y%m%d_%H%M%S}.mp4", fourcc, 20.0, (1280, 720))
    cv2.namedWindow('Haxball Tracker', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    
    # Configurar ventana superpuesta
    cv2.moveWindow('Haxball Tracker', 0, 0)  # Mover a la esquina superior izquierda
    cv2.resizeWindow('Haxball Tracker', tracker.screen_width, tracker.screen_height)
    cv2.setWindowProperty('Haxball Tracker', cv2.WND_PROP_TOPMOST, 1)  # Mantener siempre al frente
    cv2.setWindowProperty('Haxball Tracker', cv2.WND_PROP_AUTOSIZE, 1)  # Ajustar tamaño automáticamente

    while True:
        if keyboard.is_pressed('esc'):
            break

        if tracker.tracking:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Dibujo líneas azul->rojo entre posiciones
            overlay = tracker.background.copy()
            for i in range(1, len(tracker.positions)):
                start, end = tracker.positions[i-1], tracker.positions[i]
                t = i / len(tracker.positions)
                color = (int(255*t), 0, int(255*(1-t)))
                cv2.line(overlay, (start["x"], start["y"]), (end["x"], end["y"]), color, 2)

            # Dibujo eventos como círculos con colores
            for e in tracker.events:
                pos = e["position"]
                color = {"touch": (0,255,255), "goal": (0,255,0), "assist": (255,255,0), "error": (0,0,255)}.get(e["type"], (255,255,255))
                cv2.circle(overlay, (pos["x"], pos["y"]), 8, color, -1)

            # Dibujar heatmap si está activado
            if tracker.show_heatmap:
                for p in tracker.positions:
                    cv2.circle(overlay, (p["x"], p["y"]), 10, (0,0,255), -1)

            # Aplicar transparencia al overlay
            alpha = tracker.opacity
            frame = cv2.addWeighted(frame, 1-alpha, overlay, alpha, 0)

            # Heatmap transparente
            if tracker.show_heatmap:
                overlay = frame.copy()
                for p in tracker.positions:
                    cv2.circle(overlay, (p["x"], p["y"]), 10, (0,0,255), -1)
                frame = cv2.addWeighted(frame, 1-tracker.opacity, overlay, tracker.opacity, 0)

            # Leyendas abajo a la izquierda
            y0 = tracker.screen_height - 140
            cv2.putText(frame, "Toque (;): Amarillo", (20, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, "Gol (G): Verde", (20, y0+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, "Asist. (A): Celeste", (20, y0+50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
            cv2.putText(frame, "Error (E): Rojo", (20, y0+75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

            out.write(frame)
            disp = cv2.resize(frame, (1280, 720))  # escalado para ventana más chica
            cv2.imshow('Haxball Tracker', disp)
            cv2.waitKey(1)

            # No actualizar posición con el mouse cuando estamos usando WASD
            pass

    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
