import tkinter as tk
import ttkbootstrap as ttk
from music_generator.structures import Track
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE
from music_generator.structures.probability_presets import PROBABILITY_PRESETS_TABLE
from music_generator.files import generate


def create_window(width, height, title, composition=None, tracks=None):
    # Window settings
    root = ttk.Window(themename="darkly")
    root.title(title)
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=0)  # Title
    main_frame.rowconfigure(1, weight=1)  # Notebook & Controls (expand vertically)
    main_frame.rowconfigure(2, weight=0)  # Footer
    main_frame.columnconfigure(0, weight=2)  # 2/3 for notebook
    main_frame.columnconfigure(1, weight=1)  # 1/3 for controls

    title_label = ttk.Label(main_frame, text="Music Generator", font=("Arial", 20, "bold"), anchor="center", justify="center")
    title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew", columnspan=2)

    footer_label = ttk.Label(main_frame, text="Dinis Marques | 2025 | MMat, IST", font=("Arial", 10), anchor="center", justify="center")
    footer_label.grid(row=2, column=0, pady=(20, 10), sticky="nsew", columnspan=2)

    # Notebook settings
    notebook_frame = ttk.Frame(main_frame, width=(2*width)//3)
    notebook_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    notebook_frame.grid_propagate(False)
    notebook_frame.rowconfigure(0, weight=1)
    notebook_frame.columnconfigure(0, weight=1)

    notebook, tracks = create_notebook(notebook_frame, composition, tracks)
    notebook.grid(row=0, column=0, sticky="nsew")

    # Controls settings (to the right of notebook)
    controls_frame = ttk.Frame(main_frame, width=width//3)
    controls_frame.grid(row=1, column=1, sticky="nsew", padx=10)
    controls_frame.grid_propagate(False)
    controls_frame.rowconfigure(0, weight=1)  
    controls_frame.columnconfigure(0, weight=1)

    composition = create_controls(controls_frame, composition, tracks)

    # Center everything in main_frame columns
    main_frame.grid_columnconfigure(0, weight=2)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=0)
    main_frame.grid_rowconfigure(1, weight=1)  # This is crucial for vertical expansion

    return root, composition, tracks

def create_notebook(frame, composition=None, tracks=None):
    notebook = ttk.Notebook(frame)
    for i in range(len(tracks)):
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text=f'Track {i+1}')  # Add tab first
        create_notebook_tab(notebook, tab_frame, tracks, i)
    return notebook, tracks

def create_controls(master, composition, tracks):
    composition = create_boxes(master, composition)
    composition = create_button(master, composition, tracks)
    return composition
    

# Center content in notebook tabs
def create_notebook_tab(Notebook, frame, track, idx):
    # Make the tab frame expand
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    # Canvas + scrollbar inside the tab frame
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Content frame inside the canvas
    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="content_frame")

    # Ensure the canvas scrollregion updates with content
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Make content_frame width match the canvas width
        canvas.itemconfig("content_frame", width=canvas.winfo_width())
    content_frame.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("content_frame", width=canvas.winfo_width()))

    # Center all content in the notebook tab
    inner = ttk.Frame(content_frame)
    inner.pack(anchor="center", padx=15, pady=10, fill="both", expand=True)

    track[idx].set_discrete_uniform_probabilities()
    create_octave_list(inner, "Set Octave", track[idx])
    create_instrument_list(inner, "Set Instrument", track[idx])

    # Create probability preset selector above the table and get the menu/apply_preset
    preset_menu, apply_preset = create_probability_list(inner, "Set probabilities", track[idx])
    # Now create the table and get the widgets
    prob_bars, prob_entries = create_probability_table(inner, track[idx])

    # Now add the preset commands, connecting them to the actual widgets
    for preset_name in PROBABILITY_PRESETS_TABLE.keys():
        preset_menu.add_command(
            label=preset_name,
            command=lambda val=preset_name: apply_preset(val, prob_entries, prob_bars)
        )

    # Probability Table (already fills width, but you can center its content if needed)
    # If you want the table itself to be centered and not stretched, change fill='x' to anchor='center' in create_probability_table

    # Mousewheel scroll for tab content only
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

