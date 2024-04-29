import argparse
import os
from itertools import product
import pandas as pd
from benchmark import solvers
from benchmark import run as run_benchmark

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def run(args):
    os.makedirs(f'{DATA_DIR}/partials', exist_ok=True)
    
    puzzles = pd.read_csv(f'{DATA_DIR}/eterna100_puzzles.tsv', sep='\t')
    structures = pd.concat([puzzles['Secondary Structure V1'], puzzles['Secondary Structure V2']]).unique()

    for (solver, folder, (structure_id, structure), trial) in product(
        [args.solver] if args.solver is not None else solvers,
        [args.folder] if args.folder is not None else ['vienna1', 'vienna2'],
        [[args.structure_id, args.structure]] if args.structure is not None else enumerate(structures, 1),
        [args.trial] if args.trial is not None else range(args.trials)
    ):
        res = run_benchmark(solver, folder, structure, args.timeout)
        with open(f'{DATA_DIR}/partials/{solver}_{folder}_s{structure_id}_t{trial}.tsv', 'w') as f:
            f.write('\t'.join(res.keys()) + '\tTrial\n')
            f.write('\t'.join(res.values()) + f'\t{trial}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--scheduler', dest='scheduler', choices=['naive', 'slurm'], default='naive')
    parser.add_argument('--trials', dest='trials', type=int, default=5)
    parser.add_argument('--timeout', dest='timeout', type=int, default=60*60*24)

    parser.add_argument('--solver', dest='solver', choices=solvers, default=None)
    parser.add_argument('--folder', dest='folder', choices=['vienna1', 'vienna2'], default=None)
    structure_action = parser.add_argument('--structure', dest='structure', type=str, default=None)
    parser.add_argument('--structure_id', dest='structure_id', help='if --structure is provided, what unique ID for this structure should be used in the output filename?', type=str, default=None)
    parser.add_argument('--trial', dest='trial', type=int, default=None)

    args = parser.parse_args()
    if args.structure and args.structure_id is None:
        raise argparse.ArgumentError(structure_action, '--structure_id must be provided if --structure is provided')
    run(args)