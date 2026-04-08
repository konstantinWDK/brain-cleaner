# 🪟 Compilación para Windows

Este directorio contiene las herramientas para generar el ejecutable de **Brain Cleaner** en Windows.

## Instrucciones

1. Abre una terminal (PowerShell o CMD) en esta carpeta.
2. Asegúrate de tener Python instalado y en el PATH.
3. Instala las dependencias:
   ```bash
   pip install customtkinter pyinstaller
   ```
4. Ejecuta el script de compilación:
   ```bash
   python build.py
   ```
5. El archivo `.exe` se generará en la carpeta `dist/`.

---
*Nota: El script maneja automáticamente los separadores de ruta de Windows.*
