class ConnectFour(object):
    def __init__(self):
        self.board = []
        for y in range(6):
            row =[]
            for x in range(7):
                row.append(None)
            self.board.append(row)

    def get_position(self, row, column):
        """
        Returns either None or an integer 1 or 2 depending on which player
        is occupying the given row or column.  Row is an integer between 0
        and 5 and column is an integer between 0 and 6.
        """
        assert row >= 0 and row < 6 and column >= 0 and column < 7

        return self.board[row][column]

    def match_in_direction(self, row, column, step_row, step_col):
        """
        Counts how many chips, starting from (row, column) and moving in the
        direction (step_row, step_col), match the player who occupies (row,column).

        Arguments:
        row: an integer between 0 and 5
        column: an integer between 0 and 6
        step_row: an integer, either -1, 0, or 1
        step_col: an integer, either -1, 0, or 1

        This function first checks which player occupies (row,column).  If no
        player occupies this position, 0 is returned.  Otherwise, the function
        then continues checking (row + step_row, column + step_column), (row +
        2*step_row, column + 2*step_column), and so forth, continuing until a
        location is either empty, the board edge is reached, or a position is
        occupied by an opposing player.  The function then returns how many
        chips (including the first chip at (row, column), match.  Note if the
        function returns 4 or more, this is a winning position. 
        """
        assert row >= 0 and row < 6 and column >= 0 and column < 7
        assert step_row != 0 or step_col != 0 # (0,0) gives an infinite loop

        if self.get_position(row, column) == None:
        	return 0

        team = self.get_position(row, column)

        n = 1
        while (row + n*step_row < 6 and row + n*step_row >= 0 and column + n*step_col < 7 and column + n*step_col >= 0):
        	if self.get_position(row + step_row*n, column + step_col*n) == team:
        		n += 1
        	else:
        		break

        return n

    def num_of_matches(self, y, x):
        if self.board[y][x] != None:
            checklist = []
            checklist.append(self.match_in_direction(y,x,0,1))
            checklist.append(self.match_in_direction(y,x,0,-1))
            checklist.append(self.match_in_direction(y,x,1,0))
            checklist.append(self.match_in_direction(y,x,-1,0))
            checklist.append(self.match_in_direction(y,x,1,1))
            checklist.append(self.match_in_direction(y,x,1,-1))
            checklist.append(self.match_in_direction(y,x,-1,1))
            checklist.append(self.match_in_direction(y,x,-1,-1))
            return max(checklist)

        else:
            return 0

    def is_game_over(self):
        """
        Returns None if the game is not yet over, or 1 or 2 depending
        on if player 1 or 2 has won the game.
        """
        # Note, match_in_direction is very helpful.

        # Possibly make this more efficient
        for y in range(6):
            for x in range(7):
                if self.num_of_matches(y,x) >= 4:
                    return self.board[y][x]

        return None

    def play_turn(self, player, column):
        """ Updates the board so that player plays in the given column.

        player: either 1 or 2
        column: an integer between 0 and 6
        """
        assert player == 1 or player == 2
        assert column >= 0 and column < 7

        n = 0
        while n < 6:
        	if self.board[n][column] != None:
        		n += 1
        	else:
        		break

        self.board[n][column] = player

    def is_board_full(self):
        for y in range(6):
            for x in range(7):
                if self.board[y][x] == None:
                    return False

        return True

    def num_in_column(self, col, team):
        enemy = 0
        friendly = 0
        for y in range(6):
            if self.board[y][col] != None and self.board[y][col] == team:
                friendly += 1
            elif self.board[y][col] != None and self.board[y][col] != team:
                enemy += 1
            else:
                break
        return [friendly, enemy]

    def print_board(self):
        print "-" * 29
        print "| 0 | 1 | 2 | 3 | 4 | 5 | 6 |"
        print "-" * 29
        for row in range(5,-1,-1):
            s = "|"
            for col in range(7):
                p = self.get_position(row, col)
                if p == None:
                    s += "   |"
                elif p == 1:
                    s += " x |"
                elif p == 2:
                    s += " o |"
                else:
                    # This is impossible if the code is correct, should never occur.
                    s += " ! |"
            print s
        print "-" * 29