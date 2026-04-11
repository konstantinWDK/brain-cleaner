import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuración para WINDOWS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLATFORM = "windows"
APP_NAME = "BrainCleaner"
MAIN_FILE = os.path.join(BASE_DIR, "app.py")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
# En Windows usamos el archivo .ico generado
ICON_FILE = os.path.join(ASSETS_DIR, "icon.ico")

def get_python_interpreter():
    """Find the best python interpreter for building (Usually just 'python' or 'py' on Windows)"""
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
        
    # IMPORTANTE: Windows usa punto y coma (;) para separar rutas en --add-data
    separator = ";"
    
    # Flags para PyInstaller en Windows
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",           # En Windows se prefiere un único ejecutable .exe
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
        # En Windows, subprocess puede necesitar shell=True en algunos entornos
        subprocess.check_call(cmd, shell=(os.name == 'nt'))
        print(f" [+] Compilación terminada. El ejecutable está en 'dist/{APP_NAME}.exe'")
        
    except subprocess.CalledProcessError as e:
        print(f" [!] Error en la compilación: {e}")

if __name__ == "__main__":
    build()
