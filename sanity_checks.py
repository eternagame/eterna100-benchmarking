import pandas as pd
import os
from typing import Literal
from subprocess import Popen, PIPE, STDOUT
import re

VIENNA_VERSIONS = Literal['latest', '1.8.5', '2.1.9', '2.4.8', '2.6.3']

def fold(seq, version: VIENNA_VERSIONS = 'latest'):
    if version == 'latest':
        import RNA
        return RNA.fold(seq)[0]
    else:
        if version == '1.8.5':
            p = Popen(['.././ViennaRNA185/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        elif version == '2.1.9':
            p = Popen(['.././ViennaRNA219/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        elif version == '2.4.8':
            p = Popen(['.././ViennaRNA248/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        pair = p.communicate(seq)[0]
        formatted = re.split('\s+| \(?\s?',pair)
        return formatted[1]


def check_sample_sequences(infile: str, outfile: str, version: VIENNA_VERSIONS):
    e100 = pd.read_csv(infile, sep='\t', header='infer')

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
    e100 = pd.read_csv('eterna100v2_vienna2.tsv', sep='\t', header='infer')
    rnai = pd.read_csv('rnainverse/rnai_puzzle_solutions_v2.txt', sep='\t', header=None, names=['Puzzle Name', 'Secondary Structure', 'Solution'])

    # make the 'Secondary Structure' column lists
    strucs = e100['Secondary Structure'].tolist()
    folded_strucs = rnai['Secondary Structure'].tolist()
    names = e100['Puzzle Name'].tolist()

    # check if each structure matches the folded structure
    for i in range(100):
        if strucs[i] != folded_strucs[i]:
            print(f'{names[i]}')


def check_nemo_solutions(outfile: str = 'nemo_sanity_check.txt'):
    nemo_solutions = pd.read_csv('hannah_files/NEMO_solutions_by_puzzle.txt', header='infer', sep='\t')
    nemo_solutions = nemo_solutions[nemo_solutions['Vienna_version'] == 2]

    # need to check that they match nemo_solutions.target_structure and the e100-v2 solutions

    sols = nemo_solutions['MFE_seq_vienna2'].tolist()
    strucs = nemo_solutions['target_structure'].tolist()

    f = open(outfile, 'w')
    buggy = []
    f.write('Puzzle Name\tTarget Structure\tVienna2 Solution\tVienna2.1.9 Structure\tVienna2.4.8 Structure\n')
    for i in range(len(sols)):
        struc219 = fold(sols[i], '2.1.9')
        struc248 = fold(sols[i], '2.4.8')
        
        if struc219 != strucs[i] or struc248 != strucs[i]:
            f.write(f'{nemo_solutions.iloc[i]["puzzle_name"]}\t{strucs[i]}\t{sols[i]}\t{struc219}\t{struc248}\n')
            print(f'{nemo_solutions.iloc[i]["puzzle_name"]}\t{strucs[i]}\t{sols[i]}\t{struc219}\t{struc248}\n')
            buggy.append(nemo_solutions.iloc[i]["puzzle_name"])
    
    f.close()
    print(f'Number of buggy sequences: {len(buggy)}')
    print(buggy)


if __name__ == '__main__':
    if not os.path.exists('checks'):
        os.mkdir('checks')
    check_sample_sequences('eterna100v1_vienna1.tsv', 'checks/v1_vienna1_sanity_check.txt', '1.8.5')
    check_sample_sequences('eterna100v2_vienna1.tsv', 'checks/v2_vienna1_sanity_check.txt', '1.8.5')
    check_sample_sequences('eterna100v2_vienna2.tsv', 'checks/v2_vienna2_sanity_check.txt', 'latest')
    check_sample_sequences('eterna100v2_vienna2.tsv', 'checks/v2_vienna248_sanity_check.txt', '2.4.8')
    check_sample_sequences('eterna100v2_vienna2.tsv', 'checks/v2_vienna219_sanity_check.txt', '2.1.9')
