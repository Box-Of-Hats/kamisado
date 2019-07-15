from enum import Enum
from colorama import Fore, Back, Style, init


class Players(Enum):
    WHITE = 0
    BLACK = 1


class Colors(Enum):
    ANY = -1
    NONE = 0
    ORANGE = 1
    BLUE = 2
    PURPLE = 3
    PINK = 4
    YELLOW = 5
    RED = 6
    GREEN = 7
    BROWN = 8


color_mappings = {
    Colors.ORANGE: Fore.WHITE + Style.BRIGHT,
    Colors.BLUE: Fore.BLUE,
    Colors.PURPLE: Fore.MAGENTA,
    Colors.PINK: Fore.WHITE + Style.DIM,
    Colors.YELLOW: Fore.YELLOW,
    Colors.RED: Fore.RED,
    Colors.GREEN: Fore.GREEN,
    Colors.BROWN: Fore.CYAN
}


class Piece():
    def __init__(self, owner_id, color):
        self.owner_id = owner_id
        self.color = color

    def __repr__(self):
        return str(self.color)


class Kamisado():
    def __init__(self):
        self.gameboard = [[Piece(Players.BLACK, Colors.ORANGE), Piece(Players.BLACK, Colors.BLUE), Piece(Players.BLACK, Colors.PURPLE), Piece(Players.BLACK, Colors.PINK), Piece(Players.BLACK, Colors.YELLOW), Piece(Players.BLACK, Colors.RED), Piece(Players.BLACK, Colors.GREEN), Piece(Players.BLACK, Colors.BROWN)],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [Piece(Players.WHITE, Colors.BROWN), Piece(Players.WHITE, Colors.GREEN), Piece(Players.WHITE, Colors.RED), Piece(Players.WHITE, Colors.YELLOW), Piece(Players.WHITE, Colors.PINK), Piece(Players.WHITE, Colors.PURPLE), Piece(Players.WHITE, Colors.BLUE), Piece(Players.WHITE, Colors.ORANGE), ]]
        self.cell_colors = [[Colors.ORANGE, Colors.BLUE, Colors.PURPLE, Colors.PINK, Colors.YELLOW, Colors.RED, Colors.GREEN, Colors.BROWN],
                            [Colors.RED, Colors.ORANGE, Colors.PINK, Colors.GREEN,
                                Colors.BLUE, Colors.YELLOW, Colors.BROWN, Colors.PURPLE],
                            [Colors.GREEN, Colors.PINK, Colors.ORANGE, Colors.RED,
                                Colors.PURPLE, Colors.BROWN, Colors.YELLOW, Colors.BLUE],
                            [Colors.PINK, Colors.PURPLE, Colors.BLUE, Colors.ORANGE,
                                Colors.BROWN, Colors.GREEN, Colors.RED, Colors.YELLOW],
                            [Colors.YELLOW, Colors.RED, Colors.GREEN, Colors.BROWN,
                                Colors.ORANGE, Colors.BLUE, Colors.PURPLE, Colors.PINK],
                            [Colors.BLUE, Colors.YELLOW, Colors.BROWN, Colors.PURPLE,
                                Colors.RED, Colors.ORANGE, Colors.PINK, Colors.GREEN],
                            [Colors.PURPLE, Colors.BROWN, Colors.YELLOW, Colors.BLUE,
                                Colors.GREEN, Colors.PINK, Colors.ORANGE, Colors.RED],
                            [Colors.BROWN, Colors.GREEN, Colors.RED, Colors.YELLOW, Colors.PINK, Colors.PURPLE, Colors.BLUE, Colors.ORANGE]]
        self.current_turn_player = Players.WHITE
        self.current_turn_color = Colors.ANY

    def move_piece_ignoring_constraints(self, _from, to):
        """
        Move a piece from one location to another, ignoring any movement constraints.

        _from -- The coordinates to move from e.g (0, 4)
        to    -- The coordinates to move to e.g (1, 4)
        """
        moving_piece = self.get_moving_piece(_from)
        self.gameboard[_from[1]][_from[0]] = 0
        self.gameboard[to[1]][to[0]] = moving_piece

    def move_piece(self, _from, to):
        """
        Move a piece from one location to another, following movement constraints.

        _from -- The coordinates to move from e.g (0, 4)
        to    -- The coordinates to move to e.g (1, 4)

        return bool - was the move successful?
        """
        is_move_legal = self.is_move_legal(_from, to)
        if (is_move_legal):
            self.move_piece_ignoring_constraints(_from, to)

            # Update the players turn
            if (self.current_turn_player == Players.WHITE):
                self.current_turn_player = Players.BLACK
            else:
                self.current_turn_player = Players.WHITE

            # Update the turn color
            self.current_turn_color = self.cell_colors[to[1]][to[0]]

        return is_move_legal

    def is_path_blocked(self, _from, to):
        """
        Check if there are pieces in the way between two locations.
        """
        if _from[1] > to[1]:
            y_range = list(range(_from[1], to[1], -1))
        else:
            y_range = list(range(_from[1], to[1]))

        if _from[0] > to[0]:
            x_range = list(range(_from[0], to[0], -1))
        else:
            x_range = list(range(_from[0], to[0]))

        # If move is diagonal:
        if abs(to[0] - _from[0]) == abs(to[1] - _from[1]):
            cells_to_check = list(zip(x_range, y_range))
            # Dont check current position:
            if _from in cells_to_check:
                cells_to_check.remove(_from)
        # If move is vertical:
        elif _from[0] == to[0]:
            x_range = [_from[0]]*len(y_range)
            cells_to_check = list(zip(x_range, y_range))
            if _from in cells_to_check:
                cells_to_check.remove(_from)
        # If move is horizontal:
        elif _from[1] == to[1]:
            y_range = [_from[1]]*len(x_range)
            cells_to_check = list(zip(x_range, y_range))
            if _from in cells_to_check:
                cells_to_check.remove(_from)
        else:
            return False

        # Dont check current position:
        if _from in cells_to_check:
            cells_to_check.remove(_from)
        for x, y in cells_to_check:
            if self.get_moving_piece((x, y)) != None:
                return True
        return False

    def is_move_legal(self, _from, to):
        moving_piece = self.get_moving_piece(_from)

        # Is there a piece in the from location?
        if (moving_piece == None):
            return False

        # Is there a piece in the to location?
        if (self.get_moving_piece(to) != None):
            return False

        # Is the to location on the board?
        if (len(self.gameboard) <= to[1]):
            return False

        if (len(self.gameboard[0]) <= to[0]):
            return False

        # Is the from location on the board?
        if (len(self.gameboard) <= _from[1]):
            return False

        if (len(self.gameboard[0]) <= _from[0]):
            return False

        # Is the piece of the correct color?
        if (moving_piece.color != self.current_turn_color and self.current_turn_color != Colors.ANY):
            return False

        # Does the piece belong to the current player?
        if (moving_piece.owner_id != self.current_turn_player):
            return False

        # Is the piece moving forwards?
        if (moving_piece.owner_id == Players.WHITE):
            # White moves upwards
            if (_from[1] <= to[1]):
                return False
        else:
            # Black moves downwards
            if (_from[1] >= to[1]):
                return False

        # Is the move in a straight line if its diagonal??
        vector = (abs(_from[0] - to[0]), abs(_from[1] - to[1]))
        if vector[0] != 0 and vector[1] != 0 and vector[0] != vector[1]:
            return False

        # Is the path blocked?
        if (self.is_path_blocked(_from, to)):
            return False

        return True

    def get_winner(self):
        for cell in self.gameboard[0]:
            if isinstance(cell, Piece) and cell.owner_id == Players.WHITE:
                return Players.WHITE

        for cell in self.gameboard[-1]:
            if isinstance(cell, Piece) and cell.owner_id == Players.BLACK:
                return Players.BLACK

        return None

    def get_moving_piece(self, loc):
        try:
            moving_piece = self.gameboard[loc[1]][loc[0]]
            if isinstance(moving_piece, Piece):
                return moving_piece
            else:
                return None
        except IndexError:
            return None

    def draw(self):

        for x, row in enumerate(self.gameboard):
            for y, cell in enumerate(row):
                color = ""
                player_style = ""
                if isinstance(cell, Piece):
                    color_of_cell = cell.color
                    value_of_cell = cell.color.value
                else:
                    color_of_cell = self.cell_colors[y][x]
                    value_of_cell = "☐"

                color = color_mappings[color_of_cell]

                print("{}{}{}{}".format(
                    color, player_style, value_of_cell, Style.RESET_ALL), end=" ")
            print("")


if __name__ == "__main__":
    init()  # Colorama
    game = Kamisado()
    while True:
        game.draw()
        user_in = input("Your move\n>").split(" ")
        _from = (int(user_in[0]), int(user_in[1]))
        to = (int(user_in[2]), int(user_in[3]))
        is_move_valid = game.move_piece(_from, to)
        print("Move:\t", _from, "=>", to)
        print("Valid:\t", is_move_valid)
        print("Turn:\t", game.current_turn_player)
        print("Color:\t{}{}{}".format(
            color_mappings[game.current_turn_color], game.current_turn_color, Style.RESET_ALL))
        if (game.get_winner() != None):
            print("Game over, winner is: ", game.get_winner())
