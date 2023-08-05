from __future__ import annotations
from .Note__ import Note__, NoteTypes
from .Chord__ import Chord__
from typing import Union, Iterator
from ..utils import isoneof, areoneof


class Sequence:
    def __init__(self, lst: list[Union[Note__, Chord__]]) -> None:
        self.data = lst

    def __add__(self, other: Union[Note__, Chord__, Sequence]) -> Sequence:
        if not isoneof(other, [Note__, Chord__, Sequence]):
            raise TypeError("other must be of type [Note, Chord, Sequence]")
        if isoneof(other, [Note__, Chord__]):
            return self + Sequence([other])
        return Sequence(self.data+other.data)

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitenm__(self, i: int) -> Union[Note__, Chord__]:
        if not (0 <= i < len(self)):
            raise ValueError("index out of range")
        return self.data[i]

    def append(self, value: Union[Note__, Chord__]) -> Sequence:
        if not isoneof(value, [Note__, Chord__]):
            raise TypeError("value must be of type [Note, Chord]")
        self.data.append(value)
        return self

    def extend(self, lst: list[Union[Note__, Chord__]]) -> Sequence:
        if not areoneof(lst, [Note__, Chord__]):
            raise TypeError("lst must be a list of [Note, Chord]")
        self.data.extend(lst)
        return self

    def __str__(self) -> str:
        res = "\n".join([str(v) for v in self])
        return res