def create_octave_list(frame, title, track):
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))
    selected = ttk.StringVar(value=track.octave)
    def option_octave(oct):
        selected.set(str(oct))
        track.set_octave(oct)
    menubutton = ttk.Menubutton(row, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)
    for oct in range(8):
        menu.add_command(label=oct,command=lambda val=oct: option_octave(val))
    menubutton["menu"] = menu
    menubutton.pack(side='left')

def create_instrument_list(frame, title, track):
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))
    selected = ttk.StringVar(value="Piano")
    
    def option_instrument(name):
        selected.set(name)
        track.set_name(name)

    menubutton = ttk.Menubutton(row, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)
    for categories, instruments in MIDI_INSTRUMENT_TABLE.items():
        if not instruments:
            continue
        submenu = tk.Menu(menu, tearoff=0)
        for inst_name, _ in instruments:
            submenu.add_command(label=inst_name,command=lambda name=inst_name: option_instrument(name))
        menu.add_cascade(label=categories, menu=submenu)
    menubutton["menu"] = menu
    menubutton.pack(side='left')

def create_probability_list(frame, title, track):
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))

    # This function will be connected to the menu after the table is created
    def apply_preset(preset_name, prob_entries, prob_bars):
        preset_func = PROBABILITY_PRESETS_TABLE.get(preset_name)
        if not preset_func:
            ttk.messagebox.showerror("Error", "Unknown preset")
            return
        preset_func(track)
        for i, v in enumerate(track.probabilities):
            prob_entries[i].set(str(round(v, 4)))
            prob_bars[i]['value'] = v

    preset_menu = tk.Menu(frame, tearoff=0)
    # We'll add commands after table creation
    menubutton = ttk.Menubutton(row, text="Probability Presets", menu=preset_menu)
    menubutton.pack(side='left', padx=(0, 10))

    return preset_menu, apply_preset

# Remove scrollable from probability table
def create_probability_table(parent, track):
    # Use a LabelFrame for an outline (no title)
    outer_frame = ttk.LabelFrame(parent, borderwidth=2, relief="groove", text="")
    outer_frame.pack(pady=10, fill='x', expand=True)  # Fill horizontally

    excerpt_labels = []
    prob_entries = []
    prob_bars = []

    for i, excerpt in enumerate(track.input_excerpts.excerpts):
        row_frame = ttk.Frame(outer_frame)
        row_frame.pack(fill='x', expand=True, pady=2)  # Fill horizontally

        label = ttk.Label(row_frame, text=str(excerpt.name).replace('_', ' ').title(), width=20, anchor='w')
        label.pack(side='left', padx=5)

        prob_var = ttk.StringVar(value=str(track.probabilities[i]))
        entry = ttk.Entry(row_frame, textvariable=prob_var, width=5)
        entry.pack(side='left', padx=5)

        # Make the progress bar expand to fill remaining space
        bar = ttk.Progressbar(row_frame, orient='horizontal', mode='determinate')
        bar['maximum'] = 1.0
        bar['value'] = track.probabilities[i]
        bar.pack(side='left', padx=5, fill='x', expand=True)
        prob_bars.append(bar)
        prob_entries.append(prob_var)
        excerpt_labels.append(label)

        def on_prob_change(var=prob_var, idx=i):
            val_str = var.get()
            if val_str.strip() == "":
                prob_bars[idx]['value'] = 0
                track.probabilities[idx] = 0
                return
            try:
                val = float(val_str)
                if 0 <= val <= 1:
                    track.probabilities[idx] = val
                    prob_bars[idx]['value'] = val
            except ValueError:
                pass

        prob_var.trace_add('write', lambda *args, var=prob_var, idx=i: on_prob_change(var, idx))
    return prob_bars, prob_entries

