# Windows Build

This directory contains tools to generate the Brain Cleaner executable for Windows.

## Instructions

1. Open a terminal (PowerShell or CMD) in this folder.
2. Ensure Python is installed and in your PATH.
3. Install dependencies:
   ```bash
   pip install -r ../../requirements.txt
   ```
4. Run the build script:
   ```bash
   python build.py
   ```
5. The .exe file will be generated in the dist/ folder.

---
*Note: The script automatically handles Windows path separators.*
