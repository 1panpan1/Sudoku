# coding: utf-8
import logging
import time
import random
import copy
from collections import Counter

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
							used_cols[j][k] = 0
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
		input()
		return False

def printBoard(board):
	for row in board:
		for col in row:
			print(col, end=' ')
		print('')

def checkRule(board, x):
	# Keep at least 3 grids per row
	if Counter(board[x])[0] > 6:
		return False
	else:
		return True

def next_dig(board, pre_x, pre_y, how= 'random'):
	if how == 'random':
		while True:
			x, y, = random.randint(0, 8), random.randint(0, 8)
			if board[x][y] != 0 and checkRule(board, x) is True: break
		return x, y
	elif how == 'updown':
		pos = pre_x * 9 + pre_y
		while True:
			pos = (pos + 1) % 81 
			x, y = pos // 9, pos % 9
			if board[x][y] != 0 and checkRule(board, x) is True: break
		return x, y

def countNonzero(board):
	count = 0
	for row in board:
		for col in row:
			if col != 0: count += 1
	return count

def checkUnique(board, x, y):
	tmp_board = copy.deepcopy(board)

	used_rows = [[0 for i in range(10)] for i in range(9)]
	used_cols = [[0 for i in range(10)] for i in range(9)]
	used_blks = [[0 for i in range(10)] for i in range(9)]
	
	tmp_board[x][y] = 0
	for i in range(len(tmp_board)):
		for j in range(len(tmp_board[i])):
			blk_num_tmp = i // 3 * 3 + j // 3 
			if tmp_board[i][j] != 0:
				used_rows[i][tmp_board[i][j]] = 1
				used_cols[j][tmp_board[i][j]] = 1
				used_blks[blk_num_tmp][tmp_board[i][j]] = 1
	
	blk_num = x // 3 * 3 + y // 3
	for k in range(1, 10, 1):
		if k != board[x][y] and used_rows[x][k] == 0 and used_cols[y][k] == 0 and used_blks[blk_num][k] == 0:
			tmp_board[x][y] = k
			used_rows[x][k] = 1
			used_cols[y][k] = 1
			used_blks[blk_num][k] = 1
			if solver(tmp_board, used_rows, used_cols, used_blks) is True:
				return False
			used_rows[x][k] = 0
			used_cols[y][k] = 0
			used_blks[blk_num][k] = 0
	return True

def digBoard(board, n, limit= 81):
	# Keep n grids
	to_dig = 81 - n
	dig_x, dig_y = 0, -1

	while to_dig > 0 and limit > 0:
		dig_x, dig_y = next_dig(board, dig_x, dig_y, how="random")
		limit -= 1
		if checkUnique(board, dig_x, dig_y) is True:
			board[dig_x][dig_y] = 0
			to_dig -= 1
		else:
			pass

def generateBoard(n = 11):
	board = [[0 for i in range(9)] for i in range(9)]

	count = 1
	while lasVegas(board, n) is False:
		count += 1

	logging.info("Run lasVegas {} times".format(count))
	answer = copy.deepcopy(board)
	digBoard(board, 22)
	# digBoardRecur(board, 81 - 24)

	printBoard(board)
	print("Numbers= {}".format(countNonzero(board)))
	print('===========')
	printBoard(answer)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
	generateBoard()