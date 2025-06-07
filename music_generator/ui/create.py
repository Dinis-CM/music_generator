import tkinter as tk
import ttkbootstrap as ttk
from music_generator.structures import Track
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE
from music_generator.structures.probability_presets import PROBABILITY_PRESETS_TABLE
from music_generator.files import generate


def create_window(height, width, title):
    root = ttk.Window(themename="darkly")
    root.title(title)
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    return root

def create_notebook(master, composition, tracks):
    
    notebook = ttk.Notebook(master)
    Frames = [ttk.Frame(notebook) for _ in range(composition.max_tracks)]
    
    for i in range(len(tracks)):
        create_notebook_tab(notebook, Frames, tracks, i)
    
    notebook.pack(pady=20)
    return notebook, tracks

def create_notebook_tab(Notebook, frame, track, idx):
    Notebook.add(frame[idx], text=f'Track {idx+1}')
    track[idx].set_discrete_uniform_probabilities()
    create_octave_list(frame[idx], "Set Octave", track[idx])
    create_instrument_list(frame[idx], "Set Instrument", track[idx])
    prob_bars, prob_entries = create_probability_table(frame[idx], track[idx])
    create_probability_preset_menu(frame[idx], track[idx], prob_bars, prob_entries)

def create_octave_list(frame, title, track):
    text_label = ttk.Label(frame, text=title)
    text_label.pack()

    selected = ttk.StringVar(value=track.octave)

    def option_octave(oct):
        selected.set(str(oct))
        track.set_octave(oct)

    menubutton = ttk.Menubutton(frame, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)

    for oct in range(8):
        menu.add_command(label=oct,command=lambda val=oct: option_octave(val))
    menubutton["menu"] = menu
    menubutton.pack(pady=20)

def create_instrument_list(frame, title, track):
    text_label = ttk.Label(frame, text=title)
    text_label.pack()

    selected = ttk.StringVar(value="Piano")

    def option_instrument(name):
        selected.set(name)
        track.set_name(name)

    menubutton = ttk.Menubutton(frame, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)

    for categories, instruments in MIDI_INSTRUMENT_TABLE.items():
        if not instruments:
            continue
        submenu = tk.Menu(menu, tearoff=0)
        for inst_name, _ in instruments:
            submenu.add_command(label=inst_name,command=lambda name=inst_name: option_instrument(name))
        menu.add_cascade(label=categories, menu=submenu)

    menubutton["menu"] = menu
    menubutton.pack(pady=20)

def create_probability_table(parent, track):
    outer_frame = ttk.Frame(parent) 
    outer_frame.pack(pady=10, fill='both', expand=True)

    canvas = tk.Canvas(outer_frame, height=220)
    scrollbar = ttk.Scrollbar(outer_frame, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    excerpt_labels = []
    prob_entries = []
    prob_bars = []

    for i, excerpt in enumerate(track.input_excerpts.excerpts):
        row_frame = ttk.Frame(scrollable_frame) 
        row_frame.pack(fill='x', pady=2)

        label = ttk.Label(row_frame, text=str(excerpt.name).replace('_', ' ').title(), width=20, anchor='w')
        label.pack(side='left', padx=5)
        excerpt_labels.append(label)

        prob_var = ttk.StringVar(value=str(track.probabilities[i]))
        entry = ttk.Entry(row_frame, textvariable=prob_var, width=5)
        entry.pack(side='left', padx=5)
        prob_entries.append(prob_var)

        bar = ttk.Progressbar(row_frame, orient='horizontal', length=100, mode='determinate')
        bar['maximum'] = 1.0
        bar['value'] = track.probabilities[i]
        bar.pack(side='left', padx=5)
        prob_bars.append(bar)

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

def create_probability_preset_menu(frame, track, prob_bars, prob_entries):
    def apply_preset(preset_name):
        preset_func = PROBABILITY_PRESETS_TABLE.get(preset_name)
        if not preset_func:
            ttk.messagebox.showerror("Error", "Unknown preset")
            return
        preset_func(track)
        for i, v in enumerate(track.probabilities):
            prob_entries[i].set(str(round(v, 4)))
            prob_bars[i]['value'] = v

    preset_menu = tk.Menu(frame, tearoff=0)
    for preset_name in PROBABILITY_PRESETS_TABLE.keys():
        preset_menu.add_command(label=preset_name, command=lambda val=preset_name: apply_preset(val))

    menubutton = ttk.Menubutton(frame, text="Probability Presets", menu=preset_menu)
    menubutton.pack(pady=10)

def create_boxes(master, composition):
    outer_frame = ttk.Frame(master)
    outer_frame.pack(pady=20, fill='both', expand=True)

    name_var = ttk.StringVar(value=composition.name)
    bpm_var = ttk.StringVar(value=str(composition.bpm))
    length_var = ttk.StringVar(value=str(composition.length))

    name_label = ttk.Label(outer_frame, text="Composition Name:")
    name_label.pack()
    name_entry = ttk.Entry(outer_frame, textvariable=name_var)
    name_entry.pack(pady=5)

    bpm_label = ttk.Label(outer_frame, text="BPM:")
    bpm_label.pack()
    bpm_entry = ttk.Entry(outer_frame, textvariable=bpm_var)
    bpm_entry.pack(pady=5)

    length_label = ttk.Label(outer_frame, text="Composition Length:")
    length_label.pack()
    length_entry = ttk.Entry(outer_frame, textvariable=length_var)
    length_entry.pack(pady=5)

    text_label = ttk.Label(outer_frame, text="Tracks")
    text_label.pack()

    selected = ttk.StringVar(value=composition.max_tracks)

    def option_track(opt):
        selected.set(str(opt+1))
        composition.set_max_tracks(opt+1)

    menubutton = ttk.Menubutton(outer_frame, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)

    for opt in range(6):
        menu.add_command(label=opt+1,command=lambda val=opt: option_track(val))
    menubutton["menu"] = menu
    menubutton.pack(pady=20)

    # Store the StringVars for later use
    composition._name_var = name_var
    composition._bpm_var = bpm_var
    composition._length_var = length_var

    return composition

def create_button(master, Composition, Tracks):
    outer_frame = ttk.Frame(master)
    outer_frame.pack(pady=20)

    status_box = ttk.Label(outer_frame, text="", width=30, font=("Arial", 10), anchor="center")
    status_box.pack(pady=5)

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
    export_button.pack()










