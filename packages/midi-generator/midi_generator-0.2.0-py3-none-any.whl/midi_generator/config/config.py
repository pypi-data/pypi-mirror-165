from dataclasses import field, dataclass
from ..utils.scale import Scale, Mode, Key

@dataclass
class Configuration:
    bars: int = 4
    density: float = 0.4
    rate: list[float] = field(default_factory=lambda: [1 / 4, 1 / 8])
    syncopation: float = 0.3
    scale: Scale = Scale(Key.C, Mode.MINOR)
    is_polyphonic: bool = False
