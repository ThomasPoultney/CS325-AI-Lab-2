import enum
import random
import math

class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == []

	# for inserting an element in the queue
	def insert(self, data):
		self.queue.append(data)

	# for popping an element based on Priority
	def pop(self):
		try:
			max = 0
			for i in range(len(self.queue)):
				if self.queue[i] > self.queue[max]:
					max = i
			item = self.queue[max]
			del self.queue[max]
			return item
		except IndexError:
			print()
			exit()

class Node:
	def __init__(self, board, move, ancestor,value):
		self.board = board
		self.ancestor = ancestor
		self.move = move
		self.value = value
		self.cost = self.calcCost()

	def __eq__(self, other):
		if other == None:
			return False
		return self.board == other.board

	def __lt__(self, other):
		if other == None:
			return False
		return self.cost > other.cost

	def __gt__(self, other):
		if other == None:
			return False
		return self.cost < other.cost

	def calcCost(self):
		return (sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
			for i, val in enumerate(self.board) if val) + self.value)


class Move(enum.Enum):
	LEFT 	= 0
	RIGHT 	= 1
	DOWN 	= 2
	UP 		= 3

# ============================================================================ #

def generateProblem():
	array = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	random.shuffle(array)
	if checkSolvable(array) == False:
		array = generateProblem()
	return array

def checkSolvable(array):
	numInversions = 0
	for i in range(0,8):
		startValue = array[i]
		for j in range(i, 8):
			if startValue < array[j]:
				numInversions += 1
	return (numInversions % 2 == 1)

def performMove(node, move, value):
	emptyIndex = node.board.index(0)
	newBoard = node.board.copy()
	if move == Move.LEFT:
		newBoard[emptyIndex] = newBoard[emptyIndex - 1]
		newBoard[emptyIndex - 1] = 0
	if move == Move.RIGHT:
		newBoard[emptyIndex] = newBoard[emptyIndex + 1]
		newBoard[emptyIndex + 1] = 0
	if move == Move.DOWN:
		newBoard[emptyIndex] = newBoard[emptyIndex + 3]
		newBoard[emptyIndex + 3] = 0
	if move == Move.UP:
		newBoard[emptyIndex] = newBoard[emptyIndex - 3]
		newBoard[emptyIndex - 3] = 0

	return Node(newBoard, move, node,value)


def explore(goal, start, debug):
	# Setup
	node = Node(start.copy(), None, None)
	explored = []
	exploreQueue = PriorityQueue()

	# Iterate through until goal found
	while node.board != goal:
		if debug:
			print("\nCurrent Board:\t\t" + str(node.board))
			print("# Seen Boards:\t\t" + str(len(explored)))

		# Check if the node has been explored, if not add it to the list
		if node in explored:
			if debug:
				print("Seen current board, skipping...")
			node = exploreQueue.pop()
			continue
		explored.append(node)

		# Figure out which moves can be made and add them to the tree
		emptyIndex = node.board.index(0)
		if emptyIndex == 1 or emptyIndex == 2 or emptyIndex == 4 or emptyIndex == 5 or emptyIndex == 7 or emptyIndex == 8: # END MY LIFE
			exploreQueue.insert(performMove(node, Move.LEFT))
			if debug:
				print("Able to move:\t\tLEFT")
		if emptyIndex == 0 or emptyIndex == 1 or emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 6 or emptyIndex == 7: # END MY LIFE
			exploreQueue.insert(performMove(node, Move.RIGHT))
			if debug:
				print("Able to move:\t\tRIGHT")
		if emptyIndex == 0 or emptyIndex == 1 or emptyIndex == 2 or emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 5: # END MY LIFE
			exploreQueue.insert(performMove(node, Move.DOWN))
			if debug:
				print("Able to move:\t\tDOWN")
		if emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 5 or emptyIndex == 6 or emptyIndex == 7 or emptyIndex == 8: # END MY LIFE
			exploreQueue.insert(performMove(node, Move.UP))
			if debug:
				print("Able to move:\t\tUP")

		# Move on to the next priority node
		node = exploreQueue.pop()

	return node


def exploreAS(goal, start, debug):
	# Setup
	node = Node(start.copy(), None, None,0)
	node.value = 0
	cost = node.value
	explored = []
	exploreQueue = PriorityQueue()

	# Iterate through until goal found
	while node.board != goal:
		if debug:
			print("\nCurrent Board:\t\t" + str(node.board))
			print("# Seen Boards:\t\t" + str(len(explored)))

		# Check if the node has been explored, if not add it to the list
		if node in explored:
			if debug:
				print("Seen current board, skipping...")
			node = exploreQueue.pop()
			continue
		explored.append(node)

		# Figure out which moves can be made and add them to the tree
		emptyIndex = node.board.index(0)
		if emptyIndex == 1 or emptyIndex == 2 or emptyIndex == 4 or emptyIndex == 5 or emptyIndex == 7 or emptyIndex == 8: # END MY LIFE
			tempNode = performMove(node, Move.LEFT,(node.value+1))
			tempNode.value = (node.value+1)
			exploreQueue.insert(tempNode)
			if debug:
				print("Able to move:\t\tLEFT")
		if emptyIndex == 0 or emptyIndex == 1 or emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 6 or emptyIndex == 7: # END MY LIFE
			tempNode = performMove(node, Move.RIGHT,(node.value+1))
			tempNode.value = (node.value+1)
			exploreQueue.insert(tempNode)
			if debug:
				print("Able to move:\t\tRIGHT")
		if emptyIndex == 0 or emptyIndex == 1 or emptyIndex == 2 or emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 5: # END MY LIFE
			tempNode = performMove(node, Move.DOWN,(node.value+1))
			tempNode.value = (node.value+1)
			exploreQueue.insert(tempNode)
			if debug:
				print("Able to move:\t\tDOWN")
		if emptyIndex == 3 or emptyIndex == 4 or emptyIndex == 5 or emptyIndex == 6 or emptyIndex == 7 or emptyIndex == 8: # END MY LIFE
			tempNode = performMove(node, Move.UP,(node.value+1))
			exploreQueue.insert(tempNode)
			if debug:
				print("Able to move:\t\tUP")

		# Move on to the next priority node
		node = exploreQueue.pop()


	return node

goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
#start = generateProblem()
start = [3,0,2,6,5,1,4,7,8]

print("\nSolving: " + str(start) + "...\n")

root = Node(start, None, None,0)
result = exploreAS(goal, start, False)
#result = explore(goal, start, True)

curNode = result
moves = []
while curNode.ancestor != None:
	moves.insert(0, curNode.move)
	print(curNode.board)
	curNode = curNode.ancestor

print("\n==================================================================\n")
print(str(start))
print("MOVES REQUIRED:\t " + str(len(moves)))
moveStr = "MOVE ORDER:\t "
for m in moves:
	if m == Move.UP:
		moveStr += "U"
	if m == Move.DOWN:
		moveStr += "D"
	if m == Move.LEFT:
		moveStr += "L"
	if m == Move.RIGHT:
		moveStr += "R"
print(moveStr)
