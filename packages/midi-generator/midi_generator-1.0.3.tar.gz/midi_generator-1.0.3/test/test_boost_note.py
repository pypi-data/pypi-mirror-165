import note


def test_note_structure_exists():
    assert("Note" in dir(note))


def test_note_structure_has_attributes():
    assert("pitch" in dir(note.Note))
    assert("velocity" in dir(note.Note))
    assert("start" in dir(note.Note))
    assert("end" in dir(note.Note))


def test_can_create_note():
    test_note = note.Note(85, 100, 0, 1)
    assert(test_note.pitch == 85)
    assert(test_note.velocity == 100)
    assert(test_note.start == 0)
    assert(test_note.end == 1)
