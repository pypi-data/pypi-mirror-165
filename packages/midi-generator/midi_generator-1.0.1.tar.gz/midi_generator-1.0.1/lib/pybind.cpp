//
// Created by Andrei Gheorghe on 31.08.2022.
//

#include <pybind11/pybind11.h>
#include "note.h"

PYBIND11_MODULE(note, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    pybind11::class_<midi_generator::Note>(m, "Note")
            .def(pybind11::init<int, int, double, double>())
            .def_readwrite("pitch", &midi_generator::Note::pitch)
            .def_readwrite("velocity", &midi_generator::Note::velocity)
            .def_readwrite("start", &midi_generator::Note::start)
            .def_readwrite("end", &midi_generator::Note::end)
            .def("__repr__", [](const midi_generator::Note &note) {
                return "pitch: " + std::to_string(note.pitch) + " velocity: " + std::to_string(note.velocity) + \
                       " start: " + std::to_string(note.start) + " end: " + std::to_string(note.end);
            });
}