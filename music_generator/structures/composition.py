import datetime

class Composition:
    """
    Represents a final musical composition with configurable properties such as name, BPM (beats per minute), length, and tracks.
    Attributes:
        name (str): The name of the composition. Default is a timestamped name based on the current date and time.
        bpm (int): The tempo of the composition in beats per minute. Default is 120.
        length (int): The length of the composition in bars. Default is 16.
        max_tracks (int): The maximum number of tracks allowed in the composition. Default is 6 and should not be changed.
        tracks (list): A list to store the tracks added to the composition.
    Methods:
        add_track(track): Adds a track to the composition.
        set_bpm(bpm): Sets the BPM (tempo) of the composition.
        set_name(name): Sets the name of the composition.
        set_max_tracks(max_tracks): Sets the maximum number of tracks.
        set_length(length): Sets the length of the composition.
    """
    

    def __init__(self):
        '''
        Initializes a new Composition instance with default values.
        '''
        date = datetime.datetime.now()
        self.name = f"Musica_Aleatoria_{date.year}-{date.month:02d}-{date.day:02d}_{date.hour:02d}:{date.minute:02d}"
        self.bpm = 120
        self.length = 16
        self.max_tracks = 6
        self.tracks = []

    def add_track(self, track):
        '''
        Adds a track to the composition.
        '''
        self.tracks.append(track)
    
    def set_bpm(self, bpm):
        '''
        Sets the BPM of the composition.
        '''
        self.bpm = bpm
    
    def set_name(self, name):
        '''
        Sets the name of the composition.
        '''
        self.name = name

    def set_max_tracks(self, max_tracks):
        '''
        Sets the maximum number of tracks.
        '''
        self.max_tracks = max_tracks

    def set_length(self, length):
        '''
        Sets the length of the composition.
        '''
        self.length = length