from __future__ import annotations
from .Note__ import Note__, NoteTypes, NoteDuration
from ..utils import areoneof, isoneof


class Note(Note__):
    @staticmethod
    def from_note_type(note_type: NoteTypes, duration: int, velocity: int = 100) -> Note:
        if not isinstance(note_type, NoteTypes):
            raise TypeError("note_type must be of type NoteType")
        note_num = Note.note_number_from_string(note_type.value)
        return Note(note_num, duration, velocity)

    @staticmethod
    def from_string(name: str, duration: int, velocity: int = 100) -> Note__:
        if not isoneof(name, [str]):
            raise TypeError("name must be of type 'string'")
        note_num = Note__.note_number_from_string(name)
        return Note(note_num, duration, velocity)

    def __init__(self, note_num: int, duration: int, velocity: int) -> None:
        if not areoneof([note_num, duration, velocity], [int]):
            raise TypeError("note_num, duration, velocity must be of type int")
        super().__init__(note_num)
        self.duration: int = duration
        self.velocity: int = velocity

    def __str__(self) -> str:
        return " ".join([str(super().__str__()), "D="+str(self.duration), "V="+str(self.velocity)])
