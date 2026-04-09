#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * JS Wrapper for Brain Cleaner (Python)
 */

function findPython() {
    const commands = ['python3', 'python'];
    const { execSync } = require('child_process');
    
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

const python = findPython();

if (!python) {
    console.error('\x1b[31mError: Python not found!\x1b[0m');
    console.error('Brain Cleaner requires Python 3.9 or higher to run.');
    console.error('Please install Python and try again: https://www.python.org/downloads/');
    process.exit(1);
}

// Path to the python entry point
const scriptPath = path.join(__dirname, '..', 'console', 'brain_cleaner_cli.py');

// Since we are running from NPM, we might need to ensure dependencies are installed
// For now, we just pass the arguments to the python script
const args = process.argv.slice(2);
const pythonProcess = spawn(python, [scriptPath, ...args], {
    stdio: 'inherit',
    env: { ...process.env, PYTHONPATH: path.join(__dirname, '..') }
});

pythonProcess.on('close', (code) => {
    process.exit(code);
});
