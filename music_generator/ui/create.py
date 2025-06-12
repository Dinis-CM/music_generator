import tkinter as tk
import ttkbootstrap as ttk
from music_generator.structures import Track
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE
from music_generator.structures.probability_presets import PROBABILITY_PRESETS_TABLE
from music_generator.files import generate


def create_window(width, height, title, composition=None, tracks=None):
    '''
    Creates the main application window with a notebook for tracks and controls for composition settings.

    The window is divided into a grid:

    _______________________________________________________
    |                      Title                          |
    |_____________________________________________________|
    | Notebook (Tracks) | Controls (Composition Settings) |
    |_____________________________________________________|
    |                      Footer                         |
    _______________________________________________________

    Parameters:
    - width (int): Width of the window.
    - height (int): Height of the window.
    - title (str): Title of the window.
    - composition (Composition): The composition object to be edited.
    - tracks (list of Track): List of tracks to be displayed in the notebook.
    Returns:
    - root (ttk.Window): The main application window.
    - composition (Composition): The composition object with updated settings.
    - tracks (list of Track): The list of tracks with updated settings.
    '''

    # Window settings
    root = ttk.Window(themename="darkly")
    root.title(title)
    root.geometry(f"{width}x{height}")
    root.resizable(True, True)
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    
    #Window has only the main frame inside
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    main_frame.rowconfigure(0, weight=0)  # Title
    main_frame.rowconfigure(1, weight=1)  # Notebook & Controls
    main_frame.rowconfigure(2, weight=0)  # Footer
    main_frame.columnconfigure(0, weight=2)  # 2/3 for notebook
    main_frame.columnconfigure(1, weight=1)  # 1/3 for controls

    # Title and footer labels
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

    # Controls settings
    controls_frame = ttk.Frame(main_frame, width=width//3)
    controls_frame.grid(row=1, column=1, sticky="nsew", padx=10)
    controls_frame.grid_propagate(False)
    controls_frame.rowconfigure(0, weight=1)  
    controls_frame.columnconfigure(0, weight=1)
    composition = create_controls(controls_frame, composition, tracks)

    return root, composition, tracks

def create_notebook(frame, composition=None, tracks=None):
    '''
    Creates a notebook widget with tabs for each track.
    Each tab contains controls for setting the track's octave, instrument, and probabilities.
    
    Parameters:
    - frame (ttk.Frame): The frame where the notebook will be placed.
    - composition (Composition): The composition object to be edited.
    - tracks (list of Track): List of tracks to be displayed in the notebook.
    
    Returns:
    - notebook (ttk.Notebook): The notebook widget containing the track tabs.
    - tracks (list of Track): The list of tracks with updated settings.
    '''

    notebook = ttk.Notebook(frame)
    for i in range(len(tracks)):
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text=f'Track {i+1}')  # Add tab first
        create_notebook_tab(notebook, tab_frame, tracks, i)
    
    return notebook, tracks

def create_controls(master, composition, tracks):
    '''
    Creates the controls for the composition settings, including name, BPM, length, and track count.
    
    Parameters:
    - master (ttk.Frame): The frame where the controls will be placed.
    - composition (Composition): The composition object to be edited.
    - tracks (list of Track): List of tracks to be displayed in the controls.
    
    Returns:
    - composition (Composition): The composition object with updated settings.
    '''

    composition = create_boxes(master, composition)
    composition = create_button(master, composition, tracks)
    return composition
    

def create_notebook_tab(Notebook, frame, track, idx):
    '''
    Creates a tab in the notebook for a specific track. Each tab contains controls for setting the track's octave, instrument, and probabilities.

    Parameters:
    - Notebook (ttk.Notebook): The notebook widget where the tab will be added.
    - frame (ttk.Frame): The frame where the tab content will be placed.
    - track (list of Track): List of tracks to be displayed in the tab.
    - idx (int): The index of the track in the list.       
    '''

    # Set up the frame with a canvas and scrollbar for scrolling content
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    canvas = tk.Canvas(frame, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Content frame inside the canva
    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw", tags="content_frame")

    # Ensure the canvas scrollregion updates with content
    content_frame.bind("<Configure>", lambda event: update_canvas_size(event, canvas))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("content_frame", width=canvas.winfo_width()))

    # Center all content in the notebook tab
    inner = ttk.Frame(content_frame)
    inner.pack(anchor="center", padx=15, pady=10, fill="both", expand=True)

    # Create the track controls
    track[idx].set_discrete_uniform_probabilities()
    create_octave_list(inner, "Set Octave", track[idx])
    create_instrument_list(inner, "Set Instrument", track[idx])
    preset_menu = create_probability_list(inner, "Set probabilities", track[idx])
    prob_bars, prob_entries = create_probability_table(inner, track[idx])

    # Add preset commands to the menu
    for preset_name in PROBABILITY_PRESETS_TABLE.keys():
        preset_menu.add_command(
            label=preset_name,
            command=lambda val=preset_name: apply_preset(val, prob_entries, prob_bars, track[idx])
        )


