from __future__ import annotations
from .Note__ import Note__, NoteType
from enum import Enum
from typing import Union, Tuple, Iterable, ClassVar
from mido import Message
from ..utils import areoneof, isoneof, validate


class ChordType(Enum):
    MAJOR = [0, 4, 7]
    MINOR = [0, 3, 7]
    SUS4 = [0, 5, 7]
    MAJOR_7 = [0, 4, 7, 11]
    MINOR_7 = [0, 3, 7, 10]
    NO3 = [0, 7]
    DIMINISHED = [0, 3, 6]
    AUGMENTED = [0, 4, 8]
    MAJOR_6 = [0, 4, 7, 9]
    MINOR_6 = [0, 3, 7, 9]
    SUS2 = [0, 2, 7]
    DOMINANT_7 = [0, 4, 7, 10]
    DIMINISHED_7 = [0, 3, 6, 9]
    AUGMENTED_7 = [0, 4, 8, 10]


class Chord__:
    INCONCLUSIVE: ClassVar[str] = 'INCONCLUSIVE'

    @staticmethod
    @validate(Note__, ChordType)
    def from_root(root: Note__, type: ChordType) -> Chord__:
        note_nums = []
        for diff in type.value:
            note_nums.append(root.note_number+diff)
        return Chord__([Note__(v) for v in note_nums])

    @staticmethod
    @validate(str, int)
    def from_string(name: str, octave: int) -> Chord__:
        raise NotImplementedError("Implement me")

    @validate(None, [list, lambda lst:areoneof(lst, [Note__]) and len(lst) > 0])
    def __init__(self, notes: list[Note__]) -> None:
        self.notes: list[Note__] = sorted(
            notes, key=lambda note: note.note_number)
        self.root_name, self.type_name = self.__detect()

    @property
    def full_name(self) -> str:
        if self.root_name is not None and self.type_name is not None:
            return f'{self.root_name} {self.type_name}'
        return Chord__.INCONCLUSIVE

    def __str__(self):
        return self.full_name

    def __len__(self) -> int:
        return len(self.notes)

    def __iter__(self) -> Iterable[Note__]:
        return iter(self.notes)

    def __getitem__(self, selection: Union[int, slice]) -> Union[Note__, Chord__, list[Union[Note__, Chord__]]]:
        if not isoneof(selection, [int, slice]):
            raise TypeError("value must be an integer or a slice")
        if isinstance(selection, int):
            if not (0 <= selection < len(self)):
                raise ValueError("index out of range")
            return self.notes[selection]
        start, stop, step = selection.indices(len(self))
        return [self[i] for i in range(start, stop, step)]

    @validate(None, int, Note__,)
    def __setitem__(self, i: int, v: Note__) -> None:
        if not (0 <= i < len(self)):
            raise ValueError("index out of range")
        self.notes[i] = v
        self.root_name, self.type_name = self.__detect()

    def __detect(self) -> Tuple[Union[str, None], Union[str, None]]:
        def sort_keys_alphabetically(notes: list[Note__]) -> list[Note__]:
            result = []
            for key in Note__.names:
                for note in notes:
                    if key == note.key_name and note.key_name not in result:
                        result.append(key)
            return result

        def guess_octave(notes: list[Note__]) -> int:
            d = dict()
            for n in notes:
                if n.octave not in d:
                    d[n.octave] = 0
                d[n.octave] += 1
            sum = 0
            count = 0
            for key, value in d.items():
                sum += int(key)*value
                count += value
            return int(sum/count)

        sorted = sort_keys_alphabetically(self.notes)
        if len(sorted) == 1:
            return self.notes[0].full_name, None
        NOTES_IN_OCTAVE = 12
        guessed_octave = guess_octave(self.notes)
        for c in ChordType:
            if len(c.value) != len(sorted):
                continue
            for i, root in enumerate(sorted):
                rootIndex = Note__.names.index(root)
                for j, val in enumerate(c.value[1:]):
                    if Note__.names[(rootIndex+val) % NOTES_IN_OCTAVE] != sorted[(i+j+1) % len(sorted)]:
                        break
                else:
                    return f'{root}{guessed_octave}', c.name
        # special = {
        #     "MAJOR": [0, 8],
        #     "MINOR": [0, 9],
        #     "major": [0, 4],
        #     "minor": [0, 3],
        # }
        # results = {
        #     "MAJOR": sorted[1],
        #     "MINOR": sorted[1],
        #     "major": sorted[0],
        #     "minor": sorted[0],
        # }
        # for key, value in special.items():
        #     rootIndex = Note__.names.index(sorted[0])
        #     for j, val in enumerate(value[1:]):
        #         if Note__.names[(rootIndex+val) % NOTES_IN_OCTAVE] != sorted[(j+1) % len(sorted)]:
        #             break
        #     else:
        #         return f'{results[key]}{guessed_octave}', key.upper()
        return None, None

    def simplify(self) -> Note__:
        return Note__.from_string(self.root_name)

    @validate(None, [int, lambda x: 1 <= x, "inversion must be bigger than 0"])
    def inversion(self, inversion_number: int) -> Chord__:
        octave_diffrence = inversion_number//len(self)
        inversion_number %= len(self)
        OCTAVE = 12
        notes: list[Note__] = []
        for i in range(inversion_number):
            notes.append(Note__(self[i].note_number +
                         OCTAVE*(1+octave_diffrence)))
        notes.extend(self[inversion_number:])
        return Chord__(sorted(notes, key=lambda note: note.note_number))

    def to_notes(self) -> list[Note__]:
        return [v for v in self]
