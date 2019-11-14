import RNA
import pickle
import os
import sys

# Currently testing only Vienna 2
if __name__ == '__main__':
	puzzle_file = pickle.load(open(os.getcwd() + '/eterna100_v2.pkl', 'rb'))
	
	solved = []
	names = []

	for puzzle in puzzle_file:
		result = RNA.inverse_fold(puzzle[2], puzzle[1])[1]
		names.append(puzzle[0])
		if result == 0.0:
			solved.append(1)
		else:
			solved.append(0)

	for res, name in zip(solved, names):
		print('%s: %i' % (name, res))
	print('\nSolved %i/100' % sum(solved))
	
