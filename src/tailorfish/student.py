from dataclasses import dataclass
from enum import Enum


class MistakeType(Enum):
    BLUNDER = "blunder"
    INACCURACY = "inaccuracy"
    MISSED_TACTIC = "missed_tactic"
    ENDGAME_ERROR = "endgame_error"
    OPENING_MISPLAY = "opening_misplay"


@dataclass
class MistakeProfile:
    kind: MistakeType
    frequency: int
    avg_centipawn_loss: float
    typical_move_number: int
