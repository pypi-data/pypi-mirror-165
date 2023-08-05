from __future__ import annotations
from .inner_classes import Chord__, ChordType
from .Note import Note
from .utils import areoneof, check_foreach, validate
from mido import Message, MetaMessage
from typing import Iterator, Union


class Chord(Chord__):

    @staticmethod
    @validate(Note, ChordType)
    def from_root(root: Note, type: ChordType) -> Chord:
        notes = []
        for i in type.value:
            notes.append(
                Note(root.note_number+i, root.duration, root.velocity))
        return Chord(notes)

    @staticmethod
    @validate(str, [int, lambda x: 0 <= x, "octave must be non negative"])
    def from_string(name: str, octave: int) -> Chord:
        raise NotImplementedError("Implement me")

    @validate(None, [list, lambda lst: areoneof(lst, [Note]) and len(lst) > 0, "notes must not be empty and only contain objects of type Note"])
    def __init__(self, notes: list[Note]) -> None:
        for note in notes[1:]:
            if not (note.duration) == notes[0].duration:
                raise ValueError(
                    "all notes's duration must be the same in a chord")
        index = 0
        count = 0
        for i, note in enumerate(notes):
            if note.delay != 0:
                count += 1
                index = i

        if count > 1:
            raise ValueError(
                "its not a chord if more than 1 note has a delay")

        super().__init__(notes)
        self.delay = notes[index].delay
        self.duration = notes[0].duration

    def __str__(self) -> str:
        return " ".join([super().__str__(), "D="+str(self.duration), str([note.full_name for note in self])])

    def __iter__(self) -> Iterator[Note]:
        return super().__iter__()

    @property
    def total_time(self) -> int:
        return self.delay+self.duration

    @property
    def max_velocity(self) -> int:
        return max([v.velocity for v in self])

    def simplify(self) -> Note:
        if self.full_name == Chord.INCONCLUSIVE:
            return self
        return Note.from_string(self.root_name, self.duration, self.delay, max([n.velocity for n in self]))

    def inversion(self, inversion_number: int) -> Chord:
        chord__ = super().inversion(inversion_number)
        notes = []
        for note in self:
            for note__ in chord__:
                if note.key_name == note__.key_name:
                    notes.append(
                        Note(note__.note_number, note.duration, note.delay, note.velocity))
                    break
        return Chord(notes)

    def to_messages(self) -> list[Message]:
        res = []
        messages: list[list[Message]] = [n.to_messages() for n in self]
        note_ons = []
        note_offs = []
        for tup in messages:
            note_ons.append(tup[0])
            note_offs.append(tup[1])

        for msg in note_ons:
            msg.time = 0
        for msg in note_offs:
            msg.time = 0

        note_ons[0].time = self.delay
        note_offs[0].time = self.duration

        res += note_ons
        res += note_offs

        return res

    @staticmethod
    @validate(
        [list, lambda lst:areoneof(
            lst, [Message, MetaMessage]), "ons must be a list of Message or MetaMEssage"],
        [list, lambda lst:areoneof(
            lst, [Message, MetaMessage]), "offs must be a list of Message or MetaMEssage"]
    )
    def from_messages(ons: list[Union[Message, MetaMessage]], offs: list[Union[Message, MetaMessage]]) -> Chord:
        # VALIDATION
        if len(ons) != len(offs):
            raise ValueError("length of lists must be the same")
        delay_count = 0
        delay_index = 0
        for i, on in enumerate(ons):
            if on.time != 0:
                delay_count += 1
                delay_index = i
        if delay_count > 1:
            raise ValueError(
                "It is not a chord if more than 1 'on' message has a delay (aka time) which is not 0")
        duration_count = 0
        duration_index = 0
        for i, off in enumerate(offs):
            if off.time != 0:
                duration_count += 1
                duration_index = i
        if duration_count > 1:
            raise ValueError(
                "It is not a chord if more than 1 message has a value for time attribute")

        duration = offs[duration_index].time
        delay = ons[delay_index].time
        notes = []
        tups = []

        for on in ons:
            for off in offs:
                if on.note == off.note:
                    tups.append((on, off))
                    offs.remove(off)
                    break
        for tup in tups:
            tup[1].time = duration
            notes.append(Note.from_messages(*tup))
        return Chord(notes)

    @staticmethod
    @validate([list, lambda lst:areoneof(lst, [Message, MetaMessage]), "msgs must be a list of Message or MetaMEssage"])
    def from_unordered_messages(msgs: list[Union[Message, MetaMessage]]) -> Chord:
        NOTE_ON = "note_on"
        NOTE_OFF = "note_off"
        DUPLICATES_ERROR = "one of the notes has more than two messages"
        ON = 0
        OFF = 1
        d: dict[int, list[Message, Message]] = dict()
        for msg in msgs:
            note_num = msg.note
            msg_type = msg.type
            if note_num not in d:
                if msg_type == NOTE_ON:
                    d[note_num] = [msg, None]
                elif msg_type == NOTE_OFF:
                    d[note_num] = [None, msg]
                else:
                    assert False, "shouldnt have reached here"
            else:
                if msg_type == NOTE_ON:
                    if d[note_num][ON] != None:
                        raise ValueError(DUPLICATES_ERROR)
                    else:
                        d[note_num][ON] = msg
                elif msg_type == NOTE_OFF:
                    if d[note_num][OFF] != None:
                        raise ValueError(DUPLICATES_ERROR)
                    else:
                        d[note_num][OFF] = msg
                else:
                    assert False, "shouldnt have reached here"

        for key in d:
            if not check_foreach([d[key]], lambda tuple: (tuple[0] is not None) and (tuple[1] is not None)):
                raise ValueError("one of the messages lack pair message")

        ons = []
        offs = []

        for key in d:
            ons.append(d[key][ON])
            offs.append(d[key][OFF])
        try:
            return Chord.from_messages(ons, offs)
        except ValueError as e:
            raise ValueError(
                f"Internally, Chord.from_messages has raised a value error:\n1. It can be cause if there are two notes such as the first's end time is after the second's start time\n2. Here is the internal exception:{str(e)}")

    def to_notes(self) -> list[Note]:
        return [v for v in super().to_notes()]

    def fix(self) -> Chord:
        if self.full_name == Chord.INCONCLUSIVE:
            return self
        root = Note.from_string(
            self.root_name, self.duration, self.delay, self.max_velocity)
        notes = [root]
        for type in ChordType:
            if type.name == self.type_name:
                for diff in type.value[1:]:
                    notes.append(Note(root.note_number+diff,
                                 self.duration, self.delay, self.max_velocity))
                break
        return Chord(notes)
