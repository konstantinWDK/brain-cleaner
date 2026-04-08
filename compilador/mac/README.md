# 🍎 Compilación para macOS

Este directorio contiene las herramientas para generar el ejecutable de **Brain Cleaner** en macOS.

## Instrucciones

1. Abre la Terminal en esta carpeta.
2. Asegúrate de tener Python 3 instalado (recomendado via Homebrew).
3. Instala las dependencias:
   ```bash
   pip3 install -r ../../requirements.txt
   ```
4. Ejecuta el script de compilación:
   ```bash
   python3 build.py
   ```
5. La aplicación `.app` o el ejecutable se generará en la carpeta `dist/`.

---

## 🛠️ Post-Compilación e Instalación

Debido a las políticas de seguridad de macOS para aplicaciones no firmadas, sigue estos pasos para "instalar" y ejecutar tu app:

### 1. Permisos de Ejecución
Si el archivo en `dist/` no abre, dale permisos desde la terminal:
```bash
chmod +x dist/BrainCleaner_mac
```

### 2. Bypass de Gatekeeper (App no firmada)
Al abrirla por primera vez, macOS dirá que no puede verificar al desarrollador.
- **No hagas doble clic**.
- Haz **clic derecho** sobre el archivo y selecciona **Abrir**.
- En la ventana emergente, ahora aparecerá un botón de **Abrir**. (Solo tendrás que hacer esto la primera vez).

### 3. Instalación "Pro"
Para tenerla como una aplicación normal de macOS:
1. Mueve el archivo `BrainCleaner_mac` a tu carpeta `/Applications` (Aplicaciones).
2. Opcional: Cámbiale el nombre a simplemente `Brain Cleaner`.

---
*Nota: Este script utiliza el flag `--windowed` necesario para macOS.*

