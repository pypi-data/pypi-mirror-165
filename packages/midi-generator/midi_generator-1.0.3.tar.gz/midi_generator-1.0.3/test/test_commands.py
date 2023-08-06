from midi_generator.commands import generate, mutate, continue_sequence, combine
from midi_generator.config import Configuration


def test_generate():
    notes = generate(Configuration())

    assert (len(notes) > 0)


def test_mutate():
    config = Configuration()
    notes = generate(config)
    mutant = mutate(notes)

    assert (len(mutant) > 0)


def test_continue():
    config = Configuration()
    notes = generate(config)
    continued = continue_sequence(notes, config)

    assert (len(continued) > 0)


def test_combine():
    config = Configuration()
    notes = [generate(config) for _ in range(4)]
    combined = combine(notes, config)

    assert (len(combined) > 0)