def create_octave_list(frame, title, track):
    '''
    Creates a dropdown menu for selecting the octave of a track.
    Parameters:
    - frame (ttk.Frame): The frame where the dropdown will be placed.
    - title (str): The title for the dropdown menu.
    - track (Track): The track object for which the octave is being set.
    '''

    # Create a row with a label and a dropdown menu for octave selection'''
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))
    selected = ttk.StringVar(value=track.octave)

    # List of octaves from 0 to 7
    menubutton = ttk.Menubutton(row, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)
    
    for oct in range(8):
        menu.add_command(label=oct,command=lambda val=oct: update_octave(val, selected, track))
    
    menubutton["menu"] = menu
    menubutton.pack(side='left')

def create_instrument_list(frame, title, track):
    '''
    Creates a dropdown menu for selecting the instrument of a track.
    Parameters:
    - frame (ttk.Frame): The frame where the dropdown will be placed.
    - title (str): The title for the dropdown menu.
    - track (Track): The track object for which the instrument is being set.
    '''
    
    # Create a row with a label and a dropdown menu for instrument selection
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))
    selected = ttk.StringVar(value="Piano")
    
    # Create a menubutton with a menu containing all instruments
    # The menu will be populated with categories and instruments from MIDI_INSTRUMENT_TABLE
    menubutton = ttk.Menubutton(row, textvariable=selected)
    menu = tk.Menu(menubutton, tearoff=0)
    
    for categories, instruments in MIDI_INSTRUMENT_TABLE.items():
        if not instruments:
            continue
        submenu = tk.Menu(menu, tearoff=0)
        for inst_name, _ in instruments:
            submenu.add_command(label=inst_name,command=lambda name=inst_name: update_instrument(name, selected, track))
        menu.add_cascade(label=categories, menu=submenu)
    
    menubutton["menu"] = menu
    menubutton.pack(side='left')

def create_probability_list(frame, title, track):
    '''
    Creates a dropdown menu for applying probability presets to a track.
    Parameters:
    - frame (ttk.Frame): The frame where the dropdown will be placed.
    - title (str): The title for the dropdown menu.
    - track (Track): The track object for which the probabilities are being set.
    Returns:
    - preset_menu (tk.Menu): The menu containing the probability presets.
    '''

    # Create a row with a label and a menubutton for probability presets
    row = ttk.Frame(frame)
    row.pack(anchor='w', pady=5)
    text_label = ttk.Label(row, text=title)
    text_label.pack(side='left', padx=(0, 10))

    # Create the menubutton with a menu for probability presets
    preset_menu = tk.Menu(frame, tearoff=0)
    menubutton = ttk.Menubutton(row, text="Probability Presets", menu=preset_menu)
    menubutton.pack(side='left', padx=(0, 10))

    # Options added after table is created

    return preset_menu

def create_probability_table(parent, track):
    '''
    Creates a table for displaying and editing the probabilities of excerpts in a track.
    Each row contains:
    - A label for the excerpt name
    - An entry for editing the probability value
    - A progress bar for visualizing the probability value
    Parameters:
    - parent (ttk.Frame): The frame where the table will be placed.
    - track (Track): The track object containing the excerpts and their probabilities.
    Returns:
    - prob_bars (list): List of progress bars for each excerpt.
    - prob_entries (list): List of StringVars for each excerpt's probability entry.
    '''
    
    # Initialize lists to store labels, entries, and progress bars
    excerpt_labels = []
    prob_entries = []
    prob_bars = []

    # Create an outer frame to hold the excerpt rows
    outer_frame = ttk.LabelFrame(parent, borderwidth=2, relief="groove", text="")
    outer_frame.pack(pady=10, fill='x', expand=True)  

    # Create a row for each excerpt in the track
    for i, excerpt in enumerate(track.input_excerpts.excerpts):

        # Create a row frame for each excerpt
        row_frame = ttk.Frame(outer_frame)
        row_frame.pack(fill='x', expand=True, pady=2) 

        # Create a label for each excerpt
        label = ttk.Label(row_frame, text=str(excerpt.name).replace('_', ' ').title(), width=20, anchor='w')
        label.pack(side='left', padx=5)

        # Create an entry for editing the probability value
        prob_var = ttk.StringVar(value=str(track.probabilities[i]))
        entry = ttk.Entry(row_frame, textvariable=prob_var, width=5)
        entry.pack(side='left', padx=5)

        # Create a progress bar for visualizing the probability value
        bar = ttk.Progressbar(row_frame, orient='horizontal', mode='determinate')
        bar['maximum'] = 1.0
        bar['value'] = track.probabilities[i]
        bar.pack(side='left', padx=5, fill='x', expand=True)
        prob_bars.append(bar)
        prob_entries.append(prob_var)
        excerpt_labels.append(label)

        # Bind the entry to update the probability value in the track when edited
        prob_var.trace_add('write',
         lambda *args, var=prob_var, idx=i: update_probability(var, idx, prob_bars, track))
        
    return prob_bars, prob_entries

