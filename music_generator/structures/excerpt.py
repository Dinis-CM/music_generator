import math
from mido import Message
from music_generator.structures.note_message import NoteMessage

class Excerpt:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)   

    def normalize(self):
        if self.messages:
            LowestNote = min(self.messages, key=lambda x: x.note)
            offset = 12 * math.floor(LowestNote.note / 12)
            for msg in self.messages:
                msg.note = msg.note - offset

    def pad_length(self):
        time = 0
        for msg in self.messages:
            time += msg.time
        if time < 480*4:
            silence_message = Message(type='note_on', channel=0, note=0, velocity=0, time=480*4 - time)
            self.add_message(NoteMessage(silence_message))