# from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo, tempo2bpm
# from ..Classes import Creator, Track, ScaleDetector, Note
# mid = MidiFile()
# track = MidiTrack()
# mid.tracks.append(track)

# Keys = {
#     "C": 0,
# }
# DELTA = 100
# Creator().addTrack(Track().addTimeSignature(4, 4, 0).addTempo().addKeySignature(
#     "C", 0).addNotes(Note.fromList([
#         ["C4", DELTA],
#         ["C4", DELTA],
#         ["C4", DELTA],
#         ["C4", DELTA],
#         ["C4", DELTA]
#     ])).print(raw=True)).save("output/a.mid")
# # def setInstrument(track: MidiTrack, instrumentIndex: int = 0, delta: int = 0):
# #     track.append(Message('program_change',
# #                  program=instrumentIndex, time=delta))


# # def setKeySignature(track: MidiTrack, keyName: str = "Ab", delta: int = 0):
# #     track.append(MetaMessage('key_signature', key=keyName, time=delta))


# # setKeySignature(track, "C")
# # track.append(Message('note_on', note=64, velocity=100, time=0))
# # # track.append(Message('note_off', note=64, velocity=127, time=2048))

# # mid.save('output/new_song.mid')
