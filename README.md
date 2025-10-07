# Fibonacci Studio

Aplicación de escritorio en Python que visualiza la serie de Fibonacci con una interfaz moderna construida sobre `tkinter` y `ttk`.

## Características

- Ajuste dinámico del número de términos mediante `Spinbox` y control deslizante.
- Tabla detallada con cada término y la razón respecto al anterior.
- Resumen con último valor, suma total y proporción dorada aproximada.
- Exportación de la serie a CSV y copia directa al portapapeles.
- Cálculos separados en un módulo reutilizable (`fibonacci.py`).

## Requisitos

- Python 3.10 o superior.

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/AdrianCuestaX/fibonacci-codex.git
   cd fibonacci-codex
   ```

2. (Opcional) Crea y activa un entorno virtual.

## Ejecución

```bash
python app.py
```

Se abrirá la ventana principal de Fibonacci Studio.

## Estructura del proyecto

- `app.py`: Punto de entrada de la aplicación.
- `fibonacci.py`: Funciones para generar la serie y obtener métricas.
- `ui/main_window.py`: Implementación de la interfaz gráfica.

## Pruebas rápidas

```bash
python -c "from fibonacci import generate_fibonacci; print(generate_fibonacci(10))"
```

## Capturas

Puedes añadir capturas de pantalla en una carpeta `docs/` y enlazarlas aquí si lo deseas.
