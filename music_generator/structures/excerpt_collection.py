from mido import Message
from music_generator.structures.excerpt import Excerpt
from music_generator.structures.note_message import NoteMessage

class ExcerptCollection:
    
    """
    Represents a collection of all the excerpts inputted into the program.
    Attributes:
        name (str): Name of the collection.
        excerpts (Excerpt): Collection of excerpts.
    Methods:
        add_excerpt(excerpt): Adds a track to the excerpt.
        add_silence_excerpt(): Adds an excerpt with all silence to the collection.
    """
        
    def __init__(self, name):
        '''
        Initializes a new Excerpt Collection instance.
        '''
        self.name = name
        self.excerpts = []

    def add_excerpt(self, excerpt):
        '''
        Adds an excerpt to the Excerpt Collection.
        '''
        self.excerpts.append(excerpt)

    def add_silence_excerpt(self):
        '''
        Adds an excerpt with all silence to the Excerpt Collection.
        '''
        silence = Message(type='note_on', channel=0, note=0, velocity=0, time=480*4)
        silence_message = NoteMessage(silence)
        silence_excerpt = Excerpt("Silêncio")
        silence_excerpt.add_message(silence_message)
        self.add_excerpt(silence_excerpt)
