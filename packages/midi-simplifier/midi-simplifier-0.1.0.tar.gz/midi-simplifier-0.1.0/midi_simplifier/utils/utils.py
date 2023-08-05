from enum import Enum
from .types import MidoMessage, MidoMetaMessage
from mido import MidiFile, tempo2bpm, bpm2tempo, second2tick, tick2second
from typing import Union, Type, Any


def remove_unneccesary(mid: MidiFile):
    def filterFunc(item: Union[MidoMessage, MidoMetaMessage]):
        return item.type not in ["control_change", "pitchwheel", "program_change", "end_of_track", "midi_port"]
    for track in mid.tracks:
        yield list(filter(filterFunc, track))


def getNoteName(num: int) -> str:
    octave = 0
    if num-21-3 > 0:
        octave = (num-21-3)//12 + 1
    note = (num-21) % 12
    switch = {
        3: "C",
        4: "C#",
        5: "D",
        6: "D#",
        7: "E",
        8: "F",
        9: "F#",
        10: "G",
        11: "G#",
        0: "A",
        1: "A#",
        2: "B"
    }
    return switch[note] + str(octave)


class KEYS(Enum):
    C = "C"
    Cm = "Cm"
    C_SHARP = "C#"
    C_SHARPm = "C#m"
    D = "D"
    Dm = "Dm"
    D_SHARP = "D#"
    D_SHARPm = "D#m"
    E = "E"
    Em = "Em"
    F = "F"
    Fm = "Fm"
    F_SHARP = "F#"
    F_SHARPm = "F#m"
    G = "G"
    Gm = "Gm"
    G_SHARP = "G#"
    G_SHARPm = "G#m"
    A = "A"
    Am = "Am"
    A_SHARP = "A#"
    A_SHARPm = "A#m"
    B = "B"
    Bm = "Bm"


def memo(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@memo
def calculateNoteTicks(NoteDuration: float, BPM: float, TICKS_PER_BEAT: int) -> int:
    """
    @param NoteDuration: 0.25 is for quarter note
    """
    secondInBeats = 60/BPM
    return int(second2tick(secondInBeats*(NoteDuration*4), TICKS_PER_BEAT, bpm2tempo(BPM)))


@memo
def calculateNoteLengthFromTicks(ticks: float, BPM: float, TICKS_PER_BEAT: int) -> float:
    secondInBeats = 60/BPM
    sec = tick2second(ticks, TICKS_PER_BEAT, bpm2tempo(BPM))
    pass
    return sec
