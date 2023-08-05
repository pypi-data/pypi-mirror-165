from .Chord__ import Chord__, ChordTypes
from .Note import Note


class Chord(Chord__):
    @staticmethod
    def from_root(root: Note, type: ChordTypes, inversion: int = 0) -> Chord__:
        raise NotImplementedError("Implement me")

    @staticmethod
    def from_string(name: str, octave: int, inversion: int = 0) -> Chord__:
        raise NotImplementedError("Implement me")
