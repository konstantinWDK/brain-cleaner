import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuración para MACOS
PLATFORM = "mac"
APP_NAME = "BrainCleaner"
MAIN_FILE = os.path.join("..", "..", "app.py")

def get_python_interpreter():
    """Find the best python interpreter for building (preferring Homebrew/3.11)"""
    # Check for brew python 3.11 first as it handles macOS GUI better
    brew_python = "/opt/homebrew/bin/python3.11"
    if os.path.exists(brew_python):
        return brew_python
    return sys.executable

def get_customtkinter_path(python_exe):
    """Find customtkinter path using the selected interpreter"""
    cmd = [python_exe, "-c", "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"]
    try:
        result = subprocess.check_output(cmd, text=True).strip()
        return result
    except Exception:
        return None

def build():
    if not os.path.exists(MAIN_FILE):
        print(f" [!] No se encontró {MAIN_FILE}")
        return

    python_exe = get_python_interpreter()
    print(f" [*] Usando intérprete: {python_exe}")
    
    ctk_path = get_customtkinter_path(python_exe)
    if not ctk_path:
        print(" [!] No se pudo encontrar customtkinter. ¿Está instalado?")
        return
        
    separator = ":"
    
    # Flags profesionales para PyInstaller en macOS
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--noconfirm",         # No pedir confirmación
        "--clean",             # Limpiar cache antes de empezar
        "--windowed",          # Crear bundle .app (indispensable en macOS)
        "--onedir",            # Mejor rendimiento y requerido para .app en macOS
        f"--name={APP_NAME}",
        f"--add-data={ctk_path}{separator}customtkinter",
        "--collect-all", "customtkinter",
        "--collect-all", "darkdetect",
        "--osx-bundle-identifier", "com.braincleaner.app",
        "--noconsole",
        MAIN_FILE
    ]

    print(f" [*] Compilando para {PLATFORM.upper()}...")
    try:
        subprocess.check_call(cmd)
        print(f" [+] Hecho. Revisa la carpeta 'dist/{APP_NAME}.app'")
    except subprocess.CalledProcessError as e:
        print(f" [!] Error en la compilación: {e}")

if __name__ == "__main__":
    build()
