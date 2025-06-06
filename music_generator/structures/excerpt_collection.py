from mido import Message
from music_generator.structures.excerpt import Excerpt
from music_generator.structures.note_message import NoteMessage

class ExcerptCollection:
    
    def __init__(self, name):
        self.name = name
        self.excerpts = []

    def add_excerpt(self, excerpt):
        self.excerpts.append(excerpt)

    def add_silence_excerpt(self):
        silence = Message(type='note_on', channel=0, note=0, velocity=0, time=480*4)
        silence_message = NoteMessage(silence)
        silence_excerpt = Excerpt("Silêncio")
        silence_excerpt.add_message(silence_message)
        self.add_excerpt(silence_excerpt)
