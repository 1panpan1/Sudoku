# coding: utf-8
import logging
import time
import random

def solver(board, used_rows, used_cols, used_blks):	
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 0:
				blk_num = i // 3 * 3 + j // 3
				for k in range(1, 10, 1):
					if used_rows[i][k] == 0 and used_cols[j][k] == 0 and used_blks[blk_num][k] == 0:
						board[i][j] = k
						used_rows[i][k] = 1
						used_cols[j][k] = 1
						used_blks[blk_num][k] = 1
						if solver(board, used_rows, used_cols, used_blks) is False:
							board[i][j] = 0
							used_rows[i][k] = 0
							used_rows[j][k] = 0
							used_blks[blk_num][k] = 0
						else:
							return True
				return False
	return True

def lasVegas(board, n):
	used_rows = [[0 for i in range(10)] for i in range(9)]
	used_cols = [[0 for i in range(10)] for i in range(9)]
	used_blks = [[0 for i in range(10)] for i in range(9)]
	
	for i in range(len(board)):
		for j in range(len(board[i])):
			board[i][j] = 0

	while n > 0:
		i = random.randint(0, 8)
		j = random.randint(0, 8)
		if board[i][j] == 0:
			k = random.randint(1, 9)
			blk_num = i // 3 * 3 + j // 3
			if used_rows[i][k] == 0 and used_cols[j][k] == 0 and used_blks[blk_num][k] == 0:
				board[i][j] = k
				used_rows[i][k] = 1
				used_cols[j][k] = 1
				used_blks[blk_num][k] = 1
				n -= 1
	logging.info("Solving the generated board")
	if solver(board, used_rows, used_cols, used_blks) is True:
		logging.info("Generated board is valid.")
		return True
	else:
		logging.warn("Generated board is invalid.")
		return False

def printBoard(board):
	for row in board:
		for col in row:
			print(col, end=' ')
		print('')

def generateBoard(n = 11):
	board = [[0 for i in range(9)] for i in range(9)]

	count = 0
	while lasVegas(board, n) is False:
		count += 1
		logging.info("Try lasVegas")
	
	printBoard(board)
	print("count = {}".format(count))

if __name__ == '__main__':
	logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
	generateBoard()