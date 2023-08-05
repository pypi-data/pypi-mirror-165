from __future__ import annotations
from mido import Message, MidiTrack, MetaMessage, bpm2tempo, tempo2bpm
from ..utils import KEYS
from typing import Union
from .Note__ import Note__


class Track:
    def __init__(self) -> None:
        self.track = MidiTrack()
        self.notes = []

    def insert_message(self, message: Union[Message, MetaMessage], index: int) -> Track:
        self.track.insert(index, message)
        return self

    def add_message(self, msg: Union[Message, MetaMessage]) -> Track:
        if not (isinstance(msg, Message) or isinstance(msg, MetaMessage)):
            raise TypeError("msg type is not 'Message' or 'MetaMessage'")
        self.track.append(msg)
        return self

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

    def add_time_signature(self, nominator: int = 4, denominator: int = 4, delta: int = 0, resolution: int = 24) -> Track:
        self.add_message(MetaMessage('time_signature', numerator=nominator, denominator=denominator,
                                     clocks_per_click=resolution, notated_32nd_notes_per_beat=8, time=delta))
        return self

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

    def __str__(self) -> str:
        return str([str(note) for note in self.notes])

    def print(self, raw) -> Track:
        if not raw:
            print(self)
        else:
            for msg in self.track:
                print(msg)
        return self
