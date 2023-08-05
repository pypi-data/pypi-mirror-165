from __future__ import annotations
from enum import Enum
from typing import Tuple, Any
from . import Note__


class ScaleType(Enum):
    MAJOR = [0, 2, 4, 5, 7, 9, 11]
    MINOR = [0, 2, 3, 5, 7, 8, 10]
    CHROMATIC = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    INCONCLUSIVE = []
    # HARMONIC_MINOR = []
    # MELODIC_MINOR = []
    # DORIAN = []
    # PHRYGIAN = []
    # LYDIAN = []
    # MIXOLYDIAN = []
    # LOCRIAN = []
    # SUPERLOCRIAN = []
    # IONIAN = []
    # DORIAN_FLAT_FOUR = []


class ScaleDetector:
    def __init__(self, keyCount: dict[str, int]) -> None:
        self.keyCount = self.__strip(keyCount)
        self.type, self.root = self.__detect()

    def __strip(self, keyCount: dict[str, int]) -> dict:
        result = dict()
        for key in list(keyCount):
            offset = 0
            if key[-1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                offset = 1
            if key[: len(key)-offset] not in result:
                result[key[:len(key)-offset]] = 0
            result[key[:len(key)-offset]] += keyCount[key]
        return result

    def __get_sorted_keys(self) -> list:
        result = []
        for key in Note__.names:
            if key in self.keyCount:
                result.append(key)
            else:
                result.append(0)
        return list(filter(lambda item: item != 0, result))

    def __detect(self) -> Tuple[ScaleType, Any]:
        count = len(list(self.keyCount))
        if count < 7:
            return ScaleType.INCONCLUSIVE, None
        if count == 12:
            return ScaleType.CHROMATIC.name, None

        sortedKeys = list(self.__get_sorted_keys())
        for o in ScaleType:
            for root in sortedKeys:
                for i, relativeIndex in enumerate(o._value_[1:]):
                    if Note__.names[(Note__.names.index(root)+relativeIndex) % len(Note__.names)] != sortedKeys[(sortedKeys.index(root)+(i+1)) % len(sortedKeys)]:
                        break
                else:
                    return o.name, root

    def __str__(self) -> str:
        return f'{self.root} {self.type}'
