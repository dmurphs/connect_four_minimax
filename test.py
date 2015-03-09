from connect4 import ConnectFour
from minimax import MinimaxNode
from player import Human, RandomPlayer
from utility import SimpleUtility, WithColumnUtility

b = ConnectFour()

b.play_turn(2, 0)
b.play_turn(2, 1)
b.play_turn(1, 2)
b.play_turn(1,3)
b.play_turn(1,4)
b.play_turn(2,5)


root = MinimaxNode.init_root(b, 0)
root.print_board()
utility = WithColumnUtility(5, 1, [1,1,2,4,2,1,1])
#utility.compute_utility(root, 2)
utility.compute_utility(root, 1)

print utility.score
