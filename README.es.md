# Brain Cleaner

**Language / Idioma:**
[🇬🇧 English](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.md) &nbsp;|&nbsp; 🇪🇸 Español

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Plataforma macOS](https://img.shields.io/badge/plataforma-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

**Brain Cleaner** es una utilidad de escritorio para encontrar y eliminar archivos residuales dejados por herramientas de IA (Gemini, Claude, Cursor, Windsurf…) y carpetas `node_modules` pesadas.

## Características Principales

- Limpiador de IA — Detecta y elimina caché, logs y configuraciones de asistentes de IA.
- Revisor de NPM — Libera espacio en disco detectando y eliminando carpetas `node_modules` de proyectos web.
- Selección Granular — Árbol de archivos interactivo para revisar y excluir dependencias individuales antes de borrar.

## Inicio Rápido (Instalación y Ejecución)

### Instalación (Modo Consola)

Para instalar **Brain Cleaner** como un comando global en tu terminal:

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/konstantinwdk/brain-cleaner.git
   ```
2. **Navegar a la carpeta**:
   ```bash
   cd brain-cleaner
   ```
3. **Instalar el paquete**:
   ```bash
   pip install .
   ```

## Uso

Una vez instalado, puedes arrancar la **Consola Interactiva (CLI)** desde cualquier directorio:

```bash
brain-cleaner
```
*Consejo: Usa el CLI para una limpieza rápida gestionada totalmente por teclado.*

> [!TIP]
> En macOS usa Python de Homebrew para evitar cierres inesperados: `brew install python@3.11`

## Uso

1. **Ubicación** — Elige `Home`, `Full System` o `Custom Folder` en la barra lateral.
2. **Modo** — Elige entre `AI Tools` o `NPM Modules` según lo que quieras escanear.
3. **Escanear** — Pulsa `START SCAN`. Los resultados aparecen en dos secciones diferenciadas.
4. **Revisar** — Haz clic en `›` para desplegar el contenido de una carpeta. Puedes marcar o desmarcar elementos individuales.
5. **Limpiar** — Usa `Clean Selected` para los elementos marcados o `Clean All (Visible)` para todo lo visible en el filtro activo.

> [!WARNING]
> La eliminación es **permanente**. No hay papelera de reciclaje. Revisa bien antes de limpiar.

## Categorías Detectadas

| Categoría | Herramientas |
|---|---|
| **Gemini** | Caché de la CLI / API de Google Gemini |
| **Claude** | Logs y configuración de Anthropic Claude |
| **IDE Agents** | Cursor, Windsurf, Trae, Roo-Code, Claude-Dev |
| **Other Tools** | Herramientas de IA no categorizadas |
| **Node Modules** | Carpetas `node_modules` en proyectos Node.js |

## Licencia

MIT — *Desarrollado para mantener tu sistema libre de ruido digital.*
