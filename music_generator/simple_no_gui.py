import random
from music_generator import import_excerpts, Composition, Track, export_file

def simple_no_gui_test():
    input_excerpts = import_excerpts("input")
    length = int(input("Enter the desired excerpt length: "))
    number_tracks = int(input("Enter the number of tracks to include in the excerpt: "))


    composition = Composition("Generated_Excerpt")
    composition.set_bpm(80) 

    for n in range(number_tracks):
        name = ['Bassoon', 'French Horn', 'Clarinet','Flute']
        track = Track()
        track.set_probabilities([getattr(e, "probability", 1/len(input_excerpts.excerpts)) for e in input_excerpts.excerpts])
        for chosen_excerpt in random.choices(input_excerpts.excerpts, weights=track.probabilities, k=length): 
            track.add_excerpt(chosen_excerpt)        
        track.fix_octave(n+2)
        track.set_name(name[n])
        composition.add_track(track)

    export_file("output/excerpt.mid", composition)