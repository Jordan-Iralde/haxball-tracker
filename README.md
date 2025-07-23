haxtrack/
├── main.py                 # Haxball Tracker

Un tracker para Haxball que registra y visualiza el movimiento del jugador durante el juego.

## Características

- Detección en tiempo real de la posición del jugador
- Registro de eventos (toques, goles, asistencias, errores)
- Visualización de trayectoria en pantalla
- Grabación de video con la trayectoria
- Heatmap opcional
- Control de opacidad
- Interfaz gráfica intuitiva

## Teclas de Control

- F5: Iniciar tracking
- F6: Detener tracking
- ;: Registrar toque de balón
- G: Registrar gol propio
- A: Registrar asistencia
- E: Registrar error propio
- +: Aumentar opacidad
- -: Disminuir opacidad
- H: Mostrar/ocultar heatmap

## Requisitos

- Python 3.8+
- OpenCV
- NumPy
- Pygame
- Pillow
- Keyboard
- PyAutoGUI

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el tracker:
```bash
python haxball_tracker.py
```

## Uso

1. Inicia el juego de Haxball
2. Ejecuta el tracker
3. Presiona F5 para comenzar el tracking
4. Usa las teclas de control para registrar eventos
5. Presiona F6 para detener el tracking y guardar los datos

Los datos se guardarán en archivos JSON y la grabación en AVI.

├── config.py               # Carga y guarda teclas configuradas
├── keymap_config.py        # Interfaz para asignar teclas
├── tracker.py              # Registro de posición + eventos
├── heatmap.py              # Generación de mapa de calor y trazado
├── recorder.py             # Manejo de eventos, tiempo y trazado
├── utils.py                # Funciones auxiliares
├── maps/
│   └── juegantodos.json    # Datos del mapa y límites
├── data/
│   └── red_2025-07-24.json # Salida por partido
