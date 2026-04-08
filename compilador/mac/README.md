# 🍎 Compilación para macOS

Este directorio contiene las herramientas para generar el ejecutable de **Brain Cleaner** en macOS.

## Instrucciones

1. Abre la Terminal en esta carpeta.
2. Asegúrate de tener Python 3 instalado (recomendado via Homebrew).
3. Instala las dependencias:
   ```bash
   pip3 install customtkinter pyinstaller
   ```
4. Ejecuta el script de compilación:
   ```bash
   python3 build.py
   ```
5. La aplicación `.app` o el ejecutable se generará en la carpeta `dist/`.

---
*Nota: Este script utiliza el flag `--windowed` necesario para macOS.*
