# 🧠 Brain Cleaner

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://en.wikipedia.org/wiki/Linux)

**Brain Cleaner** es una potente utilidad profesional diseñada para identificar y eliminar residuos persistentes de agentes de IA y registros "brain" que congestionan tu sistema y comprometen tu privacidad.

---

## ✨ Características Principales

- 🔍 **Escaneo Inteligente Multicapa**: Detecta carpetas y archivos de configuración de Gemini, Claude, Claude-Dev (Roo-Code), Cursor, Windsurf y más.
- 📦 **Limpieza de Dependencias**: Incluye soporte para detectar y eliminar pesadas carpetas `node_modules`.
- 🌓 **Interfaz Moderna e Intuitiva**: UI compacta construida con `CustomTkinter`, con soporte nativo para temas **Oscuro** y **Claro**.
- 📊 **Gestión por Categorías**: Los residuos se organizan en pestañas (Gemini, Claude, IDE Agents, Node Modules) para una revisión segura antes de borrar.
- ⚡ **Feedback en Tiempo Real**: Barra de progreso indeterminada y registro de actividad detallado para monitorear cada acción.
- 🛡️ **Limpieza Selectiva o Masiva**: Botones dedicados para borrar solo lo seleccionado o realizar una limpieza total de lo visible.

---

## 🛠️ Instalación y Requisitos

### Requisitos Previos
- Python 3.11 o superior instalado (Se recomienda **Homebrew** en macOS para evitar errores de compatibilidad con la interfaz gráfica).

### Clonar y Configurar
1. Instala las dependencias necesarias:
   ```bash
   python3.11 -m pip install -r requirements.txt
   ```

2. Ejecuta la aplicación:
   ```bash
   python3.11 app.py
   ```

> [!TIP]
> Si al intentar ejecutar con `python3` recibes un error de "abort", asegúrate de estar usando la versión de Homebrew (`brew install python@3.11`).

---

## 🚀 Cómo Usarlo

1. **Seleccionar Ubicación**: Elge el alcance del escaneo (Home, Sistema Completo, o una carpeta personalizada).
2. **Iniciar Escaneo**: Haz clic en `🚀 START SCAN` y espera a que la IA encuentre los residuos.
3. **Revisar y Seleccionar**: Navega por las categorías para ver cuánto espacio puedes recuperar.
4. **Limpiar**: Usa `Clean Selected` para elementos específicos o `Clean All` para vaciar la categoría actual.

---

## 🏗️ Compilación (Instaladores)

He preparado carpetas específicas para compilar la aplicación en cada plataforma. Solo tienes que ir a la carpeta correspondiente y ejecutar el script `build.py`:

- 🐧 **Linux**: `cd compilador/linux && python3 build.py`
- 🪟 **Windows**: `cd compilador/windows && python build.py`
- 🍎 **macOS**: `cd compilador/mac && python3 build.py`

Cada script generará un ejecutable único en la carpeta `dist/` dentro de su respectivo directorio, optimizado para esa plataforma.

> [!IMPORTANT]
> Debes ejecutar el script de cada carpeta **dentro de su sistema operativo nativo** para obtener el archivo de instalación correcto.

---


## 📸 Vista de la Aplicación

*(Próximamente: Añade aquí capturas de pantalla de la interfaz)*

---

## ⚠️ Aviso Legal (Safety First)

> [!WARNING]
> Esta herramienta elimina carpetas de forma permanente. **No hay papelera de reciclaje**. Por favor, revisa cuidadosamente la lista de elementos detectados antes de proceder con la limpieza. No nos hacemos responsables de pérdidas de datos accidentales por una selección incorrecta.

---

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulte `LICENSE` (próximamente) para obtener más información.

---
*Desarrollado con ❤️ para mantener tu sistema libre de ruido digital.*

