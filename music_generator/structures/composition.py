import datetime

class Composition:
    def __init__(self):
        date = datetime.datetime.now()
        self.name = f"Musica_Aleatoria_{date.year}-{date.month:02d}-{date.day:02d}_{date.hour:02d}:{date.minute:02d}"
        self.bpm = 120
        self.length = 16
        self.max_tracks = 6
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)
    
    def set_bpm(self, bpm):
        self.bpm = bpm
    
    def set_name(self, name):
        self.name = name

    def set_max_tracks(self, max_tracks):
        self.max_tracks = max_tracks

    def set_length(self, length):
        self.length = length