from music_generator import Composition, Track, import_excerpts, create_window
import tkinter as tk
import ttkbootstrap as ttk
import os


def simple_gui_test():
    '''Simple GUI test for the music generator application.
    This function initializes the GUI, sets up the composition and tracks, and starts the main event loop.
    '''

    # Initialize all necessary folders and classes
    composition=Composition()
    for folder in ["input", "output", "debug"]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    # Import excerpts from the input folder
    input_excerpts=import_excerpts(os.path.join("input"))


    tracks = [Track(f"Track {i+1}", input_excerpts) for i in range(composition.max_tracks)]

    # Create the main window
    root, composition, tracks = create_window(1200, 800, "Music Generator by Dinis Marques", composition, tracks)

    root.mainloop()