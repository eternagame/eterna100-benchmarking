import RNA
import pickle
import os
import sys

# Currently testing only Vienna 2
if __name__ == '__main__':
	puzzle_file = pickle.load(open(os.getcwd() + '/eterna100_v2.pkl', 'rb'))
	
	solved = []
	names = []
        
        i = 1
	for puzzle in puzzle_file:
                assert(len(puzzle[2]) == len(puzzle[1]), 'Starting sequence length and puzzle length do not match')
		result = RNA.inverse_fold(puzzle[2], puzzle[1])[1]
		names.append(puzzle[0])
		if result == 0.0:
			solved.append(1)
		else:
			solved.append(0)
                print('Completed %i/100: %s' % (i, puzzle[0]))

                i += 1

	for res, name in zip(solved, names):
		print('%s: %i' % (name, res))
	print('\nSolved %i/100' % sum(solved))
	
