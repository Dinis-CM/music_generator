import os
from music_generator.structures import Excerpt, ExcerptCollection, NoteMessage
from mido import MidiFile



def import_excerpts(folder_path):
    
    """
    Imports all MIDI files in a folder and saves the excerpts.

    Parameters:
        folder_path: The path where the MIDI files are stored.

    Returns:
        input_excerpts: An ExcerptCollection containing all the imported excerpts.
    """

    # Create an ExcerptCollection to hold all the excerpts
    input_excerpts = ExcerptCollection("Input_Excerpts")

    # Add a silence excerpt to the collection
    input_excerpts.add_silence_excerpt()
    
    # Find all excerpt in all midi files in the specified folder
    for x in sorted(os.listdir(folder_path)): 

        if x.endswith(".mid"):
            
            #Create an Excerpt object for each MIDI file
            excerpt = Excerpt(x[:-4])
            mid = MidiFile(os.path.join(folder_path, x)) 

            # Print the MIDI file for debugging purposes
            print(mid, file=open(os.path.join("debug", "debug_input.txt"), mode='w', encoding="utf-8"))  

            # Iterate through all tracks in the MIDI file and add note messages to the excerpt
            for track in mid.tracks:
                for msg in track:
                    if msg.type == 'note_on' or msg.type == 'note_off':
                        excerpt.add_message(NoteMessage(msg))     

            # Make sure the excerpt is normalized and padded, so that it works correctly in the generator.
            excerpt.normalize()
            excerpt.pad_length()

            # Add the excerpt to the ExcerptCollection
            input_excerpts.add_excerpt(excerpt)
    return input_excerpts







