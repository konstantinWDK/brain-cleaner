#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Premium Post-install script for Brain Cleaner
 * Automatically handles Python dependency setup.
 */

const COLORS = {
    cyan: '\x1b[36m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    bold: '\x1b[1m',
    reset: '\x1b[0m'
};

function log(msg, color = COLORS.reset) {
    console.log(`${color}${msg}${COLORS.reset}`);
}

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

async function run() {
    log('\n── Brain Cleaner CLI Setup ──────────────────', COLORS.cyan + COLORS.bold);
    
    const python = findPython();
    if (!python) {
        log('⚠️  Python 3.9+ not found in your PATH.', COLORS.yellow);
        log('Brain Cleaner requires Python to run its core logic.');
        log('Please install it from https://python.org\n');
        process.exit(0); // Exit gracefully during install to not break npm flow
    }

    log(`Found ${COLORS.bold}${python}${COLORS.reset}. Installing dependencies...`, COLORS.cyan);

    const requirementsPath = path.join(__dirname, '..', 'requirements.txt');
    
    try {
        // Use -m pip to ensure we use the pip associated with the detected python
        execSync(`${python} -m pip install --upgrade pip`, { stdio: 'ignore' });
        execSync(`${python} -m pip install -r "${requirementsPath}"`, { stdio: 'inherit' });
        
        log('\n✅ Dependencies installed successfully!', COLORS.green + COLORS.bold);
        log('You can now run Brain Cleaner using: ' + COLORS.bold + 'brain-cleaner', COLORS.green);
        log('────────────────────────────────────────────\n', COLORS.cyan);
    } catch (error) {
        log('\n⚠️  Could not install dependencies automatically.', COLORS.yellow);
        log('This often happens due to permission restrictions.');
        log(`Please run manually: ${COLORS.bold}${python} -m pip install -r requirements.txt`, COLORS.reset);
        log('────────────────────────────────────────────\n', COLORS.cyan);
    }
}

run();
