from __future__ import annotations
from mido import Message
from enum import Enum
from typing import Union, Tuple
from ..utils import areoneof, isoneof


class NoteDuration(Enum):
    WHOLE = 1
    HALF = 0.5
    QUARTER = 0.25
    EIGHTH = 0.125
    SIXTEENTH = 0.0625


class NoteTypes(Enum):
    C = "C"
    C_SHARP = "C#"
    D = "D"
    D_SHARP = "D#"
    E = "E"
    F = "F"
    F_SHARP = "F#"
    G = "G"
    G_SHARP = "G#"
    A = "A"
    A_SHARP = "A#"
    B = "B"


class Note__:
    names: list[str] = [n.value for n in NoteTypes]

    @ staticmethod
    def note_number_from_string(s: str) -> int:
        # OFFSET = 21
        NOTES_IN_OCTAVE = 12
        s = s.upper()
        try:
            octave = int(s[-1])
        except ValueError:
            raise ValueError("note must have an octave number: " + s)
        s = s[:-1]
        switch = {
            "C": 3,
            "C#": 4,
            "DB": 4,
            "D": 5,
            "D#": 6,
            "EB": 6,
            "E": 7,
            "F": 8,
            "F#": 9,
            "GB": 9,
            "G": 10,
            "G#": 11,
            "AB": 11,
            "A": 0,
            "A#": 1,
            "BB": 1,
            "B": 2
        }
        try:
            note = switch[s.upper()]
            if note not in [0, 1, 2]:
                octave -= 1
        except KeyError:
            raise ValueError("note must be a valid note: " + s)
        return octave*NOTES_IN_OCTAVE+note  # +OFFSET

    @staticmethod
    def from_note_type(note_type: NoteTypes) -> Note__:
        if not isinstance(note_type, NoteTypes):
            raise TypeError("note_type must be of type NoteType")
        note_num = Note__.note_number_from_string(note_type.value)
        return Note__(note_num)

    @staticmethod
    def from_string(name: str) -> Note__:
        if not isoneof(name, [str]):
            raise TypeError("name must be of type 'string'")
        note_num = Note__.note_number_from_string(name)
        return Note__(note_num)

    def __init__(self, note_number: int) -> None:
        if not (0 <= note_number < 88):
            raise ValueError("note_number must be in range of [0,87]")
        self.note_numer: int = note_number
        self.octave: int = self.__calculate_octave()
        self.key_name: str = self.__get_key_name()

    @property
    def full_name(self) -> str:
        return self.key_name+str(self.octave)

    def __str__(self) -> str:
        return self.full_name

    def __calculate_octave(self) -> int:
        NOTES_IN_OCTAVE = 12
        octave = 0
        if self.note_numer > 3:  # we are not in octave 0
            octave = (self.note_numer-3)//NOTES_IN_OCTAVE + 1
        return octave

    def __get_key_name(self) -> str:
        NOTES_IN_OCTAVE = 12
        ZERO_OCATEVE_SIZE = 3
        i = self.note_numer % NOTES_IN_OCTAVE
        res = Note__.names[i-ZERO_OCATEVE_SIZE]
        if i < 3:  # we need to wrap
            res = Note__.names[NOTES_IN_OCTAVE-(ZERO_OCATEVE_SIZE-i)]

        if res is None:
            pass

        return res

    def is_flat(self) -> bool:
        return self.full_name[1].lower() == "b"

    def is_sharp(self) -> bool:
        return self.full_name[1] == "#"

    def has_accidental(self, note: Note__) -> bool:
        return self.is_sharp(note) or self.is_flat(note)
