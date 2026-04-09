# Brain Cleaner Console (CLI)

Interactive terminal interface to find and remove residual files quickly and efficiently.

## Installation

To install this console interface as a global command:

1. Open your terminal in the root directory of the project.
2. Run:
   ```bash
   pip install .
   ```

## Quick Start

Once installed, you can launch the **Interactive Console (CLI)** from any directory:

```bash
brain-cleaner
```

## Argument Options

Customize the scan using the following flags:

- `-d <path>`: Specifies the root directory (default: Home).
- `-t <pattern>`: Search for specific directory names instead of defaults.
- `--delete-all`: Automatically removes detected items (use with caution).
- `--dry-run`: Simulates the process without deletion.
- `--sort <path|size>`: Sorts results.

## Interactive Controls

- **Arrow Up/Down**: Navigate.
- **m**: Mark/Unmark an item.
- **a**: Select/Deselect all visible items.
- **Space / Enter**: Delete selected items (with confirmation).
- **b**: Go back to the mode menu.
- **q**: Quit.

---
*Developed for efficient and rapid system maintenance.*
