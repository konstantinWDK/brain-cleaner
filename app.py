import os
import sys

# macOS Compatibility fixes (must be before ANY gui import)
if sys.platform == "darwin":
    # Prevent macOS 11+ from reporting as 10.16 for legacy apps
    os.environ["SYSTEM_VERSION_COMPAT"] = "0"
    # Ensure UI performance and log output
    os.environ["NSUnbufferedIO"] = "YES"

import customtkinter as ctk
import threading
from scanner import BrainScanner
from pathlib import Path

# Theme configuration
try:
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
except Exception:
    pass # Safe fallback for environment issues

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
            "Node Modules": "Busca y elimina carpetas de dependencias de Node.js (node_modules), que pueden ocupar GBs de espacio.",
            "All": "Vista combinada de todos los residuos de IA detectados en la ubicación seleccionada."
        }

        self.info_states = [
            {
                "title": "💡 Consecuencias del Borrado",
                "text": "Liberarás espacio valioso, pero podrías perder historiales de chat locales y configuraciones de plugins. Algunos asistentes podrían reiniciarse.",
                "color": ("#e0e0e0", "#2b2b2b")
            },
            {
                "title": "🚀 Consejos de Uso",
                "text": "Escanea semanalmente para mantener tu sistema optimizado. Usa 'Select Custom Folder' para limpiar solo proyectos técnicos específicos.",
                "color": ("#d1e7dd", "#0f5132")
            },
            {
                "title": "⚡ Optimización Pro",
                "text": "Para un borrado total, cierra tu IDE (Cursor, VSCode) antes de limpiar archivos temporales (.cursor, .windsurf). Esto evita bloqueos del sistema.",
                "color": ("#fff3cd", "#664d03") # Amarillito suave para advertencias pro
            }
        ]
        self.current_info_index = 0

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Space pusher

        self.logo_label = ctk.CTkLabel(self.sidebar, text="Brain Cleaner", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Scan Location Selection
        self.location_label = ctk.CTkLabel(self.sidebar, text="Scan Location:", anchor="w")
        self.location_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        self.location_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Home (~/)", "Full System (/)", "Drives (/media)", "Mounts (/mnt)"], command=self.change_location_event)
        self.location_optionemenu.grid(row=2, column=0, padx=20, pady=10)
        self.location_optionemenu.set("Full System (/)")
        self.current_scan_path = "/"

        self.custom_folder_button = ctk.CTkButton(self.sidebar, text="Select Custom Folder", command=self.select_custom_folder, fg_color="transparent", border_width=1)
        self.custom_folder_button.grid(row=3, column=0, padx=20, pady=10)

        # BOTTOM CONTROLS SECTION
        self.bottom_sidebar = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.bottom_sidebar.grid(row=5, column=0, padx=10, pady=20, sticky="s")

        self.run_scan_button = ctk.CTkButton(self.bottom_sidebar, text="START SCAN", 
                                            command=lambda: self.start_scan(self.current_scan_path), 
                                            fg_color="#1f538d", hover_color="#14375e",
                                            width=160, height=140, corner_radius=20,
                                            font=ctk.CTkFont(size=16, weight="bold"),
                                            image=None, # We use emoji/text for simplicity
                                            compound="top")
        self.run_scan_button.configure(text="🚀\n\nSTART SCAN")
        self.run_scan_button.grid(row=0, column=0, padx=10, pady=(0, 20))

        self.stop_scan_button = ctk.CTkButton(self.bottom_sidebar, text="🛑\n\nSTOP SCAN", 
                                             command=self.stop_scan, fg_color="#d32f2f", hover_color="#b71c1c",
                                             width=160, height=140, corner_radius=20,
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             compound="top")
        self.stop_scan_button.grid(row=0, column=0, padx=10, pady=(0, 20))
        self.stop_scan_button.grid_remove() 

        self.clean_selected_button = ctk.CTkButton(self.bottom_sidebar, text="✨ Publicar Seleccionados", 
                                                 command=self.clean_selected, state="disabled",
                                                 fg_color="#2b71b1", hover_color="#1a4d7d",
                                                 height=40, font=ctk.CTkFont(weight="bold"))
        self.clean_selected_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.clean_all_button = ctk.CTkButton(self.bottom_sidebar, text="🗑️ Clean All (Visible)", 
                                             command=self.clean_all, state="disabled", 
                                             fg_color="transparent", border_width=1,
                                             text_color=("#d32f2f", "#ff6666"),
                                             height=32)
        self.clean_all_button.grid(row=2, column=0, padx=10, pady=(5, 15), sticky="ew")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance:", anchor="w", font=ctk.CTkFont(size=10))
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], 
                                                           command=self.change_appearance_mode_event, height=20, font=ctk.CTkFont(size=10))
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(5, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # Main Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1) # Tabview gets weight

        # 1. Mini-Slider (Dynamic Info Capsule)
        self.info_bubble = ctk.CTkFrame(self.main_container, fg_color=self.info_states[0]["color"], corner_radius=15, border_width=1)
        self.info_bubble.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        self.info_bubble.grid_columnconfigure(1, weight=1) # Central column for text
        
        # Navigation Arrow Left
        self.left_btn = ctk.CTkButton(self.info_bubble, text="❮", width=30, height=40, font=ctk.CTkFont(size=20), 
                                     command=lambda: self.navigate_slider(-1), fg_color="transparent", border_width=0, hover_color=("#c0c0c0", "#3d3d3d"))
        self.left_btn.grid(row=0, column=0, rowspan=2, padx=(10, 0))

        self.info_title = ctk.CTkLabel(self.info_bubble, text=self.info_states[0]["title"], font=ctk.CTkFont(size=14, weight="bold"))
        self.info_title.grid(row=0, column=1, padx=15, pady=(10, 0), sticky="")
        
        self.info_text = ctk.CTkLabel(self.info_bubble, 
                                     text=self.info_states[0]["text"],
                                     font=ctk.CTkFont(size=11), justify="center", wraplength=500)
        self.info_text.grid(row=1, column=1, padx=15, pady=(0, 5), sticky="")

        # Navigation Arrow Right
        self.right_btn = ctk.CTkButton(self.info_bubble, text="❯", width=30, height=40, font=ctk.CTkFont(size=20), 
                                      command=lambda: self.navigate_slider(1), fg_color="transparent", border_width=0, hover_color=("#c0c0c0", "#3d3d3d"))
        self.right_btn.grid(row=0, column=2, rowspan=2, padx=(0, 10))

        # Pagination Dots Container
        self.dots_frame = ctk.CTkFrame(self.info_bubble, fg_color="transparent")
        self.dots_frame.grid(row=2, column=1, pady=(0, 5))
        self.dots_labels = []
        for i in range(len(self.info_states)):
            dot = ctk.CTkLabel(self.dots_frame, text="●" if i == 0 else "○", font=ctk.CTkFont(size=10))
            dot.pack(side="left", padx=3)
            self.dots_labels.append(dot)

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

    def navigate_slider(self, direction):
        """Moves the slider state in the specified direction"""
        self.current_info_index = (self.current_info_index + direction) % len(self.info_states)
        self.update_slider_ui()

    def update_slider_ui(self):
        state = self.info_states[self.current_info_index]
        
        # Cross-fade blink effect
        self.info_bubble.configure(border_width=3)
        self.after(150, lambda: self.info_bubble.configure(border_width=1))
        
        self.info_title.configure(text=state["title"])
        self.info_text.configure(text=state["text"])
        self.info_bubble.configure(fg_color=state["color"])
        
        # Update Dots
        for i, dot in enumerate(self.dots_labels):
            dot.configure(text="●" if i == self.current_info_index else "○")
        
        self.log(f"Slider: {state['title']}")

    def update_info_bubble(self):
        current_tab = self.tabview.get()
        info = self.category_info.get(current_tab, "")
        self.log(f"Categoría: {current_tab} - {info}")

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
        
        # Start button animation
        self.scanning_active = True
        self.scan_icons = ["🔍", "⚡", "🚀", "🛰️", "☄️"]
        self.current_icon_idx = 0
        self.animate_scan_button()

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

    def animate_scan_button(self):
        if hasattr(self, 'scanning_active') and self.scanning_active:
            icon = self.scan_icons[self.current_icon_idx]
            self.stop_scan_button.configure(text=f"{icon}\n\nSCANNING...")
            self.current_icon_idx = (self.current_icon_idx + 1) % len(self.scan_icons)
            self.after(400, self.animate_scan_button)

    def run_scan(self, path):
        results = self.scanner.find_residues(path, self.interrupt_event)
        self.scanning_active = False # Stop animation
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
                
                # Row Frame for multi-colored item
                item_frame = ctk.CTkFrame(frame, fg_color="transparent")
                item_frame.grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
                
                cb = ctk.CTkCheckBox(item_frame, text="", variable=var, width=20)
                cb.pack(side="left", padx=(5, 0))
                
                # Size Label (Bold & Orange)
                size_label = ctk.CTkLabel(item_frame, text=f"[{size_str}] ", 
                                         text_color="#FF9500", font=ctk.CTkFont(size=11, weight="bold"))
                size_label.pack(side="left")
                
                # Path Label
                path_label = ctk.CTkLabel(item_frame, text=path, font=ctk.CTkFont(size=11, weight="bold"))
                path_label.pack(side="left")

                # Bind clicks on labels to toggle checkbox
                def toggle_cb(event, v=var):
                    v.set(not v.get())
                
                size_label.bind("<Button-1>", toggle_cb)
                path_label.bind("<Button-1>", toggle_cb)

                self.checkboxes_by_cat[cat].append((item_frame, var, path))
        self.clean_all_button.configure(state="normal")
        self.clean_selected_button.configure(state="normal")

    def clean_selected(self):
        to_clean = []
        for cat in self.categories:
            if cat == "All": continue
            for item_row, var, path in self.checkboxes_by_cat[cat]:
                if var.get():
                    to_clean.append((cat, item_row, var, path))
        
        if not to_clean:
            self.log("No items selected for cleaning.")
            return

        cleaned_count = 0
        for cat, item_row, var, path in to_clean:
            if self.scanner.delete_folder(path):
                self.log(f"CLEANED: {path}")
                cleaned_count += 1
                # Remove from UI (destroys the whole row frame)
                item_row.destroy()
                # Remove from tracking
                self.checkboxes_by_cat[cat] = [item for item in self.checkboxes_by_cat[cat] if item[2] != path]
                self.checkboxes_by_cat["All"] = [item for item in self.checkboxes_by_cat["All"] if item[2] != path]
            else:
                self.log(f"FAILED to clean: {path}")

        self.log(f"Clean up complete. {cleaned_count} items removed.")
        self.status_label.configure(text=f"Cleaned {cleaned_count} items. Rescan recommended.")
        
        # Trigger weight update (will recalculate from remaining checkboxes)
        self.update_total_weight_display()

    def clean_all(self):
        current_tab = self.tabview.get()
        if current_tab == "All":
            self.log("Cleaning ALL detected residues...")
            to_clean = []
            for cat in self.categories:
                if cat == "All": continue
                for item_row, var, path in self.checkboxes_by_cat[cat]:
                    to_clean.append((cat, item_row, var, path))
        else:
            self.log(f"Cleaning all in {current_tab}...")
            to_clean = [(current_tab, item_row, var, path) for item_row, var, path in self.checkboxes_by_cat[current_tab]]

        cleaned_count = 0
        for cat, item_row, var, path in to_clean:
            if self.scanner.delete_folder(path):
                cleaned_count += 1
                item_row.destroy()
                # Remove from tracking
                self.checkboxes_by_cat[cat] = [item for item in self.checkboxes_by_cat[cat] if item[2] != path]
                self.checkboxes_by_cat["All"] = [item for item in self.checkboxes_by_cat["All"] if item[2] != path]
            else:
                self.log(f"FAILED to clean: {path}")

        self.log(f"Done. Removed {cleaned_count} items.")
        self.status_label.configure(text=f"Removed {cleaned_count} items.")
        self.update_total_weight_display()

    def update_total_weight_display(self):
        # We need to recalculate or just show info from what's left
        # Actually, let's just update the status label with a summary
        total_remaining = sum(len(items) for cat, items in self.checkboxes_by_cat.items() if cat != "All")
        if total_remaining == 0:
            self.status_label.configure(text="Everything clean! ✨")
            self.clean_selected_button.configure(state="disabled")
            self.clean_all_button.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = BrainCleanerApp()
    app.mainloop()
