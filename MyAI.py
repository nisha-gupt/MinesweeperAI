# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================


from AI import AI
from Action import Action
from collections import deque
import random



class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.board = Board(rowDimension, colDimension, totalMines)
		self.zeros = deque()
		self.uncovered = deque()
		self.covered = set()
		self.to_flag = deque()
		self.flags = set()
		self.visited = set()
		self.exhausted = set()
		self.tiles = 0

		self.action = Action(AI.Action.UNCOVER, startX, startY)
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		if self.tiles == self.board.goal:
			return Action(AI.Action.LEAVE)

		if number == 0:
			if (self.action.getX(), self.action.getY()) in self.uncovered:
				self.uncovered.remove((self.action.getX(),self.action.getY()))
			x = self.getNeighbors(self.action.getX(), self.action.getY(), self.visited, self.visited)
			if len(x) != 0:
				self.zeros.extend(x)

		else:
			self.uncovered.append((self.action.getX(), self.action.getY()))
			self.board.update((self.action.getX(), self.action.getY()), number)
			if self.board.board[self.action.getY()][self.action.getX()] == 0:
				x = self.getNeighbors(self.action.getX(), self.action.getY(), self.visited, self.visited)
				if len(x) != 0:
					self.zeros.extend(x)

		self.visited.add((self.action.getX(), self.action.getY()))

		if len(self.to_flag) != 0:
			f = self.to_flag[0]
			self.to_flag.popleft()
			self.action = Action(AI.Action.FLAG, f[0], f[1])


		if len(self.zeros) != 0:
			if self.zeros[0] in self.covered:
				self.covered.remove(self.zeros[0])
			self.action = Action(AI.Action.UNCOVER, self.zeros[0][0], self.zeros[0][1])
			self.tiles += 1
			self.zeros.popleft()


		else:
			c = 0
			for point in self.uncovered.copy():
				if point in self.uncovered:
					n = self.getNeighbors(point[0], point[1], self.visited)
					if len(n) == 0:
						self.uncovered.remove(point)
					else:
						self.covered |= set(n)
						if len(n) == self.board.board[point[1]][point[0]]:
							c+=1
							for neighbor in n:
								self.flag(neighbor)

			if (c == 0):
				probabilities = {}
				for p in self.covered:
					probabilities[p] = 0
					x = self.getNeighbors(p[0], p[1], self.covered)
					for n in x:
						if n in self.uncovered:
							probabilities[p] += self.board.board[n[1]][n[0]]

				it = sorted(list(probabilities.items()),key=lambda x: x[1],reverse = True)
				if len(it) != 0:
					self.flag(it[0][0])

				elif len(self.covered) != 0:
					r = random.choice(list(self.covered))
					self.action = Action(AI.Action.UNCOVER, r[0], r[1])
					self.tiles += 1


			if len(self.to_flag) != 0:
				f = self.to_flag[0]
				self.to_flag.popleft()
				self.action = Action(AI.Action.FLAG, f[0], f[1])
		#print(self.tiles)
		return self.action

		# return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def getNeighbors(self, x, y, group=set(), add_to = set()):
		neighbors = []
		if self.board.inBounds((x-1, y)) and (x-1, y) not in group: #and self.board.board[x-1][y] == 0:
			add_to.add((x-1, y))
			neighbors.append((x-1,y))
			#self.board.update((x-1,y))

		if self.board.inBounds((x-1, y-1)) and (x-1, y-1) not in group: #and self.board.board[x-1][y-1] == 0:
			add_to.add((x-1, y-1))
			neighbors.append((x-1,y-1))
			#self.board.update((x - 1, y-1))

		if self.board.inBounds((x-1, y+1)) and (x-1, y+1) not in group: #and self.board.board[x-1][y+1] == 0:
			neighbors.append((x-1,y+1))
			add_to.add((x - 1, y + 1))
			#self.board.update((x - 1, y+1))

		if self.board.inBounds((x, y-1)) and (x, y-1) not in group: #and self.board.board[x][y-1] == 0:
			add_to.add((x, y - 1))
			neighbors.append((x,y-1))
			#self.board.update((x, y-1))

		if self.board.inBounds((x, y+1)) and (x, y+1) not in group: #and self.board.board[x][y+1] == 0:
			add_to.add((x, y + 1))
			neighbors.append((x,y+1))
			#self.board.update((x, y+1))

		if self.board.inBounds((x+1, y)) and (x+1, y) not in group: #and self.board.board[x+1][y] == 0:
			add_to.add((x+1, y))
			neighbors.append((x+1,y))
			#self.board.update((x+1, y))

		if self.board.inBounds((x+1, y-1)) and (x+1, y-1) not in group: #and self.board.board[x+1][y-1] == 0:
			add_to.add((x +1, y - 1))
			neighbors.append((x+1,y-1))
			#self.board.update((x+1, y-1))

		if self.board.inBounds((x+1, y+1)) and (x+1, y+1) not in group: #and self.board.board[x+1][y+1] == 0:
			add_to.add((x + 1, y + 1))
			neighbors.append((x+1,y+1))

			#self.board.update((x+1, y+1))

		return neighbors



	def flag(self, point):
		self.flags.add(point)
		self.to_flag.append(point)
		self.covered.remove(point)
		self.board.board[point[1]][point[0]] = 0
		self.visited.add(point)

		for p in self.getNeighbors(point[0],point[1], self.flags):
			self.board.update(p, -1)
			if self.board.board[p[1]][p[0]] == 0:
				x = self.getNeighbors(p[0], p[1], self.visited, self.visited)
				if len(x) != 0:
					self.zeros.extend(x)




class Board:

	def __init__(self, rowDim, colDim, numMines):
		self.rows = rowDim
		self.cols = colDim
		self.board = [[0 for i in range(colDim)] for j in range(rowDim)]
		self.goal = rowDim * colDim - numMines

	def update(self, coord, number):
		try:
			self.board[coord[1]][coord[0]] += number
		except IndexError:
			pass

	def inBounds(self, coord):
		return (0 <= coord[0] < self.cols) and (0 <= coord[1] < self.rows)


class Constraint:

	def __init__(self, point, variables, value):
		self.point = point
		self.variables = variables
		self.value = value

	def isTrivial(self):
		return self.value == len(self.variables)