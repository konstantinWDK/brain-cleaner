import customtkinter as ctk
import os
import threading
from scanner import BrainScanner
from pathlib import Path

# Theme configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BrainCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Brain Cleaner - Professional Residue Removal")
        self.geometry("1000x700")
        self.scanner = BrainScanner()
        self.found_items_by_cat = {}
        self.checkboxes_by_cat = {}
        self.interrupt_event = threading.Event()
        
        self.category_info = {
            "Gemini": "Limpia residuos de Google Gemini (.gemini), incluyendo registros del 'brain' y grabaciones.",
            "Claude": "Elimina carpetas de Anthropic Claude y archivos de configuración asociados.",
            "IDE Agents": "Borra datos temporales de extensiones de IA como Cursor, Windsurf, Codeium y Tabnine.",
            "Other Tools": "Limpia rastros de OpenAI, Continue, Roo-Code, Copilot y otras utilidades de IA.",
            "All": "Vista combinada de todos los residuos de IA detectados en la ubicación seleccionada."
        }

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Brain Cleaner", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Scan Location Selection
        self.location_label = ctk.CTkLabel(self.sidebar, text="Scan Location:", anchor="w")
        self.location_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        self.location_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Home (~/)", "Full System (/)", "Drives (/media)", "Mounts (/mnt)"], command=self.change_location_event)
        self.location_optionemenu.grid(row=2, column=0, padx=20, pady=10)
        self.location_optionemenu.set("Full System (/)")
        self.current_scan_path = "/"

        self.custom_folder_button = ctk.CTkButton(self.sidebar, text="Select Custom Folder", command=self.select_custom_folder, fg_color="transparent", border_width=2)
        self.custom_folder_button.grid(row=3, column=0, padx=20, pady=10)

        self.run_scan_button = ctk.CTkButton(self.sidebar, text="🚀 START SCAN", command=lambda: self.start_scan(self.current_scan_path), fg_color="#1f538d", hover_color="#14375e")
        self.run_scan_button.grid(row=4, column=0, padx=20, pady=(20, 10))

        self.stop_scan_button = ctk.CTkButton(self.sidebar, text="Stop Scan", command=self.stop_scan, fg_color="#d32f2f", hover_color="#b71c1c")
        self.stop_scan_button.grid(row=4, column=0, padx=20, pady=(20, 10)) # Same position as start button
        self.stop_scan_button.grid_remove() 

        self.clean_selected_button = ctk.CTkButton(self.sidebar, text="Clean Selected", command=self.clean_selected, state="disabled")
        self.clean_selected_button.grid(row=5, column=0, padx=20, pady=10)

        self.clean_all_button = ctk.CTkButton(self.sidebar, text="Clean All (Visible)", command=self.clean_all, state="disabled", fg_color="#d32f2f", hover_color="#b71c1c")
        self.clean_all_button.grid(row=6, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # Main Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1) # Tabview gets weight

        # 1. Info Bubble (Bocadillo)
        self.info_bubble = ctk.CTkFrame(self.main_container, fg_color=("#e0e0e0", "#2b2b2b"), corner_radius=10)
        self.info_bubble.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        self.info_title = ctk.CTkLabel(self.info_bubble, text="💡 AI Brain Cleaner Info", font=ctk.CTkFont(size=14, weight="bold"))
        self.info_title.pack(padx=10, pady=(5, 0), anchor="w")
        
        self.info_text = ctk.CTkLabel(self.info_bubble, 
                                     text="Esta herramienta detecta 'cerebros' y registros temporales de asistentes IA.\nLimpiarlos ayuda a liberar espacio y mantener la privacidad de tus promts.",
                                     font=ctk.CTkFont(size=11), justify="left")
        self.info_text.pack(padx=10, pady=(0, 5), anchor="w")

        # 2. Tabview for categories (NOW ON TOP)
        self.tabview = ctk.CTkTabview(self.main_container, command=self.update_info_bubble)
        self.tabview.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.categories = list(self.scanner.categories.keys()) + ["All"]
        self.scrollable_frames = {}
        for cat in self.categories:
            tab = self.tabview.add(cat)
            frame = ctk.CTkScrollableFrame(tab, label_text=f"{cat} Residues")
            frame.pack(fill="both", expand=True)
            self.scrollable_frames[cat] = frame
            self.checkboxes_by_cat[cat] = []
        
        self.tabview.set("All")

        # 3. Residue Manager Footer Info
        self.footer_info = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_info.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.header = ctk.CTkLabel(self.footer_info, text="AI Residue Manager", font=ctk.CTkFont(size=16, weight="bold"))
        self.header.pack(side="left", padx=5)

        self.path_display_label = ctk.CTkLabel(self.footer_info, text=f"Target: {self.current_scan_path}", font=ctk.CTkFont(size=10, slant="italic"))
        self.path_display_label.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(self.footer_info, text="Ready to scan", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="right", padx=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_container, mode="indeterminate", height=6)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.progress_bar.grid_remove()

        # 4. Compact Log Area
        self.log_textbox = ctk.CTkTextbox(self.main_container, height=80, font=ctk.CTkFont(size=10))
        self.log_textbox.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.log_textbox.insert("0.0", "--- Activity Log ---\n")
        self.log_textbox.configure(state="disabled")

    def log(self, text):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{text}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def toggle_selection(self, category, value):
        for cb, var, path in self.checkboxes_by_cat[category]:
            var.set(value)
        self.log(f"{'Selected' if value else 'Deselected'} all in {category}")

    def update_info_bubble(self):
        current_tab = self.tabview.get()
        info = self.category_info.get(current_tab, "")
        self.info_text.configure(text=info)

    def change_location_event(self, selection):
        if selection == "Home (~/)":
            self.current_scan_path = str(Path.home())
        elif selection == "Full System (/)":
            self.current_scan_path = "/"
        elif selection == "Drives (/media)":
            self.current_scan_path = "/media"
        elif selection == "Mounts (/mnt)":
            self.current_scan_path = "/mnt"
        
        self.path_display_label.configure(text=f"Target: {self.current_scan_path}")

    def select_custom_folder(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.current_scan_path = path
            self.path_display_label.configure(text=f"Target: {self.current_scan_path}")
            self.location_optionemenu.set("Custom") # Add a custom option visually if needed
            self.log(f"Custom path selected: {path}")

    def stop_scan(self):
        self.interrupt_event.set()
        self.log("Stopping scan... Please wait.")
        self.stop_scan_button.configure(state="disabled")

    def start_scan(self, path):
        self.run_scan_button.grid_remove()
        self.stop_scan_button.grid()
        self.stop_scan_button.configure(state="normal")
        self.progress_bar.grid()
        self.progress_bar.start()
        
        self.status_label.configure(text=f"Scanning {path}... Please wait.")
        self.log(f"Starting scan on {path}...")
        
        self.interrupt_event.clear()
        
        # Clear existing items
        for cat in self.checkboxes_by_cat:
            for cb, var, p in self.checkboxes_by_cat[cat]:
                cb.destroy()
            self.checkboxes_by_cat[cat] = []
        
        self.found_items_by_cat = {}

        # Run scan in background thread
        thread = threading.Thread(target=self.run_scan, args=(path,))
        thread.daemon = True
        thread.start()

    def run_scan(self, path):
        results = self.scanner.find_residues(path, self.interrupt_event)
        self.after(0, lambda: self.finish_scan(results))

    def finish_scan(self, results):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.stop_scan_button.grid_remove()
        self.run_scan_button.grid()
        
        if self.interrupt_event.is_set():
            self.status_label.configure(text="Scan stopped by user.")
            self.log("Scan stopped.")
        
        total_found = len(results["All"])
        total_bytes = sum(item[2] for item in results["All"])
        total_str = self.scanner.format_size(total_bytes)

        if total_found == 0:
            self.status_label.configure(text="No residues found.")
            self.log("Scan complete. Nothing found.")
            self.clean_all_button.configure(state="disabled")
            self.clean_selected_button.configure(state="disabled")
            return

        self.status_label.configure(text=f"Found {total_found} items. Total Weight: {total_str}")
        self.log(f"Scan complete. Found {total_found} items ({total_str}).")
        
        for cat, items in results.items():
            frame = self.scrollable_frames[cat]
            
            # Calculate category total
            cat_bytes = sum(item[2] for item in items)
            cat_str = self.scanner.format_size(cat_bytes)
            
            # Add a summary label at the top of the frame
            top_frame = ctk.CTkFrame(frame, fg_color="transparent")
            top_frame.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="w")
            
            summary_label = ctk.CTkLabel(top_frame, text=f"Total: {len(items)} items | Weight: {cat_str}", font=ctk.CTkFont(weight="bold"))
            summary_label.pack(side="left", padx=(0, 20))
            
            select_all_btn = ctk.CTkButton(top_frame, text="Select All", width=80, height=24, font=ctk.CTkFont(size=11), 
                                          command=lambda c=cat: self.toggle_selection(c, True))
            select_all_btn.pack(side="left", padx=5)
            
            deselect_all_btn = ctk.CTkButton(top_frame, text="Deselect", width=80, height=24, font=ctk.CTkFont(size=11),
                                            fg_color="transparent", border_width=1,
                                            command=lambda c=cat: self.toggle_selection(c, False))
            deselect_all_btn.pack(side="left", padx=5)

            for i, (path, size_str, size_bytes) in enumerate(items):
                var = ctk.BooleanVar(value=False)
                # Display size in the checkbox text
                display_text = f"[{size_str}] {path}"
                cb = ctk.CTkCheckBox(frame, text=display_text, variable=var)
                cb.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                self.checkboxes_by_cat[cat].append((cb, var, path))

        self.clean_all_button.configure(state="normal")
        self.clean_selected_button.configure(state="normal")

    def clean_selected(self):
        current_tab = self.tabview.get()
        selected_paths = [path for cb, var, path in self.checkboxes_by_cat[current_tab] if var.get()]
        
        if not selected_paths:
            self.log(f"No items selected for cleaning in {current_tab}.")
            return
        
        self.execute_cleaning(selected_paths)

    def clean_all(self):
        current_tab = self.tabview.get()
        paths = [path for cb, var, path in self.checkboxes_by_cat[current_tab]]
        self.execute_cleaning(paths)

    def execute_cleaning(self, paths):
        count = 0
        self.log(f"Starting cleaning of {len(paths)} items...")
        for path in paths:
            success, msg = self.scanner.delete_item(path)
            if success:
                count += 1
                self.log(f"[OK] {msg}")
            else:
                self.log(f"[ERROR] {msg}")
        
        self.log(f"Cleaning complete. {count}/{len(paths)} items removed.")
        self.status_label.configure(text=f"Cleaned {count} items.")
        # We don't refresh all, just clear the log or allow manual refresh
        # But for better UX, let's suggest a re-scan.
        self.log("Click Scan to refresh results.")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = BrainCleanerApp()
    app.mainloop()
