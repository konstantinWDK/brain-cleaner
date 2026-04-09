# macOS Build

This directory contains tools to generate the Brain Cleaner executable for macOS.

## Instructions

1. Open Terminal in this folder.
2. Ensure Python 3 is installed (recommended via Homebrew).
3. Install dependencies:
   ```bash
   pip3 install -r ../../requirements.txt
   ```
4. Run the build script:
   ```bash
   python3 build.py
   ```
5. The .app bundle or DMG installer will be generated in the dist/ folder.

---

## Post-Build & Installation

Due to macOS security policies for unsigned apps, follow these steps to install and run your app:

### 1. Execution Permissions
If the file in dist/ doesn't open, give it permissions from the terminal:
```bash
chmod +x dist/BrainCleaner-macOS.dmg
```

### 2. Bypass Gatekeeper (Unsigned App)
When opening for the first time, macOS will say it cannot verify the developer.
- **Do not double-click.**
- **Right-click** the file and select **Open**.
- In the popup, an **Open** button will now appear. (You only need to do this once).

### 3. Installation
To install as a normal macOS application:
1. Open the .dmg and drag the application to your Applications folder.

---
*Note: This script uses the --windowed flag required for macOS GUI apps.*
