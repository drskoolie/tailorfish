from pathlib import Path

from textual.app import App

from tailorfish.analysis import GameEvaluator, load_games_into_ram

class TailorfishTUI(App):
    BINDINGS = [
            ("q", "quit", "Quit")
            ]

    def action_quit(self):
        self.exit()

if __name__ == "__main__":
    if False:
        pgn_path_drskoolie = Path("data/raw/lichess_drskoolie_2025-12-14.pgn")
        games = load_games_into_ram(pgn_path_drskoolie)

        ge = GameEvaluator()
        ge.load_game_directly(games[0]["game"], games[0]["target"])
        df = ge.move_analyzer()

    app = TailorfishTUI()
    app.run()