def create_boxes(master, composition):
    '''
    Creates the input boxes for the composition settings, including name, BPM, length, and track count.
    Parameters:
    - master (ttk.Frame): The frame where the input boxes will be placed. 
    - composition (Composition): The composition object to be edited.
    Returns:
    - composition (Composition): The composition object with updated settings.
    '''

    # Create an outer frame to hold the input boxes
    outer_frame = ttk.Frame(master)
    outer_frame.grid(row=0, column=0, pady=20, sticky="ew")
    outer_frame.grid_columnconfigure(0, weight=1)

    # Create composition name box
    row1 = ttk.Frame(outer_frame)
    row1.grid(row=0, column=0, sticky="ew", pady=5)
    row1.grid_columnconfigure(0, weight=1)
    name_label = ttk.Label(row1, text="Composition Name:")
    name_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    name_var = ttk.StringVar(value=composition.name)
    name_entry = ttk.Entry(row1, textvariable=name_var)
    name_entry.grid(row=1, column=0, sticky="ew")  

    # Create the composition tempo box
    row2 = ttk.Frame(outer_frame)
    row2.grid(row=1, column=0, sticky="ew", pady=5)
    row2.grid_columnconfigure(0, weight=1)
    bpm_label = ttk.Label(row2, text="BPM:")
    bpm_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    bpm_var = ttk.StringVar(value=str(composition.bpm))
    bpm_entry = ttk.Entry(row2, textvariable=bpm_var)
    bpm_entry.grid(row=1, column=0, sticky="ew")  # Below the label

    # Create the composition length box
    row3 = ttk.Frame(outer_frame)
    row3.grid(row=2, column=0, sticky="ew", pady=5)
    row3.grid_columnconfigure(0, weight=1)
    length_label = ttk.Label(row3, text="Composition Length:")
    length_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
    length_var = ttk.StringVar(value=str(composition.length))
    length_entry = ttk.Entry(row3, textvariable=length_var)
    length_entry.grid(row=1, column=0, sticky="ew")  # Below the label

    # Create the number of tracks box
    row4 = ttk.Frame(outer_frame)
    row4.grid(row=3, column=0, sticky="ew", pady=5)
    text_label = ttk.Label(row4, text="Number of Tracks")
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

    # Store the StringVars
    composition._name_var = name_var
    composition._bpm_var = bpm_var
    composition._length_var = length_var

    return composition

def create_button(master, Composition, Tracks):
    '''
    Creates a button to generate the composition based on the settings and tracks.
    Parameters:
    - master (ttk.Frame): The frame where the button will be placed.
    - Composition (Composition): The composition object to be edited.
    '''

    # Create an outer frame to hold the button and status box
    outer_frame = ttk.Frame(master)
    outer_frame.grid(row=1, column=0, pady=20, sticky="ew")
    outer_frame.grid_columnconfigure(0, weight=1)

    # Create a status box to display messages
    status_box = ttk.Label(outer_frame, text="", width=30, font=("Arial", 10), anchor="center", justify="center")
    status_box.grid(row=0, column=0, pady=5, columnspan=2, sticky="ew")

    # Create a button to generate the composition
    export_button = ttk.Button(outer_frame, text="Generate Composition", command=lambda: generate_button_pressed(Tracks, Composition, status_box), bootstyle="primary")
    export_button.grid(row=1, column=0, sticky="ew", padx=5)


def update_canvas_size(event, canvas):
    '''
    Updates the canvas scroll region and content frame width when the content frame is resized.
    '''
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig("content_frame", width=canvas.winfo_width())

def update_octave(oct, selected, track):
    '''
    Updates the octave of a track and adjusts the selected value in the dropdown menu.'''
    selected.set(str(oct))
    track.set_octave(oct)

def update_instrument(name, selected, track):
    '''
    Updates the instrument of a track and adjusts the selected value in the dropdown menu.
    '''
    selected.set(name)
    track.set_name(name)

def apply_preset(preset_name, prob_entries, prob_bars, track):
    '''
    Applies a probability preset to the track and updates the entries and bars accordingly.
    '''
    preset_func = PROBABILITY_PRESETS_TABLE.get(preset_name)
    if not preset_func:
        ttk.messagebox.showerror("Error", "Unknown preset")
        return
    preset_func(track)
    for i, v in enumerate(track.probabilities):
        prob_entries[i].set(str(round(v, 4)))
        prob_bars[i]['value'] = v

def update_probability(var, idx, prob_bars, track):
    '''
    Updates the probability value of a track excerpt based on the entry field input.
    '''
    val_str = var.get()
    if val_str.strip() == "":
        prob_bars[idx]['value'] = 0
        track.probabilities[idx] = 0
        return
    try:
        val = float(val_str)
        if val < 0:
            val = 0
        elif val > 1:
            val = 1
        track.probabilities[idx] = val
        prob_bars[idx]['value'] = val
        var.set(str(val)) 
    except:
        pass

def generate_button_pressed(Tracks, Composition, status_box):
    '''
    Generates the composition based on the settings and tracks when the button is pressed.
    '''
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







