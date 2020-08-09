import RNA
import pickle
import os
import sys
from tqdm import tqdm

def run():
	puzzle_file = pickle.load(open(os.getcwd() + '/eterna100_v2.pkl', 'rb'))

	solved = []
	names = []
		
	i = 1
	for puzzle in tqdm(puzzle_file):
		assert(len(puzzle[2]) == len(puzzle[1]), 'Starting sequence length and puzzle length do not match')
		solution, result = RNA.inverse_fold(puzzle[2], puzzle[1])
		names.append(puzzle[0])
		if result == 0.0:
			solved.append(1)
		else:
			solved.append(0)

		with open(os.getcwd()+'/rnai_puzzle_solutions_v2.txt', 'a') as f:
			f.write('%i\t%s\t%s\t%s\n' % (i, puzzle[0], puzzle[1], solution))
		
		with open(os.getcwd()+'/rnai_puzzle_results_v2.txt', 'a') as f:
			if result == 0:
				f.write('%i\n' % 0)
			else:
				f.write('%i\n' % 1)
			
		# print('Completed %i/100: %s' % (i, puzzle[0]))
		i += 1
	print('\nSolved %i/100' % sum(solved))

# Currently testing only Vienna 2
if __name__ == '__main__':
	run()
	
