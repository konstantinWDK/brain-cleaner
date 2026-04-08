# 🧠 Brain Cleaner - Guía de Compilación

Este documento contiene los comandos necesarios para compilar la aplicación en diferentes sistemas operativos.

---

## 🏗️ Comandos de Compilación

Para generar el ejecutable portable, entra en la carpeta correspondiente a tu sistema operativo y ejecuta el script:

### 🐧 Linux
```bash
cd compilador/linux && python3 build.py
```

### 🪟 Windows
```bash
cd compilador/windows && python build.py
```

### 🍎 macOS
```bash
cd compilador/mac && python3 build.py
```

---

## ℹ️ Información Importante

- **Salida**: El archivo ejecutable se generará en la carpeta `dist/` dentro de cada directorio de compilación.
- **Entorno**: Se recomienda ejecutar el comando **dentro del sistema operativo nativo** para asegurar la compatibilidad del binario.
- **Dependencias**: El script instalará automáticamente `PyInstaller` y sus dependencias si no están presentes.

---
*Manten tu sistema limpio y libre de residuos de IA.*

