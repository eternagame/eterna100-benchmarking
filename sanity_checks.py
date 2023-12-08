import RNA
import pandas as pd
import os

def check_v2_sequences(outfile='v2_sanity_check.txt'):
    e100 = pd.read_csv('eterna100_vienna2.txt', sep='\t', header='infer')
    # make the 'Sample Solution (1)' and 'Sample Solution (2)' columns lists
    sols1 = e100['Sample Solution (1)'].tolist()
    sols2 = e100['Sample Solution (2)'].tolist()
    strucs = e100['Secondary Structure'].tolist()
    names = e100['Puzzle Name'].tolist()

    buggy = []
    f = open(outfile, 'w')
    for i in range(100):
        struc1 = RNA.fold(sols1[i])[0]
        if struc1 != strucs[i]:
            struc2 = RNA.fold(sols2[i])[0]
            if struc2 != strucs[i]:
                f.write(f'{names[i]}\t{strucs[i]}\t{sols1[i]}\t{struc1}\t{sols2[i]}\t{struc2}\n')
                buggy.append(names[i])
            else:
                f.write('fine\n')
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
    check_identical_structures()
