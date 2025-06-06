import tkinter as tk
from tkinter import ttk
from file_management import import_files

# Use ttkbootstrap for modern look
import ttkbootstrap as tb

class ProbabilityTable(ttk.Frame):
    def __init__(self, parent, excerpts):
        super().__init__(parent)
        self.excerpts = excerpts
        self.rows = []
        self._build_ui()

    def _build_ui(self):
        test_font = ("Arial", 10)
        max_name_len = max([len(excerpt.name) for excerpt in self.excerpts] + [9])
        name_col_width = max(120, min(400, max_name_len * 8 + 30))
        total_width = name_col_width + 90 + 180

        canvas = tk.Canvas(self, height=220, width=total_width, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview, style="primary.Vertical.TScrollbar")
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Table headers as first row
        ttk.Label(self.scrollable_frame, text="Track Name", style="primary.TLabel", font=('Arial', 10, 'bold'), width=int(name_col_width/8)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Label(self.scrollable_frame, text="Probability", style="primary.TLabel", font=('Arial', 10, 'bold'), width=10).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(self.scrollable_frame, text="Probability Bar", style="primary.TLabel", font=('Arial', 10, 'bold'), width=20).grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Table rows
        for idx, excerpt in enumerate(self.excerpts):
            self._add_row(idx + 1, excerpt, name_col_width)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _add_row(self, row_idx, excerpt, name_col_width=20):
        # Track Name
        name_label = ttk.Label(self.scrollable_frame, text=excerpt.name, anchor="w", width=int(name_col_width/8))
        name_label.grid(row=row_idx, column=0, padx=5, pady=2, sticky="ew")

        # Probability Entry
        prob_var = tk.DoubleVar(value=excerpt.probability)
        prob_entry = ttk.Entry(self.scrollable_frame, textvariable=prob_var, width=8)
        prob_entry.grid(row=row_idx, column=1, padx=5, pady=2, sticky="ew")

        # Probability Bar
        prob_bar = ttk.Progressbar(self.scrollable_frame, orient="horizontal", length=150, mode="determinate", maximum=1.0, style="success.Horizontal.TProgressbar")
        prob_bar.grid(row=row_idx, column=2, padx=5, pady=2, sticky="ew")
        prob_bar["value"] = excerpt.probability

        def on_prob_change(*args):
            try:
                val = float(prob_var.get())
                if val < 0:
                    val = 0
                    prob_var.set(val)
                elif val > 2:
                    val = 1
                    prob_var.set(val)
                elif val > 1:
                    val = 1
                    prob_var.set(val)
                excerpt.probability = val
                prob_bar["value"] = val
            except Exception:
                prob_bar["value"] = 0

        prob_var.trace_add("write", on_prob_change)
        self.rows.append((name_label, prob_entry, prob_bar, prob_var))

if __name__ == "__main__":
    folder_path = "input"
    excerpts = import_files(folder_path)

    # Use ttkbootstrap themed root
    root = tb.Window(themename="flatly")
    root.title("Track Probabilities")
    root.geometry("1050x600")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=(10, 10))
    main_frame.pack(fill="both", expand=True)

    # Table on the left
    table = ProbabilityTable(main_frame, excerpts)
    table.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

    # BPM, Measures, and Track Settings box on the right
    settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding=(10, 10))
    settings_frame.grid(row=0, column=1, sticky="n")

    bpm_var = tk.IntVar(value=120)
    measures_var = tk.IntVar(value=16)
    num_tracks_var = tk.IntVar(value=4)

    ttk.Label(settings_frame, text="BPM:").grid(row=0, column=0, sticky="w")
    bpm_entry = ttk.Entry(settings_frame, textvariable=bpm_var, width=8)
    bpm_entry.grid(row=0, column=1, pady=2)

    ttk.Label(settings_frame, text="Track Length (measures):").grid(row=1, column=0, sticky="w")
    measures_entry = ttk.Entry(settings_frame, textvariable=measures_var, width=8)
    measures_entry.grid(row=1, column=1, pady=2)

    ttk.Label(settings_frame, text="Number of Tracks:").grid(row=2, column=0, sticky="w")
    num_tracks_entry = ttk.Entry(settings_frame, textvariable=num_tracks_var, width=8)
    num_tracks_entry.grid(row=2, column=1, pady=2)

    # Frame for track names table (now scrollable)
    track_names_frame = ttk.LabelFrame(settings_frame, text="Track Names", padding=(5, 5))
    track_names_frame.grid(row=3, column=0, columnspan=2, pady=(10,0), sticky="ew")

    # --- Make track names table scrollable ---
    track_names_canvas = tk.Canvas(track_names_frame, height=170, highlightthickness=0)
    track_names_scrollbar = ttk.Scrollbar(track_names_frame, orient="vertical", command=track_names_canvas.yview, style="primary.Vertical.TScrollbar")
    track_names_inner = ttk.Frame(track_names_canvas)

    track_names_inner.bind(
        "<Configure>",
        lambda e: track_names_canvas.configure(
            scrollregion=track_names_canvas.bbox("all")
        )
    )
    track_names_canvas.create_window((0, 0), window=track_names_inner, anchor="nw")
    track_names_canvas.configure(yscrollcommand=track_names_scrollbar.set)

    track_names_canvas.pack(side="left", fill="both", expand=True)
    track_names_scrollbar.pack(side="right", fill="y")

    # --- Track name persistence ---
    track_name_vars = []
    track_name_memory = {}  # Persist names even if box is empty
    track_octave_vars = []
    track_octave_memory = {}

    def update_track_names_table(*args):
        # Save current names and octaves to memory
        for idx, var in enumerate(track_name_vars):
            track_name_memory[idx] = var.get()
        for idx, var in enumerate(track_octave_vars):
            track_octave_memory[idx] = var.get()
        # Clear previous widgets
        for widget in track_names_inner.winfo_children():
            widget.destroy()
        track_name_vars.clear()
        track_octave_vars.clear()
        # Add new widgets, keeping previous names and octaves if possible (even if empty)
        for i in range(num_tracks_var.get()):
            ttk.Label(track_names_inner, text=f"Track {i+1}:").grid(row=i, column=0, sticky="w")
            prev_name = track_name_memory.get(i, f"Track {i+1}")
            name_var = tk.StringVar(value=prev_name)
            def save_var(idx=i, v=name_var):
                track_name_memory[idx] = v.get()
            name_var.trace_add("write", lambda *a, idx=i, v=name_var: save_var(idx, v))
            entry = ttk.Entry(track_names_inner, textvariable=name_var, width=15)
            entry.grid(row=i, column=1, pady=2)
            track_name_vars.append(name_var)

            # Octave dropdown
            prev_octave = track_octave_memory.get(i, "4")
            octave_var = tk.StringVar(value=prev_octave)
            octave_menu = ttk.Combobox(track_names_inner, textvariable=octave_var, values=[str(o) for o in range(1, 7)], width=3, state="readonly", style="info.TCombobox")
            octave_menu.grid(row=i, column=2, padx=5)
            track_octave_vars.append(octave_var)
            def save_octave(idx=i, v=octave_var):
                track_octave_memory[idx] = v.get()
            octave_var.trace_add("write", lambda *a, idx=i, v=octave_var: save_octave(idx, v))

    # Update table when number of tracks changes
    num_tracks_var.trace_add("write", lambda *args: update_track_names_table())
    update_track_names_table()

    # Define check_probabilities before using it
    def check_probabilities():
        total = sum(excerpt.probability for excerpt in excerpts)
        if abs(total - 1.0) < 1e-6:
            status_box.config(text="Probabilities sum to 1!", bootstyle="success")
        else:
            status_box.config(text=f"Sum is {total:.4f} (should be 1)", bootstyle="danger")

    # --- Place generate button and status/message box immediately below the settings box ---
    generate_btn = ttk.Button(settings_frame, text="Generate", command=check_probabilities, bootstyle="primary")
    generate_btn.grid(row=4, column=0, columnspan=2, pady=(15, 2), sticky="ew")

    status_box = ttk.Label(settings_frame, text="", width=30, font=("Arial", 10), anchor="center")
    status_box.grid(row=5, column=0, columnspan=2, pady=(0, 2), sticky="ew")

    # Only allow the table to expand vertically, not horizontally
    main_frame.columnconfigure(0, weight=0)
    main_frame.columnconfigure(1, weight=0)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=0)

    root.mainloop()