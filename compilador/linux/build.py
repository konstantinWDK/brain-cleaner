import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuración para LINUX
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLATFORM = "linux"
APP_NAME = "BrainCleaner"
MAIN_FILE = os.path.join(BASE_DIR, "app.py")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_FILE = os.path.join(ASSETS_DIR, "icon.png")

def get_python_interpreter():
    """Find the best python interpreter for building"""
    return sys.executable

def get_customtkinter_path(python_exe):
    """Find customtkinter path using the selected interpreter"""
    cmd = [python_exe, "-c", "import customtkinter, os; print(os.path.dirname(customtkinter.__file__))"]
    try:
        result = subprocess.check_output(cmd, text=True).strip()
        return result
    except Exception:
        return None

def check_tkinter(python_exe):
    """Check if tkinter is available (Essential for CustomTkinter on Linux)"""
    try:
        subprocess.check_call([python_exe, "-c", "import tkinter"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def build():
    if not os.path.exists(MAIN_FILE):
        print(f" [!] No se encontró {MAIN_FILE}")
        return

    python_exe = get_python_interpreter()
    print(f" [*] Usando intérprete: {python_exe}")
    
    if not check_tkinter(python_exe):
        print(" [!] ERROR: tkinter no está instalado en este Python.")
        print("     Sugerencia: Ejecuta 'sudo apt install python3-tk' (o el equivalente en tu distro).")
        return
    
    ctk_path = get_customtkinter_path(python_exe)
    if not ctk_path:
        print(" [!] No se pudo encontrar customtkinter. ¿Está instalado?")
        return
        
    separator = ":"
    
    # Flags para PyInstaller en Linux
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        f"--name={APP_NAME}",
        f"--add-data={ctk_path}{separator}customtkinter",
        f"--add-data={ASSETS_DIR}{separator}assets",
        f"--icon={ICON_FILE}",
        "--collect-all", "customtkinter",
        "--collect-all", "darkdetect",
        "--noconsole",
        MAIN_FILE
    ]

    print(f" [*] Compilando para {PLATFORM.upper()}...")
    try:
        subprocess.check_call(cmd)
        print(f" [+] Compilación terminada. El binario está en 'dist/{APP_NAME}'")
        print(f" [🚀] Sugerencia: Puedes empaquetarlo como AppImage si lo deseas.")
        
    except subprocess.CalledProcessError as e:
        print(f" [!] Error en la compilación: {e}")

if __name__ == "__main__":
    build()
