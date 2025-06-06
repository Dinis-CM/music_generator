import tkinter as tk
import ttkbootstrap as ttk
from music_generator.structures import Track
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE


def create_window(height, width, title):
    """
    Create a Tkinter window with the specified height, width, and title.
    """
    root = ttk.Window(themename="darkly")
    root.title(title)
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    return root

def create_notebook(master, input_excerpts):
    max_tracks = 6
    Notebook = ttk.Notebook(master)
    Tracks = [Track(f"Track {i+1}", input_excerpts) for i in range(max_tracks)]
    Frames = [ttk.Frame(Notebook) for _ in range(max_tracks)]
    
    for i in range(len(Tracks)):
        create_notebook_tab(Notebook, Frames, Tracks, i)
    
    Notebook.pack(pady=20)
    return Notebook, Tracks

def create_notebook_tab(Notebook, frame, track, idx):
    Notebook.add(frame[idx], text=f'Track {idx+1}')
    track[idx].set_discrete_uniform_probabilities()
    create_octave_list(frame[idx], "Set Octave", track[idx])
    create_instrument_list(frame[idx], "Set Instrument", track[idx])
    create_probability_table()
    create_probability_preset_list()

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

def create_probability_table():
    pass

def create_probability_preset_list():
    pass










