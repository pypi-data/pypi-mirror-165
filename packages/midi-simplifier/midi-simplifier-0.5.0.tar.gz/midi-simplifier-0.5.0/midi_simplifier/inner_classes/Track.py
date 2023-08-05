from __future__ import annotations
from mido import Message, MidiTrack, MetaMessage, bpm2tempo, tempo2bpm
from ..utils import KEYS, validate, areoneof
from typing import Union
from . import Note__


class Track:
    def __init__(self) -> None:
        self.track = MidiTrack()
        self.notes = []

    def __str__(self) -> str:
        return str([str(note) for note in self.notes])

    @validate(None, [[Message, MetaMessage], None], int)
    def insert_message(self, message: Union[Message, MetaMessage], index: int) -> Track:
        if not (0 <= index < len(self)):
            raise ValueError("index out of range")
        self.track.insert(index, message)
        return self

    @validate(None, [[Message, MetaMessage], None])
    def add_message(self, msg: Union[Message, MetaMessage]) -> Track:
        self.track.append(msg)
        return self

    @validate(None, [list, lambda lst:areoneof(lst, [Message, MetaMessage])])
    def add_messages(self, messages: list[Union[Message, MetaMessage]]) -> Track:
        for msg in messages:
            self.add_message(msg)
        return self

    def set_instrument(self, instrumentIndex: int = 0, delta: int = 0) -> Track:
        self.add_message(
            Message('program_change', program=instrumentIndex, time=delta))
        return self

    def add_key_signature(self, key: KEYS = KEYS.C, delta: int = 0) -> Track:
        self.add_message(MetaMessage('key_signature', key=key, time=delta))
        return self

    @validate(
        None,
        [int, lambda v: 0 < v, "nominator must be positive"],
        [int, lambda v: 0 < v, "denominator must be positive"],
        int,
        int
    )
    def add_time_signature(self, nominator: int = 4, denominator: int = 4, delta: int = 0, resolution: int = 24) -> Track:
        self.add_message(MetaMessage('time_signature', numerator=nominator, denominator=denominator,
                                     clocks_per_click=resolution, notated_32nd_notes_per_beat=8, time=delta))
        return self

    @validate(None, [int, lambda v:0 < v, "tempo must be positive"], [int, lambda v:0 <= v, "delta must be non negative"])
    def add_tempo(self, tempo: int = 120, delta: int = 0) -> Track:
        self.add_message(MetaMessage(
            'set_tempo', tempo=bpm2tempo(tempo), time=delta))
        return self

    def add_note(self, note: Note__) -> Track:
        if not isinstance(note, Note__):
            raise TypeError("note type is not 'Note'")
        self.notes.append(note)
        self.add_message(note.on)
        self.add_message(note.off)
        return self

    def add_notes(self, notes: list[Note__]) -> Track:
        for note in notes:
            self.add_note(note)
        return self

    def add_key_signature(self, keyName: str = "Ab", delta: int = 0) -> Track:
        if keyName is not None:
            self.add_message(MetaMessage(
                'key_signature', key=keyName, time=delta))
        return self
