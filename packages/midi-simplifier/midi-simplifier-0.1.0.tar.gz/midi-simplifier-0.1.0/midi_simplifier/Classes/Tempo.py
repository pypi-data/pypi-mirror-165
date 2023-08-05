from mido import tempo2bpm


class Tempo:
    def __init__(self, tempo: int) -> None:
        self.bpm = format(tempo2bpm(tempo), ".3f")

    def __init__(self, bpm: int) -> None:
        self.bpm = bpm

    def __str__(self) -> str:
        return str({self.time: self.tempo})
