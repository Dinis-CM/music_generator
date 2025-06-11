from music_generator import Composition, Track, import_excerpts, create_window
import tkinter as tk
import ttkbootstrap as ttk
import os

def simple_gui_test():

    composition=Composition()
    for folder in ["input", "output", "debug"]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    input_excerpts=import_excerpts(os.path.join("input"))
    
    tracks = [Track(f"Track {i+1}", input_excerpts) for i in range(composition.max_tracks)]

    root, composition, tracks = create_window(800, 500, "Music Generator Test GUI", composition, tracks)

    root.mainloop()