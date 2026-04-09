import os
import sys
import threading
import argparse
import time
from blessed import Terminal
from pathlib import Path

# Add parent directory to sys.path to import scanner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scanner import BrainScanner

ASCII_ART = r"""
  ____  ____      _    ___ _   _ 
 | __ )|  _ \    / \  |_ _| \ | |
 |  _ \| |_) |  / _ \  | ||  \| |
 | |_) |  _ <  / ___ \ | || |\  |
 |____/|_| \_\/_/   \_\___|_| \_|
  ____ _     _____    _    _   _ _____ ____  
 / ___| |   | ____|  / \  | \ | | ____|  _ \ 
| |   | |   |  _|   / _ \ |  \| |  _| | |_) |
| |___| |___| |___ / ___ \| |\  | |___|  _ < 
 \____|_____|_____/_/   \_\_| \_|_____|_| \_\
"""

class BrainCleanerCLI:
    def __init__(self, start_path, dry_run=False, delete_all=False, sort_by='path'):
        self.term = Terminal()
        self.scanner = BrainScanner()
        self.start_path = start_path
        self.dry_run = dry_run
        self.delete_all = delete_all
        self.sort_by = sort_by
        
        self.results = [] # List of {'cat':, 'path':, 'size_str':, 'size_bytes':, 'deleted': False}
        self.cursor_idx = 0
        self.is_scanning = True
        self.scroll_pos = 0
        self.interrupt_event = threading.Event()
        self.status_msg = "Waiting for selection..."
        self.total_saved_bytes = 0
        self.mode = None # 'ai' or 'npm'

    def show_splash(self):
        print(self.term.home + self.term.clear)
        print(self.term.cyan(ASCII_ART))
        print(self.term.bold("\n  Welcome to Brain Cleaner CLI v1.1.0"))
        print("  " + "-" * 40)
        print("\n  Select Mode to begin:")
        print(self.term.blue("  [1] AI Tools Cleanup"))
        print(self.term.green("  [2] NPM Modules Cleanup"))
        print("\n  Press 'q' to exit")

    def _apply_mode_filter(self, mode):
        # Mutual exclusivity like GUI
        if mode == 'ai':
            self.scanner.categories = {k: v for k, v in self.scanner.categories.items() if k != "Node Modules"}
        else:
            self.scanner.categories = {k: v for k, v in self.scanner.categories.items() if k == "Node Modules"}
        self.scanner.all_patterns = [p for patterns in self.scanner.categories.values() for p in patterns]
        thread = threading.Thread(target=self._scan_worker, daemon=True)
        thread.start()

    def _scan_worker(self):
        try:
            for cat, path, size_str, size_bytes in self.scanner.scan_stream(self.start_path, self.interrupt_event):
                self.results.append({
                    'cat': cat,
                    'path': path,
                    'size_str': size_str,
                    'size_bytes': size_bytes,
                    'deleted': False
                })
                self._sort_results()
        except Exception as e:
            self.status_msg = f"Error: {e}"
        finally:
            self.is_scanning = False
            if not self.results:
                self.status_msg = "Scan complete. No residues found."
            else:
                self.status_msg = "Scan complete. Use Arrows to navigate, Space to delete, 'q' to quit."

    def _sort_results(self):
        if self.sort_by == 'size':
            self.results.sort(key=lambda x: x['size_bytes'], reverse=True)
        elif self.sort_by == 'path':
            self.results.sort(key=lambda x: x['path'])

    def draw(self):
        print(self.term.home + self.term.clear)
        
        # Header
        header = f" Brain Cleaner CLI - Scanning: {self.start_path} "
        print(self.term.black_on_cyan(header.center(self.term.width)))
        
        # Status Bar
        status_color = self.term.yellow if self.is_scanning else self.term.green
        print(status_color(f" Status: {self.status_msg}"))
        print("-" * self.term.width)

        # List Area
        list_height = self.term.height - 6
        visible_results = [r for r in self.results if not r['deleted']]
        
        if not visible_results:
            if not self.is_scanning:
                print(self.term.move_y(self.term.height // 2) + self.term.center("No items to display.").rstrip())
            return

        # Ensure cursor within bounds
        if self.cursor_idx >= len(visible_results):
            self.cursor_idx = max(0, len(visible_results) - 1)
        
        # Handle Scrolling
        if self.cursor_idx < self.scroll_pos:
            self.scroll_pos = self.cursor_idx
        elif self.cursor_idx >= self.scroll_pos + list_height:
            self.scroll_pos = self.cursor_idx - list_height + 1

        for i in range(list_height):
            idx = self.scroll_pos + i
            if idx >= len(visible_results):
                break
            
            res = visible_results[idx]
            is_selected = (idx == self.cursor_idx)
            
            # Formatting
            prefix = " > " if is_selected else "   "
            line = f"{prefix} [{res['cat']:<12}] {res['path']}"
            
            # Trim path if too long
            max_p_len = self.term.width - 25
            if len(line) > self.term.width - 15:
                line = line[:self.term.width - 15] + "..."
            
            # Add size to the right
            size_txt = res['size_str']
            line = line.ljust(self.term.width - 12) + self.term.bold(size_txt.rjust(10))

            if is_selected:
                print(self.term.reverse(line))
            else:
                # Highlight critical folders (optional)
                if "node_modules" in res['path'].lower() or any(p in res['path'] for p in [".cursor", ".trae"]):
                    print(self.term.cyan(line))
                else:
                    print(line)

        # Footer
        footer = f" [Space] Delete  [q] Quit  [Up/Down] Navigate  |  Saved: {self.scanner.format_size(self.total_saved_bytes)} "
        print(self.term.move_y(self.term.height - 1) + self.term.black_on_white(footer.ljust(self.term.width)))

    def handle_delete(self):
        visible_results = [r for r in self.results if not r['deleted']]
        if not visible_results: return
        
        target = visible_results[self.cursor_idx]
        
        if not self.dry_run:
            success, msg = self.scanner.delete_folder(target['path'])
            if success:
                self.total_saved_bytes += target['size_bytes']
                target['deleted'] = True
                self.status_msg = f"Deleted: {os.path.basename(target['path'])}"
            else:
                self.status_msg = f"Error: {msg}"
        else:
            self.status_msg = f"[Dry Run] Would delete {target['path']}"

    def run(self):
        # Step 0: Splash & Mode Selection
        with self.term.cbreak(), self.term.hidden_cursor():
            while self.mode is None:
                self.show_splash()
                val = self.term.inkey(timeout=0.5)
                if val == '1':
                    self.mode = 'ai'
                    self._apply_mode_filter('ai')
                elif val == '2':
                    self.mode = 'npm'
                    self._apply_mode_filter('npm')
                elif val.lower() == 'q':
                    return

        # Step 1: Scanner Execution
        if self.delete_all and not self.dry_run:
            print(f"[*] Starting automatic deletion in: {self.start_path}")
            count = 0
            for cat, path, size_str, size_bytes in self.scanner.scan_stream(self.start_path):
                success, msg = self.scanner.delete_folder(path)
                if success:
                    print(f" [OK] Deleted: {path} ({size_str})")
                    self.total_saved_bytes += size_bytes
                    count += 1
                else:
                    print(f" [ERR] {msg}")
            print(f"\n[+] Done. Deleted {count} items. Total saved: {self.scanner.format_size(self.total_saved_bytes)}")
            return

        self.start_scan_thread()
        
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                self.draw()
                
                # Check for input with timeout to allow UI refresh while scanning
                val = self.term.inkey(timeout=0.2)
                
                if val.code == self.term.KEY_DOWN:
                    visible_count = len([r for r in self.results if not r['deleted']])
                    self.cursor_idx = min(self.cursor_idx + 1, visible_count - 1)
                elif val.code == self.term.KEY_UP:
                    self.cursor_idx = max(self.cursor_idx - 1, 0)
                elif val == ' ' or val.code == self.term.KEY_DELETE:
                    self.handle_delete()
                elif val.lower() == 'q':
                    self.interrupt_event.set()
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brain Cleaner CLI - Interactive Residue Removal")
    parser.add_argument("-d", "--dir", default=str(Path.home()), help="Directory to scan")
    parser.add_argument("-t", "--target", help="Specific pattern to search (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Do not actually delete files")
    parser.add_argument("--delete-all", action="store_true", help="Delete everything found without asking")
    parser.add_argument("--sort", choices=['path', 'size'], default='path', help="Sort results")
    
    args = parser.parse_args()
    
    # Optional: Override categories if -t is provided
    if args.target:
        # We can dynamically adjust the scanner categories for this run
        cli_scanner = BrainScanner()
        cli_scanner.categories = {"Custom": [args.target]}
        cli_scanner.all_patterns = [args.target]
        cli = BrainCleanerCLI(args.dir, dry_run=args.dry_run, delete_all=args.delete_all, sort_by=args.sort)
        cli.scanner = cli_scanner
    else:
        cli = BrainCleanerCLI(args.dir, dry_run=args.dry_run, delete_all=args.delete_all, sort_by=args.sort)
    try:
        cli.run()
    except KeyboardInterrupt:
        pass
    print("\nGoodbye!")
