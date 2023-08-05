from __future__ import annotations
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo, tempo2bpm
from .Track import Track
import os


class Creator:
    def __init__(self, mid: MidiFile = None) -> None:
        if mid is None:
            mid = MidiFile()
        self.mid = mid

    def add_track(self, track: Track) -> Creator:
        if not isinstance(track, Track):
            raise TypeError("track type is not 'Track'")
        self.mid.tracks.append(track.track)
        return self

    def add_tracks(self, tracks: list[Track]) -> Creator:
        for track in tracks:
            self.add_track(track)
        return self

    def set_ticks_per_beat(self, ticksPerBeat: int) -> Creator:
        self.mid.ticks_per_beat = ticksPerBeat
        return self

    def save(self, path: str = "./data/output/output.mid") -> None:
        directory = os.path.abspath(os.getcwd())+"\\output\\"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.mid.save(path)
