from note import Note
from math import floor


def weighted_note_to_beat(notes: list[Note]) -> float:
    if len(notes) < 5:
        return -1
    total = 0

    for note in notes:
        left = floor(note.start)
        right = left + 1
        distance = min(note.start - left, abs(note.start - right))

        if distance == 0:
            continue
        if right < note.end < right + 1:
            total += 2 / distance
        else:
            total += 1 / distance

    return total / len(notes)


def density(notes) -> float:
    return len(list(filter(lambda note: note.remaining_ticks != 0, notes))) / len(notes)
