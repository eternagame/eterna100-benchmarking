import RNA
import pickle
import os
import sys
import pandas as pd
from tqdm import tqdm

# Currently testing only Vienna 2
if __name__ == '__main__':
	puzzle_file = pd.read_csv(os.getcwd() + '/eterna100_v1_tabs.txt', sep='\t', delimiter='\t', names=['Name', 'Structure', 'Start', 'Locks'])
	
	solved = []
	names = []
		
	i = 1
	for puzzle in tqdm(puzzle_file):
		assert(len(puzzle[2]) == len(puzzle[1]), 'Starting sequence length and puzzle length do not match')
		result = RNA.inverse_fold(puzzle[2], puzzle[1])[1]
		names.append(puzzle[0])
		if result == 0.0:
			solved.append(1)
		else:
			solved.append(0)
			
		# print('Completed %i/100: %s' % (i, puzzle[0]))
		i += 1

	for res in solved:
		print('%i' % res)
	print('\nSolved %i/100' % sum(solved))
	
