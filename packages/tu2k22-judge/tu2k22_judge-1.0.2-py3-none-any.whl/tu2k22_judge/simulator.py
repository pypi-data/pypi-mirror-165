from pydoc import plain
from time import sleep
from typing import Any, List, Optional, Tuple
import logging

import requests
from requests import Timeout
from colorama import Fore, Style
from pydantic import ValidationError

from .schema import Piece, Move, Player, InvalidMovesMessage, BotResponse, PlayerMove, Position
from .custom_exceptions import InvalidMovesException, TimeoutException, MovesExceededException
from .constants import MAX_MOVES_ALLOWED
from .logger_utils import get_logger, game_visualizer


class Simulator:
    def __init__(self, move_timeout: int = 4, visualize: bool = True, logging_level: int = logging.WARNING) -> None:
        pieces = ['B', 'b', '_', 'r', 'R']
        self.board = [[pieces[i] for _ in range(5)] for i in range(5)]
        self.RED_PIECES = [Piece.RED_BOMBER, Piece.RED_STINGER]
        self.BLUE_PIECES = [Piece.BLUE_BOMBER, Piece.BLUE_STINGER]
        self.move_timeout = move_timeout
        self.logger = get_logger(__name__, level=logging_level)
        self.visualizer = game_visualizer(level=logging_level)
        if visualize:
            self.visualizer.setLevel(level=logging.INFO)

    def print_board(self):
        """
            Print Board state while testing bots in local development
        """
        self.visualizer.info(Fore.BLACK + Style.BRIGHT + "  0 1 2 3 4")
        for index, row in enumerate(self.board):
            row_message = Fore.BLACK + Style.BRIGHT + str(index) + " "
            for cell in row:
                if cell in self.RED_PIECES:
                    row_message += Fore.RED + cell + " "
                elif cell in self.BLUE_PIECES:
                    row_message += Fore.BLUE + cell + " "
                else:
                    row_message += Fore.WHITE + cell + " "
            # row_message = Fore.RESET + Style.RESET_ALL
            self.visualizer.info(row_message)
        self.visualizer.info(Fore.BLACK + Style.DIM +
                             "==================================================")
        self.visualizer.info(Fore.RESET + Style.RESET_ALL)

    @staticmethod
    def validate_direction(move: Move, player: Player):
        """
        Check if player is moving in correct vertical direction, blue should move down the board, red should move up
        """
        sign = 2*player - 1
        absolute_direction = move.dst.row - move.src.row
        if absolute_direction*sign < 0:
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_DIRECTION, player=player)

    def validate_endpoints(self, move: Move, player: Player) -> None:
        """
        Check if the source and destination endpoints are valid.
        Source should hold a piece of the player and destination should be an empty space
        Raise an exception if this is not followed, return None otherwise

        Parameters
        ----------
        move : Move
        player : Player

        Raises
        ------
        InvalidMovesException
        InvalidMovesException
        """
        if self.board[move.dst.row][move.dst.col] != Piece.EMPTY_SPACE:
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_DESTINATION, player=player)
        if (player == player.BLUE and self.board[move.src.row][move.src.col] not in self.BLUE_PIECES) or (
            player == player.RED and self.board[move.src.row][move.src.col] not in self.RED_PIECES
        ):
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_SOURCE, player=player)
        return None

    def validate_elimination_move(self, move: Move, player: Player) -> None:

        if move.src.row == move.dst.row == 0 or move.src.row == move.dst.row == 4:
            raise InvalidMovesException(
                reason=InvalidMovesMessage.HOME_ROW_ELIMINATION_FORBIDDEN, player=player)
        eliminated_row = int((move.src.row + move.dst.row) / 2)
        eliminated_col = int((move.src.col + move.dst.col) / 2)
        eliminated_piece = self.board[eliminated_row][eliminated_col]

        if (
            player == Player.RED and eliminated_piece in self.BLUE_PIECES
        ) or (
            player == Player.BLUE and eliminated_piece in self.RED_PIECES
        ):
            return None
        else:
            print(f"{self.BLUE_PIECES}, {self.RED_PIECES}")
            print(
                f"player {player}, elim_coords {eliminated_row, eliminated_col}, eliminated_piece: {eliminated_piece}")
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_ELIMINATION_TARGET, player=player)

    def validate_stinger_move(self, move: Move, player: Player):
        if abs(move.src.row - move.dst.row) == abs(move.src.col - move.dst.col) == 1:
            # simply diagonal move (direction in y axis has already been validated)
            return None
        elif (
            # horizontal elimination
            abs(move.src.row - move.dst.row) == 2 and move.src.col == move.dst.col
        ) or (
            # vertical elimination
            abs(move.src.col - move.dst.col) == 2 and move.src.row == move.dst.row
        ):
            self.validate_elimination_move(move, player)
        else:
            # move doesn't fit either simple moves or elimination moves
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_STINGER_MOVE, player=player)

    def validate_bomber_move(self, move: Move, player: Player):
        if abs(move.src.col - move.dst.col) <= 1 and abs(move.src.row - move.dst.row) <= 1 and move.src != move.dst:
            return  # single move in any direction
        elif (
            # horizontal elimination
            abs(move.src.row - move.dst.row) == 2 and move.src.col == move.dst.col
        ) or (
            # vertical elimination
            abs(move.src.col - move.dst.col) == 2 and move.src.row == move.dst.row
        ):
            self.validate_elimination_move(move, player)
        else:
            raise InvalidMovesException(
                reason=InvalidMovesMessage.INVALID_BOMBER_MOVE, player=player)

    def validate_move(self, move: Move, player: Player) -> None:
        """
        Check if the move is valid for the given board state and given Player
        Raise the required exception if move is invalid, return None otherwise
        Parameters
        ----------
        move : Move
        player : Player
        """
        self.logger.debug(f"Validating Player {player} Move")

        if player == Player.BLUE:
            color = Fore.BLUE
        else:
            color = Fore.RED
        self.visualizer.info(color + Style.BRIGHT + f"Player {player} move")
        self.visualizer.info(color + Style.BRIGHT + str(move))
        self.visualizer.info(Fore.RESET + Style.RESET_ALL)
        self.validate_direction(move, player)
        self.validate_endpoints(move, player)
        piece = self.board[move.src.row][move.src.col]
        if piece in [Piece.BLUE_STINGER, Piece.RED_STINGER]:
            self.validate_stinger_move(move, player)
        else:
            self.validate_bomber_move(move, player)

    def make_move(self, move: Move, player: Player):
        """
        Make the given move and Modify the board state accordingly

        Parameters
        ----------
        move : Move
        player : Player
        """
        self.board[move.dst.row][move.dst.col] = self.board[move.src.row][move.src.col]
        self.board[move.src.row][move.src.col] = Piece.EMPTY_SPACE
        if abs(move.src.row - move.dst.row) == 2 or abs(move.src.col - move.dst.col) == 2:
            eliminated_x_coord = int((move.src.row + move.dst.row) / 2)
            eliminated_y_coord = int((move.src.col + move.dst.col) / 2)
            self.board[eliminated_x_coord][eliminated_y_coord] = Piece.EMPTY_SPACE

    def check_if_game_over(self) -> Tuple[bool, Optional[Player]]:
        # RED BOMBER reaches blue home row
        if Piece.RED_BOMBER in self.board[0]:
            return True, Player.RED
        # BLUE BOMBER reaches red home row
        elif Piece.BLUE_BOMBER in self.board[4]:
            return True, Player.BLUE
        return False, None

    def simulate(self, bot_urls: List[str], bot_data: List[Any], player_moves: List[PlayerMove]):
        player = Player.BLUE
        self.logger.debug("Starting game simulation")
        self.print_board()
        while len(player_moves) < MAX_MOVES_ALLOWED:
            bot_input = {"board": self.board,
                         "data": bot_data[player], "player": player}

            response = requests.post(
                bot_urls[player], json=bot_input, timeout=self.move_timeout, headers={
                    "Content-Type": "application/json"}
            )
            if response.status_code != 200:
                self.logger.error(
                    f"Invalid status code {response.status_code} received from player {player}. Expected: {200}")
                raise InvalidMovesException(
                    InvalidMovesMessage.INVALID_STATUS_CODE, player=player)

            try:
                bot_response = BotResponse.validate(response.json())
                bot_data[player] = bot_response.data
                player_moves.append(PlayerMove(
                    move=bot_response.move, player=player))

                self.validate_move(bot_response.move, player=player)
                self.make_move(bot_response.move, player=player)
                self.print_board()
                game_over, winner = self.check_if_game_over()
                if game_over:
                    self.logger.info(f"Player {player} wins")
                    return winner
                if player == Player.BLUE:
                    player = Player.RED
                else:
                    player = Player.BLUE
            except InvalidMovesException as imex:
                self.logger.error(
                    f"Invalid response received from player: {player}. Message: ", imex.message)
                # append player info to exception
                raise InvalidMovesException(reason=imex.reason, player=player)
            except Timeout as t:
                self.logger.error(f"Request to player: {player} times out")
                raise TimeoutException(player=player)
            except ValidationError as ve:
                self.logger.error(
                    f"Invalid response received from player: {player}. Message: ", str(ve))
                raise InvalidMovesException(
                    reason=f"Incorrect schema", player=player)
        raise MovesExceededException()

    def replay(self, player_moves: List[PlayerMove]):
        self.print_board()
        for player_move in player_moves:
            if player_move is None:
                return
            player = player_move.player
            move = player_move.move
            try:
                self.validate_move(move=move, player=player)
                self.make_move(player=player, move=move)
                self.print_board()
                winner = self.check_if_game_over()
                if winner[0]:
                    self.logger.info(f"Player {winner[1]} wins!")
                sleep(1)
            except InvalidMovesException as ex:
                self.logger.error(
                    f"Invalid response received from player: {player}. Message: {ex.message}")
                # append player info to exception
                raise InvalidMovesException(reason=ex.reason, player=player)

    def play(self):
        self.print_board()
        self.visualizer.info(Fore.BLACK + Style.BRIGHT +
                             "Enter the inputs turn by turn in the following format: <src row> <src col> <dst row> <dst col>")
        self.visualizer.info("Spaces matter!")
        self.visualizer.info(Fore.RESET + Style.RESET_ALL)
        player = Player.BLUE
        while not self.check_if_game_over()[0]:
            prompt_color = Fore.BLUE if player == Player.BLUE else Fore.RED
            input_string = input(
                prompt_color + f"Player {player}:\n" + Fore.RESET)
            try:
                positions = [int(pos) for pos in input_string.split(" ")]
                move = Move(src=Position(row=positions[0], col=positions[1]), dst=Position(
                    row=positions[2], col=positions[3]))
                self.validate_move(move=move, player=player)
                self.make_move(move=move, player=player)
                self.print_board()
                if player == Player.BLUE:
                    player = player.RED
                else:
                    player = Player.BLUE
            except InvalidMovesException as ex:
                self.visualizer.error(
                    Fore.RED + Style.BRIGHT + f"Entered move was invalid. Reason: {str(ex)}")
                self.visualizer.info(
                    Fore.BLACK + Style.BRIGHT + f"Play again as player {player}")
                self.print_board()
                self.visualizer.info(Fore.RESET + Style.RESET_ALL)
            except Exception as ex:
                self.visualizer.error(
                    Fore.RED + Style.BRIGHT + f"Entered move format was incorrect. Play again as player {player}")
                self.visualizer.info(
                    "Enter the inputs in the following format: <src row> <src col> <dst row> <dst col>")
                self.visualizer.info("Spaces matter!")
                self.print_board()
        _, winner = self.check_if_game_over()
        prompt_color = Fore.BLUE if winner == Player.BLUE else Fore.RED
        self.visualizer.info(
            prompt_color + f"Player {winner} wins!" + Fore.RESET)
