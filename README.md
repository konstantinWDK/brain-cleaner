# Brain Cleaner

**Language / Idioma:**
🇬🇧 English &nbsp;|&nbsp; [🇪🇸 Español](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.es.md)

---

---

## Why Brain Cleaner?

In the modern development era, our systems are constantly cluttered with "digital noise." Every interaction with AI assistants (Gemini, Claude, Cursor), every NPM project, and every Python experiment leaves behind a trail of logs, cache, and heavy virtual environments that quickly eat up hundreds of gigabytes of disk space.

**Brain Cleaner was built to solve this.** It provides a professional, high-performance interface to reclaim your disk space by targeting precisely those development residues that standard cleaners miss.

---

## 🚀 Key Features

- **AI Residue Cleaner** — Deep scan for cache, logs, and configs from Gemini, Claude, Cursor, Windsurf, Trae, and more.
- **NPM Optimization** — Instantly find and safely delete heavy `node_modules` folders from forgotten projects.
- **Python Env Manager** — Detect obsolete virtual environments (`venv`, `.venv`) that haven't been touched in over 90 days.
- **Hybrid Power** — The ease of an NPM global install with the high-performance scanning engine of Python.
- **Interactive UI** — Choice between a sleek Desktop GUI or a professional Command Line Interface (CLI).

---

## ⚙️ Installation

Install globally via NPM to start cleaning immediately:

```bash
npm install -g brain-cleaner
```

### Requirements
- **Python 3.9+** (Required for the scanning engine).
- **Node.js 14+**.

---

## 📖 How to Use

### 1. Launch the Interface
Simply run the command from any terminal:
```bash
brain-cleaner
```

### 2. Choose Your Scope
Select between scanning your **Home** directory, the **Full System**, or a **Custom Folder** in the sidebar.

### 3. Select Mode & Scan
- **AI Tools**: For logs and cache from AI assistants.
- **NPM Modules**: For heavy `node_modules`.
- **Python Envs**: For identifying abandoned virtual environments.

### 4. Review & Clean
Expand entries to review subfolders, check individual items, and click **Clean Selected** or **Clean All**.

---

## 🛠 Technical Details

While distributed via NPM, Brain Cleaner is a hybrid tool. The Node.js wrapper automatically:
1. Detects your local Python environment.
2. Auto-installs core dependencies (`customtkinter`, `blessed`, `Pillow`) on the first run.
3. Securely executes the cross-platform cleaning engine.

---

## ⚠️ Safety First

> [!WARNING]
> Deletion is **permanent**. Brain Cleaner does not move files to the trash; it deletes them to reclaim space immediately. Always review the scan results before confirming cleanup.

---

## 📄 License

MIT — *Developed to keep your development system lean and focused.*
