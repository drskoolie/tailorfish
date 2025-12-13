from pathlib import Path

from tailorfish.student import MistakeProfile, MistakeType

def analyze_pgn(path: Path) -> list[MistakeProfile]:
    return [
            MistakeProfile(
                kind=MistakeType.BLUNDER,
                frequency=1,
                avg_centipawn_loss=300.0,
                typical_move_number = 3,
                )
            ]
