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


def off_beatness(notes: list[Note]) -> float:
    b = [x for x in filter(lambda i: len(notes) % i == 0, range(1, len(notes) + 1))]
    weights = [0 if len(list(filter(lambda i: x % i == 0, b))) else 1 for x in notes]
    return sum(weights) / len(notes)


def density(notes) -> float:
    return len(list(filter(lambda note: note.velocity != 0, notes))) / len(notes)
