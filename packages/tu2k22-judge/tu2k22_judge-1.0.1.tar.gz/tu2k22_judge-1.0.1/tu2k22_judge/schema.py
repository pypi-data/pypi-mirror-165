from typing import Any, Optional
from enum import Enum, IntEnum
from pydantic import BaseModel, validator

from .custom_exceptions import InvalidMovesException


class Piece(str, Enum):
    BLUE_BOMBER = 'B'
    BLUE_STINGER = 'b'
    EMPTY_SPACE = '_'
    RED_STINGER = 'r'
    RED_BOMBER = 'R'


class Player(IntEnum):
    RED = 0
    BLUE = 1


class InvalidMovesMessage(str, Enum):
    INVALID_STATUS_CODE = "Bot is supposed to return status code 200. Received invalid status code"
    OUT_OF_BOUNDS = "Given co-ordinates are out of bound. All Co-ordinates should be between 0 and 4"
    INVALID_DIRECTION = "Pieces cannot move backwards. Player 0 moves up the board and player 1 moves down"
    INVALID_SOURCE = "Invalid Source. Source co-ordinates must have one of the players piece on it"
    INVALID_DESTINATION = "Invalid Destination. Destination co-ordinate should be an empty space"
    INVALID_STINGER_MOVE = "Invalid Move for Stinger. Consult the rules to understand how a stinger moves"
    INVALID_BOMBER_MOVE = "Invalid Move for Bomber. Consult the rules to understand how a bomber moves"
    INVALID_ELIMINATION_TARGET = "A two jump move can be only be made by eliminating an enemy piece"
    HOME_ROW_ELIMINATION_FORBIDDEN = "Eliminations are forbidden in the home rows fo both player, i.e., row 0 and 4"


class Position(BaseModel):
    row: int
    col: int

    @validator("*")
    def validate_coordinates(cls, v):
        if not 0 <= v <= 4:
            raise InvalidMovesException(
                reason=InvalidMovesMessage.OUT_OF_BOUNDS)
        return v

    def __eq__(self, other: Any) -> bool:
        return self.row == other.row and self.col == other.col


class Move(BaseModel):
    src: Position
    dst: Position

    def __str__(self) -> str:
        return f"Source: ({self.src.row}, {self.src.col})\nDest: ({self.dst.row}, {self.dst.col})"


class BotResponse(BaseModel):
    move: Move
    data: Optional[Any] = None


class PlayerMove(BaseModel):
    move: Move
    player: Player


class GameResult(str, Enum):
    PLAYER1_WINS = "player1_wins"
    PLAYER0_WINS = "player0_wins"
    DRAW = "draw"
    INVALID = "invalid"
