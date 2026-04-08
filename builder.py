import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    print(" [!] PyInstaller no encontrado. Intentando instalar...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print(" [+] PyInstaller instalado con éxito.\n")
    except Exception as e:
        print(f" [!] Error al instalar PyInstaller: {e}")
        sys.exit(1)

def get_customtkinter_path():
    try:
        import customtkinter
        return os.path.dirname(customtkinter.__file__)
    except ImportError:
        print(" [!] CustomTkinter no encontrado. Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        import customtkinter
        return os.path.dirname(customtkinter.__file__)

def build():
    # 1. Verificar PyInstaller
    try:
        import PyInstaller
    except ImportError:
        install_pyinstaller()

    # 2. Identificar el archivo principal
    files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'builder.py']
    if not files:
        print(" [!] No se encontró ningún archivo .py para compilar.")
        return
    
    # Priorizar 'app.py' o 'main.py'
    main_file = 'app.py' if 'app.py' in files else ('main.py' if 'main.py' in files else files[0])
    app_name = Path(main_file).stem.replace('_', ' ').title().replace(' ', '')

    print(f" [*] Preparando compilación de: {main_file} -> {app_name}")

    # 3. Obtener ruta de CustomTkinter para los assets
    ctk_path = get_customtkinter_path()
    print(f" [*] Ruta de CustomTkinter: {ctk_path}")

    # 4. Configurar comando de PyInstaller
    # --noconsole: No mostrar terminal negra (para apps GUI)
    # --onefile: Un solo ejecutable
    # --add-data: Incluir temas y assets de CTK
    
    separator = ';' if sys.platform == 'win32' else ':'
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name={app_name}",
        f"--add-data={ctk_path}{separator}customtkinter",
        main_file
    ]

    print(f" [*] Ejecutando: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print(f"\n [+] ¡Compilación completada con éxito!")
        print(f" [+] El ejecutable se encuentra en la carpeta: {os.path.join(os.getcwd(), 'dist')}")
    except subprocess.CalledProcessError:
        print("\n [!] Error durante la compilación.")
    except Exception as e:
        print(f"\n [!] Ocurrió un error inesperado: {e}")

    # Limpiar archivos temporales (.spec y build/) si el usuario quiere
    # (Opcional, pero suele ser mejor dejarlos o borrarlos automáticamente)
    spec_file = f"{app_name}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
    # if os.path.exists('build'):
    #    shutil.rmtree('build')

if __name__ == "__main__":
    build()
