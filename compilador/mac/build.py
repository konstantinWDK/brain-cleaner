import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuración para MACOS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLATFORM = "mac"
APP_NAME = "BrainCleaner"
MAIN_FILE = os.path.join(BASE_DIR, "app.py")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_FILE = os.path.join(ASSETS_DIR, "icon.png")

def get_python_interpreter():
    """Find the best python interpreter for building (preferring .venv_gui/3.11)"""
    # Check for our GUI environment first
    venv_gui_python = os.path.join(BASE_DIR, ".venv_gui", "bin", "python3")
    if os.path.exists(venv_gui_python):
        return venv_gui_python
    
    # Fallback to brew python 3.11
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
        f"--add-data={ASSETS_DIR}{separator}assets",
        f"--icon={ICON_FILE}",
        "--collect-all", "customtkinter",
        "--collect-all", "darkdetect",
        "--osx-bundle-identifier", "com.braincleaner.app",
        "--noconsole",
        MAIN_FILE
    ]

    print(f" [*] Compilando para {PLATFORM.upper()}...")
    try:
        subprocess.check_call(cmd)
        print(f" [+] Compilación terminada. Creando DMG con instalador arrastrable...")
        
        dmg_root = "dist/dmg_builder"
        if os.path.exists(dmg_root):
            shutil.rmtree(dmg_root)
        os.makedirs(dmg_root)
        
        # Copiar app y crear enlace a Applications
        app_path = f"dist/{APP_NAME}.app"
        shutil.copytree(app_path, f"{dmg_root}/{APP_NAME}.app")
        os.symlink("/Applications", f"{dmg_root}/Applications")
        
        # Construir DMG
        dmg_path = f"dist/{APP_NAME}-macOS.dmg"
        if os.path.exists(dmg_path):
            os.remove(dmg_path)
            
        hdiutil_cmd = [
            "hdiutil", "create", "-volname", f"{APP_NAME} Installer", 
            "-srcfolder", dmg_root, "-ov", "-format", "UDZO", dmg_path
        ]
        
        # Silenciar la salida de hdiutil para mantener la terminal limpia
        subprocess.check_output(hdiutil_cmd)
        
        # Limpiar temporal
        shutil.rmtree(dmg_root)
        
        print(f" [🚀] ÉXITO: Instalador generado correctamente en '{dmg_path}'")
        
    except subprocess.CalledProcessError as e:
        print(f" [!] Error en la compilación: {e}")

if __name__ == "__main__":
    build()
