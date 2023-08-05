from __future__ import annotations
from typing import Union
from mido import MidiFile, Message, MetaMessage
from .utils import validate
from .inner_classes import Creator, ScaleDetector, Track
from .Sequence import Sequence
from .Note import Note


class Simplifier:
    @validate(None, str, str, str)
    def __init__(self, path: str, right_track_name: str, left_track_name: str) -> None:
        self.path = path
        self.right_track_name = right_track_name
        self.left_track_name = left_track_name
        self.mid = MidiFile(self.path)
        self.keycount: dict = dict()
        self.tracks: list[Track] = []

    def __remove_unneccesary(mid: MidiFile):
        def filterFunc(item: Union[Message, MetaMessage]):
            return item.type not in ["control_change", "pitchwheel", "program_change", "end_of_track", "midi_port"]
        for track in mid.tracks:
            yield list(filter(filterFunc, track))

    def simplify(self) -> Simplifier:
        for track in self.__remove_unneccesary(self.mid):
            t = Track()
            for i in range(len(track)):
                msg: Union[Message, MetaMessage] = track[i]
                if msg.is_meta:
                    if msg.type == "track_name":
                        if msg.name.upper() == self.right_track_name:
                            seq = Sequence.from_messages(
                                track).simplify_chords()
                            t.add_messages(seq.to_messages())
                            break
                        elif msg.name.upper() == self.left_track_name:
                            seq = Sequence.from_messages(track)\
                                .simplify(self.mid.ticks_per_beat)
                            t.add_messages(seq.to_messages())
                            break
                    t.add_message(msg)
                else:
                    if "note" in msg.type:
                        n = Note(msg.note, 0)
                        if n.key_name not in self.keycount:
                            self.keycount[n.key_name] = 0
                        self.keycount[n.key_name] += 1
                    else:
                        print(msg)

            self.tracks.append(t)
        return self

    @validate(None, str)
    def save(self, path: str = "./data/output/song.mid"):
        s = ScaleDetector(self.keycount)
        Creator().set_ticks_per_beat(self.mid.ticks_per_beat).add_tracks(
            [track for track in self.tracks]).save(path)
