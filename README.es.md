# Brain Cleaner

[![NPM Version](https://img.shields.io/npm/v/brain-cleaner.svg)](https://www.npmjs.com/package/brain-cleaner)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

**Language / Idioma:**
🇪🇸 Español &nbsp;|&nbsp; [🇬🇧 English](https://github.com/konstantinWDK/brain-cleaner/blob/main/README.md)

![Brain Cleaner Demostración de Interfaz](./assets/ui-demo.png)

---

## ¿Por qué Brain Cleaner?

En la era del desarrollo moderno, nuestros sistemas se llenan constantemente de "ruido digital". Cada interacción con asistentes de IA (Gemini, Claude, Cursor), cada proyecto NPM y cada experimento en Python dejan un rastro de registros, caché y entornos virtuales pesados que rápidamente consumen cientos de gigabytes de espacio en disco.

**Brain Cleaner nació para solucionar esto.** Ofrece una interfaz profesional de alto rendimiento para recuperar espacio en disco, atacando precisamente esos residuos de desarrollo que los limpiadores estándar pasan por alto.

---

## 🚀 Características Principales

- **Limpiador de Residuos de IA** — Escaneo profundo de caché, logs y configuraciones de Gemini, Claude, Cursor, Windsurf, Trae y más.
- **Optimización NPM** — Encuentra y elimina de forma segura carpetas `node_modules` pesadas de proyectos olvidados.
- **Gestión de Entornos Python** — Detecta entornos virtuales obsoletos (`venv`, `.venv`) que no se han tocado en más de 90 días.
- **Potencia Híbrida** — La facilidad de una instalación global de NPM con el motor de escaneo de alto rendimiento de Python.
- **Interfaz Interactiva** — Elige entre una elegante GUI de escritorio o una interfaz de línea de comandos (CLI) profesional.

---

## ⚙️ Instalación

Instala globalmente a través de NPM para empezar a limpiar inmediatamente:

```bash
npm install -g brain-cleaner
```

### Requisitos
- **Python 3.9+** (Requerido para el motor de escaneo).
- **Node.js 14+**.

---

## 📖 Cómo Usar

### 1. Iniciar la Interfaz
Simplemente ejecuta el comando desde cualquier terminal:
```bash
brain-cleaner
```

### 2. Elige el Alcance
Selecciona en la barra lateral entre escanear tu directorio **Home**, el **Sistema Completo** o una **Carpeta Personalizada**.

### 3. Selecciona Modo y Escanea
- **AI Tools**: Para logs y caché de asistentes de IA.
- **NPM Modules**: Para carpetas `node_modules` pesadas.
- **Python Envs**: Para identificar entornos virtuales abandonados.

### 4. Revisa y Limpia
Despliega las entradas para revisar las subcarpetas, marca elementos individuales y haz clic en **Clean Selected** o **Clean All**.

---

## 🛠 Detalles Técnicos

Aunque se distribuye a través de NPM, Brain Cleaner es una herramienta híbrida. El wrapper de Node.js automáticamente:
1. Detecta tu entorno local de Python.
2. Auto-instala las dependencias principales (`customtkinter`, `blessed`, `Pillow`) en la primera ejecución.
3. Ejecuta de forma segura el motor de limpieza multiplataforma.

---

## ⚠️ Seguridad Primero

> [!WARNING]
> La eliminación es **permanente**. Brain Cleaner no mueve archivos a la papelera; los elimina para recuperar espacio inmediatamente. Siempre revisa los resultados del escaneo antes de confirmar la limpieza.

---

## 📄 Licencia

MIT — *Desarrollado para mantener tu sistema de desarrollo ligero y enfocado.*
