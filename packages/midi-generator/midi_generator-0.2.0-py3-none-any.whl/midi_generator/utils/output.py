from midiutil import MIDIFile
from time import sleep
from .constants import MIDI_EVENT_NOTE_ON
from note import Note


# def play(notes: list[Note]):
#     source = MIDISource("Python")

#     for note in notes:
#         source.send((MIDI_EVENT_NOTE_ON, note.pitch, note.velocity))
#         sleep(note.end - note.start)
#         source.send((MIDI_EVENT_NOTE_ON, note.pitch, 0))


def write_file(notes: list[Note], file_name: str):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    for note in notes:
        midi.addNote(0, 0, note.pitch, note.start, note.end - note.start, note.velocity)

    with open(f'midi/{file_name}.mid', "wb") as output_file:
        midi.writeFile(output_file)
