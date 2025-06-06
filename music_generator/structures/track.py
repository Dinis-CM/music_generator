from copy import deepcopy
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE

class Track:
    
    def __init__(self, name="Unnamed Track", input_excerpts=[]):
        self.name = name
        self.midi_number = 0
        self.input_excerpts = deepcopy(input_excerpts)
        self.excerpts = []
        self.octave = 0
        self.probabilities = []

    def set_name(self, name):
        self.name = name
        for instruments in MIDI_INSTRUMENT_TABLE.values():
            for inst_name, midi_number in instruments:
                if inst_name == name:
                    self.midi_number = midi_number
                    return

        self.midi_number = 0

    def set_probabilities(self, probabilities):
        if len(probabilities) != len(self.input_excerpts.excerpts): return
        self.probabilities = probabilities

    def set_discrete_uniform_probabilities(self):
        if not self.input_excerpts:
            return
        probability = 1 / len(self.input_excerpts.excerpts)
        self.probabilities = [probability] * len(self.input_excerpts.excerpts)

    def set_octave(self, octave):
        self.octave = octave
        for e in self.excerpts:
            for msg in e.messages:
                msg.note += 12 * (octave + 1)
                msg.note = max(0, min(127, msg.note))  # Clamp to MIDI range

    def add_excerpt(self, excerpt):
        self.excerpts.append(deepcopy(excerpt))

    def check_probabilities(self):
        total = sum(getattr(e, "probability", 1/len(self.excerpts)) for e in self.excerpts)
        if total != 1:
            return False
        return True