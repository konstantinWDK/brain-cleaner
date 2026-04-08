# 🧠 Brain Cleaner

**Language / Idioma:**
🇬🇧 English &nbsp;|&nbsp; [🇪🇸 Español](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.es.md)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

---

**Brain Cleaner** is a desktop utility to find and remove residual files left by AI tools (Gemini, Claude, Cursor, Windsurf…) and heavy `node_modules` folders from your system.

## Installation

```bash
# 1. Install dependencies
python3.11 -m pip install -r requirements.txt

# 2. Run
python3.11 app.py
```

> [!TIP]
> On macOS, use the Homebrew Python to avoid GUI crashes: `brew install python@3.11`

## Usage

1. **Scope** — Choose `🏠 Home`, `💻 Full System` or `📁 Custom Folder` in the sidebar.
2. **Mode** — Choose between `🤖 AI Tools` or `📦 NPM Modules` to set what to scan.
3. **Scan** — Click `🚀 START SCAN`. Results appear in two labeled sections.
4. **Review** — Click `›` on any row to expand its subfolders. Check/uncheck individual items.
5. **Clean** — Use `✨ Clean Selected` for marked items or `🗑️ Clean All (Visible)` for everything in the active filter.

> [!WARNING]
> Deletion is **permanent**. There is no recycle bin. Review carefully before cleaning.

## Detected Categories

| Category | Tools |
|---|---|
| **Gemini** | Google Gemini CLI / API cache |
| **Claude** | Anthropic Claude logs & config |
| **IDE Agents** | Cursor, Windsurf, Roo-Code, Claude-Dev |
| **Other Tools** | Uncategorized AI tools |
| **Node Modules** | `node_modules` in Node.js projects |

## License

MIT — *Developed with ❤️ to keep your system free of digital noise.*
