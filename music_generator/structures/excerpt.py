import math
from mido import Message
from music_generator.structures.note_message import NoteMessage

class Excerpt:

    """
    Represents an excerpt. It is a collection of messages that can be used to create a musical piece.
    Attributes:
        name (str): Name of the excerpt.
        messages (note_message): Collection of messsages.
    Methods:
        add_message(message): Adds a message to the excerpt.
        normalize(): Normalizes the notes so that the lowest note in the excerpt corresponds to the same note in the -1 octave.
        pad_length(): Pads the excerpt to ensure it has a length of 1 bar (480 ticks per beat; 4/4 time signature).
    """

    def __init__(self, name):
        '''
        Initializes a new Excerpt instance.
        '''
        self.name = name
        self.messages = []

    def add_message(self, message):
        '''
        Adds a message to the excerpt.
        '''
        self.messages.append(message)   

    def normalize(self):
        '''
        Normalizes the notes in the excerpt so that the lowest note corresponds to the same note in the -1 octave. This is done by subtracting the offset from each note in the excerpt.
        '''
        if self.messages:
            LowestNote = min(self.messages, key=lambda x: x.note)
            offset = 12 * math.floor(LowestNote.note / 12)
            for msg in self.messages:
                msg.note = msg.note - offset

    def pad_length(self):
        '''
        Pads the excerpt to ensure it has a length of 1 bar (480 ticks per beat; 4/4 time signature).
        '''
        time = 0
        for msg in self.messages:
            time += msg.time
        if time < 480*4:
            silence_message = Message(type='note_on', channel=0, note=0, velocity=0, time=480*4 - time)
            self.add_message(NoteMessage(silence_message))