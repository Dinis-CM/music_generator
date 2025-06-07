from music_generator import *
import tkinter as tk
import ttkbootstrap as ttk

def simple_gui_test():

    composition=Composition()

    input_excerpts=import_excerpts("input")
    
    tracks = [Track(f"Track {i+1}", input_excerpts) for i in range(composition.max_tracks)]

    root = create_window(1000, 1000, "Music Generator Test GUI")
    _, tracks = create_notebook(root, composition, tracks)
    composition = create_boxes(root, composition)
    composition = create_button(root, composition, tracks)
    

    root.mainloop()