from __future__ import annotations
from typing import Union
from .Track import Track
from .Note__ import Note__
from mido import MidiFile, Message, MetaMessage
from ..utils import remove_unneccesary
from .Chord__ import Chord__
from .Creator import Creator
from .ScaleDetector import ScaleDetector
from ..utils import MidoMessage, MidoMetaMessage


class Simplifier:
    def simplify_right_hand(self) -> Track:
        pass

    def simplify_left_hand(self, track: Track) -> Track:
        def create_start_end(track, i) -> tuple[list, list, int]:
            def get_notes_in_same_instant(track, start_index):
                result = []
                for j in range(start_index, len(track)):
                    message = track[j]
                    if message.time == 0:
                        result.append(message)
                    else:
                        break
                return result

            # get all note_on events that happend at the same time
            start = [track[i], *get_notes_in_same_instant(track, i+1)]
            # advance i
            i += len(start)
            # check bounds
            if i >= len(track):
                return start, [], i
            # mark the first note_off message of the chord and add all messages that happen with it
            end = [track[i], *get_notes_in_same_instant(track, i+1)]
            # advance i
            i += len(end)
            return start, end, i

        def create_chord(start: list, end: list, i: int) -> tuple[Chord__, int]:

            def remove_irrelevant(start: list, end: list) -> list:
                messages_to_remove = []
                for end_message in end:
                    for start_message in start:
                        if start_message.note == end_message.note:
                            break
                    else:
                        messages_to_remove.append(end_message)
                for message in messages_to_remove:
                    end.remove(message)
                return end

            new_end = remove_irrelevant(start, end)
            i -= (len(end)-len(new_end)+1)
            end = new_end
            return Chord__.from_messages(start, end), i

        def update_chord_count(chordCount: dict, chord: Chord__):
            if chord.type_name not in chordCount:
                chordCount[chord.type_name] = dict()
            if chord.root_name[:-1] not in chordCount[chord.type_name]:
                chordCount[chord.type_name][chord.root_name[:-1]] = 0
            chordCount[chord.type_name][chord.root_name[:-1]] += 1

        result = Track()
        length = len(track)
        i = 0
        # just for printing
        chordCount = dict()
        total_ticks = 0
        measure_number = 1
        # iterate over all messages
        # we use while so we can control the index ourselfs insted of for _ in range(_) which doesnt allow to control the index
        while i < length:

            msg = track[i]

            # if its a meta message just add it
            if msg.is_meta:
                result.add_message(msg)
            else:
                start, end, i = create_start_end(track, i)
                # check bounds
                if i >= length:
                    break

                # # for debugging
                # total_ticks += end[0].time + start[0].time
                # measure_number = total_ticks // (self.mid.ticks_per_beat*4) + 1
                # if measure_number == 19:
                #     # result.addNote(Note.fromName("C1", 0))
                #     pass

                # if we have a chord
                if len(start+end) > 2:
                    chord, i = create_chord(start, end, i)

                    # # for printing
                    # update_chord_count(chordCount, chord)

                    # add simplified version of the chord becuase we add only the root note
                    result.add_note(chord.simplify())
                else:
                    # t.addMessages([*start, *end])
                    pass
            i += 1
        # print(chordCount)
        return result

    def __init__(self, path: str, right_track_name: str, left_track_name: str) -> None:
        self.path = path
        self.right_track_name = right_track_name
        self.left_track_name = left_track_name
        self.mid = MidiFile(self.path)
        self.keycount: dict = dict()
        self.tracks: list[Track] = []

    def simplify(self) -> None:
        for track in remove_unneccesary(self.mid):
            t = Track()
            for i in range(len(track)):
                msg: Union[Message, MetaMessage] = track[i]
                # if count <= LIMIT:
                #     count += 1
                if msg.is_meta:
                    if msg.type == "track_name":
                        if msg.name.upper() == self.right_track_name:
                            # t = rightHand(track)
                            # no need to add because we already add it below
                            break
                        elif msg.name.upper() == self.left_track_name:
                            t = self.simplify_left_hand(track)
                            break
                    t.add_message(msg)
                else:
                    if "note" in msg.type:
                        n = Note__.from_number(msg.note, 0)
                        if n.key_name not in self.keycount:
                            self.keycount[n.key_name] = 0
                        self.keycount[n.key_name] += 1
                    else:
                        print(msg)
            # add my track
            self.tracks.append(t)
            # add original so we can compare
            self.tracks.append(Track().add_messages(m for m in track))

    def out(self):
        s = ScaleDetector(self.keycount)
        Creator().set_ticks_per_beat(self.mid.ticks_per_beat).add_tracks(
            [track for track in self.tracks]).save("./data/output/song.mid")
