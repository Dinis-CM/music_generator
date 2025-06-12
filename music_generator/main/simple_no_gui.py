import random
import os
from music_generator import import_excerpts, Composition, Track, export_file

def simple_no_gui_test():
    '''Simple no GUI test for the music generator application.'''

    # Initialize all necessary folders and classes
    input_excerpts = import_excerpts("input")
    length = int(input("Enter the desired excerpt length: "))
    number_tracks = int(input("Enter the number of tracks to include in the excerpt: "))

    #Initialize the composition
    composition = Composition("Generated_Excerpt")
    composition.set_bpm(80) 

    # Create test tracks and add excerpts
    for n in range(number_tracks):
        name = ['Bassoon', 'French Horn', 'Clarinet','Flute']
        track = Track(input_excerpts=input_excerpts.excerpts)
        track.set_discrete_uniform_probabilities()
        print(track.probabilities)
        for chosen_excerpt in random.choices(input_excerpts.excerpts, weights=track.probabilities, k=length): 
            track.add_excerpt(chosen_excerpt)        
        track.set_octave(n+2)
        track.set_name(name[n])
        composition.add_track(track)
    
    # Export the composition to a MIDI file
    file_path = os.path.join("output", f"{composition.name}.mid")
    export_file(file_path, composition)