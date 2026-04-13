# Brain Cleaner

**Language / Idioma:**
🇪🇸 Español &nbsp;|&nbsp; [🇬🇧 English](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.md)

---

### 🚀 Instalación Recomendada (Global)
Instala directamente desde NPM para obtener la última versión estable:

```bash
npm install -g brain-cleaner
```

#### Alternativa: Instalación desde el Código Fuente (Python)
Si prefieres instalar vía Python/Pip directamente desde el repositorio:

```bash
pip install git+https://github.com/konstantinwdk/brain-cleaner
```

---

### 🚀 Requisitos
- Se requiere **Python 3.9+**.
- **Node.js 14+** (si se instala por NPM).

---

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

### Instalación (Modo NPM)
Si prefieres usar NPM, puedes instalarlo globalmente:
```bash
npm install -g brain-cleaner
```
*Nota: Requiere tener Python 3.9+ instalado en el sistema.*

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
