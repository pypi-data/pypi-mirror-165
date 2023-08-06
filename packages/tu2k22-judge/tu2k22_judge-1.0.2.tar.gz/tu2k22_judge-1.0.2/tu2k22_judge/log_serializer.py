from typing import List, Optional
from pathlib import Path
import os
import logging

from .schema import Move, PlayerMove, Player, Position
from .logger_utils import get_logger


class LogSerializer:
    def __init__(
        self, path: str, log_level: int = logging.WARN
    ) -> None:
        self.path = path
        self.logger = get_logger(__name__, level=log_level)

    def serialize(self, player_moves: List[PlayerMove]) -> List[str]:
        serialized_moves: List[str] = []
        for player_move in player_moves:
            move = player_move.move
            serialized_move = f'M, {player_move.player}, {move.src.row} {move.src.col} {move.dst.row} {move.dst.col}\n'
            serialized_moves.append(serialized_move)
        return serialized_moves

    def deserialize(self, serialized_move: str) -> Optional[PlayerMove]:
        if serialized_move[0] == "M":
            splits = serialized_move.split(", ")
            player = Player.BLUE if int(splits[1]) == 1 else Player.RED
            points = [int(point) for point in splits[2].split(" ")]
            move = Move(src=Position(row=points[0], col=points[1]), dst=Position(row=points[2], col=points[3]))
            player_move = PlayerMove(move=move, player=player)
            return player_move
        return None

    def dump(self, player_moves: List[PlayerMove], winner: Optional[Player] = None, error_message: Optional[str] = None):
        self.logger.debug(f"Dumping game moves to {self.path}")
        serialized_moves = self.serialize(player_moves=player_moves)
        Path(os.path.dirname(self.path)).mkdir(parents=True, exist_ok=True)
        with open(self.path, "w+") as log_file:
            log_file.writelines(serialized_moves)
            if winner is not None:
                log_file.write(f"W, Player {winner} wins\n")
            elif error_message is not None:
                log_file.write(f"E, {error_message}\n")

    def load(self) -> List[PlayerMove]:
        self.logger.debug(f"Loading game moves from {self.path}")
        with open(self.path, "r+") as log_file:
            serialized_moves = log_file.readlines()
        try:
            player_moves = [self.deserialize(serialized_move) for serialized_move in serialized_moves]
            for index, player_move in enumerate(player_moves):
                if player_move is None:
                    player_moves.pop(index)
            return player_moves  # type: ignore
        except Exception as ex:
            self.logger.error(
                """The log file is not valid. All lines except last line must fit into the following pattern:
                M , <player id>, <src row> <src col> <dst row> <dst col>
                """
            )
            return []
