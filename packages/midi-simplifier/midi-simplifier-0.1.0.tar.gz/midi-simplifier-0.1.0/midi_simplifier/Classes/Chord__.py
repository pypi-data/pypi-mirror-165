from __future__ import annotations
from .Note__ import Note__, NoteTypes
from enum import Enum
from typing import Union, Tuple
from mido import Message
from ..utils import areoneof, notempty


class ChordTypes(Enum):
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
    @staticmethod
    def from_root(root: Note__, type: ChordTypes, inversion: int = 0) -> Chord__:
        raise NotImplementedError("Implement me")

    @staticmethod
    def from_string(name: str, octave: int, inversion: int = 0) -> Chord__:
        raise NotImplementedError("Implement me")

    def __init__(self, notes: list[Note__]) -> None:
        if notempty(notes, "Chord must have at least one note"):
            if not areoneof(notes, [Note__]):
                raise TypeError(
                    "Chord must be created from a list of 'Note' objects")
            self.notes: list[Note__] = notes
            self.root_name, self.type_name = self.__detect()

    def __detect(self) -> Tuple[Union[str, None], Union[str, None]]:
        sorted = self.__get_sorted_keys()
        if len(sorted) == 1:
            return self.notes[0].full_name, None
        NOTES_IN_OCTAVE = 12
        guessed_octave = self.__guess_octave()
        for c in ChordTypes:
            if len(c.value) != len(sorted):
                continue
            for i, root in enumerate(sorted):
                rootIndex = Note__.names.index(root)
                for j, val in enumerate(c.value[1:]):
                    if Note__.names[(rootIndex+val) % NOTES_IN_OCTAVE] != sorted[(i+j+1) % len(sorted)]:
                        break
                else:
                    return f'{root}{guessed_octave}', c.name
        special = {
            "MAJOR": [0, 8],
            "MINOR": [0, 9],
            "major": [0, 4],
            "minor": [0, 3],
        }
        results = {
            "MAJOR": sorted[1],
            "MINOR": sorted[1],
            "major": sorted[0],
            "minor": sorted[0],
        }
        for key, value in special.items():
            rootIndex = Note__.names.index(sorted[0])
            for j, val in enumerate(value[1:]):
                if Note__.names[(rootIndex+val) % NOTES_IN_OCTAVE] != sorted[(j+1) % len(sorted)]:
                    break
            else:
                return f'{results[key]}{guessed_octave}', key.upper()
        return None, None

    def __guess_octave(self):
        d = dict()
        for n in self.notes:
            if n.octave not in d:
                d[n.octave] = 0
            d[n.octave] += 1
        sum = 0
        count = 0
        for key, value in d.items():
            sum += int(key)*value
            count += value
        return int(sum/count)

    def __get_sorted_keys(self):
        result = []
        for key in Note__.names:
            for note in self.notes:
                if key == note.key_name and note.key_name not in result:
                    result.append(key)
        return result

    def __str__(self):
        if self.root_name is not None and self.type_name is not None:
            return f'{self.root_name} {self.type_name}'
        return f'INCONCLUSIVE'

    def simplify(self) -> Note__:
        raise NotImplementedError("Implement me")
