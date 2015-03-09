import random
from minimax import MinimaxNode
from utility import SimpleUtility

class Player(object):
    def __init__(self, playernum):
        self.playernum = playernum

    def play_turn(self, board):
        """
        This method is passed an instance of ConnectFour.  It should examine the board
        (using methods on the ConnectFour class) and eventually call board.play_turn and return.
        """
        pass

class Human(Player):
	def __init__(self, playernum):
		super(Human, self).__init__(playernum)

	def play_turn(self, board, col):

		board.play_turn(self.playernum, col)



class RandomPlayer(Player):
	def __init__(self, playernum):
		super(RandomPlayer, self).__init__(playernum)

	def play_turn(self, board):
		col = random.randint(0,6)

		while (board.get_position(5,col) != None):
			col = random.randint(0,6)
		board.play_turn(self.playernum, col)



class MinimaxPlayer(Player):
    def __init__(self, playernum, ply_depth, utility):
        super(MinimaxPlayer, self).__init__(playernum)
        self.ply_depth = ply_depth
        self.utility = utility

    def minimax(self, node, cur_depth):
        """
        This is the recursive procedure for minimax.  It computes the number N where
        N is the best utlity that can be forced on a leaf.  This value N is stored
        in the tree node by calling set_minimax_value and is also returned from this
        method.

        The cur_depth is used to distinguish min/max nodes and the recursion ends
        once cur_depth equals self.ply_depth
        """

        if cur_depth == self.ply_depth:
        	v = self.utility.compute_utility(node, self.playernum)
        	node.set_minimax_value(v)
        	return v

        node.compute_children()

        if cur_depth % 2 == 0:
        	v = -100000
        	for child in node.children:
        		child_value = self.minimax(child, cur_depth + 1)

        		if child_value > v:
        			v = child_value


        else:
        	v = 100000
        	for child in node.children:
        		child_value = self.minimax(child, cur_depth + 1)

        		if child_value < v:
        			v = child_value

        node.set_minimax_value(v)
        return v

    def play_turn(self, board):
        # Initialize the board as a root node and run minimax.  Then find the child of the
        # a board move.
        # TODO: write me
        root = MinimaxNode.init_root(board, self.playernum)
        
        self.minimax(root, 0)
        
        max_value = -10000000

        for child in root.children:
            if child.get_minimax_value() > max_value:
                max_value = child.get_minimax_value()

        for child in root.children:
        	if child.get_minimax_value() == max_value:
        		col = child.from_parent_column
        		break

        board.play_turn(self.playernum, col)