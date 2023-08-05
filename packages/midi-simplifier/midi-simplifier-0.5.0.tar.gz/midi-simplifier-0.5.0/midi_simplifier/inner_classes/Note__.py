from __future__ import annotations
from mido import Message
from enum import Enum
from typing import Union, Tuple
from ..utils import areoneof, isoneof, validate


class NoteDuration(Enum):
    WHOLE = 1
    HALF = 0.5
    QUARTER = 0.25
    EIGHTH = 0.125
    SIXTEENTH = 0.0625


class NoteType(Enum):
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
    names: list[str] = [n.value for n in NoteType]

    @ staticmethod
    @validate(str)
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
    @validate(NoteType)
    def from_note_type(note_type: NoteType) -> Note__:
        note_num = Note__.note_number_from_string(note_type.value)
        return Note__(note_num)

    @staticmethod
    @validate(str)
    def from_string(name: str) -> Note__:
        note_num = Note__.note_number_from_string(name)
        return Note__(note_num)

    @validate(None, [int, lambda num: 0 <= num < 88, "note_number must be in range of [0,87]"])
    def __init__(self, note_number: int) -> None:
        self.__note_number: int = note_number
        self.__octave: int = self.__calculate_octave()
        self.__key_name: str = self.__get_key_name()

    @property
    def note_number(self) -> int:
        return self.__note_number

    @note_number.setter
    @validate(None, [int, lambda n: 0 <= n < 88, "note_number must be in [0,87]"])
    def note_number(self, value: int) -> None:
        self.__note_number = value
        self.__octave = self.__calculate_octave()
        self.__key_name = self.__get_key_name()

    @property
    def key_name(self) -> str:
        return self.__key_name

    @key_name.setter
    @validate(None, [str, lambda v: v.upper() not in [t.value for t in NoteType], f"key_name must be in {[t.value for t in NoteType]} (or lowercase)"])
    def key_name(self, value: str) -> None:
        curr_i = new_i = 0
        for i, t in enumerate(NoteType):
            if value.upper() == t.value:
                new_i = i
            if self.key_name == t.value:
                curr_i = i
        semitones_diff = new_i - curr_i
        self.note_number += semitones_diff

    @property
    def octave(self) -> int:
        return self.__octave

    @octave.setter
    @validate(None, [int, lambda x:0 <= x, "octave must be not negative"])
    def octave(self, value: int) -> None:
        OCTAVE = 12
        octave_diff = value-self.__octave
        self.__note_number += OCTAVE*octave_diff
        self.__octave = value

    @property
    def full_name(self) -> str:
        return self.key_name+str(self.octave)

    def __str__(self) -> str:
        return self.full_name

    def __calculate_octave(self) -> int:
        NOTES_IN_OCTAVE = 12
        octave = 0
        if self.note_number > 3:  # we are not in octave 0
            octave = (self.note_number-3)//NOTES_IN_OCTAVE + 1
        return octave

    def __get_key_name(self) -> str:
        NOTES_IN_OCTAVE = 12
        ZERO_OCATEVE_SIZE = 3
        i = self.note_number % NOTES_IN_OCTAVE
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

    def has_accidental(self) -> bool:
        return self.is_sharp() or self.is_flat()

    def simplify(self) -> Note__:
        return self
