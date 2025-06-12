from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
import random
import os
import re

def generate(composition, tracks):

    """
    Generates an aleatoric composition based on the provided composition and tracks parameters.

    Parameters:
        composition: The composition object containing metadata and track information.
        tracks: A list of track objects, each containing excerpts and probabilities.
    
    Returns:
        None
    """

    # Clear previous generations
    composition.tracks = []
    for track in tracks:
        track.excerpts = []  

    # Generate excerpts for each track based on the probabilities
    for n in range(composition.max_tracks):
        chosen_excerpts = random.choices(tracks[n].input_excerpts.excerpts, weights=tracks[n].probabilities, k=composition.length)
        for chosen_excerpt in chosen_excerpts:
            tracks[n].add_excerpt(chosen_excerpt)        
        composition.add_track(tracks[n])

    # Set the name of the composition
    composition.name=re.sub(r'[^A-Za-z0-9_\-\.]', '_', composition.name)

    # Export the composition to a MIDI file
    file_path = os.path.join("output", f"{composition.name}.mid")
    export_file(file_path, composition)


def export_file(file_path, composition):
    
    """
    Exports a composition to a MIDI file.

    Parameters:
        file_path: The path where the MIDI file will be saved.
        composition: The composition object containing the tracks.

    Returns:
        None
    """
    
    mid = MidiFile()
    
    # Write messages for all tracks
    for t in composition.tracks:
        
        track = MidiTrack()
       
        if composition.tracks.index(t) == 0:
            # Add global meta messages required for the Midi File
            track = add_composition_meta_messages(track, composition)
        
        # Add track meta messages
        track = add_track_meta_messages(track, t)
        
        # Add note messages
        for e in t.excerpts:
            for msg in e.messages:
                track.append(Message(type=msg.type, channel=msg.channel, note=msg.note, velocity=msg.velocity, time=msg.time))
        
        track.append(MetaMessage('end_of_track', time=1))
        mid.tracks.append(track)

    # Debug txt with data from the midi file
    print(mid, file=open(os.path.join("debug", "debug_output.txt"), mode='w', encoding="utf-8"))

    # Save the midi file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    mid.save(file_path)


def add_composition_meta_messages(output, composition):
    """
    Adds time signature and tempo messages.

    Parameters:
        output: The track where the messages will be added.
        composition: The composition object containing the tracks.

    Returns:
        output: The track with added meta messages.
    """
    output.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    output.append(MetaMessage('set_tempo', tempo=bpm2tempo(composition.bpm), time=0))
    
    return output

def add_track_meta_messages(output, track):

    """
    Adds name, key signature, instrument and other track messages required to correctly work with musescore.

    Parameters:
        output: The track where the messages will be added.
        composition: The composition object containing the tracks.

    Returns:
        output: The track with added meta messages.
    """
    
    output.append(MetaMessage('track_name', name=track.name, time=0))
    output.append(MetaMessage('key_signature', key='C', time=0))
    output.append(Message('control_change', channel=0, control=121, value=0, time=0))
    output.append(Message('control_change', channel=0, control=100, value=0, time=0))
    output.append(Message('control_change', channel=0, control=101, value=0, time=0))
    output.append(Message('control_change', channel=0, control=6, value=12, time=0))
    output.append(Message('control_change', channel=0, control=100, value=127, time=0))
    output.append(Message('control_change', channel=0, control=101, value=127, time=0))
    output.append(Message('program_change', channel=0, program=track.midi_number, time=0))
    output.append(Message('control_change', channel=0, control=7, value=100, time=0))
    output.append(Message('control_change', channel=0, control=10, value=64, time=0))
    output.append(Message('control_change', channel=0, control=91, value=0, time=0))
    output.append(Message('control_change', channel=0, control=93, value=0, time=0))
    output.append(MetaMessage('midi_port', port=0, time=0))

    return output




