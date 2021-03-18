# Author:       Derek Hand
# Date:         02/27/2021
# Description:  A program that implements Janggi, or Korean Chess. The board will have 9 columns and 10 rows,
#               and each piece will have the same rules for movement as the board game. There will be two
#               players, and the blue player will always go first.


class JanggiGame:
    """
    Description:    Game class that includes the board, pieces, and state members along with controlling piece
                    movement.
    """

    def __init__(self):
        """
        Description:    Initializes the board and pieces for a new game.
        """

        self._pieces = self.new_pieces()
        self._board = self.new_board(self._pieces)
        self._turn = "B"
        self._game_state = "UNFINISHED"
        self._is_in_check = None
        self._checkmate = None

    def get_check(self):
        """
        Description:    Returns who is in check, if anyone
        """

        return self._is_in_check

    def set_is_in_check(self, player):
        """
        Description:    Updates who is in check
        Input(s):       player:     The player in check. None if neither player is in check
        """

        self._is_in_check = player

    def get_pieces(self):
        """
        Description:    Returns the boards pieces
        Output(s):      the boards pieces
        """

        return self._pieces

    def get_board(self):
        """
        Description:    Returns the board
        Output(s):      the board
        """

        return self._board

    def set_board(self, key, value):
        """
        Description:    Updates the board when a piece is moved
        Input(s):       key:    the new tuple of coordinates
                        value:  the piece object
        """

        self._board[key] = value

    def get_game_state(self):
        """
        Description:    Returns the state of the game
        Output(s):      "UNFINISHED" if the game is not complete
                        "RED_WON" if red player has won
                        "BLUE_WON" if blue player has won
        """

        return self._game_state

    def set_game_state(self, set_state):
        """
        Description:    Updates the game state
        Input(s):       set_state:  a string with what to update the game_state to.
        """

        self._game_state = set_state

    def get_turn(self):
        """
        Description:    Returns whose turn it is
        """

        return self._turn

    def set_turn(self, turn):
        """
        Description:    Updates whose turn it is
        Input(s):       "B", or "R" depending on whose turn it will be
        """

        self._turn = turn

    def new_pieces(self):
        """
        Description:    Sets up the pieces for both players by initializing the Piece class objects based on player
                        and the appropriate starting positions for each piece. This information is stored into a
                        dictionary. This is called when a new game is initialized.
        """

        pieces = {Soldier("R", 3, 0), Soldier("R", 3, 2), Soldier("R", 3, 4), Soldier("R", 3, 6), Soldier("R", 3, 8),
                  Soldier("B", 6, 0), Soldier("B", 6, 2), Soldier("B", 6, 4), Soldier("B", 6, 6), Soldier("B", 6, 8),
                  Cannon("R", 2, 1), Cannon("R", 2, 7),
                  Cannon("B", 7, 1), Cannon("B", 7, 7),
                  Chariot("R", 0, 0), Chariot("R", 0, 8),
                  Chariot("B", 9, 0), Chariot("B", 9, 8),
                  Elephant("R", 0, 1), Elephant("R", 0, 6),
                  Elephant("B", 9, 1), Elephant("B", 9, 6),
                  Horse("R", 0, 2), Horse("R", 0, 7),
                  Horse("B", 9, 2), Horse("B", 9, 7),
                  Advisor("R", 0, 3), Advisor("R", 0, 5),
                  Advisor("B", 9, 3), Advisor("B", 9, 5),
                  General("R", 1, 4),
                  General("B", 8, 4)
                  }

        return pieces

    def new_board(self, pieces):
        """
        Description:    Sets up the board for both players. Initialized when starting a new game.
        Input(s):       pieces: a dictionary of the piece locations.
        Output(s):      a new janggi board, ready to play
        """

        board = dict()
        for piece in pieces:
            board[(piece.get_row(), piece.get_column())] = piece
        return board

    def convert_coords(self, loc):
        """
        Description:    Converts the algebraic notation to cartesian coordinates
        Input(s):       loc: algebraic expression for piece placement
        """

        rows = int(loc[1:]) - 1              # to convert to 0 index

        possible_cols = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        cols = possible_cols.index(loc[0])
        return (rows, cols)

    def make_move(self, current_loc, new_loc):
        """
        Description:    Attempts to move the piece. If it is able to, captures the opponents piece if applicable,
                        update the game state if applicable, and updates player turn
        Input(s):       current_loc:    The location of the piece you want to move
                        new_loc:        The location you want to move the piece to
        Output(s):      True:   If the move has been made
                        False:  If the move is illegal
        """

        curr = self.convert_coords(current_loc)
        new  = self.convert_coords(new_loc)

        #print("Testing move from", curr, current_loc, "to", new, new_loc)

        if curr not in self.get_board():    # no pieces at that location
            return False
        if self.get_turn() != self.get_board()[curr].get_player():   # is it the players piece/turn?
            return False

        # should also check if current player is in check. If in check and not moving to get out, invalid move
        else:
            if self.get_turn() == "B" and curr == new and self.is_in_check("blue") == False:
                self.set_turn("R")
                return True
            if self.get_turn() == "R" and curr == new and self.is_in_check("red") == False:
                self.set_turn("B")
                return True

            self.possible_moves()
            if new not in self.get_board()[curr].get_moves():
                return False
            else:
                self.get_board()[curr].set_row(new[0])
                self.get_board()[curr].set_column(new[1])
                self.set_board(new, self.get_board()[curr])
                del self.get_board()[curr]                      # update board
                self.possible_moves()

                if self.get_board()[new].get_type() == "general" and \
                        self.is_in_check(self.get_turn()) == True:
                    self.get_board()[new].set_row(curr[0])
                    self.get_board()[new].set_column(curr[1])
                    self.set_board(curr, self.get_board()[new])
                    del self.get_board()[new]
                    return False
                elif self.get_turn() == "B":
                    self.possible_moves()
                    self.set_turn("R")
                    self.check_check()
                    """
                    if self.get_check() == "R":
                        for object in self.get_board():
                            # if general has no moves, and in check, checkmate (for now)
                            if self.get_board()[object].get_type() == "general" and \
                                    self.get_board()[object].get_player() == self.get_turn() and \
                                    len(self.get_board()[object].get_moves()) == 0:
                                self.set_game_state("BLUE_WON")
                    """
                    return True
                elif self.get_turn() == "R":
                    self.possible_moves()
                    self.set_turn("B")
                    self.check_check()
                    """
                    if self.get_check() == "B":
                        for object in self.get_board():
                            # if general has no moves, and in check, checkmate (for now)
                            if self.get_board()[object].get_type() == "general" and \
                                    self.get_board()[object].get_player() == self.get_turn() and \
                                    len(self.get_board()[object].get_moves()) == 0:
                                self.set_game_state("RED_WON")
                    """
                    return True
            return False

    def is_in_check(self, player):
        """
        Description:    Checks if the player is in check
        Input(s):       player: string of who we want to check, "red" or "blue"
        Output(s):      True:   if requested player is in check
                        False:  if requested player is not in check
        """

        if player == "blue" and self.get_check() == "B":
            return True
        elif player == "red" and self.get_check() == "R":
            return True
        else:
            return False

    def possible_moves(self):
        """
        Description:    The goal is to make a list of all of the possible moves on the board for each piece. This will
                        use the Piece class set_move method. I am not sure what methods it will need from the
                        JanggiGame class. Will update as needed.
        """

        for piece in self.get_pieces():
            if piece.get_type() == "soldier":
                piece.set_moves(self.soldier_moves(piece))  # sets all valid moves for each piece
            if piece.get_type() == "cannon":
                piece.set_moves(self.cannon_moves(piece))
            if piece.get_type() == "chariot":
                piece.set_moves(self.chariot_moves(piece))
            if piece.get_type() == "elephant":
                piece.set_moves(self.elephant_moves(piece))
            if piece.get_type() == "horse":
                piece.set_moves(self.horse_moves(piece))
            if piece.get_type() == "advisor":
                piece.set_moves(self.advisor_moves(piece))
            if piece.get_type() == "general":
                piece.set_moves(self.general_moves(piece))

    def check_check(self):
        """
        Description:    Checks if the move resulted in a check, or checkmate.
        Input(s):       coords:     coords to check
                        piece:      the general to check for check
        """

        for item in self.get_board():
            if self.get_board()[item].get_type() == "general" and \
                    self.get_board()[item].get_player() == self.get_turn():
                temp = (self.get_board()[item].get_row(), self.get_board()[item].get_column())
        try:
            for piece in self.get_board():
                if self.get_board()[piece].get_player() != self.get_turn():
                    if temp in self.get_board()[piece].get_moves():
                        self.set_is_in_check(self.get_turn())
                    elif temp not in self.get_board()[piece].get_moves() and self.get_check() != None:
                        self.set_is_in_check(None)

        except NameError:
            pass

        return False


    def soldier_moves(self, piece):
        """
        Description:    Determines the moves for a soldier and is called by the possible_moves method. Soldiers do not
                        move backwards, so do not have to check for that. Once they are at the last row, they can only
                        move side to side.
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        if piece.get_player() == "R":
            moves = self.soldier_moves_helper(piece, moves, 1, 0)       # test moving soldier forward one space
            moves = self.soldier_moves_helper(piece, moves, 0, 1)
            moves = self.soldier_moves_helper(piece, moves, 0, -1)
            if (piece.get_row() > 6) and (piece.get_column() > 2) and (piece.get_column() < 6):
                if piece.get_column() - 1 < 3:                      # check diagonals if in enemy palace
                    moves = self.soldier_moves_helper(piece, moves, 1, 1)
                elif piece.get_column() + 1 > 5:
                    moves = self.soldier_moves_helper(piece, moves, 1, -1)
                else:
                    moves = self.soldier_moves_helper(piece, moves, 1, 1)
                    moves = self.soldier_moves_helper(piece, moves, 1, -1)
                    # don't need to check side to side, or forward. already checked
        else:
            moves = self.soldier_moves_helper(piece, moves, -1, 0)      # blue moves "down" the list
            moves = self.soldier_moves_helper(piece, moves, 0, 1)
            moves = self.soldier_moves_helper(piece, moves, 0, -1)
            if (piece.get_row() < 3) and (piece.get_column() > 2) and (piece.get_column() < 6):
                if piece.get_column() -1 < 3:
                    moves = self.soldier_moves_helper(piece, moves, -1, 1)
                elif piece.get_column() + 1 > 5:
                    moves = self.soldier_moves_helper(piece, moves, -1, -1)
                else:
                    moves = self.soldier_moves_helper(piece, moves, -1, -1)
                    moves = self.soldier_moves_helper(piece, moves, -1, 1)
        return moves

    def soldier_moves_helper(self, piece, moves, test_row, test_column):
        """
        Description:    Instead of writing each test, write a helper function that can be called multiple times to
                        test if a given move is valid.
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
        """

        row = piece.get_row()
        col = piece.get_column()

        if row + test_row in range(10) and col + test_column in range(9):    # check if the move would leave the board
            test_coord = (row + test_row, col + test_column)    # check if square is occupied
            if test_coord not in self.get_board():
                moves[test_coord] = True
            elif self.get_board()[test_coord].get_player() != piece.get_player():   # occupied, but by other player
                moves[test_coord] = self.get_board()[test_coord]

        return moves

    def cannon_moves(self, piece):
        """
        Description:    Determines the moves for a cannon and is called by the possible_moves method
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        moves = self.cannon_moves_helper(piece, moves, 1, 0)  # vertical
        moves = self.cannon_moves_helper(piece, moves, -1, 0)
        moves = self.cannon_moves_helper(piece, moves, 0, 1)  # horizontal
        moves = self.cannon_moves_helper(piece, moves, 0, -1)

        return moves

    def cannon_moves_helper(self, piece, moves, test_row, test_col):
        """
        Description:    Called by cannon_moves to help keep the code clear
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
        """

        # will need to implement fortress jumping, but this will take care of things for now

        row = piece.get_row()
        col = piece.get_column()
        able_to_jump = False

        if test_row != 0:
            counter = 1
            while row + test_row * counter in range(10):
                test_coord = (row + test_row * counter, col)

                if test_coord not in self.get_board() and able_to_jump == False:    # can't jump yet
                    counter += 1
                    continue

                if test_coord in self.get_board() and able_to_jump == False:
                    if self.get_board()[test_coord].get_type() == "cannon":
                        # can't jump cannons, no valid moves in this direction
                        return moves
                    else:
                        able_to_jump = True
                        counter += 1
                        continue

                if test_coord not in self.get_board() and able_to_jump == True: # able to jump, not taking a piece
                    moves[test_coord] = True
                    counter += 1
                    continue

                if self.get_board()[test_coord].get_player() == piece.get_player() and able_to_jump == True:
                    break   # can't jump anymore

                elif self.get_board()[test_coord].get_player() != piece.get_player() and able_to_jump == True:
                    # able to jump, will capture enemy piece
                    moves[test_coord] = self.get_board()[test_coord]
                    break

        else:
            counter = 1
            while col + test_col * counter in range(9):
                test_coord = (row, col + test_col * counter)
                if test_coord not in self.get_board() and able_to_jump == False:  # can't jump yet
                    counter += 1
                    continue

                if test_coord in self.get_board() and able_to_jump == False:
                    if self.get_board()[test_coord].get_type() == "cannon":
                        # can't jump cannons, no valid moves in this direction
                        return moves
                    else:
                        able_to_jump = True
                        counter += 1
                        continue

                if test_coord not in self.get_board() and able_to_jump == True:  # able to jump, not taking a piece
                    moves[test_coord] = True
                    counter += 1
                    continue

                if self.get_board()[test_coord].get_player() == piece.get_player() and able_to_jump == True:
                    break   # can't jump anymore

                if self.get_board()[test_coord].get_player() != piece.get_player() and able_to_jump == True:
                    # able to jump, will capture enemy piece
                    moves[test_coord] = self.get_board()[test_coord]
                    break
        return moves

    def chariot_moves(self, piece):
        """
        Description:    Determines the moves for a chariot and is called by the possible_moves method
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()
        # need to implement diaganol when they are in the fortress. Waiting for now

        moves = self.chariot_moves_helper(piece, moves, 1, 0) # vertical
        moves = self.chariot_moves_helper(piece, moves, -1, 0)
        moves = self.chariot_moves_helper(piece, moves, 0, 1) # horizontal
        moves = self.chariot_moves_helper(piece, moves, 0, -1)

        return moves

    def chariot_moves_helper(self, piece, moves, test_row, test_col):
        """
        Description:    Called by chariot_moves to help keep the code clear
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
        """

        row = piece.get_row()
        col = piece.get_column()

        if test_row != 0:
            counter = 1
            while row + test_row*counter in range(10):
                test_coord = (row + test_row*counter, col)
                if test_coord not in self.get_board():
                    moves[test_coord] = True
                    counter += 1
                elif self.get_board()[test_coord].get_player() != piece.get_player():   # occupied, but by other player
                    moves[test_coord] = self.get_board()[test_coord]
                    break
                else:
                    break
            return moves
        else:
            counter = 1
            while col + test_col*counter in range(9):
                test_coord = (row, col + test_col*counter)
                if test_coord not in self.get_board():
                    moves[test_coord] = True
                    counter += 1
                elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                    moves[test_coord] = self.get_board()[test_coord]
                    break
                else:
                    break
            return moves

    def elephant_moves(self, piece):
        """
        Description:    Determines the moves for a elephant and is called by the possible_moves method
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        moves = self.elephant_moves_helper(piece, moves, 1, 0)  # vertical 3, over 2
        moves = self.elephant_moves_helper(piece, moves, -1, 0)
        moves = self.elephant_moves_helper(piece, moves, 0, 1)  # over 3, up/down 2
        moves = self.elephant_moves_helper(piece, moves, 0, -1)

        return moves

    def elephant_moves_helper(self, piece, moves, test_row, test_column):
        """
        Description:    Called by elephant_moves to help keep the code clear
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
                """

        row = piece.get_row()
        col = piece.get_column()

        if test_row == 1:
            if (row + test_row, col) not in self.get_board() and (row + test_row + 1, col + 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + test_row + 2) in range(10) and (col + 2) in range(9):  # up 3, 2 to the right
                    test_coord = (row + test_row + 2, col + 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

            if (row + test_row, col) not in self.get_board() and (row + test_row + 1, col - 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + test_row + 2) in range(10) and (col - 2) in range(9):  # down 3, 2 to the right
                    test_coord = (row + test_row + 2, col - 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_row == -1:
            if (row + test_row, col) not in self.get_board() and (row + test_row - 1, col + 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + test_row - 2) in range(10) and (col + 2) in range(9):  # up 3, 2 to the right
                    test_coord = (row + test_row - 2, col + 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

            if (row + test_row, col) not in self.get_board() and (row + test_row - 1, col - 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + test_row - 2) in range(10) and (col - 2) in range(9):  # down 3, 2 to the right
                    test_coord = (row + test_row - 2, col - 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_column == 1:
            if (row, col + test_column) not in self.get_board() and (row + 1, col + test_column + 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + 2) in range(10) and (col + test_column + 2) in range(9):  # over 3, up 2
                    test_coord = (row + 2, col + test_column + 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

            if (row, col + test_column) not in self.get_board() and (row - 1, col + test_column + 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row - 2) in range(10) and (col + test_column + 2) in range(9):  # over 3 down 2
                    test_coord = (row - 2, col + test_column + 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():
                        # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_column == -1:
            if (row, col + test_column) not in self.get_board() and (row + 1, col + test_column - 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row + 2) in range(10) and (col + test_column - 2) in range(9):  # over 3, up 2
                    test_coord = (row + 2, col + test_column - 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

            if (row, col + test_column) not in self.get_board() and (row - 1, col + test_column - 1) not in \
                    self.get_board():  # if any piece is blocking, can't move
                if (row - 2) in range(10) and (col + test_column - 2) in range(9):  # over 3 down 2
                    test_coord = (row - 2, col + test_column - 2)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        return moves

    def horse_moves(self, piece):
        """
        Description:    Determines the moves for a horse and is called by the possible_moves method
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        moves = self.horse_moves_helper(piece, moves, 1, 0)     # vertical 2, over 1
        moves = self.horse_moves_helper(piece, moves, -1, 0)
        moves = self.horse_moves_helper(piece, moves, 0, 1)     # over 2, up/down 1
        moves = self.horse_moves_helper(piece, moves, 0, -1)

        return moves

    def horse_moves_helper(self, piece, moves, test_row, test_column):
        """
        Description:    Called by horse_moves to help keep the code clear
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
        """

        row = piece.get_row()
        col = piece.get_column()

        # need to implement if a piece is blocking

        if test_row == 1:
            if (row + test_row, col) not in self.get_board():   # if any piece is blocking, can't move
                if (row + test_row + 1) in range(10) and (col + 1) in range(9):  # down 2, 1 to the right
                    test_coord = (row + test_row + 1, col + 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]
                if (row + test_row + 1) in range(10) and (col - 1) in range(9):  # down 2, 1 to the right
                    test_coord = (row + test_row + 1, col - 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_row == -1:
            if (row + test_row, col) not in self.get_board():   # if any piece is blocking, can't move
                if (row + test_row - 1) in range(10) and (col + 1) in range(9):  # up 2, 1 to the right
                    test_coord = (row + test_row - 1, col + 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]
                if (row + test_row - 1) in range(10) and (col - 1) in range(9):  # up 2, 1 to the right
                    test_coord = (row + test_row - 1, col - 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_column == 1:
            if (row, col + test_column) not in self.get_board():    # if any piece is blocking, can't move
                if (row + 1) in range(10) and (col + test_column + 1) in range(9):  # over 2, up 1
                    test_coord = (row + 1, col + test_column + 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]
                if (row - 1) in range(10) and (col + test_column + 1) in range(9):  # over 2 down 1
                    test_coord = (row - 1, col + test_column + 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        if test_column == -1:
            if (row, col + test_column) not in self.get_board():    # if any piece is blocking, can't move
                if (row + 1) in range(10) and (col + test_column - 1) in range(9):  # over 2, up 1
                    test_coord = (row + 1, col + test_column - 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]
                if (row - 1) in range(10) and (col + test_column - 1) in range(9):  # over 2 down 1
                    test_coord = (row - 1, col + test_column - 1)
                    if test_coord not in self.get_board():
                        moves[test_coord] = True
                    elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                        moves[test_coord] = self.get_board()[test_coord]

        return moves

    def advisor_moves(self, piece):
        """
        Description:    Determines the moves for an advisor and is called by the possible_moves method. Will call
                        general_moves_helper as the advisors have to adhere to the same rules
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        if (piece.get_row(), piece.get_column()) == (0, 3) or (piece.get_row(), piece.get_column()) == (7, 3):
            moves = self.general_moves_helper(piece, moves, 0, 1)
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, 1)
        if (piece.get_row(), piece.get_column()) == (0, 5) or (piece.get_row(), piece.get_column()) == (7, 5):
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, -1)

        if (piece.get_row(), piece.get_column()) == (2, 3) or (piece.get_row(), piece.get_column()) == (9, 3):
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, 1)
            moves = self.general_moves_helper(piece, moves, -1, 1)

        if (piece.get_row(), piece.get_column()) == (2, 5) or (piece.get_row(), piece.get_column()) == (8, 5):
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, -1, -1)

        if (piece.get_row(), piece.get_column()) == (1, 4) or (piece.get_row(), piece.get_column()) == (8, 4):
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, 1)
            moves = self.general_moves_helper(piece, moves, 1, -1)

            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 0, 1)

            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, -1, 1)
            moves = self.general_moves_helper(piece, moves, -1, -1)

        else:
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 0, 1)

        return moves

    def general_moves(self, piece):
        """
        Description:    Determines the moves for a general and is called by the possible_moves method
        Input(s):       piece:  The piece that is at a particular location on the board
        """

        moves = dict()

        if (piece.get_row(), piece.get_column()) == (0, 3) or (piece.get_row(), piece.get_column()) == (7, 3):
            moves = self.general_moves_helper(piece, moves, 0, 1)
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, 1)

        if (piece.get_row(), piece.get_column()) == (0, 5) or (piece.get_row(), piece.get_column()) == (7, 5):
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, -1)

        if (piece.get_row(), piece.get_column()) == (2, 3) or (piece.get_row(), piece.get_column()) == (9, 3):
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, 1)
            moves = self.general_moves_helper(piece, moves, -1, 1)

        if (piece.get_row(), piece.get_column()) == (2, 5) or (piece.get_row(), piece.get_column()) == (8, 5):
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, -1, -1)

        if (piece.get_row(), piece.get_column()) == (1, 4) or (piece.get_row(), piece.get_column()) == (8, 4):
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, 1, 1)
            moves = self.general_moves_helper(piece, moves, 1, -1)

            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 0, 1)

            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, -1, 1)
            moves = self.general_moves_helper(piece, moves, -1, -1)

        else:
            moves = self.general_moves_helper(piece, moves, 1, 0)
            moves = self.general_moves_helper(piece, moves, -1, 0)
            moves = self.general_moves_helper(piece, moves, 0, -1)
            moves = self.general_moves_helper(piece, moves, 0, 1)

        temp = dict()

        for item in moves:
            for object in self.get_board():
                if item in self.get_board()[object].get_moves() and \
                    self.get_turn() != self.get_board()[object].get_player():
                    temp[item] = item

        for item in temp:
            if item in moves:
                del moves[item]
        return moves

    def general_moves_helper(self, piece, moves, test_row, test_column):
        """
        Description:    Called by general_moves to help keep the code clear
        Input(s):       piece:          the piece to check if the move is valid
                        moves:          dictionary of possible moves for the piece
                        test_row:       the row to test the move
                        test_column:    the column to test the move
        """

        row = piece.get_row()
        col = piece.get_column()

        if piece.get_player() == "R":
            if (row + test_row >= 0) and (row + test_row < 3) and (col + test_column > 2) and (col + test_column < 6):
                test_coord = (row + test_row, col + test_column)  # check if square is occupied
                if test_coord not in self.get_board():
                    moves[test_coord] = True
                elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                    moves[test_coord] = self.get_board()[test_coord]

        if piece.get_player() == "B":
            if (row + test_row > 6) and (row + test_row < 10) and (col + test_column > 2) and (col + test_column < 6):
                test_coord = (row + test_row, col + test_column)  # check if square is occupied
                if test_coord not in self.get_board():
                    moves[test_coord] = True
                elif self.get_board()[test_coord].get_player() != piece.get_player():  # occupied, but by other player
                    moves[test_coord] = self.get_board()[test_coord]
        return moves


    def show_board(self):
        """
        Description:    Used for my own sanity checks, will comment out for the final graded version
        """
        from game2dboard import Board

        b = Board(10, 9)  # 3 rows, 4 columns, filled w/ None
        b.cell_size = 80
        for item in self.get_board().keys():
            b[item[0]][item[1]] = self.get_board()[item].get_name()
        b.show()

