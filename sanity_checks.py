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


def check_sample_sequences(infile: str, version: VIENNA_VERSIONS):
    print(f'Checking sample solution file {infile} with vienna version {version}')
    solutions = pd.read_csv(infile, sep='\t', header='infer')
    for (_, solution) in solutions.iterrows():
        if solution['Sample Solution'] == 'Undisclosed' or solution['Sample Solution'] == 'Unsolved': continue
        folded = fold(solution['Sample Solution'], version)
        if folded != solution['Secondary Structure']:
            print(f'BAD FOLDED SEQUENCE for puzzle {solution["Puzzle Name"]}: got {folded} - should be {solution["Secondary Structure"]:}')

def check_sequences(
    puzzle_infile: str,
    solution_infile: str,
    version: VIENNA_VERSIONS
):
    print(f'Checking solution file {puzzle_infile} against solution file {solution_infile} with vienna version {version}')
    puzzles = pd.read_csv(puzzle_infile, sep='\t', header='infer')
    solutions = pd.read_csv(solution_infile, sep='\t', header='infer')
    
    for (_, solution) in solutions.iterrows():
        correct_ss = puzzles[puzzles['Puzzle Name'] == solution['Puzzle Name']]['Secondary Structure'].iloc[0]
        if correct_ss != solution['Secondary Structure']:
            print(f'BAD TARGET STRUCTURE for puzzle {solution["Puzzle Name"]} is {solution["Puzzle Name"]} but should be {correct_ss}')
        folded = fold(solution['Solution'], version)
        if folded != correct_ss:
            print(f'BAD FOLDED SEQUENCE for puzzle {solution["Puzzle Name"]}: got {folded} - should be {correct_ss}')

if __name__ == '__main__':
    check_sample_sequences('eterna100v1_vienna1.tsv', '1.8.5')
    check_sample_sequences('eterna100v2_vienna1.tsv', '1.8.5')
    check_sample_sequences('eterna100v2_vienna2.tsv', 'latest')
    check_sample_sequences('eterna100v2_vienna2.tsv', '2.4.8')
    check_sample_sequences('eterna100v2_vienna2.tsv', '2.1.9')
    check_sequences('eterna100v1_vienna1.tsv', 'nemo/nemo_v1_vienna1.tsv', '1.8.5')
    check_sequences('eterna100v1_vienna1.tsv', 'nemo/nemo_v1_vienna2.tsv', '2.1.9')
    check_sequences('eterna100v2_vienna2.tsv', 'nemo/nemo_v2_vienna1.tsv', '1.8.5')
    check_sequences('eterna100v2_vienna2.tsv', 'nemo/nemo_v2_vienna2.tsv', '2.1.9')
    check_sequences('eterna100v1_vienna1.tsv', 'eternabrain/eb_v1.txt', '1.8.5')
    check_sequences('eterna100v2_vienna2.tsv', 'eternabrain/eb_v2.txt', '2.1.9')
    check_sequences('eterna100v1_vienna1.tsv', 'learna/learna_v1_sols.txt', '1.8.5')
    check_sequences('eterna100v2_vienna2.tsv', 'learna/learna_v2_sols.txt', '2.1.9')
    check_sequences('eterna100v1_vienna1.tsv', 'rnainverse/rnai_puzzle_solutions_v1.txt', '1.8.5')
    check_sequences('eterna100v2_vienna2.tsv', 'rnainverse/rnai_puzzle_solutions_v2.txt', '2.1.9')
    check_sequences('eterna100v1_vienna1.tsv', 'sentrna/sentrna_v1_sols.txt', '1.8.5')
    check_sequences('eterna100v2_vienna2.tsv', 'sentrna/sentrna_v2_sols.txt', '2.1.9')
