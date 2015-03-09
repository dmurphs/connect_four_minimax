class Utility(object):
	def compute_utility(self, node, utilityplayer):
		"""
		Computes the utility of node with positive values good for utilityplayer
		and negative values good for the other player.
		"""
		pass

class SimpleUtility(Utility):
	def __init__(self, three_score, two_score):
		self.three_score = three_score
		self.two_score = two_score

	def compute_utility(self, node, utilityplayer):
		directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
		self.score = 0

		if utilityplayer == 1:
			enemy = 2
		else:
			enemy = 1
		if node.is_game_over() == utilityplayer:
			self.score = 1000000
		elif node.is_game_over() == enemy:
			
			self.score = -1000000
		else:
			for y in range(6):
				for x in range(7):
					for direction in directions:
						matches = node.match_in_direction(y, x, direction[0], direction[1])
						if matches == 2:
							if node.board[y][x] == utilityplayer:
								self.score += self.two_score
							else:
								self.score -= self.two_score
						elif matches == 3:
							#improvements to function here
							if y - direction[0] >= 0 and y + 3*direction[0] >= 0 and y - direction[0] <= 5 and y + 3*direction[0] <= 5 and x - direction[1] >= 0 and x + 3*direction[1] >= 0 and x - direction[1] <= 6 and x + 3*direction[1] <= 6:
								if node.board[y - direction[0]][x - direction[1]] != utilityplayer and node.board[y + 3*direction[0]][x + 3*direction[1]] != utilityplayer:
									self.score += 0
								else:
									self.score += self.three_score
							#improvements end
							elif node.board[y][x] == utilityplayer:
								self.score += self.three_score
							else:
								self.score -= self.three_score

		if node.nodeplayer == utilityplayer:
			self.score += 1
		else:
			self.score -= 1

		return self.score

class WithColumnUtility(SimpleUtility):
    def __init__(self, three_score, two_score, column_scores):
        self.three_score = three_score
        self.two_score = two_score
        self.column_scores = column_scores

    def compute_utility(self, node, utilityplayer):
        score = super(WithColumnUtility, self).compute_utility(node, utilityplayer)

        for i in range(7):
        	row_nums = node.num_in_column(i, utilityplayer)
        	score += self.column_scores[i]*row_nums[0]
        	score -= self.column_scores[i]*row_nums[1]
        # TODO: use self.column_scores to assign points to each chip

        return score