from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

 
def export_file(file_path, composition):
    
    mid = MidiFile()
    for t in composition.tracks:
        track = MidiTrack()
        if composition.tracks.index(t) == 0:
            track = add_composition_meta_messages(track, composition)
        track = add_track_meta_messages(track, t)
        
        for e in t.excerpts:
            for msg in e.messages:
                track.append(Message(type=msg.type, channel=msg.channel, note=msg.note, velocity=msg.velocity, time=msg.time))
        track.append(MetaMessage('end_of_track', time=1))
        mid.tracks.append(track)
    print(mid, file=open('debug/debug_output.txt', mode='w'))
    mid.save(file_path)

def add_composition_meta_messages(output, composition):
    output.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    output.append(MetaMessage('set_tempo', tempo=bpm2tempo(composition.bpm), time=0))
    return output

def add_track_meta_messages(output, track):
    
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