from player import Human, RandomPlayer, MinimaxPlayer
from connect4 import ConnectFour
from utility import SimpleUtility, WithColumnUtility

def play_game(board, player1, player2):
    """
    Alternates calling play_turn for players 1 and 2.  In between move3s, checks for a winning
    board position.  If a winning position is found, prints a message saying who is the winner
    and returns.
    """

    winner = None
    while (winner == None):
    	player1.play_turn(board)
        if board.is_board_full() == True:
            print "Tie"
            board.print_board()
            return
    	winner = board.is_game_over()
    	if winner == None:
            player2.play_turn(board)
            if board.is_board_full() == True:
                print "Tie"
                board.print_board()
                return
        winner = board.is_game_over()
    board.print_board()
    print "Player " + str(winner) + " Wins"
    return

board = ConnectFour()
p1 = MinimaxPlayer(playernum = 1, ply_depth=4, utility=WithColumnUtility(5,1, [1,2,3,4,3,2,1]))
p2 = MinimaxPlayer(playernum=2, ply_depth=4, utility=WithColumnUtility(5,1, [1,2,3,4,3,2,1]))
play_game(board, p1, p2)

'''
Minimax will typically win in no more than six moves when playing against random player.

Minimax puts up a bit of challenge at ply depth 2 but is not terribly difficult to beat.
It sometimes detects if i'm about to win and blocks me.

Minimax does slightly better with higher ply depth and is very difficult to beat at ply depth 4.
It gets better at blocking wins.

If minimax with ply depth 3 and minimax with ply depth 2 play each other, when two goes first, two wins.
When three goes first, they tie?

Ply depth 2 always beats ply depth 4?

It seems that it works best when three score is 5 and two score is 1.
The results vary as the utility scores change.

The board at the end of a ply depth two vs ply depth four game has the left side of the board filled
and the right side not.

I cannot win against minimax using WithColumnUtility

When playing With Column Utility against SimpleUtility, The utility point totals
make a large difference compared to the ply depth.

Larger three in a row values seem to make the biggest differences due to the point discreapencies and
calculation weight against the two in a row values.

For a larger configuration, it wouldn't be necessary to give extra points to a situation where two possible
three in a rows could happen because a deeper ply would detect the configuration.
'''