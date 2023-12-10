import pandas as pd
import os
from typing import Literal
from subprocess import Popen, PIPE, STDOUT
import re

VIENNA_VERSIONS = Literal['latest', '2.1.9', '2.4.8']

def fold(seq, version: VIENNA_VERSIONS = 'latest'):
    if version == 'latest':
        import RNA
        return RNA.fold(seq)[0]
    else:
        if version == '2.1.9':
            p = Popen(['.././ViennaRNA219/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        elif version == '2.4.8':
            p = Popen(['.././ViennaRNA248/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        pair = p.communicate(seq)[0]
        formatted = re.split('\s+| \(?\s?',pair)
        return formatted[1]


def check_v2_sequences(outfile: str = 'v2_sanity_check.txt', version: VIENNA_VERSIONS = 'latest'):
    e100 = pd.read_csv('eterna100_vienna2.txt', sep='\t', header='infer')
    # make the 'Sample Solution (1)' and 'Sample Solution (2)' columns lists
    sols1 = e100['Sample Solution'].tolist()
    strucs = e100['Secondary Structure'].tolist()
    names = e100['Puzzle Name'].tolist()

    buggy = []
    f = open(outfile, 'w')
    for i in range(100):
        struc1 = fold(sols1[i], version)
        if struc1 != strucs[i]:
            f.write(f'{names[i]}\t{strucs[i]}\t{sols1[i]}\t{struc1}\n')
            buggy.append(names[i])
        else:
            f.write('fine\n')
    
    f.close()

    print(f'Number of buggy sequences: {len(buggy)}')
    print(buggy)


def check_identical_structures():
    e100 = pd.read_csv('eterna100_vienna2.txt', sep='\t', header='infer')
    rnai = pd.read_csv('rnainverse/rnai_puzzle_solutions_v2.txt', sep='\t', header=None, names=['Puzzle Name', 'Secondary Structure', 'Solution'])

    # make the 'Secondary Structure' column lists
    strucs = e100['Secondary Structure'].tolist()
    folded_strucs = rnai['Secondary Structure'].tolist()
    names = e100['Puzzle Name'].tolist()

    # check if each structure matches the folded structure
    for i in range(100):
        if strucs[i] != folded_strucs[i]:
            print(f'{names[i]}')


if __name__ == '__main__':
    check_v2_sequences(version='2.4.8')
