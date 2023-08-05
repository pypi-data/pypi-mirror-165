from __future__ import annotations
from .Note import Note
from .Chord import Chord
from typing import Union, Iterator, Tuple
from .utils import isoneof, areoneof, validate
from mido import Message, MetaMessage
from copy import deepcopy

validate_ticks_per_beat = [int, lambda x: 0 <
                           x, "ticks_per_second must be positive"]


class Sequence:
    @validate(None, [list, lambda lst: areoneof(lst, [Note, Chord]), "all objects must be of type Note or Chord"])
    def __init__(self, lst: list[Union[Note, Chord]]) -> None:
        self.data = lst
        self.extra_messages: list[Tuple[int, Union[Message, MetaMessage]]] = []

    def __add__(self, other: Union[Note, Chord, Sequence]) -> Sequence:
        if not isoneof(other, [Note, Chord, Sequence]):
            raise TypeError("other must be of type [Note, Chord, Sequence]")
        if isoneof(other, [Note, Chord]):
            return self + Sequence([other])
        return Sequence(self.data+other.data)

    def __iter__(self) -> Iterator[Union[Note, Chord]]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    @validate(None, [[int, slice], None])
    def __getitem__(self, selection: Union[int, slice]) -> Union[Union[Note, Chord], list[Union[Note, Chord]]]:
        if isinstance(selection, int):
            if not (-len(self) <= selection < len(self)):
                raise ValueError("index out of range")
            return self.data[selection]
        start, stop, step = selection.indices(len(self))
        return [self[i] for i in range(start, stop, step)]

    @validate(None, [[int, slice], None], [[list, Note, Chord], None])  # FIXME
    def __setitem__(self, selector: Union[int, slice], value: Union[list[Union[Note, Chord]], Note, Chord]) -> None:
        if isinstance(selector, int):
            raise NotImplementedError("Implement me")
        start, stop, step = selector.indices(len(self))
        if step == 1:
            total_ticks = 0
            for i in range(start, stop):
                total_ticks += self[i].total_time
            del self.data[start:stop]
            value.duration = total_ticks
            self.data.insert(start, value)
            return
        raise NotImplementedError("not implemented yet")

    @validate(None, [[Note, Chord], None])
    def append(self, value: Union[Note, Chord]) -> Sequence:
        self.data.append(value)
        return self

    @validate(None, [[Message, MetaMessage], None])
    def append_message(self, msg: Union[Message, MetaMessage]) -> None:
        self.extra_messages.append((len(self.data), msg))

    @validate(None, [list, lambda lst: areoneof(lst, [Note, Chord]), "lst must be a list of [Note, Chord]"])
    def extend(self, lst: list[Union[Note, Chord]]) -> Sequence:
        self.data.extend(lst)
        return self

    def __str__(self) -> str:
        res = "\n".join([str(v) for v in self])
        return res

    @validate(None, validate_ticks_per_beat)
    def get_number_of_measures(self, ticks_per_beat: int) -> int:
        count = 0
        for v in self:
            count += v.total_time
        return count//(ticks_per_beat*4)

    @validate(None, [int, lambda x:0 <= x, "measure_number must be non negative"], validate_ticks_per_beat)
    def get_indecies_for_measure(self, measure_number: int, ticks_per_beat: int) -> Tuple[int, int]:
        if not (0 <= measure_number):
            raise ValueError("measure_number must be not negative")

        ticks_in_measure = ticks_per_beat*4
        total_ticks = measure_number*ticks_in_measure

        current_total = 0
        start = 0
        while current_total < total_ticks:
            current_total += self[start].total_time
            start += 1

        end = start
        current_total = 0
        while current_total < ticks_in_measure:
            current_total += self[end].total_time
            end += 1

        return (start, end)

    @validate(None, int, int, [int, lambda x: 0 < x, "ticks_per_second must be positive"])
    def determine_chord_for_indecies(self, start: int, end: int, ticks_per_beat: int) -> Chord:
        if not areoneof([ticks_per_beat, start, end], [int]):
            raise TypeError("1 or more values are of incorrect type")
        values = self[start:end]

        notes: list[Note] = []
        for v in values:
            if isinstance(v, Note):
                notes.append(v)
            elif isinstance(v, Chord):
                notes.extend(v.to_notes())
            else:
                assert False, "shouldnt be here"

        unique_key_names = []
        average_octave = 0
        for note in notes:
            if note.key_name not in unique_key_names:
                unique_key_names.append(note.key_name)
            average_octave += note.octave

        average_octave //= len(notes)
        # for better results
        average_octave += 1

        guess = Chord([Note.from_key_name(name, average_octave, 10)
                      for name in unique_key_names]).fix()

        return guess

    @validate(None, bool, bool)
    def simplify_chords(self, keep_root: bool = True, keep_top: bool = False) -> Sequence:
        if keep_root and keep_top:
            raise ValueError("can only keep one")
        if keep_root:
            return Sequence([v.simplify() for v in self])
        raise NotImplementedError("Implement me")  # TODO

    @validate(None, validate_ticks_per_beat)
    def simplify_confinment(self, ticks_per_beat: int) -> Sequence:
        def find_best_confinment(notes: list[Note]) -> list[Note]:
            average_note = 0
            for n in notes:
                average_note += n.note_number
            average_note //= len(notes)

            AMOUNT_OF_KEYS = 88

            for note in notes:
                min_diff = AMOUNT_OF_KEYS+1
                curr_diff = winning_note_number = 0
                changed = True
                while changed:
                    changed = False

                    if note.note_number < average_note:
                        note.octave += 1
                    else:
                        note.octave -= 1

                    curr_diff = abs(note.note_number-average_note)
                    if curr_diff < min_diff:
                        min_diff = curr_diff
                        winning_note_number = note.note_number
                        changed = True

                note.note_number = winning_note_number
            return notes
        res = self
        curr_measure_number = 0
        while curr_measure_number < res.get_number_of_measures(ticks_per_beat):
            start, end = res.get_indecies_for_measure(
                curr_measure_number, ticks_per_beat)
            notes: list[Note] = []
            for i in range(start, end):
                if isinstance(self[i], Note):
                    notes.append(self[i])
                elif isinstance(self[i], Chord):
                    notes.extend(self[i].to_notes())
                else:
                    assert False, "shouldnt be here"
            new_notes = find_best_confinment(notes)
            for i in range(start, end):
                self[i].note_number = new_notes[i-start].note_number
            curr_measure_number += 1
        return res

    @validate(None, validate_ticks_per_beat)
    def simplifiy_measures(self, ticks_per_beat: int) -> Sequence:
        res = self
        curr_measure_number = 0
        while curr_measure_number < res.get_number_of_measures(ticks_per_beat):
            start, end = res.get_indecies_for_measure(
                curr_measure_number, ticks_per_beat)
            guess = res.determine_chord_for_indecies(
                start, end, ticks_per_beat)
            if guess.full_name != Chord.INCONCLUSIVE:
                guess.delay = 0
                res[start:end] = guess
            curr_measure_number += 1
        return res

    @validate(None, validate_ticks_per_beat, bool, bool, bool)
    def simplify(self, ticks_per_beat: int, simplify_confinment: bool = True, simplify_chords: bool = True, simplify_measures: bool = True) -> Sequence:
        res = self
        if simplify_confinment:
            res = res.simplify_confinment(ticks_per_beat)
        if simplify_chords:
            res = res.simplify_chords()
        if simplify_measures:
            res = res.simplifiy_measures(ticks_per_beat)
        return res

    def to_messages(self) -> list[Message]:
        res = []
        INDEX = 0
        MSG = 1
        for v in self:
            res.extend(v.to_messages())
        for msg in self.extra_messages:
            res.insert(msg[INDEX], msg[MSG])
        return res

    @staticmethod
    @validate([list, lambda lst:areoneof(lst, [Message, MetaMessage])])
    def from_messages(msgs: list[Union[Message, MetaMessage]]) -> Sequence:
        NOTE_ON = "note_on"
        NOTE_OFF = "note_off"
        start = i = 0
        group_indecies: list[Union[int, Tuple[int, int]]] = []

        while i < len(msgs)-1:
            msg: Message = msgs[i]
            if not msg.is_meta:
                next_msg: Message = msgs[i+1]
                if msg.type == NOTE_OFF and next_msg.type == NOTE_ON:
                    group_indecies.append((start, i+1))
                    start = i+1
            else:
                group_indecies.append(start)
                start += 1
            i += 1

        res = Sequence([])
        for v in group_indecies:
            if isinstance(v, Tuple):
                start, end = v[0], v[1]
                msg_count = end-start
                if msg_count > 2:
                    res.append(
                        Chord.from_unordered_messages(deepcopy(msgs[start:end])))
                else:
                    res.append(Note.from_messages(
                        deepcopy(msgs[start]), deepcopy(msgs[end-1])))
            else:  # v is int
                res.append_message(msgs[v])
        return res
