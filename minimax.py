from connect4 import ConnectFour

class MinimaxNode(ConnectFour):

    @staticmethod
    def init_root(copyfrom, nodeplayer):
        """
        Creates a new instance of the MinimaxNode class, with the board state copied
        from the copyfrom object, which is an instance of the ConnectFour class.  

        Also, create two properties:
        * a nodeplayer property, storing the fact that this node is a play for nodeplayer.
        * a from_parent_column property set to None (see below).  This marks that the
          node did not come from a parent.

        This method should only be used to create the root of the game tree from
        the current board state.
        """
        node = MinimaxNode()
        node.nodeplayer = nodeplayer
        node.from_parent_column = None

        for y in range(6):
            for x in range(7):
                node.board[y][x] = copyfrom.board[y][x]

        return node

    @staticmethod
    def init_child(parent, playcolumn):
        """
        Creates a MinimaxNode by copying the board state from parent (which is an instance
        of MinimaxNode) and then making a play in playcolumn (which is an integer
        between 0 and 6).

        Also, create two properties:
        * nodeplayer property, which is the opposite of the parent nodeplayer, representing
          that the child is now a play for the other player.
        * from_parent_column property, which stores the playcolumn parameter.  This is used to
          know which column was played to to get from the parent to the child, and is used
          at the very end to know which play to make.
        """
        node = MinimaxNode()
        # TODO: set properties on node
        if parent.nodeplayer == 1:
            node.nodeplayer = 2
        else:
            node.nodeplayer = 1

        node.from_parent_column = playcolumn

        for y in range(6):
            for x in range(7):
                node.board[y][x] = parent.board[y][x]


        node.play_turn(parent.nodeplayer, node.from_parent_column)

        return node

    def compute_children(self):
        """
        Computes the list of children of this node and stores it in a property called children.
        This method only creates the immediate children (this is lazy evaluation).
        """
        # Iterate the non-full columns, createing a new node for each.
        self.children = []
        for i in range(7):
            if self.get_position(5, i) == None:
                self.children.append(self.init_child(self, i))
        

    def set_minimax_value(self, val):
        """
        Stores the minimax value for this node.  This represents the largest utility
        that can be forced on a leaf no matter how the enemy plays.
        """
        self.value = val

    def get_minimax_value(self):
        """
        From this node, it is possible to reach a leaf with this utility.
        """
        return self.value