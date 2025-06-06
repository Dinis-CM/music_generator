class NoteMessage:
    def __init__(self, message):
        self.type = message.type
        self.channel = message.channel
        self.note = message.note
        self.velocity = message.velocity
        self.time = message.time