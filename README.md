# Brain Cleaner

**Language / Idioma:**
🇬🇧 English &nbsp;|&nbsp; [🇪🇸 Español](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.es.md)

**Brain Cleaner** is a professional CLI utility designed to reclaim disk space by identifying and removing digital noise:
- **AI Residue Cleaner** — Finds cache, logs, and config files from Gemini, Claude, Cursor, Windsurf, and more.
- **NPM Optimization** — Detects and safely deletes heavy `node_modules` folders from your development projects.
- **Interactive UI** — High-performance terminal interface with granular selection and safety checks.

### 🚀 Recommended Installation (Global)
Install directly from NPM to get the latest stable version:

```bash
npm install -g brain-cleaner
```

#### Alternative: Install from Source (Python)
If you prefer to install via Python/Pip directly from the repository:

```bash
pip install git+https://github.com/konstantinwdk/brain-cleaner
```

### 🚀 Requirements
- **Python 3.9+** is required.
- **Node.js 14+** (if installing via NPM).

## Quick Start

   ```bash
   cd brain-cleaner
   ```
3. **Install the package**:
   ```bash
   pip install .
   ```

### Installation (NPM Mode)
If you are coming from the Node.js ecosystem, you can install it globally via NPM:
```bash
npm install -g brain-cleaner
```
*Note: Requires Python 3.9+ installed on your system.*

## Installation

To install this console interface as a global command:

1. Open your terminal in the root directory of the project.
2. Run:
   ```bash
   pip install .
   ```

## Quick Start

Once installed, you can run the interactive interface from anywhere:

```bash
brain-cleaner
```
*Tip: Use the CLI for fast, keyboard-driven system cleaning.*

> [!IMPORTANT]
> **macOS 26 (Tahoe) Compatibility**: Use Homebrew Python 3.11 or later to avoid "macOS 26 required" errors in GUI mode.
> ```bash
> brew install python@3.11 python-tk@3.11
> python3.11 -m venv .venv
> source .venv/bin/activate
> pip install .
> ```

## Usage

1. **Scope** — Choose `Home`, `Full System` or `Custom Folder` in the sidebar.
2. **Mode** — Choose between `AI Tools` or `NPM Modules` to set what to scan.
3. **Scan** — Click `START SCAN`. Results appear in two labeled sections.
4. **Review** — Click `›` on any row to expand its subfolders. Check/uncheck individual items.
5. **Clean** — Use `Clean Selected` for marked items or `Clean All (Visible)` for everything in the active filter.

> [!WARNING]
> Deletion is **permanent**. There is no recycle bin. Review carefully before cleaning.

## Detected Categories

| Category | Tools |
|---|---|
| **Gemini** | Google Gemini CLI / API cache |
| **Claude** | Anthropic Claude logs & config |
| **IDE Agents** | Cursor, Windsurf, Trae, Roo-Code, Claude-Dev |
| **Other Tools** | Uncategorized AI tools |
| **Node Modules** | `node_modules` in Node.js projects |

## License

MIT — *Developed to keep your system free of digital noise.*
