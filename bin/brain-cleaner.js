#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const path = require('path');

/**
 * Enhanced JS Wrapper for Brain Cleaner (Python)
 * Handles auto-installation of dependencies.
 */

function findPython() {
    const commands = ['python3', 'python', 'py'];
    for (const cmd of commands) {
        try {
            execSync(`${cmd} --version`, { stdio: 'ignore' });
            return cmd;
        } catch (e) {
            continue;
        }
    }
    return null;
}

function checkAndInstallDeps(python) {
    console.log('\x1b[36mFinalizing Brain Cleaner installation...\x1b[0m');
    const deps = ['blessed', 'Pillow'];
    
    for (const dep of deps) {
        try {
            // Check if dependency exists
            execSync(`${python} -c "import ${dep.toLowerCase()}"`, { stdio: 'ignore' });
        } catch (e) {
            console.log(`\x1b[33mDependency '${dep}' not found. Installing...\x1b[0m`);
            try {
                execSync(`${python} -m pip install ${dep}`, { stdio: 'inherit' });
            } catch (pipErr) {
                console.error(`\x1b[31mFailed to install '${dep}'. Please run 'pip install ${dep}' manually.\x1b[0m`);
            }
        }
    }
}

const python = findPython();

if (!python) {
    console.error('\x1b[31mError: Python not found!\x1b[0m');
    console.error('Brain Cleaner requires Python 3.9 or higher.');
    console.error('Please install Python: https://www.python.org/downloads/');
    process.exit(1);
}

// Ensure dependencies are present
checkAndInstallDeps(python);

// Path to the python entry point
const scriptPath = path.join(__dirname, '..', 'console', 'brain_cleaner_cli.py');
const args = process.argv.slice(2);

const pythonProcess = spawn(python, [scriptPath, ...args], {
    stdio: 'inherit',
    env: { ...process.env, PYTHONPATH: path.join(__dirname, '..') }
});

pythonProcess.on('close', (code) => {
    process.exit(code);
});
