import os
from music_generator.structures import Excerpt, ExcerptCollection, NoteMessage
from mido import MidiFile

def import_excerpts(folder_path):
    input_excerpts = ExcerptCollection("Input_Excerpts")
    input_excerpts.add_silence_excerpt()

    for x in sorted(os.listdir(folder_path)):  # Sort files alphabetically
        if x.endswith(".mid"):
            excerpt = Excerpt(x[:-4])
            mid = MidiFile(os.path.join(folder_path, x)) 
            print(mid, file=open('debug/debug_input.txt', mode='w'))     
            for track in mid.tracks:
                for msg in track:
                    if msg.type == 'note_on' or msg.type == 'note_off':
                        excerpt.add_message(NoteMessage(msg))      
            excerpt.normalize()
            excerpt.pad_length()
            input_excerpts.add_excerpt(excerpt)
    return input_excerpts







