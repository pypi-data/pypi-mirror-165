from enum import Enum
# from .types import MidoMessage, MidoMetaMessage
# from mido import MidiFile, tempo2bpm, bpm2tempo, second2tick, tick2second
# from typing import Union, Type, Any
# from .decorators import memo


# def get_note_name(num: int) -> str:
#     octave = 0
#     if num-21-3 > 0:
#         octave = (num-21-3)//12 + 1
#     note = (num-21) % 12
#     switch = {
#         3: "C",
#         4: "C#",
#         5: "D",
#         6: "D#",
#         7: "E",
#         8: "F",
#         9: "F#",
#         10: "G",
#         11: "G#",
#         0: "A",
#         1: "A#",
#         2: "B"
#     }
#     return switch[note] + str(octave)


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


# @memo
# def calculate_note_ticks(NoteDuration: float, BPM: float, TICKS_PER_BEAT: int) -> int:
#     """
#     @param NoteDuration: 0.25 is for quarter note
#     """
#     secondInBeats = 60/BPM
#     return int(second2tick(secondInBeats*(NoteDuration*4), TICKS_PER_BEAT, bpm2tempo(BPM)))


# @memo
# def calculate_note_length_from_ticks(ticks: float, BPM: float, TICKS_PER_BEAT: int) -> float:
#     secondInBeats = 60/BPM
#     sec = tick2second(ticks, TICKS_PER_BEAT, bpm2tempo(BPM))
#     pass
#     return sec
