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

        # Translation System
        self.lang = "es"
        self.texts = {
            "es": {
                "logo": "Brain Cleaner",
                "scope": "Alcance del Escaneo:",
                "home": "🏠 Home",
                "system": "💻 Sistema",
                "custom": "📁 Carpeta",
                "custom_btn": "Seleccionar Carpeta",
                "start_scan": "EMPEZAR ESCANEO",
                "stop_scan": "DETENER ESCANEO",
                "scanning": "ESCANEO EN CURSO...",
                "clean_selected": "✨ Limpiar Seleccionados",
                "clean_all": "🗑️ Limpiar Todo (Visible)",
                "appearance": "Apariencia:",
                "show_logs": "Mostrar Logs de Actividad",
                "filters": "Filtros:",
                "ready": "Listo para escanear",
                "all": "Todos",
                "found_total": "Hallados {count} ítems. Peso Total: {size}",
                "consequences_title": "💡 Consecuencias del Borrado",
                "consequences_text": "Liberarás espacio valioso, pero podrías perder historiales de chat locales y configuraciones de plugins.",
                "tips_title": "🚀 Consejos de Uso",
                "tips_text": "Escanea semanalmente para mantener tu sistema optimizado. Usa 'Carpeta' para limpiezas técnicas específicas.",
                "opt_title": "⚡ Optimización Pro",
                "opt_text": "Para un borrado total, cierra tu IDE (Cursor, VSCode) antes de limpiar archivos temporales.",
                "no_results": "Sin resultados",
                "everything_clean": "¡Todo limpio! ✨"
            },
            "en": {
                "logo": "Brain Cleaner",
                "scope": "Scan Scope:",
                "home": "🏠 Home",
                "system": "💻 System",
                "custom": "📁 Custom",
                "custom_btn": "Select Custom Folder",
                "start_scan": "START SCAN",
                "stop_scan": "STOP SCAN",
                "scanning": "SCANNING...",
                "clean_selected": "✨ Clean Selected",
                "clean_all": "🗑️ Clean All (Visible)",
                "appearance": "Appearance:",
                "show_logs": "Show Activity Logs",
                "filters": "Filters:",
                "ready": "Ready to scan",
                "all": "All",
                "found_total": "Found {count} items. Total Weight: {size}",
                "consequences_title": "💡 Delete Consequences",
                "consequences_text": "You will free up space, but might lose local chat histories and plugin configurations.",
                "tips_title": "🚀 Usage Tips",
                "tips_text": "Scan weekly to keep your system optimized. Use 'Custom' for specific technical cleanups.",
                "opt_title": "⚡ Pro Optimization",
                "opt_text": "For a full cleanup, close your IDE (Cursor, VSCode) before cleaning temporary files.",
                "no_results": "No results",
                "everything_clean": "Everything clean! ✨"
            }
        }
        
        self.update_info_states()
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
        self.location_label = ctk.CTkLabel(self.sidebar, text=self.texts[self.lang]["scope"], anchor="w", font=ctk.CTkFont(weight="bold"))
        self.location_label.grid(row=1, column=0, padx=20, pady=(10, 5))
        
        self.home_btn = ctk.CTkButton(self.sidebar, text=self.texts[self.lang]["home"], 
                                     command=lambda: self.change_location_event("Home"),
                                     fg_color="transparent", border_width=1)
        self.home_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.system_btn = ctk.CTkButton(self.sidebar, text=self.texts[self.lang]["system"], 
                                       command=lambda: self.change_location_event("System"),
                                       fg_color="transparent", border_width=1)
        self.system_btn.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.custom_btn = ctk.CTkButton(self.sidebar, text=self.texts[self.lang]["custom_btn"], 
                                       command=self.select_custom_folder,
                                       fg_color="transparent", border_width=1)
        self.custom_btn.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        # Set default active style
        self.current_loc_type = "Home"
        self.update_location_buttons_ui()
        self.current_scan_path = str(Path.home())

        # BOTTOM CONTROLS SECTION
        self.bottom_sidebar = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.bottom_sidebar.grid(row=5, column=0, padx=20, pady=20, sticky="ew") # Changed sticky to ew
        self.bottom_sidebar.grid_columnconfigure(0, weight=1)

        self.run_scan_button = ctk.CTkButton(self.bottom_sidebar, text="START SCAN", 
                                            command=lambda: self.start_scan(self.current_scan_path), 
                                            fg_color="#1f538d", hover_color="#14375e",
                                            width=160, height=140, corner_radius=20,
                                            font=ctk.CTkFont(size=16, weight="bold"),
                                            compound="top")
        self.run_scan_button.configure(text="🚀\n\nSTART SCAN")
        self.run_scan_button.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew") # sticky ew

        self.stop_scan_button = ctk.CTkButton(self.bottom_sidebar, text="🛑\n\nSTOP SCAN", 
                                             command=self.stop_scan, fg_color="#d32f2f", hover_color="#b71c1c",
                                             width=160, height=140, corner_radius=20,
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             compound="top")
        self.stop_scan_button.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew") # sticky ew
        self.stop_scan_button.grid_remove() 

        self.clean_selected_button = ctk.CTkButton(self.bottom_sidebar, text="✨ Publicar Seleccionados", 
                                                 command=self.clean_selected, state="disabled",
                                                 fg_color="#2b71b1", hover_color="#1a4d7d",
                                                 height=40, font=ctk.CTkFont(weight="bold"))
        self.clean_selected_button.grid(row=1, column=0, padx=0, pady=5, sticky="ew")

        self.clean_all_button = ctk.CTkButton(self.bottom_sidebar, text="🗑️ Clean All (Visible)", 
                                             command=self.clean_all, state="disabled", 
                                             fg_color="transparent", border_width=1,
                                             text_color=("#d32f2f", "#ff6666"),
                                             height=32)
        self.clean_all_button.grid(row=2, column=0, padx=0, pady=(5, 15), sticky="ew")

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance:", anchor="w", font=ctk.CTkFont(size=10))
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(0, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], 
                                                           command=self.change_appearance_mode_event, height=20, font=ctk.CTkFont(size=10))
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(5, 5))
        self.appearance_mode_optionemenu.set("Dark")

        self.lang_label = ctk.CTkLabel(self.sidebar, text="Language:", anchor="w", font=ctk.CTkFont(size=10))
        self.lang_label.grid(row=8, column=0, padx=20, pady=(5, 0))
        self.lang_optionmenu = ctk.CTkOptionMenu(self.sidebar, values=["Español", "English"], 
                                               command=self.change_language_event, height=20, font=ctk.CTkFont(size=10))
        self.lang_optionmenu.grid(row=9, column=0, padx=20, pady=(5, 10))
        self.lang_optionmenu.set("Español")

        self.show_logs_var = ctk.BooleanVar(value=False)
        self.show_logs_switch = ctk.CTkSwitch(self.sidebar, text=self.texts[self.lang]["show_logs"], variable=self.show_logs_var, 
                                             command=self.toggle_logs, font=ctk.CTkFont(size=10))
        self.show_logs_switch.grid(row=10, column=0, padx=20, pady=10)

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

        self.tabview = None # Will be replaced by dynamic filters
        self.residue_rows = [] # To track [(frame, category, var, path)]
        self.filter_buttons = {} # To track category -> button
        self.active_filter = "All"
        
        # 2. Filter Bar (NOW BUBBLES)
        self.filter_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.filter_frame.grid(row=1, column=0, padx=10, pady=(15, 0), sticky="ew")
        
        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filters:", font=ctk.CTkFont(size=12, weight="bold"))
        self.filter_label.pack(side="left", padx=(5, 10))

        self.bubbles_container = ctk.CTkFrame(self.filter_frame, fg_color="transparent")
        self.bubbles_container.pack(side="left", fill="x", expand=True)
        
        # Initial bubbles

        # 3. Unified Results Scroll Frame
        self.results_frame = ctk.CTkScrollableFrame(self.main_container, label_text="Detected AI Residues")
        self.results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.main_container.grid_rowconfigure(2, weight=1)

        # 4. Residue Manager Footer Info
        self.footer_info = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.footer_info.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.header = ctk.CTkLabel(self.footer_info, text="AI Residue Manager", font=ctk.CTkFont(size=16, weight="bold"))
        self.header.pack(side="left", padx=5)

        self.path_display_label = ctk.CTkLabel(self.footer_info, text=f"Target: {self.current_scan_path}", font=ctk.CTkFont(size=10, slant="italic"))
        self.path_display_label.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(self.footer_info, text="Ready to scan", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="right", padx=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_container, mode="indeterminate", height=6)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.progress_bar.grid_remove()

        # 5. Compact Log Area
        self.log_textbox = ctk.CTkTextbox(self.main_container, height=80, font=ctk.CTkFont(size=10))
        self.log_textbox.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.log_textbox.insert("0.0", "--- Activity Log ---\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.grid_remove() # Hidden by default
        
        # Initialize with translations AFTER all widgets are created
        self.refresh_ui_text()

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

    def update_info_states(self):
        t = self.texts[self.lang]
        self.info_states = [
            {
                "title": t["consequences_title"],
                "text": t["consequences_text"],
                "color": ("#e0e0e0", "#2b2b2b")
            },
            {
                "title": t["tips_title"],
                "text": t["tips_text"],
                "color": ("#d1e7dd", "#0f5132")
            },
            {
                "title": t["opt_title"],
                "text": t["opt_text"],
                "color": ("#fff3cd", "#664d03")
            }
        ]

    def change_language_event(self, selection):
        self.lang = "es" if selection == "Español" else "en"
        self.update_info_states()
        self.refresh_ui_text()
        self.log(f"Language changed to: {self.lang}")

    def refresh_ui_text(self):
        t = self.texts[self.lang]
        self.logo_label.configure(text=t["logo"])
        self.location_label.configure(text=t["scope"])
        
        # Update buttons
        self.home_btn.configure(text=t["home"])
        self.system_btn.configure(text=t["system"])
        self.custom_btn.configure(text=t["custom_btn"])
        
        # Footer & Misc
        self.filter_label.configure(text=t["filters"])
        self.status_label.configure(text=t["ready"] if self.status_label.cget("text") in ["Listo para escanear", "Ready to scan"] else self.status_label.cget("text"))
        self.show_logs_switch.configure(text=t["show_logs"])
        
        # Update Scan Buttons Text (maintaining the icon format)
        self.run_scan_button.configure(text=f"🚀\n\n{t['start_scan']}")
        # Stop scan is usually dynamic but let's set base
        self.stop_scan_button.configure(text=f"🛑\n\n{t['stop_scan']}")
        
        self.clean_selected_button.configure(text=t["clean_selected"])
        self.clean_all_button.configure(text=t["clean_all"])
        
        # If after scan, refresh bubbles
        if self.filter_buttons:
            # We keep 'All' translated, other categories stay technical
            current_filter = self.active_filter
            new_cats = []
            for cat in self.filter_buttons.keys():
                if cat in ["All", "Todos", "¡Todo limpio!", "Everything clean!"]:
                    new_cats.append(t["all"])
                else:
                    new_cats.append(cat)
            self.create_filter_bubbles(new_cats)
            
        # Refresh current info bubble
        state = self.info_states[self.current_info_index]
        self.info_title.configure(text=state["title"])
        self.info_text.configure(text=state["text"])

    def change_location_event(self, selection):
        self.current_loc_type = selection
        if selection == "Home":
            self.current_scan_path = str(Path.home())
        elif selection == "System":
            self.current_scan_path = "/"
        
        self.update_location_buttons_ui()
        self.path_display_label.configure(text=f"Target: {self.current_scan_path}")

    def update_location_buttons_ui(self):
        # Update button highlight
        btns = {"Home": self.home_btn, "System": self.system_btn, "Custom": self.custom_btn}
        for name, btn in btns.items():
            if name == self.current_loc_type:
                btn.configure(fg_color="#1f538d", border_width=0)
            else:
                btn.configure(fg_color="transparent", border_width=1)

    def select_custom_folder(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.current_scan_path = path
            self.path_display_label.configure(text=f"Target: {self.current_scan_path}")
            self.current_loc_type = "Custom"
            self.update_location_buttons_ui()
            self.log(f"Custom path selected: {path}")
        else:
            # Revert to Home if cancelled and no current custom
            if self.current_loc_type == "Custom":
                self.change_location_event("Home")

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
        
        # Reset UI
        for frame, cat, var, p in self.residue_rows:
            frame.destroy()
        self.residue_rows = []
        self.create_filter_bubbles(["Scanning..."])

        self.found_items_by_cat = {}

        # Run scan in background thread
        thread = threading.Thread(target=self.run_scan, args=(path,))
        thread.daemon = True
        thread.start()

    def animate_scan_button(self):
        if hasattr(self, 'scanning_active') and self.scanning_active:
            t = self.texts[self.lang]
            icon = self.scan_icons[self.current_icon_idx]
            self.stop_scan_button.configure(text=f"{icon}\n\n{t['scanning']}")
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
        
        t = self.texts[self.lang]
        
        if self.interrupt_event.is_set():
            self.status_label.configure(text="Scan stopped by user.")
            self.log("Scan stopped.")
        
        total_found = len(results["All"])
        total_bytes = sum(item[2] for item in results["All"])
        total_str = self.scanner.format_size(total_bytes)

        if total_found == 0:
            self.status_label.configure(text=t["no_results"])
            self.log("Scan complete. Nothing found.")
            self.create_filter_bubbles([t["no_results"]])
            self.clean_all_button.configure(state="disabled")
            self.clean_selected_button.configure(state="disabled")
            return

        self.status_label.configure(text=t["found_total"].format(count=total_found, size=total_str))
        self.log(f"Scan complete. Found {total_found} items ({total_str}).")
        
        # Identify found categories
        found_cats = [cat for cat in self.scanner.categories.keys() if len(results[cat]) > 0]
        self.create_filter_bubbles([t["all"]] + found_cats)
        self.active_filter = t["all"]
        
        # Populate unified list
        for i, (cat, items) in enumerate(results.items()):
            if cat == "All": continue
            
            for path, size_str, size_bytes in items:
                var = ctk.BooleanVar(value=False)
                
                # Row Frame
                item_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
                item_frame.grid(column=0, padx=5, pady=2, sticky="w")
                
                cb = ctk.CTkCheckBox(item_frame, text="", variable=var, width=20)
                cb.pack(side="left", padx=(5, 5))
                
                # Category Tag (Badge)
                cat_color = self.get_category_color(cat)
                cat_badge = ctk.CTkLabel(item_frame, text=f" {cat} ", 
                                        fg_color=cat_color, text_color="white", corner_radius=6, font=ctk.CTkFont(size=9, weight="bold"))
                cat_badge.pack(side="left", padx=(0, 10))

                # Size Label (Bold & Orange)
                size_label = ctk.CTkLabel(item_frame, text=f"[{size_str}] ", 
                                         text_color="#FF9500", font=ctk.CTkFont(size=11, weight="bold"))
                size_label.pack(side="left")
                
                # Path Label
                path_label = ctk.CTkLabel(item_frame, text=path, font=ctk.CTkFont(size=11, weight="bold"))
                path_label.pack(side="left")

                def toggle_cb(event, v=var): v.set(not v.get())
                size_label.bind("<Button-1>", toggle_cb)
                path_label.bind("<Button-1>", toggle_cb)

                self.residue_rows.append((item_frame, cat, var, path))

        self.clean_all_button.configure(state="normal")
        self.clean_selected_button.configure(state="normal")

    def create_filter_bubbles(self, categories):
        # Clear existing bubbles
        for btn in self.filter_buttons.values():
            btn.destroy()
        self.filter_buttons = {}

        for cat in categories:
            btn = ctk.CTkButton(self.bubbles_container, text=cat, width=80, height=30, 
                               corner_radius=15, border_width=1, border_color="#757575",
                               fg_color="transparent", hover_color=("#c0c0c0", "#3d3d3d"),
                               text_color=("#333333", "#eeeeee"),
                               command=lambda c=cat: self.apply_filter(c))
            btn.pack(side="left", padx=5)
            self.filter_buttons[cat] = btn

        if "All" in self.filter_buttons:
            self.update_bubble_selection("All")

    def update_bubble_selection(self, selected_cat):
        self.active_filter = selected_cat
        for cat, btn in self.filter_buttons.items():
            if cat == selected_cat:
                btn.configure(fg_color="#1f538d", border_width=0, text_color="white")
            else:
                btn.configure(fg_color="transparent", border_width=1, text_color=("#333333", "#eeeeee"))

    def apply_filter(self, selection):
        if selection in ["Scanning...", "No results", "ESCANEO EN CURSO...", "Sin resultados"]: return
        
        self.update_bubble_selection(selection)
        self.log(f"Filtering by: {selection}")
        
        t = self.texts[self.lang]
        for frame, cat, var, path in self.residue_rows:
            if selection == t["all"] or selection == cat:
                frame.grid()
            else:
                frame.grid_remove()
        self.clean_all_button.configure(state="normal")
        self.clean_selected_button.configure(state="normal")

    def clean_selected(self):
        to_clean = []
        for frame, cat, var, path in self.residue_rows:
            if var.get():
                to_clean.append((frame, cat, var, path))
        
        if not to_clean:
            self.log("No items selected for cleaning.")
            return

        cleaned_count = 0
        for frame, cat, var, path in to_clean:
            if self.scanner.delete_folder(path):
                self.log(f"CLEANED: {path}")
                cleaned_count += 1
                frame.destroy()
                self.residue_rows = [r for r in self.residue_rows if r[3] != path]
            else:
                self.log(f"FAILED to clean: {path}")

        self.log(f"Clean up complete. {cleaned_count} items removed.")
        self.status_label.configure(text=f"Cleaned {cleaned_count} items. Rescan recommended.")
        self.update_total_weight_display()

    def clean_all(self):
        selection = self.active_filter
        t = self.texts[self.lang]
        self.log(f"Cleaning all in filter: {selection}...")
        
        to_clean = []
        for frame, cat, var, path in self.residue_rows:
            if selection == t["all"] or selection == cat:
                to_clean.append((frame, cat, var, path))

        cleaned_count = 0
        for frame, cat, var, path in to_clean:
            if self.scanner.delete_folder(path):
                cleaned_count += 1
                frame.destroy()
                self.residue_rows = [r for r in self.residue_rows if r[3] != path]
            else:
                self.log(f"FAILED to clean: {path}")

        self.log(f"Done. Removed {cleaned_count} items.")
        self.status_label.configure(text=f"Removed {cleaned_count} items.")
        self.update_total_weight_display()

    def update_total_weight_display(self):
        total_remaining = len(self.residue_rows)
        t = self.texts[self.lang]
        if total_remaining == 0:
            self.status_label.configure(text=t["everything_clean"])
            self.clean_selected_button.configure(state="disabled")
            self.clean_all_button.configure(state="disabled")
            self.create_filter_bubbles([t["everything_clean"]])

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def toggle_logs(self):
        if self.show_logs_var.get():
            self.log_textbox.grid()
        else:
            self.log_textbox.grid_remove()

if __name__ == "__main__":
    app = BrainCleanerApp()
    app.mainloop()
