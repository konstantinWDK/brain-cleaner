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
        self.selected_path = start_path # Default to provided start_path

        self.dry_run = dry_run
        self.delete_all = delete_all
        self.sort_by = sort_by
        
        self.results = [] # List of {'cat':, 'path':, 'size_str':, 'size_bytes':, 'deleted': False}
        self.cursor_idx = 0
        self.is_scanning = True
        self.scroll_pos = 0
        self.interrupt_event = threading.Event()
        self.mode = None # 'ai' or 'npm'
        self.total_saved_bytes = 0
        self.status_msg = "Waiting for selection..."
        self.confirmation_target = None # Path or "batch"
        self.all_selected = False
        self.spinner_frames = ["-", "\\", "|", "/"]
        self.spinner_idx = 0

    def draw_splash(self):
        content = []
        content.append(self.term.cyan(ASCII_ART))
        content.append(self.term.bold("\n  Welcome to Brain Cleaner CLI v1.1.0"))
        content.append("  " + "-" * 40)
        content.append("\n  Select Mode to begin:")
        content.append(self.term.blue("  [1] AI Tools Cleanup"))
        content.append(self.term.green("  [2] NPM Modules Cleanup"))
        content.append("\n  Press 'q' to exit")
        
        output = self.term.home + self.term.clear + "\n".join(content)
        sys.stdout.write(output)
        sys.stdout.flush()

    def draw_path_selector(self):
        content = []
        content.append(self.term.cyan(ASCII_ART))
        content.append(self.term.bold(f"\n  Mode: {self.term.yellow(self.mode.upper() if self.mode else '')}"))
        content.append("  " + "-" * 40)
        content.append("\n  Select Scan Path:")
        content.append(self.term.blue("  [1] User Home (~)"))
        content.append(self.term.green("  [2] Entire System (/)"))
        content.append(self.term.magenta("  [3] External Disks (/Volumes)"))
        content.append("\n  Press 'b' to go back, 'q' to exit")
        
        output = self.term.home + self.term.clear + "\n".join(content)
        sys.stdout.write(output)
        sys.stdout.flush()

    def _apply_mode_filter(self, mode, path=None):
        # Use provided path or fallback to self.start_path
        scan_root = path if path else self.start_path
        
        # Mutual exclusivity like GUI
        if mode == 'ai':
            self.scanner.categories = {k: v for k, v in self.scanner.categories.items() if k != "Node Modules"}
        else:
            self.scanner.categories = {k: v for k, v in self.scanner.categories.items() if k == "Node Modules"}
        self.scanner.all_patterns = [p for patterns in self.scanner.categories.values() for p in patterns]
        
        self.status_msg = f"Scanning {mode.upper()} residues in {scan_root}..."
        thread = threading.Thread(target=self._scan_worker, args=(scan_root,), daemon=True)
        thread.start()

    def _scan_worker(self, path):
        try:
            for cat, path, size_str, size_bytes in self.scanner.scan_stream(path, self.interrupt_event):

                self.results.append({
                    'cat': cat,
                    'path': path,
                    'size_str': size_str,
                    'size_bytes': size_bytes,
                    'deleted': False,
                    'selected': False
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
        content = []
        
        def btn(key, label, color=self.term.black_on_cyan):
            return f"{color(f' {key} ')} {self.term.bold(label)} "

        # Header
        header = f" BRAIN CLEANER CLI "
        content.append(self.term.black_on_cyan(header.center(self.term.width)))
        
        # Status Bar with Buttons
        self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_frames)
        spinner = self.term.yellow(self.spinner_frames[self.spinner_idx]) if self.is_scanning else self.term.green("√")
        
        status_line = f" {spinner} Status: "
        if self.is_scanning:
            status_line += btn("ESC", "Stop Scan", self.term.black_on_yellow)
        else:
            status_line += self.term.green("Scan Complete  ")

        status_line += " | "
        status_line += btn("↑↓", "Nav")
        status_line += btn("m", "Mark")
        status_line += btn("a", "All")
        status_line += btn("b", "Back")
        
        content.append(status_line)
        content.append("-" * self.term.width)

        # List Area
        list_height = self.term.height - 7
        visible_results = [r for r in self.results if not r['deleted']]
        marked_count = len([r for r in visible_results if r['selected']])
        
        if not visible_results:
            if not self.is_scanning:
                content.append("\n" * (list_height // 2) + self.term.center("No items to display."))
        else:
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
                    content.append("") # Fill space
                    continue
                
                res = visible_results[idx]
                is_selected = (idx == self.cursor_idx)
                is_marked = res.get('selected', False)
                
                # Formatting
                cursor_ptr = " > " if is_selected else "   "
                mark_ptr = "[*]" if is_marked else "[ ]"
                item_text = f"{mark_ptr} [{res['cat']:<12}] {res['path']}"
                
                # Trim path if too long
                available_width = self.term.width - 24
                if len(item_text) > available_width:
                    item_text = item_text[:available_width-3] + "..."
                
                line = f"{cursor_ptr}{item_text}"
                line = line.ljust(self.term.width - 12) + self.term.bold(res['size_str'].rjust(10))

                if is_selected:
                    content.append(self.term.reverse(line))
                else:
                    if "node_modules" in res['path'].lower() or any(p in res['path'] for p in [".cursor", ".trae"]):
                        content.append(self.term.cyan(line))
                    else:
                        content.append(line)

        # Footer
        sel_box = self.term.black_on_white(f" SELECTED: {marked_count} ")
        saved_box = self.term.black_on_green(f" SAVED: {self.scanner.format_size(self.total_saved_bytes)} ")
        footer = f" {btn('SPACE/ENTER', 'DELETE', self.term.black_on_red)} {sel_box} {saved_box} "
        
        # Confirmation Overlay
        if self.confirmation_target:
            msg = f" CONFIRM DELETE? {self.confirmation_target} [y/N] "
            overlay = self.term.move_y(self.term.height // 2) + self.term.black_on_red(msg.center(self.term.width))
            content.append(overlay)

        # Final output assembly
        output = self.term.home + self.term.clear + "\n".join(content)
        # Position footer at the bottom
        output += self.term.move_y(self.term.height - 1) + footer.ljust(self.term.width)
        
        sys.stdout.write(output)
        sys.stdout.flush()
        
        sys.stdout.write(output)
        sys.stdout.flush()

    def handle_delete(self):
        visible_results = [r for r in self.results if not r['deleted']]
        marked_items = [r for r in visible_results if r['selected']]
        
        targets = []
        if marked_items:
            targets = marked_items
            self.confirmation_target = f"{len(targets)} marked items"
        else:
            if not visible_results: return
            targets = [visible_results[self.cursor_idx]]
            self.confirmation_target = os.path.basename(targets[0]['path'])

        return targets

    def execute_deletion(self, targets):
        if self.dry_run:
            self.status_msg = f"[Dry Run] Scoped {len(targets)} items"
        else:
            count = 0
            for t in targets:
                success, msg = self.scanner.delete_folder(t['path'])
                if success:
                    self.total_saved_bytes += t['size_bytes']
                    t['deleted'] = True
                    count += 1
            self.status_msg = f"Deleted {count} items successfully."
        
        self.confirmation_target = None

    def run(self):
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            state = "SELECT_MODE"
            path_mapping = {
                '1': str(Path.home()),
                '2': '/',
                '3': '/Volumes'
            }
            targets_to_delete = []

            while True:
                if state == "SELECT_MODE":
                    self.draw_splash()
                    val = self.term.inkey(timeout=0.1)
                    if val == '1':
                        self.mode = 'ai'
                        state = "SELECT_PATH"
                    elif val == '2':
                        self.mode = 'npm'
                        state = "SELECT_PATH"
                    elif val.lower() == 'q':
                        return

                elif state == "SELECT_PATH":
                    self.draw_path_selector()
                    val = self.term.inkey(timeout=0.1)
                    if val in path_mapping:
                        self.selected_path = path_mapping[val]
                        
                        # Handle delete_all shortcut if needed (legacy support)
                        if self.delete_all and not self.dry_run:
                            print(self.term.home + self.term.clear + f"[*] Starting automatic deletion in: {self.selected_path}")
                            count = 0
                            for cat, p, s_str, s_bytes in self.scanner.scan_stream(self.selected_path):
                                success, msg = self.scanner.delete_folder(p)
                                if success:
                                    print(f" [OK] Deleted: {p} ({s_str})")
                                    self.total_saved_bytes += s_bytes
                                    count += 1
                                else:
                                    print(f" [ERR] {msg}")
                            print(f"\n[+] Done. Deleted {count} items. Total saved: {self.scanner.format_size(self.total_saved_bytes)}")
                            print("\nPress any key to exit.")
                            self.term.inkey()
                            return

                        self._apply_mode_filter(self.mode, self.selected_path)
                        state = "SCANNING"
                    elif val.lower() == 'b':
                        self.mode = None
                        state = "SELECT_MODE"
                    elif val.lower() == 'q':
                        return

                elif state == "SCANNING":
                    self.draw()
                    val = self.term.inkey(timeout=0.1)
                    
                    # If confirming, only Y/N work
                    if self.confirmation_target:
                        if val.lower() == 'y':
                            self.execute_deletion(targets_to_delete)
                            targets_to_delete = []
                        elif val.lower() == 'n' or val.code == self.term.KEY_ESCAPE:
                            self.confirmation_target = None
                            targets_to_delete = []
                        continue

                    if val.code == self.term.KEY_DOWN:
                        visible_results = [r for r in self.results if not r['deleted']]
                        self.cursor_idx = min(self.cursor_idx + 1, len(visible_results) - 1)
                    elif val.code == self.term.KEY_UP:
                        self.cursor_idx = max(self.cursor_idx - 1, 0)
                    elif val == ' ' or val.code == self.term.KEY_ENTER:
                        targets_to_delete = self.handle_delete()
                    elif val.lower() == 'm':
                        visible_results = [r for r in self.results if not r['deleted']]
                        if visible_results:
                            visible_results[self.cursor_idx]['selected'] = not visible_results[self.cursor_idx]['selected']
                    elif val.lower() == 'a':
                        self.all_selected = not self.all_selected
                        for r in self.results:
                            if not r['deleted']:
                                r['selected'] = self.all_selected
                    elif val.lower() == 'b':
                        self.interrupt_event.set()
                        self.interrupt_event = threading.Event() # Reset
                        self.mode = None
                        self.selected_path = None
                        self.results = []
                        self.cursor_idx = 0
                        self.scroll_pos = 0
                        self.is_scanning = True # Reset for next scan
                        state = "SELECT_MODE"
                    elif val.lower() == 'q':
                        self.interrupt_event.set()
                        return


def main():
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

if __name__ == "__main__":
    main()
