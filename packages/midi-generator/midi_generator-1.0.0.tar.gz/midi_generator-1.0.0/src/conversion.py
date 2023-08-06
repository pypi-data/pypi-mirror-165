from functools import reduce

from note import Note
from .types import Gene


def individual_to_melody(individual: list[Gene]) -> list[Note]:
    notes = []
    start = 0.0
    time = 0.0
    for i, gene in enumerate(individual):
        time += 0.5

        if gene.remaining_ticks > 1:
            continue

        notes.append(Note(int(gene.pitch), int(gene.velocity), start, time))
        start = time

    return notes


def melody_to_individual(melody: list[Note]) -> list[Gene]:
    genes = [Gene(0, 0, 1)] * 32
    for note in melody:
        ticks = int((note.end - note.start) * 2) + 1
        for i in range(ticks, 0, -1):
            genes[int(note.start * 2 + ticks - i - 1)] = Gene(note.pitch, note.velocity, i)

    return genes


def encodable(notes: list[Gene]) -> str:
    return reduce(lambda x, y: x + ',' + y, [str(note.pitch) for note in notes])
