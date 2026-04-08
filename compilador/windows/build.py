import os
import sys
import subprocess
from pathlib import Path

# Configuración para WINDOWS
PLATFORM = "windows"
EXT = ".exe"

def get_customtkinter_path():
    import customtkinter
    return os.path.dirname(customtkinter.__file__)

def build():
    main_file = os.path.join("..", "..", "app.py")
    if not os.path.exists(main_file):
        print(f" [!] No se encontró {main_file}")
        return

    ctk_path = get_customtkinter_path()
    separator = ";" # Windows usa punto y coma
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name=BrainCleaner_{PLATFORM}",
        f"--add-data={ctk_path}{separator}customtkinter",
        main_file
    ]

    print(f" [*] Compilando para {PLATFORM.upper()}...")
    print(" [!] Nota: Debes ejecutar este script en una máquina Windows.")
    subprocess.check_call(cmd)
    print(f" [+] Hecho. Revisa la carpeta 'dist'")

if __name__ == "__main__":
    build()
