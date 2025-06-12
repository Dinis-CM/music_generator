import math
from copy import deepcopy
from music_generator.structures.midi_instrument_table import MIDI_INSTRUMENT_TABLE

class Track:
    '''
    Represents a musical track. It is an ordered excerpt list inserted into a musical composition.
    Attributes:
        name (str): Name of the track (instrument).
        midi_number (int): MIDI number of the instrument.
        input_excerpts (ExcerptCollection): Collection of excerpts inputted into the program.
        excerpts (list): List of ordered excerpts in the track in the final piece.
        octave (int): Octave of the track.
        probabilities (list): List of probabilities for each input excerpt in the track.
    Methods:
        set_name(name): Sets the name/instrument of the track and updates the MIDI number based on the name.
        set_probabilities(probabilities): Sets the probabilities for each input excerpt in the track.   
        set_discrete_uniform_probabilities(): Sets uniform probabilities for all excerpts in the track.
        set_first_only_probability(): Sets the probability of the first non-silent excerpt to 1 and all others to 0.
        set_last_only_probability(): Sets the probability of the last excerpt to 1 and all others to 0.
        set_binomial_probabilities(p): Sets the probabilities based on a binomial distribution with parameter p.  
        set_octave(octave): Sets the octave for the track and adjusts the notes in the excerpts accordingly.
        add_excerpt(excerpt): Adds an excerpt to the track.
        check_probabilities(): Checks if the sum of probabilities equals 1.
    '''
    
    def __init__(self, name="Unnamed Track", input_excerpts=[]):
        '''
        Initializes a new Track instance.
        '''
        self.name = name
        self.midi_number = 0
        self.input_excerpts = deepcopy(input_excerpts)
        self.excerpts = []
        self.octave = 0
        self.probabilities = []

    def set_name(self, name):
        '''
        Sets the name/instrument of the track and updates the MIDI number based on the name. If no instrument is found, defaults to 0.
        '''
        self.name = name
        for instruments in MIDI_INSTRUMENT_TABLE.values():
            for inst_name, midi_number in instruments:
                if inst_name == name:
                    self.midi_number = midi_number
                    return

        self.midi_number = 0

    def set_probabilities(self, probabilities):
        '''
        Sets the probabilities for each input excerpt in the track.
        '''
        if len(probabilities) != len(self.input_excerpts.excerpts): return
        self.probabilities = probabilities

    def set_discrete_uniform_probabilities(self):
        '''
        Sets uniform probabilities for all excerpts in the track.
        '''
        if not self.input_excerpts:
            return
        probability = 1 / len(self.input_excerpts.excerpts)
        self.probabilities = [probability] * len(self.input_excerpts.excerpts)

    def set_first_only_probability(self):
        '''
        Sets the probability of the first non-silent excerpt to 1 and all others to 0.'''
        self.probabilities = [1 if i == 1 else 0 for i in range(len(self.input_excerpts.excerpts))]

    def set_last_only_probability(self):
        '''
        Sets the probability of the last excerpt to 1 and all others to 0.'''
        self.probabilities = [1 if i == len(self.input_excerpts.excerpts) - 1 else 0 for i in range(len(self.input_excerpts.excerpts))]

    def set_binomial_probabilities(self, p):
        '''
        Sets the probabilities based on a binomial distribution with parameter p.
        '''
        n = len(self.input_excerpts.excerpts)
        self.probabilities = [math.comb(n - 1, k) * (p ** k) * ((1 - p) ** (n - 1 - k)) for k in range(n)]

    def set_octave(self, octave):
        '''
        Sets the octave for the track and adjusts the notes in the excerpts accordingly.
        '''
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
        '''
        Adds an excerpt to the track.
        '''
        self.excerpts.append(deepcopy(excerpt))

    def check_probabilities(self):
        '''
        Checks if the sum of probabilities equals 1, accounting for floating point arithmetic.
        Returns True if the sum is close to 1, otherwise False.
        '''
        total = sum(self.probabilities)
        return math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9)
