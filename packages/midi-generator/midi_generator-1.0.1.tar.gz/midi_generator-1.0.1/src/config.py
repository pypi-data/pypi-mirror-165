from dataclasses import field, dataclass
from .types import Scale, Mode, Key


@dataclass
class Configuration:
    bars: int = 4
    notes_per_bar: int = 4
    ticks_per_note: int = 16
    density: float = 0.4
    rate: list[float] = field(default_factory=lambda: [1 / 4, 1 / 8])
    syncopation: float = 0.3
    scale: Scale = Scale(Key.C, Mode.MINOR)
    match: list[list[int]] = field(default=lambda: [])
    compression_method: str = 'LZ77'
    fitness_method: str = 'normal'
    consonance_rate: float = 0.8
    pitch_change_rate: float = 0.2
    length_change_rate: float = 0.1
