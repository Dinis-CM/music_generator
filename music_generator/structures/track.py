import math
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

    def set_first_only_probability(self):
        self.probabilities = [1 if i == 0 else 0 for i in range(len(self.input_excerpts.excerpts))]

    def set_last_only_probability(self):
        self.probabilities = [1 if i == len(self.input_excerpts.excerpts) - 1 else 0 for i in range(len(self.input_excerpts.excerpts))]

    def set_binomial_probabilities(self, p):
        n = len(self.input_excerpts.excerpts)
        self.probabilities = [math.comb(n - 1, k) * (p ** k) * ((1 - p) ** (n - 1 - k)) for k in range(n)]

    def set_octave(self, octave):
        self.octave = octave
        all_messages = [msg for excerpt in self.input_excerpts.excerpts for msg in excerpt.messages]
        if not all_messages:
            return
        LowestNote = min(all_messages, key=lambda x: x.note)
        offset = 12 * math.floor(LowestNote.note / 12)
        for msg in all_messages:
            msg.note = msg.note - offset
            msg.note = msg.note + ((octave + 1) * 12)
            msg.note = max(0, min(127, msg.note))

    def add_excerpt(self, excerpt):
        self.excerpts.append(deepcopy(excerpt))

    def check_probabilities(self):
        total = sum(self.probabilities)
        if total != 1:
            return False
        return True