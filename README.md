# 🧠 Brain Cleaner

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

## 🇬🇧 English

**Brain Cleaner** is a desktop utility to find and remove residual files left by AI tools (Gemini, Claude, Cursor, Windsurf…) and heavy `node_modules` folders from your system.

### Installation

```bash
# 1. Install dependencies
python3.11 -m pip install -r requirements.txt

# 2. Run
python3.11 app.py
```

> [!TIP]
> On macOS, use the Homebrew Python to avoid GUI crashes: `brew install python@3.11`

### Usage

1. **Scope** — Choose `🏠 Home`, `💻 Full System` or `📁 Custom Folder` in the sidebar.
2. **Mode** — Toggle `🤖 AI Tools` and/or `📦 NPM Modules` to set what to scan.
3. **Scan** — Click `🚀 START SCAN`. Results appear in two labeled sections.
4. **Review** — Click `›` on any row to expand its subfolders. Check/uncheck individual items.
5. **Clean** — Use `✨ Clean Selected` for marked items or `🗑️ Clean All (Visible)` for everything in the current filter.

> [!WARNING]
> Deletion is **permanent**. There is no recycle bin. Review carefully before cleaning.

---

## 🇪🇸 Español

**Brain Cleaner** es una utilidad de escritorio para encontrar y eliminar archivos residuales dejados por herramientas de IA (Gemini, Claude, Cursor, Windsurf…) y carpetas `node_modules` pesadas.

### Instalación

```bash
# 1. Instalar dependencias
python3.11 -m pip install -r requirements.txt

# 2. Ejecutar
python3.11 app.py
```

> [!TIP]
> En macOS usa Python de Homebrew para evitar cierres inesperados: `brew install python@3.11`

### Uso

1. **Ubicación** — Elige `🏠 Home`, `💻 Full System` o `📁 Custom Folder` en la barra lateral.
2. **Modo** — Activa `🤖 AI Tools` y/o `📦 NPM Modules` según lo que quieras escanear.
3. **Escanear** — Pulsa `🚀 START SCAN`. Los resultados aparecen en dos secciones diferenciadas.
4. **Revisar** — Haz clic en `›` para desplegar el contenido de una carpeta. Puedes marcar o desmarcar elementos individuales.
5. **Limpiar** — Usa `✨ Clean Selected` para los marcados o `🗑️ Clean All (Visible)` para todo lo visible en el filtro activo.

> [!WARNING]
> La eliminación es **permanente**. No hay papelera de reciclaje. Revisa bien antes de limpiar.

---

## 🗂️ Detected Categories / Categorías Detectadas

| Category | Tools |
|---|---|
| **Gemini** | Google Gemini CLI / API cache |
| **Claude** | Anthropic Claude logs & config |
| **IDE Agents** | Cursor, Windsurf, Roo-Code, Claude-Dev |
| **Other Tools** | Uncategorized AI tools |
| **Node Modules** | `node_modules` in Node.js projects |

---

## ⚠️ License / Licencia

MIT — *Developed with ❤️ to keep your system free of digital noise.*
