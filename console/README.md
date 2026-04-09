# Brain Cleaner Console (CLI)

Interactive terminal interface to find and remove residual files quickly and efficiently.

## Quick Start

You can run the interactive interface directly from this folder:

```bash
python3 brain-cleaner-cli.py
```

## Argument Options

Customize the scan using the following flags:

- `-d <path>`: Specifies the root directory to start the scan (default: Home).
- `-t <pattern>`: Search for specific directory names instead of the default ones.
- `--delete-all`: Automatically removes all detected items without confirmation.
- `--dry-run`: Simulates the process without actually deleting anything.
- `--sort <path|size>`: Sorts the results by file path or disk size.

## Interactive Controls

Once the interface is open, use the following keys:

- **Arrow Up/Down**: Navigate through the detected items.
- **Space / Delete**: Delete the currently selected item.
- **Q**: Quit the application and stop the scan.

---
*Developed for efficient and rapid system maintenance.*
