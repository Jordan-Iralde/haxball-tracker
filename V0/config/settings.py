# config/settings.py

config = {
    "player_name": "Jordan",
    "team": "red",  # o "blue"

    "field_size": (900, 450),  # Ancho x Alto en pixeles

    "key_bindings": {
        "start_tracking":    {"key": "F5", "label": "Iniciar Tracking",  "editable": True},
        "stop_tracking":     {"key": "F6", "label": "Detener Tracking",  "editable": True},
        "log_touch":         {"key": ";",  "label": "Toque Balón",       "editable": True},
        "log_goal":          {"key": "G",  "label": "Gol Propio",        "editable": True},
        "log_assist":        {"key": "A",  "label": "Asistencia",        "editable": True},
        "log_error":         {"key": "E",  "label": "Error Propio",      "editable": True},
        "increase_opacity":  {"key": "+",  "label": "Subir Opacidad",    "editable": False},
        "decrease_opacity":  {"key": "-",  "label": "Bajar Opacidad",    "editable": False},
        "toggle_heatmap":    {"key": "H",  "label": "Mostrar Heatmap",   "editable": False}
    },

    "colors": {
        "background": "#202020",
        "trace_line": "#00ffcc",
        "heatmap_color": "#ff0000",
        "player_dot": "#ffffff",
        "goal_dot": "#00ff00",
        "assist_dot": "#0000ff",
        "error_dot": "#ff9900"
    },

    "save_path": "records/",  # Carpeta donde guardar trazos
    "record_duration_limit": 8 * 60,  # 8 minutos máximo
    "opacity_step": 0.1,
}
