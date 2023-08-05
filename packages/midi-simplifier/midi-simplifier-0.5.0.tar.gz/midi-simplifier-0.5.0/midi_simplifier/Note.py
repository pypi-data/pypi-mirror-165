from __future__ import annotations
from .inner_classes import Note__, NoteType, NoteDuration
from .utils import validate
from mido import Message
from typing import ClassVar


class Note(Note__):
    OFFSET: ClassVar[int] = 21

    @staticmethod
    @validate(
        NoteType,
        [int, lambda x:0 < x, "duration must be bigger than 0"],
        [int, lambda x:0 <= x, "delay must be non negative"],
        [int, lambda x:0 <= x <= 100, "velocity must be in [0,100]"],
    )
    def from_note_type(note_type: NoteType, duration: int, delay: int = 0, velocity: int = 100) -> Note:
        note_num = Note.note_number_from_string(note_type.value)
        return Note(note_num, duration, delay, velocity)

    @staticmethod
    @validate(
        str,
        [int, lambda x:0 <= x, "ocateve must be non negative"],
        [int, lambda x:0 < x, "duration must be bigger than 0"],
        [int, lambda x:0 <= x, "delay must be non negative"],
        [int, lambda x:0 <= x <= 100, "velocity must be in [0,100]"],
    )
    def from_key_name(key_name: str, octave: int, duration: int, delay: int = 0, velocity: int = 100) -> Note:
        return Note.from_string(key_name+str(octave), duration, delay, velocity)

    @staticmethod
    @validate(
        str,
        [int, lambda x:0 < x, "duration must be bigger than 0"],
        [int, lambda x:0 <= x, "delay must be non negative"],
        [int, lambda x:0 <= x <= 100, "velocity must be in [0,100]"],
    )
    def from_string(name: str, duration: int, delay: int = 0, velocity: int = 100) -> Note:
        """Create a note from string

        Args:
            name (str): the name of the note - key and octave as in formal musical notation. e.g: "c4"
            duration (int): the duration in ticks for the note
            delay (int, optional): the delay in ticks for the note. Defaults to 0.
            velocity (int, optional): the velocity in which the note is pressed. Defaults to 100.

        Returns:
            Note
        """
        note_num = Note__.note_number_from_string(name)
        return Note(note_num, duration, delay, velocity)

    @validate(
        None,
        [int, lambda x: 0 <= x < 88, "note must be in [0,87]"],
        [int, lambda x:0 < x, "duration must be bigger than 0"],
        [int, lambda x:0 <= x, "delay must be non negative"],
        [int, lambda x:0 <= x <= 100, "velocity must be in [0,100]"],
    )
    def __init__(self, note_num: int, duration: int, delay: int = 0, velocity: int = 100) -> None:
        super().__init__(note_num)
        self.delay = delay
        self.duration: int = duration
        self.velocity: int = velocity

    def __str__(self) -> str:
        return " ".join([super().__str__(), "D="+str(self.duration), "V="+str(self.velocity)])

    @property
    def total_time(self) -> int:
        return self.delay+self.duration

    def to_messages(self) -> list[Message]:
        # my note_number 0 which is A0 corresponds with actual note number 21
        return [
            Message('note_on', note=self.note_number +
                    Note.OFFSET, time=self.delay),
            Message('note_off', note=self.note_number +
                    Note.OFFSET, time=self.duration)
        ]

    @staticmethod
    @validate(Message, Message)
    def from_messages(on: Message, off: Message) -> Note:
        return Note(on.note-Note.OFFSET, off.time, on.time, on.velocity)
