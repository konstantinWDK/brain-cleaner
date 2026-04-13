#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const path = require('path');

/**
 * Robust JS Wrapper for Brain Cleaner (Python)
 * Focuses on execution and clear error reporting.
 */

const COLORS = {
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  reset: '\x1b[0m'
};

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

const python = findPython();

if (!python) {
  console.error(`\n${COLORS.red}${COLORS.bold}Error: Python not found!${COLORS.reset}`);
  console.error(`${COLORS.yellow}Brain Cleaner requires Python 3.9 or higher to operate.${COLORS.reset}`);
  console.error(`Please install Python: ${COLORS.cyan}https://www.python.org/downloads/${COLORS.reset}\n`);
  process.exit(1);
}

// Path to the python entry point
const scriptPath = path.join(__dirname, '..', 'console', 'brain_cleaner_cli.py');
const args = process.argv.slice(2);

const pythonProcess = spawn(python, [scriptPath, ...args], {
  stdio: 'inherit',
  env: { 
    ...process.env, 
    PYTHONPATH: path.join(__dirname, '..'),
    PYTHONIOENCODING: 'utf-8' // Ensure rich terminal output works well
  }
});

pythonProcess.on('error', (err) => {
  console.error(`\n${COLORS.red}Failed to start Brain Cleaner:${COLORS.reset}`, err.message);
  process.exit(1);
});

pythonProcess.on('close', (code) => {
  if (code !== 0 && code !== null) {
    console.log(`\n${COLORS.yellow}Note: If you see "ModuleNotFoundError", please run:${COLORS.reset}`);
    console.log(`${COLORS.bold}npm install${COLORS.reset} again to finalize the setup.\n`);
  }
  process.exit(code);
});