# Center controls content
def create_boxes(master, composition):
    outer_frame = ttk.Frame(master)
    outer_frame.grid(row=0, column=0, pady=20, sticky="ew")
    outer_frame.grid_columnconfigure(0, weight=1)

    # Name
    row1 = ttk.Frame(outer_frame)
    row1.grid(row=0, column=0, sticky="ew", pady=5)
    row1.grid_columnconfigure(0, weight=1)
    name_label = ttk.Label(row1, text="Composition Name:")
    name_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    name_var = ttk.StringVar(value=composition.name)
    name_entry = ttk.Entry(row1, textvariable=name_var)
    name_entry.grid(row=1, column=0, sticky="ew")  # Below the label

    # BPM
    row2 = ttk.Frame(outer_frame)
    row2.grid(row=1, column=0, sticky="ew", pady=5)
    row2.grid_columnconfigure(0, weight=1)
    bpm_label = ttk.Label(row2, text="BPM:")
    bpm_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    bpm_var = ttk.StringVar(value=str(composition.bpm))
    bpm_entry = ttk.Entry(row2, textvariable=bpm_var)
    bpm_entry.grid(row=1, column=0, sticky="ew")  # Below the label

    # Length
    row3 = ttk.Frame(outer_frame)
    row3.grid(row=2, column=0, sticky="ew", pady=5)
    row3.grid_columnconfigure(0, weight=1)
    length_label = ttk.Label(row3, text="Composition Length:")
    length_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    length_var = ttk.StringVar(value=str(composition.length))
    length_entry = ttk.Entry(row3, textvariable=length_var)
    length_entry.grid(row=1, column=0, sticky="ew")  # Below the label

    # Tracks (side by side, not full row)
    row4 = ttk.Frame(outer_frame)
    row4.grid(row=3, column=0, sticky="ew", pady=5)
    text_label = ttk.Label(row4, text="Tracks")
    text_label.pack(side="left", padx=(0, 10))
    selected = ttk.StringVar(value=composition.max_tracks)
    def option_track(opt):
        selected.set(str(opt+1))
        composition.set_max_tracks(opt+1)
    menubutton = ttk.Menubutton(row4, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)
    for opt in range(6):
        menu.add_command(label=opt+1,command=lambda val=opt: option_track(val))
    menubutton["menu"] = menu
    menubutton.pack(side="left")

    # Store the StringVars for later use
    composition._name_var = name_var
    composition._bpm_var = bpm_var
    composition._length_var = length_var

    return composition

def create_button(master, Composition, Tracks):
    outer_frame = ttk.Frame(master)
    outer_frame.grid(row=1, column=0, pady=20, sticky="ew")
    outer_frame.grid_columnconfigure(0, weight=1)

    status_box = ttk.Label(outer_frame, text="", width=30, font=("Arial", 10), anchor="center", justify="center")
    status_box.grid(row=0, column=0, pady=5, columnspan=2, sticky="ew")

    def on_generate():
        print("Generate button pressed")  # Debug print
        for idx, track in enumerate(Tracks[:Composition.max_tracks]):
            if not track.check_probabilities():
                total = sum(track.probabilities)
                status_box.config(text=f"Sum in track {idx+1} {total:.4f} (should be 1)", bootstyle="danger")
                return 

        Composition.name = Composition._name_var.get()
        try:
            Composition.bpm = int(Composition._bpm_var.get())
        except ValueError:
            Composition.bpm = 120
        try:
            Composition.length = int(Composition._length_var.get())
        except ValueError:
            Composition.length = 16
        generate(Composition, Tracks)
        status_box.config(text="Track generated succesfully!", bootstyle="success")

    export_button = ttk.Button(outer_frame, text="Generate Composition", command=on_generate)
    export_button.grid(row=1, column=0, sticky="ew", padx=5)













