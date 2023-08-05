from .Note__ import Note__


class Channel:
    def __init__(self, index: int, name: str) -> None:
        self.index = index
        self.name = name
        self.notes = []

    def add_note(self, note: Note__) -> None:
        self.notes.append(note)

    def __str__(self) -> str:
        return self.name + ": "+str([str(note) for note in self.notes])
