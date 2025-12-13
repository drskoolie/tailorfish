from dataclasses import dataclass
from pathlib import Path
from types import TracebackType

import chess
import chess.engine


@dataclass
class StockfishEvaluator:
    engine_path: Path
    depth: int = 10

    def __post_init__(self) -> None:
        self._engine = chess.engine.SimpleEngine.popen_uci(str(self.engine_path))

    def close(self) -> None:
        self._engine.quit()

    def __enter__(self) -> "StockfishEvaluator":
        return self


    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc: BaseException | None,
        _tb: TracebackType | None,
    ) -> None:

        self.close()

    def eval_cp(self, board: chess.Board) -> int:
        info = self._engine.analyse(board, chess.engine.Limit(depth=self.depth))
        score = info["score"].pov(board.turn)
        cp = score.score(mate_score=10000)

        assert cp is not None
        return cp
    
