import pickle
import os
import sys
import pandas as pd
from tqdm import tqdm
from subprocess import PIPE, Popen, STDOUT
import re

RNAINVERSE_PATH = '../../ViennaRNA-1.8.5/Progs/./RNAinverse' 
RNAFOLD_PATH = '../../ViennaRNA-1.8.5/Progs/./RNAfold'  

def inverse_fold(struc, start):
	p = Popen([RNAINVERSE_PATH, '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
	pair = p.communicate(input='%s\n%s' % (struc, start))[0]
	formatted = re.split('\s+| \(?\s?',pair)
	return formatted[0]

def fold(struc):
	p = Popen([RNAFOLD_PATH, '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
	pair = p.communicate(input='%s' % struc)[0]
	formatted = re.split('\s+| \(?\s?',pair)
	return formatted[1]


if __name__ == '__main__':
	df = pd.read_csv(os.getcwd() + '/eterna100_v1_tabs.txt', sep='\t', delimiter='\t', names=['Name', 'Structure', 'Start', 'Locks'])
	struc = df['Structure'].tolist()
	start = df['Start'].tolist()
	puzzle_file = list(zip(start, struc))
	
	solved = []
	names = []
		
	i = 1
	for puzzle in tqdm(puzzle_file):
		# assert(len(puzzle[2]) == len(puzzle[1]), 'Starting sequence length and puzzle length do not match')
		result = RNA.inverse_fold(puzzle[0], puzzle[1])[1]
		names.append(puzzle[0])
		if result == 0.0:
			solved.append(1)
		else:
			solved.append(0)
			
		# print('Completed %i/100: %s' % (i, puzzle[0]))
		i += 1

	for res in solved:
		print('%i' % res)
	with open(os.getcwd() + '/results_rnai_vienna_1.txt', 'w') as f:
		for res in solved:
			f.write("%i\n" % res)
	print('\nSolved %i/100' % sum(solved))
	