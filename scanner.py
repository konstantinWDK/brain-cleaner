import os
import shutil
from pathlib import Path

class BrainScanner:
    def __init__(self):
        # Patterns organized by category
        self.categories = {
            "Gemini": [".gemini"],
            "Claude": [".claude", ".anthropic"],
            "IDE Agents": [
                ".cursor", 
                ".windsurf", 
                ".codeium", 
                ".cody", 
                ".tabnine", 
                ".supermaven", 
                ".blackbox",
                ".amazon-codewhisperer"
            ],
            "Other Tools": [
                ".openai", 
                ".continue", 
                ".roo-code", 
                ".cline", 
                ".gh-copilot", 
                ".github-copilot",
                "brain-recordings"
            ]
        }
        # Flattened list for the walker
        self.all_patterns = [p for patterns in self.categories.values() for p in patterns]
        
        # Directories to skip during full scans (system/virtual FS)
        self.skip_dirs = {
            "proc", "sys", "dev", "run", "var/lib/docker", "snap", "root",
            "var/cache", "var/log", "tmp", ".cache"
        }
        
    def get_dir_size(self, path):
        """
        Calculates the total size of a directory in bytes.
        """
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size

    def format_size(self, size_bytes):
        """
        Formats bytes to human readable format.
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def find_residues(self, start_path, interrupt_event=None):
        """
        Scans and returns categorized results with sizes.
        Returns a dict: {category: [(path, size_formatted, size_bytes)]}
        """
        found = {cat: [] for cat in self.categories.keys()}
        found["All"] = []

        try:
            for root, dirs, files in os.walk(start_path):
                # Check for interruption
                if interrupt_event and interrupt_event.is_set():
                    print("Scan interrupted by user.")
                    return found

                # Filter out system directories to skip
                # We do this for better speed and stability on full system scans
                if start_path == "/":
                    # Check if current directory path starts with any of the skip paths
                    # or if any of the subdirs are in the skip list
                    dirs[:] = [d for d in dirs if d not in self.skip_dirs and 
                              not any(os.path.join(root, d).startswith(os.path.join("/", s)) for s in self.skip_dirs)]

                matched_in_this_root = []
                for d in dirs:
                    # Check against all patterns
                    for cat, patterns in self.categories.items():
                        if d in patterns or any(d.startswith(p) for p in patterns):
                            full_path = os.path.join(root, d)
                            
                            # Calculate size
                            size_bytes = self.get_dir_size(full_path)
                            size_str = self.format_size(size_bytes)
                            
                            item = (full_path, size_str, size_bytes)
                            found[cat].append(item)
                            found["All"].append(item)
                            matched_in_this_root.append(d)
                            break # Move to next directory
                
                # Don't recurse into directories we already marked
                for m in matched_in_this_root:
                    if m in dirs:
                        dirs.remove(m)
                    
        except Exception as e:
            print(f"Error scanning {start_path}: {e}")
            
        # Sort by path
        for cat in found:
            found[cat] = sorted(list(set(found[cat])), key=lambda x: x[0])
            
        return found

    def delete_item(self, path):
        """
        Deletes a directory or file.
        """
        try:
            path_obj = Path(path)
            if path_obj.is_dir():
                shutil.rmtree(path)
            else:
                os.remove(path)
            return True, f"Successfully deleted {path}"
        except Exception as e:
            return False, f"Failed to delete {path}: {e}"

if __name__ == "__main__":
    # Quick test
    scanner = BrainScanner()
    home = str(Path.home())
    print(f"Scanning {home}...")
    results = scanner.find_residues(home)
    for r in results:
        print(f"Found: {r}")
