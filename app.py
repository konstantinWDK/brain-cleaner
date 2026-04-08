import os
import sys

# macOS Compatibility fixes (must be before ANY gui import)
if sys.platform == "darwin":
    os.environ["SYSTEM_VERSION_COMPAT"] = "0"
    os.environ["NSUnbufferedIO"] = "YES"

import customtkinter as ctk
import threading
import subprocess
from scanner import BrainScanner
from pathlib import Path

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class BrainCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Brain Cleaner - AI Residue Removal")
        self.geometry("1100x720")
        self.scanner = BrainScanner()
        self.interrupt_event = threading.Event()
        self.residue_rows = []   # [(wrapper, cat, var, path, children_frame, child_rows)]
        self.filter_buttons = {}
        self.active_filter = "All"
        self.current_scan_path = str(Path.home())
        self.current_loc_type = "Home"

        # Category definitions
        self.AI_CATS  = ["Gemini", "Claude", "IDE Agents", "Other Tools"]
        self.NPM_CATS = ["Node Modules"]

        # Info slider data
        self.info_states = [
            {
                "title": "💡 Delete Consequences",
                "text": "You will free up space, but might lose local chat histories and plugin configurations.",
            },
            {
                "title": "🚀 Usage Tips",
                "text": "Scan weekly to keep your system optimized. Use 'Custom Folder' for specific project cleanups.",
            },
            {
                "title": "⚡ Pro Optimization",
                "text": "For a full cleanup, close your IDE (Cursor, VSCode) before cleaning temporary files.",
            }
        ]
        self.current_info_index = 0

        # ── Grid Layout ──────────────────────────────────────────
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ───────────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.sidebar, text="🧠 Brain Cleaner",
                     font=ctk.CTkFont(size=20, weight="bold")
                     ).grid(row=0, column=0, padx=20, pady=(20, 15), sticky="ew")

        # Location
        ctk.CTkLabel(self.sidebar, text="Scan Scope:", anchor="w",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).grid(row=1, column=0, padx=20, pady=(0, 5), sticky="ew")

        self.home_btn = ctk.CTkButton(self.sidebar, text="🏠  Home",
                                      command=lambda: self.set_location("Home"),
                                      fg_color="transparent", border_width=1, anchor="w")
        self.home_btn.grid(row=2, column=0, padx=20, pady=3, sticky="ew")

        self.system_btn = ctk.CTkButton(self.sidebar, text="💻  Full System",
                                        command=lambda: self.set_location("System"),
                                        fg_color="transparent", border_width=1, anchor="w")
        self.system_btn.grid(row=3, column=0, padx=20, pady=3, sticky="ew")

        self.custom_folder_btn = ctk.CTkButton(self.sidebar, text="📁  Custom Folder",
                                               command=self.select_custom_folder,
                                               fg_color="transparent", border_width=1, anchor="w")
        self.custom_folder_btn.grid(row=4, column=0, padx=20, pady=3, sticky="ew")

        self._highlight_loc_btn()

        # Scan Mode
        ctk.CTkLabel(self.sidebar, text="Scan Mode:", anchor="w",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).grid(row=5, column=0, padx=20, pady=(14, 4), sticky="ew")

        self.mode_ai_var = ctk.BooleanVar(value=True)
        self.mode_npm_var = ctk.BooleanVar(value=True)

        ctk.CTkCheckBox(self.sidebar, text="🤖  AI Tools",
                        variable=self.mode_ai_var,
                        font=ctk.CTkFont(size=12),
                        checkbox_width=18, checkbox_height=18,
                        checkmark_color="white", fg_color="#1f538d"
                        ).grid(row=6, column=0, padx=24, pady=2, sticky="w")

        ctk.CTkCheckBox(self.sidebar, text="📦  NPM Modules",
                        variable=self.mode_npm_var,
                        font=ctk.CTkFont(size=12),
                        checkbox_width=18, checkbox_height=18,
                        checkmark_color="white", fg_color="#2e7d32"
                        ).grid(row=7, column=0, padx=24, pady=(2, 4), sticky="w")

        # ── Bottom Sidebar Controls ───────────────────────────────
        bottom = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom.grid(row=10, column=0, padx=20, pady=20, sticky="ew")
        bottom.grid_columnconfigure(0, weight=1)

        self.run_scan_button = ctk.CTkButton(
            bottom, text="🚀\n\nSTART SCAN",
            command=lambda: self.start_scan(self.current_scan_path),
            fg_color="#1f538d", hover_color="#14375e",
            height=130, corner_radius=18,
            font=ctk.CTkFont(size=15, weight="bold"))
        self.run_scan_button.grid(row=0, column=0, pady=(0, 15), sticky="ew")

        self.stop_scan_button = ctk.CTkButton(
            bottom, text="🛑\n\nSTOP",
            command=self.stop_scan, fg_color="#d32f2f", hover_color="#b71c1c",
            height=130, corner_radius=18,
            font=ctk.CTkFont(size=15, weight="bold"))
        self.stop_scan_button.grid(row=0, column=0, pady=(0, 15), sticky="ew")
        self.stop_scan_button.grid_remove()

        self.clean_selected_button = ctk.CTkButton(
            bottom, text="✨ Clean Selected",
            command=self.clean_selected, state="disabled",
            fg_color="#2b71b1", hover_color="#1a4d7d",
            height=38, font=ctk.CTkFont(weight="bold"))
        self.clean_selected_button.grid(row=1, column=0, pady=4, sticky="ew")

        self.clean_all_button = ctk.CTkButton(
            bottom, text="🗑️ Clean All (Visible)",
            command=self.clean_all, state="disabled",
            fg_color="transparent", border_width=1,
            text_color=("#d32f2f", "#ff6666"), height=30)
        self.clean_all_button.grid(row=2, column=0, pady=(4, 12), sticky="ew")

        # Appearance
        ctk.CTkLabel(self.sidebar, text="Appearance:", anchor="w",
                     font=ctk.CTkFont(size=10)
                     ).grid(row=11, column=0, padx=20, pady=(0, 2), sticky="ew")
        app_menu = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light", "System"],
                                     command=lambda m: ctk.set_appearance_mode(m),
                                     height=24, font=ctk.CTkFont(size=10))
        app_menu.grid(row=12, column=0, padx=20, pady=(0, 5), sticky="ew")
        app_menu.set("Dark")

        self.show_logs_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(self.sidebar, text="Show Activity Logs",
                      variable=self.show_logs_var, command=self.toggle_logs,
                      font=ctk.CTkFont(size=10)
                      ).grid(row=13, column=0, padx=20, pady=10, sticky="ew")

        # ── Main Area ─────────────────────────────────────────────
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(3, weight=1)
        self.main = main

        # Info Slider
        self.info_bubble = ctk.CTkFrame(main, corner_radius=14, border_width=1)
        self.info_bubble.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="ew")
        self.info_bubble.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(self.info_bubble, text="❮", width=28, fg_color="transparent",
                      hover_color=("#c0c0c0", "#3d3d3d"),
                      command=lambda: self.navigate_slider(-1)
                      ).grid(row=0, column=0, rowspan=2, padx=(8, 0))

        self.info_title = ctk.CTkLabel(self.info_bubble, text=self.info_states[0]["title"],
                                       font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
        self.info_title.grid(row=0, column=1, pady=(8, 0), sticky="ew", padx=(8, 0))

        self.info_text = ctk.CTkLabel(self.info_bubble, text=self.info_states[0]["text"],
                                      font=ctk.CTkFont(size=10), wraplength=480,
                                      justify="left", anchor="w")
        self.info_text.grid(row=1, column=1, pady=(2, 4), sticky="ew", padx=(8, 0))

        ctk.CTkButton(self.info_bubble, text="❯", width=28, fg_color="transparent",
                      hover_color=("#c0c0c0", "#3d3d3d"),
                      command=lambda: self.navigate_slider(1)
                      ).grid(row=0, column=2, rowspan=2, padx=(0, 8))

        dots_f = ctk.CTkFrame(self.info_bubble, fg_color="transparent")
        dots_f.grid(row=2, column=1, pady=(0, 6), sticky="w", padx=(8, 0))
        self.dots_labels = []
        for i in range(len(self.info_states)):
            d = ctk.CTkLabel(dots_f, text="●" if i == 0 else "○", font=ctk.CTkFont(size=9))
            d.pack(side="left", padx=2)
            self.dots_labels.append(d)

        # Filter Bubbles Bar
        filter_bar = ctk.CTkFrame(main, fg_color="transparent")
        filter_bar.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

        ctk.CTkLabel(filter_bar, text="Filters:", font=ctk.CTkFont(size=12, weight="bold")
                     ).pack(side="left", padx=(5, 10))

        self.bubbles_container = ctk.CTkFrame(filter_bar, fg_color="transparent")
        self.bubbles_container.pack(side="left", fill="x", expand=True)

        # Select All / None (right side)
        ctk.CTkButton(filter_bar, text="☑ All", width=62, height=26,
                      corner_radius=8, border_width=1, border_color="#757575",
                      fg_color="transparent", hover_color=("#d0d0d0", "#3a3a3a"),
                      text_color=("#333333", "#cccccc"), font=ctk.CTkFont(size=11),
                      command=lambda: self.set_all_visible(True)
                      ).pack(side="right", padx=(4, 2))

        ctk.CTkButton(filter_bar, text="☐ None", width=68, height=26,
                      corner_radius=8, border_width=1, border_color="#757575",
                      fg_color="transparent", hover_color=("#d0d0d0", "#3a3a3a"),
                      text_color=("#333333", "#cccccc"), font=ctk.CTkFont(size=11),
                      command=lambda: self.set_all_visible(False)
                      ).pack(side="right", padx=(2, 4))

        # Progress Area
        self.progress_container = ctk.CTkFrame(main, fg_color="transparent")
        self.progress_container.grid(row=2, column=0, padx=10, pady=(8, 0), sticky="ew")
        self.progress_container.grid_columnconfigure(0, weight=1)
        self.progress_container.grid_remove()

        self.progress_label = ctk.CTkLabel(self.progress_container, text="",
                                           font=ctk.CTkFont(size=10, slant="italic"))
        self.progress_label.grid(row=0, column=0, pady=(0, 2))

        self.progress_bar = ctk.CTkProgressBar(self.progress_container, mode="indeterminate",
                                               height=10, progress_color="#1f538d")
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")

        # Results Scrollable Frame
        self.results_frame = ctk.CTkScrollableFrame(main, label_text="Detected AI Residues")
        self.results_frame.grid(row=3, column=0, padx=10, pady=8, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)

        # Footer
        footer = ctk.CTkFrame(main, fg_color="transparent")
        footer.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkLabel(footer, text="AI Residue Manager",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)

        self.path_display = ctk.CTkLabel(footer, text=f"Target: {self.current_scan_path}",
                                         font=ctk.CTkFont(size=10, slant="italic"))
        self.path_display.pack(side="left", padx=15)

        self.status_label = ctk.CTkLabel(footer, text="Ready to scan",
                                         font=ctk.CTkFont(size=11))
        self.status_label.pack(side="right", padx=10)

        # Log Area
        self.log_textbox = ctk.CTkTextbox(main, height=80, font=ctk.CTkFont(size=10))
        self.log_textbox.grid(row=5, column=0, padx=10, pady=(0, 8), sticky="nsew")
        self.log_textbox.insert("0.0", "--- Activity Log ---\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.grid_remove()

        self.create_filter_bubbles(["All"])

    # ── Helpers ───────────────────────────────────────────────────

    def log(self, text):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{text}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def toggle_logs(self):
        if self.show_logs_var.get():
            self.log_textbox.grid()
        else:
            self.log_textbox.grid_remove()

    def get_category_color(self, cat):
        return {
            "Gemini": "#1a73e8",
            "Claude": "#d97757",
            "IDE Agents": "#7c4dff",
            "Other Tools": "#546e7a",
            "Node Modules": "#2e7d32"
        }.get(cat, "#757575")

    # ── Info Slider ───────────────────────────────────────────────

    def navigate_slider(self, direction):
        self.current_info_index = (self.current_info_index + direction) % len(self.info_states)
        state = self.info_states[self.current_info_index]
        self.info_bubble.configure(border_width=3)
        self.after(150, lambda: self.info_bubble.configure(border_width=1))
        self.info_title.configure(text=state["title"])
        self.info_text.configure(text=state["text"])
        for i, dot in enumerate(self.dots_labels):
            dot.configure(text="●" if i == self.current_info_index else "○")

    # ── Location ──────────────────────────────────────────────────

    def set_location(self, loc_type):
        self.current_loc_type = loc_type
        if loc_type == "Home":
            self.current_scan_path = str(Path.home())
        elif loc_type == "System":
            self.current_scan_path = "/"
        self._highlight_loc_btn()
        self.path_display.configure(text=f"Target: {self.current_scan_path}")

    def _highlight_loc_btn(self):
        mapping = {"Home": self.home_btn, "System": self.system_btn, "Custom": self.custom_folder_btn}
        for name, btn in mapping.items():
            try:
                if name == self.current_loc_type:
                    btn.configure(fg_color="#1f538d", border_width=0)
                else:
                    btn.configure(fg_color="transparent", border_width=1)
            except Exception:
                pass

    def select_custom_folder(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.current_scan_path = path
            self.current_loc_type = "Custom"
            self._highlight_loc_btn()
            self.path_display.configure(text=f"Target: {path}")
            self.log(f"Custom path: {path}")

    # ── Scan ──────────────────────────────────────────────────────

    def stop_scan(self):
        self.interrupt_event.set()
        self.stop_scan_button.configure(state="disabled")
        self.log("Stopping scan...")

    def start_scan(self, path):
        if not self.mode_ai_var.get() and not self.mode_npm_var.get():
            self.status_label.configure(text="Select at least one scan mode.")
            return

        self.interrupt_event.clear()

        # Reset results
        for frame, *_ in self.residue_rows:
            frame.destroy()
        self.residue_rows = []

        # UI state
        self.run_scan_button.grid_remove()
        self.stop_scan_button.grid()
        self.stop_scan_button.configure(state="normal")
        self.clean_selected_button.configure(state="disabled")
        self.clean_all_button.configure(state="disabled")

        self.progress_label.configure(text=f"Scanning {path} ...")
        self.progress_container.grid()
        self.progress_bar.start()
        self.status_label.configure(text="Scanning...")
        self.create_filter_bubbles(["Scanning..."])

        self.scanning_active = True
        self.scan_icons = ["🔍", "⚡", "🚀", "🛰️", "☄️"]
        self.scan_icon_idx = 0
        self._animate_scan()

        active_modes = []
        if self.mode_ai_var.get():
            active_modes.append("ai")
        if self.mode_npm_var.get():
            active_modes.append("npm")

        self.log(f"Scan: {path} | modes: {', '.join(active_modes)}")
        threading.Thread(target=self._run_scan, args=(path, active_modes), daemon=True).start()

    def _animate_scan(self):
        if getattr(self, "scanning_active", False):
            icon = self.scan_icons[self.scan_icon_idx % len(self.scan_icons)]
            self.stop_scan_button.configure(text=f"{icon}\n\nSCANNING...")
            self.scan_icon_idx += 1
            self.after(400, self._animate_scan)

    def _run_scan(self, path, modes):
        raw = self.scanner.find_residues(path, self.interrupt_event)
        # Filter by mode
        results = {"All": []}
        if "ai" in modes:
            for c in self.AI_CATS:
                results[c] = raw.get(c, [])
                results["All"] += results[c]
        if "npm" in modes:
            for c in self.NPM_CATS:
                results[c] = raw.get(c, [])
                results["All"] += results[c]
        self.scanning_active = False
        self.after(0, lambda: self._finish_scan(results, modes))

    def _finish_scan(self, results, modes):
        self.progress_bar.stop()
        self.progress_container.grid_remove()
        self.stop_scan_button.grid_remove()
        self.run_scan_button.grid()

        total = len(results.get("All", []))
        total_bytes = sum(item[2] for item in results.get("All", []))
        total_str = self.scanner.format_size(total_bytes)

        if total == 0:
            self.status_label.configure(text="No residues found.")
            self.log("Scan complete. Nothing found.")
            self.create_filter_bubbles(["No results"])
            return

        self.status_label.configure(text=f"Found {total} items — {total_str}")
        self.log(f"Scan complete. {total} items found ({total_str}).")

        found_cats = [c for c in (self.AI_CATS + self.NPM_CATS) if results.get(c)]
        self.create_filter_bubbles(["All"] + found_cats)

        # Render sections
        def render_section(title, color, cats):
            section_cats = [c for c in cats if results.get(c)]
            if not section_cats:
                return
            hdr = ctk.CTkFrame(self.results_frame, fg_color=color, corner_radius=8)
            hdr.pack(fill="x", padx=4, pady=(10, 2))
            ctk.CTkLabel(hdr, text=title, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="white").pack(side="left", padx=12, pady=6)
            count = sum(len(results[c]) for c in section_cats)
            ctk.CTkLabel(hdr, text=f"{count} items",
                         font=ctk.CTkFont(size=10), text_color="#cccccc"
                         ).pack(side="right", padx=12, pady=6)
            for cat in section_cats:
                self._render_rows(results[cat], cat)

        if "ai" in modes:
            render_section("🤖  AI Tools", "#1f538d", self.AI_CATS)
        if "npm" in modes:
            render_section("📦  NPM Modules", "#2e7d32", self.NPM_CATS)

        self.clean_selected_button.configure(state="normal")
        self.clean_all_button.configure(state="normal")
        self.active_filter = "All"
        self.update_bubble_selection("All")

    def _render_rows(self, items, cat):
        """Render a list of (path, size_str, size_bytes) result items."""
        for path, size_str, _ in items:
            var = ctk.BooleanVar(value=False)

            wrapper = ctk.CTkFrame(self.results_frame, fg_color="transparent")
            wrapper.pack(fill="x", padx=4, pady=2)

            row = ctk.CTkFrame(wrapper, fg_color=("#f5f5f5", "#2b2b2b"), corner_radius=8)
            row.pack(fill="x")
            row.grid_columnconfigure(3, weight=1)

            ctk.CTkCheckBox(row, text="", variable=var, width=24
                            ).grid(row=0, column=0, padx=(10, 4), pady=6)

            ctk.CTkLabel(row, text=f" {cat} ",
                         fg_color=self.get_category_color(cat),
                         text_color="white", corner_radius=5,
                         font=ctk.CTkFont(size=9, weight="bold")
                         ).grid(row=0, column=1, padx=(4, 10), pady=6)

            size_lbl = ctk.CTkLabel(row, text=size_str, text_color="#FF9500",
                                    font=ctk.CTkFont(size=11, weight="bold"),
                                    width=72, anchor="e")
            size_lbl.grid(row=0, column=2, padx=(0, 10), pady=6)

            path_lbl = ctk.CTkLabel(row, text=path,
                                    font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
            path_lbl.grid(row=0, column=3, padx=(0, 4), pady=6, sticky="ew")

            expand_btn = ctk.CTkButton(
                row, text="›", width=28, height=28,
                fg_color=("#e0e0e0", "#3a3a3a"),
                hover_color=("#c8c8c8", "#484848"),
                text_color=("#333333", "#eeeeee"),
                corner_radius=8, border_width=0,
                font=ctk.CTkFont(size=16, weight="bold"))
            expand_btn.grid(row=0, column=4, padx=(0, 8), pady=6)

            children_frame = ctk.CTkFrame(wrapper, fg_color=("#ececec", "#242424"), corner_radius=8)
            child_rows = []
            expanded = [False]

            def _sync_children(*_, pv=var, cr=child_rows):
                state = pv.get()
                for _, cv in cr:
                    cv.set(state)

            var.trace_add("write", _sync_children)

            def _populate_children(p=path, cf=children_frame, cr=child_rows, pv=var):
                if cr:
                    return
                try:
                    entries = sorted(os.scandir(p), key=lambda e: (not e.is_dir(), e.name.lower()))
                except PermissionError:
                    ctk.CTkLabel(cf, text="  ⚠️ Permission denied",
                                 font=ctk.CTkFont(size=10), text_color="#FF9500"
                                 ).pack(anchor="w", padx=12, pady=4)
                    return
                for entry in entries:
                    child_var = ctk.BooleanVar(value=pv.get())
                    child_row = ctk.CTkFrame(cf, fg_color="transparent")
                    child_row.pack(fill="x", padx=8, pady=1)
                    child_row.grid_columnconfigure(1, weight=1)
                    ctk.CTkCheckBox(child_row, text="", variable=child_var, width=20
                                    ).grid(row=0, column=0, padx=(8, 4), pady=3)
                    icon = "📁" if entry.is_dir() else "📄"
                    ctk.CTkLabel(child_row, text=f"{icon}  {entry.name}",
                                 font=ctk.CTkFont(size=10), anchor="w"
                                 ).grid(row=0, column=1, padx=2, pady=3, sticky="ew")
                    try:
                        sz_str = self.scanner.format_size(entry.stat().st_size) if entry.is_file() else ""
                    except Exception:
                        sz_str = ""
                    if sz_str:
                        ctk.CTkLabel(child_row, text=sz_str, text_color="#FF9500",
                                     font=ctk.CTkFont(size=10, weight="bold")
                                     ).grid(row=0, column=2, padx=(0, 10), pady=3)
                    cr.append((entry.path, child_var))

            def _toggle_expand(cf=children_frame, btn=expand_btn, ex=expanded,
                               populate=_populate_children):
                populate()
                if ex[0]:
                    cf.pack_forget()
                    btn.configure(text="›")
                else:
                    cf.pack(fill="x", pady=(2, 0))
                    btn.configure(text="⌄")
                ex[0] = not ex[0]

            expand_btn.configure(command=_toggle_expand)

            def _toggle(e, v=var):
                v.set(not v.get())

            for w in (size_lbl, path_lbl, row):
                w.bind("<Button-1>", _toggle)

            self.residue_rows.append((wrapper, cat, var, path, children_frame, child_rows))

    # ── Filters ───────────────────────────────────────────────────

    def set_all_visible(self, state: bool):
        for entry in self.residue_rows:
            wrapper, cat, var = entry[0], entry[1], entry[2]
            if self.active_filter in ("All", cat):
                var.set(state)

    def create_filter_bubbles(self, categories):
        for btn in self.filter_buttons.values():
            btn.destroy()
        self.filter_buttons = {}

        for cat in categories:
            btn = ctk.CTkButton(
                self.bubbles_container, text=cat,
                width=max(70, len(cat) * 8), height=28,
                corner_radius=14, border_width=1, border_color="#757575",
                fg_color="transparent", hover_color=("#c0c0c0", "#3d3d3d"),
                text_color=("#333333", "#eeeeee"),
                command=lambda c=cat: self.apply_filter(c))
            btn.pack(side="left", padx=5)
            self.filter_buttons[cat] = btn

        if self.filter_buttons:
            first = list(self.filter_buttons.keys())[0]
            self.update_bubble_selection(first)

    def update_bubble_selection(self, selected):
        self.active_filter = selected
        for cat, btn in self.filter_buttons.items():
            if cat == selected:
                btn.configure(fg_color="#1f538d", border_width=0, text_color="white")
            else:
                btn.configure(fg_color="transparent", border_width=1,
                              text_color=("#333333", "#eeeeee"))

    def apply_filter(self, selection):
        if selection in ("Scanning...", "No results", "Everything clean! ✨"):
            return
        self.update_bubble_selection(selection)
        for entry in self.residue_rows:
            wrapper, cat = entry[0], entry[1]
            if selection == "All" or selection == cat:
                wrapper.pack(fill="x", padx=4, pady=2)
            else:
                wrapper.pack_forget()

    # ── Cleaning ──────────────────────────────────────────────────

    def clean_selected(self):
        count = 0
        to_remove = []
        for entry in list(self.residue_rows):
            wrapper, cat, var, path = entry[0], entry[1], entry[2], entry[3]
            child_rows = entry[5] if len(entry) > 5 else []
            selected_children = [(cp, cv) for cp, cv in child_rows if cv.get()]
            all_selected = child_rows and all(cv.get() for _, cv in child_rows)

            if var.get() and (not child_rows or all_selected):
                ok, msg = self.scanner.delete_folder(path)
                self.log(msg)
                if ok:
                    wrapper.destroy()
                    if len(entry) > 4:
                        entry[4].destroy()
                    to_remove.append(entry)
                    count += 1
            elif selected_children:
                for cp, cv in selected_children:
                    ok, msg = self.scanner.delete_folder(cp)
                    self.log(msg)
                    if ok:
                        count += 1

        for r in to_remove:
            self.residue_rows = [e for e in self.residue_rows if e is not r]

        if count == 0:
            self.log("No items selected.")
        else:
            self.status_label.configure(text=f"Cleaned {count} items.")
        self._post_clean()

    def clean_all(self):
        count = 0
        to_remove = []
        for entry in list(self.residue_rows):
            wrapper, cat, var, path = entry[0], entry[1], entry[2], entry[3]
            if self.active_filter not in ("All", cat):
                continue
            ok, msg = self.scanner.delete_folder(path)
            self.log(msg)
            if ok:
                wrapper.destroy()
                if len(entry) > 4:
                    entry[4].destroy()
                to_remove.append(entry)
                count += 1

        for r in to_remove:
            self.residue_rows = [e for e in self.residue_rows if e is not r]

        self.status_label.configure(text=f"Removed {count} items.")
        self._post_clean()

    def _post_clean(self):
        if not self.residue_rows:
            self.status_label.configure(text="Everything clean! ✨")
            self.clean_selected_button.configure(state="disabled")
            self.clean_all_button.configure(state="disabled")
            self.create_filter_bubbles(["Everything clean! ✨"])


if __name__ == "__main__":
    app = BrainCleanerApp()
    app.mainloop()
