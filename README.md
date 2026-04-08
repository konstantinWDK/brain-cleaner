# 🧠 Brain Cleaner

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet.svg)](https://github.com/TomSchimansky/CustomTkinter)

**Brain Cleaner** es una utilidad profesional diseñada para identificar y eliminar residuos persistentes de herramientas de IA y dependencias de proyectos que congestionan tu sistema. Interfaz moderna con escaneo en dos modos independientes: **AI Tools** y **NPM Modules**.

---

## ✨ Características Principales

| Característica | Descripción |
|---|---|
| 🤖 **Modo AI Tools** | Detecta residuos de Gemini, Claude, IDE Agents (Cursor, Windsurf, Roo-Code) y otras herramientas de IA |
| 📦 **Modo NPM Modules** | Detecta y elimina carpetas `node_modules` pesadas en proyectos de Node.js |
| 📂 **Árbol Expandible** | Despliega el contenido de cada carpeta detectada directamente en la lista para revisar y deseleccionar archivos individuales |
| ✅ **Selección en Cascada** | Al marcar la carpeta padre, todos los hijos se seleccionan automáticamente; cada hijo puede excluirse individualmente |
| 🔍 **Filtros Dinámicos** | Filtra resultados por categoría (Gemini, Claude, Node Modules…) con burbujas de navegación |
| ☑️ **Seleccionar Todo / Ninguno** | Botones para marcar o desmarcar todos los elementos visibles en el filtro activo |
| 📊 **Secciones Separadas** | Los resultados se renderizan en dos bloques diferenciados: AI Tools (azul) y NPM Modules (verde) |
| ⚡ **Barra de Progreso** | Indicador visual animado durante el escaneo con información de la ruta que se analiza |
| 🛡️ **Limpieza Selectiva o Masiva** | `Clean Selected` para elementos específicos o `Clean All (Visible)` para limpiar el filtro activo |
| 🌓 **Temas Oscuro / Claro / Sistema** | Selector de apariencia integrado en la barra lateral |
| 📋 **Log de Actividad** | Panel de texto ocultable que registra cada acción en tiempo real |

---

## 🛠️ Instalación y Requisitos

### Requisitos Previos
- **Python 3.11+** — Se recomienda la versión de Homebrew en macOS:
  ```bash
  brew install python@3.11
  ```

### Instalar dependencias
```bash
python3.11 -m pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python3.11 app.py
```

> [!TIP]
> Si recibes un error `Abort trap: 6` al ejecutar con `python3` del sistema, asegúrate de usar la versión de Homebrew (`/opt/homebrew/bin/python3.11`).

---

## 🚀 Cómo Usarlo

### 1. Configurar el escaneo
- **Scan Scope** (barra lateral): Elige entre `🏠 Home`, `💻 Full System` o `📁 Custom Folder`.
- **Scan Mode**: Activa o desactiva los modos:
  - ✅ **🤖 AI Tools** — Residuos de herramientas de inteligencia artificial
  - ✅ **📦 NPM Modules** — Carpetas `node_modules` de proyectos web

### 2. Ejecutar el escaneo
- Pulsa `🚀 START SCAN`. La barra de progreso se activará mientras analiza el sistema.
- Pulsa `🛑 STOP` en cualquier momento para interrumpir el escaneo.

### 3. Revisar los resultados
- Los resultados aparecen en **dos secciones** diferenciadas:
  - 🔵 **AI Tools** — Archivos de configuración, caché y datos de agentes de IA
  - 🟢 **NPM Modules** — Carpetas de dependencias de Node.js
- Usa los **filtros de burbuja** en la barra superior para filtrar por herramienta.
- Haz clic en `›` para **desplegar el contenido** de una carpeta y revisar sus archivos individuales.
- Usa **☑ All / ☐ None** para seleccionar o deseleccionar todos los elementos visibles.

### 4. Limpiar
- `✨ Clean Selected` → Elimina solo los elementos marcados (respeta la selección individual de subcarpetas).
- `🗑️ Clean All (Visible)` → Elimina todos los elementos del filtro activo.

> [!WARNING]
> La eliminación es **permanente** — no hay papelera de reciclaje. Revisa detenidamente la lista antes de limpiar.

---

## 🏗️ Estructura del Proyecto

```
brain-cleaner/
├── app.py          # Interfaz gráfica principal (CustomTkinter)
├── scanner.py      # Lógica de escaneo y detección de residuos
├── requirements.txt
├── compilador/
│   ├── linux/      # Script de compilación para Linux
│   ├── mac/        # Script de compilación para macOS
│   └── windows/    # Script de compilación para Windows
└── README.md
```

---

## 🏗️ Compilación (Instaladores)

Genera un ejecutable nativo para cada plataforma desde su respectivo directorio:

- 🐧 **Linux**: `cd compilador/linux && python3 build.py`
- 🪟 **Windows**: `cd compilador/windows && python build.py`
- 🍎 **macOS**: `cd compilador/mac && python3 build.py`

> [!IMPORTANT]
> Ejecuta cada script **dentro del sistema operativo de destino** para obtener el binario correcto.

---

## 🗂️ Categorías Detectadas

| Categoría | Herramientas / Rutas |
|---|---|
| **Gemini** | `.gemini/`, configuración de la CLI/API de Google Gemini |
| **Claude** | `.claude/`, logs de API de Anthropic |
| **IDE Agents** | Cursor, Windsurf, Roo-Code / Claude-Dev y sus cachés |
| **Other Tools** | Otras herramientas de IA no categorizadas |
| **Node Modules** | Carpetas `node_modules` en proyectos de Node.js |

---

## ⚠️ Aviso Legal

> [!CAUTION]
> Esta herramienta elimina carpetas de forma **permanente e irreversible**. Asegúrate de revisar los elementos detectados antes de proceder. Los autores no se hacen responsables de pérdidas de datos por una selección incorrecta.

---

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulta `LICENSE` para más información.

---
*Desarrollado con ❤️ para mantener tu sistema libre de ruido digital.*
