import re, argparse
from os import path
from subprocess import PIPE, Popen, STDOUT
import pandas as pd

FILE_DIR = path.abspath(path.dirname(__file__))
NEMO_DIR = path.join(FILE_DIR, '../ViennaRNA-2.1.9-NEMO/nemo')

def try_inverse_fold(struct: str, vienna_ver: int):
    params = [path.join(NEMO_DIR, 'nemo'), '-i','10000']
    if vienna_ver == 1:
        params.append('-E')
    params.append(struct)
   
    print(f'Running: {" ".join(params)}') 
    for i in range(1000):
        p = Popen(params, stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=NEMO_DIR)
        (res, err) = p.communicate()
        print(f'********* Trial {i} *********')
        print(res)
        print('---')
        print(err)
        match = re.search(r'NMC: ([AUGC]+).*\nSTR: ([\(\).]+)', res)
        if match.group(2) == struct:
            return match.group(1)

def run(
    vienna_ver = None,
    eterna100_ver = None,
    puzzle_num = None,
    outfile = None
):
    if vienna_ver is not None:
        vienna_versions = [vienna_ver]
    else:
        vienna_versions = [1, 2]
    
    puzzles = pd.DataFrame()
    if eterna100_ver == 1 or eterna100_ver == None:
        v1 = pd.read_csv('eterna100v1_vienna1.tsv', sep='\t', header='infer')
        v1['Eterna100 Version'] = 1
        puzzles = pd.concat([puzzles, v1])
    if eterna100_ver == 2 or eterna100_ver == None:
        v2 = pd.read_csv('eterna100v2_vienna2.tsv', sep='\t', header='infer')
        v2['Eterna100 Version'] = 2
        puzzles = pd.concat([puzzles, v2])
    
    if puzzle_num is not None:
        puzzles = puzzles[puzzles['Puzzle #'] == puzzle_num]
        
    if outfile:
        with open(outfile, 'w') as f:
            f.write('Puzzle Name\tEterna100 Version\tSecondary Structure\tVienna Version\tSolution\n')
    else:
        print('Puzzle Name\tEterna100 Version\tSecondary Structure\tVienna Version\tSolution')
        
    for (_, puz) in puzzles.iterrows():
        for vver in vienna_versions:
            res = try_inverse_fold(puz['Secondary Structure'], vver)
            if res:
                if outfile:
                    with open(outfile, 'a') as f:
                        f.write(f'{puz["Puzzle Name"]}\t{puz["Eterna100 Version"]}\t{puz["Secondary Structure"]}\t{vver}\t{res}\n')
                else:
                    print(f'{puz["Puzzle Name"]}\t{puz["Eterna100 Version"]}\t{puz["Secondary Structure"]}\t{vver}\t{res}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--vienna_ver', dest='vienna_ver', type=int)
    parser.add_argument('--eterna100_ver', dest='eterna100_ver', type=int)
    parser.add_argument('--puzzle_num', dest='puzzle_num', type=int)
    parser.add_argument('--outfile', dest='outfile')
    args = parser.parse_args()
    run(args.vienna_ver, args.eterna100_ver, args.puzzle_num, args.outfile)
