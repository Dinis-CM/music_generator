class NoteMessage:
    '''
    Represents a note message. It is a wrapper around the mido Message class.
    Attributes:
        type (str): Type of the message (e.g., 'note_on', 'note_off').
        channel (int): MIDI channel number.
        note (int): MIDI note number.
        velocity (int): Velocity of the note.
        time (int): Time in ticks when the message should be played.
    '''
    def __init__(self, message):
        '''
        Initializes a new NoteMessage instance.
        '''
        self.type = message.type
        self.channel = message.channel
        self.note = message.note
        self.velocity = message.velocity
        self.time = message.time