class Piece:
    """
    Description:    Represents a piece object in the game. It is also the parent class for each piece type.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes a piece object for the given player and position. Called by JanggiGame when
                        the game is first initialized
        Input(s):       player: the player who's pieces are being initialized
                        row:    x-coordinate to place the piece
                        column: y-coordinate to place the piece
        """

        self._player = player
        self._row = row
        self._column = column
        self._moves = dict()       # used to track moves available to each piece

    def get_row(self):
        """
        Description:    Returns the row the piece is in
        """

        return self._row

    def set_row(self, value):
        """
        Description:    Updates the row value the piece is in
        Input(s):       value:  The new row value
        """

        self._row = value

    def get_column(self):
        """
        Description:    Returns the column the piece is in
        """

        return self._column

    def set_column(self, value):
        """
        Description:    Updates the column value the piece is in
        Input(s):       value:  the new column value
        """

        self._column = value

    def get_player(self):
        """
        Description:    Returns who belongs the piece at the given location
        """

        return self._player

    def get_moves(self):
        """
        Description:    Returns the pieces available moves
        """

        return self._moves

    def set_moves(self, moves):
        """
        Description:    Updates a pieces available moves
        """

        self._moves = moves


class Soldier(Piece):
    """
    Description:    Represents the soldier pieces. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the soldier piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Soldier"
        self._type = "soldier"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class Cannon(Piece):
    """
    Description:    Represents the cannon pieces. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the cannon piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Cannon"
        self._type = "cannon"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class Chariot(Piece):
    """
    Description:    Represents the chariot pieces. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the chariot piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Chariot"
        self._type = "chariot"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class Elephant(Piece):
    """
    Description:    Represents the elephants. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the elephant piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Elephant"
        self._type = "elephant"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class Horse(Piece):
    """
    Description:    Represents the horses. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the horse piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Horse"
        self._type = "horse"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class Advisor(Piece):
    """
    Description:    Represents the Advisors. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the advisor piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "Advisor"
        self._type = "advisor"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


