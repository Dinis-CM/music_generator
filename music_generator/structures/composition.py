class Composition:
    def __init__(self, name, bpm=120):
        self.name = name
        self.bpm = bpm
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)
    
    def set_bpm(self, bpm):
        self.bpm = bpm
