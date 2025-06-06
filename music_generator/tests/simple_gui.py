from music_generator import *
import tkinter as tk
import ttkbootstrap as ttk

def simple_gui_test():

    input_excerpts=import_excerpts("input")

    root = create_window(600, 800, "Music Generator Test GUI")
    Notebook, Tracks = create_notebook(root, input_excerpts)

    root.mainloop()