class General(Piece):
    """
    Description:    Represents the generals. A child class of Piece. Used to make an object for each piece
                    on the board.
    """

    def __init__(self, player, row, column):
        """
        Description:    Initializes the general piece for a given player using the parent Piece class.
        Input(s):       player: who to initialize the piece for
                        row:    what row to initialize the piece in
                        column: what column to initialize the piece in
        """

        super().__init__(player, row, column)
        self._name = str(player) + "General"
        self._type = "general"

    def get_name(self):
        """
        Description:    Returns the name of the piece and who owns it. Will be used for sanity checks
        """

        return self._name

    def get_type(self):
        """
        Description:    Returns what kind of piece it is
        """

        return self._type


if __name__ == "__main__":
    game = JanggiGame()
    game.make_move("c7", "c6")
    game.make_move("c1", "d3")
    game.make_move("b10", "d7")
    game.make_move("b3", "e3")
    game.make_move("c10", "d8")
    game.make_move("h1", "g3")
    game.make_move("e7", "e6")
    game.make_move("e3", "e6")
    game.make_move("h8", "c8")
    game.make_move("d3", "e5")
    game.make_move("c8", "c4")
    game.make_move("e5", "c4")
    game.make_move("i10", "i8")
    game.make_move("g4", "f4")
    game.make_move("i8", "f8")
    game.make_move("g3", "h5")
    game.make_move("h10", "g8")
    game.make_move("e6", "e3")
    game.make_move("e9", "d9")
    game.show_board()