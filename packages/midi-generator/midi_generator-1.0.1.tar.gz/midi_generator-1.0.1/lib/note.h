#pragma once
#include <iostream>

namespace midi_generator
{
    class Note;
}

class midi_generator::Note {
public:
    Note(int p=0, int v=0, double s=0.0f, double e=0.0f) : pitch(p), velocity(v), start(s), end(e) {}
    Note(const Note &note) : pitch(note.pitch), velocity(note.velocity), start(note.start), end(note.end) {}
    int pitch;
    int velocity;
    double start;
    double end; 
    bool operator==(const Note &rhs) const {
        return pitch == rhs.pitch &&
            velocity == rhs.velocity &&
            start == rhs.start &&
            end == rhs.end;
    }
    bool operator!=(const Note &rhs) const {
        return !(rhs == *this);
    }

    Note& operator=(const Note& note) = default;

    friend std::ostream& operator<<(std::ostream& os, const Note& note) {
        os << "Note(" << note.pitch << ", " << note.velocity << ", " << note.start << ", " << note.end << ")\n";
        return os;
    }
};