import os
import argparse
import time
import pandas as pd
from algorithms import rnainverse, nemo, learna, sentrna, eternabrain
from util.fold import fold

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def run(solver, folder, structure_id, trial, timeout):
    puzzles = pd.read_csv(f'{DATA_DIR}/eterna100_puzzles.tsv', sep='\t')
    structures = pd.concat([puzzles['Secondary Structure V1'], puzzles['Secondary Structure V2']]).unique()
    structure = structures[structure_id]

    os.makedirs(f'{DATA_DIR}/partials', exist_ok=True)

    if solver == 'rnainverse':
        solve = lambda: rnainverse.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', timeout)
    elif solver == 'nemo-2500':
        solve = lambda: nemo.solve(structure, '1' if folder == 'vienna1' else '2', 2500, timeout)
    elif solver == 'nemo-10k':
        solve = lambda: nemo.solve(structure, '1' if folder == 'vienna1' else '2', 10000, timeout)
    elif solver == 'learna-pretrained':
        solve = lambda: learna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'ICLR_2019/224_0_1', timeout)
    elif solver == 'learna-retrained-vienna1':
        solve = lambda: learna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5', timeout)
    elif solver == 'learna-retrained-vienna2':
        solve = lambda: learna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-2.6.4', timeout)
    elif solver == 'sentrna-pretrained':
        solve = lambda: sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'trained_models/batch1', 'rnaplot')
    elif solver == 'sentrna-retrained-vienna1-rnaplot':
        solve = lambda: sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5-rnaplot', 'rnaplot')
    elif solver == 'sentrna-retrained-vienna1-eterna':
        solve = lambda: sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5-eterna', 'eterna')
    elif solver == 'sentrna-retrained-vienna2-rnaplot':
        solve = lambda: sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5-rnaplot', 'rnaplot')
    elif solver == 'sentrna-retrained-vienna2-eterna':
        solve = lambda: sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5-eterna', 'eterna')
    elif solver == 'eternabrain-pretrained':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'CNN15', timeout)
    elif solver == 'eternabrain-pretrained-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'CNN15', timeout)
    elif solver == 'eternabrain-retrained-f1-sm':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F1-SM', timeout)
    elif solver == 'eternabrain-retrained-f1-sm-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F1-SM', timeout)
    elif solver == 'eternabrain-retrained-f2-sm':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F2-SM', timeout)
    elif solver == 'eternabrain-retrained-f2-sm-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F2-SM', timeout)
    elif solver == 'eternabrain-retrained-f1-ext':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F1-EXT', timeout)
    elif solver == 'eternabrain-retrained-f1-ext-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F1-EXT', timeout)
    elif solver == 'eternabrain-retrained-f2-ext':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F2-EXT', timeout)
    elif solver == 'eternabrain-retrained-f2-ext-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F2-EXT', timeout)
    else:
        raise NotImplementedError(f'Invalid solver {solver}')

    with open(f'{DATA_DIR}/partials/{solver}_{folder}_s{structure_id}_t{trial}.tsv', 'w') as f:
        start = time.perf_counter()
        solution = solve()
        end = time.perf_counter()
        
        sequence = solution.pop('Sequence')
        f.write('\t'.join(['Algorithm', 'Variant', 'Folder', 'Target Structure', 'Trial', 'Sequence', 'Folded Structure', 'Time', 'Success', *solution.keys()]) + '\n')
        (algorithm, variant, *_) = solver.split('-', 1) + ['default']
        if sequence != '<timeout>':
            folded = fold(sequence, '1.8.5' if folder == 'vienna1' else '2.6.4')
        else:
            folded = '<timeout>'
        f.write('\t'.join([algorithm, variant, folder, structure, trial, sequence, folded, str(end - start), '1' if structure == folded else '0', *solution.values()]) + '\n')
        f.flush()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', dest='solver', choices=[
        'rnainverse',
        'nemo-2500', 'nemo-10k',
        'learna-pretrained', 'learna-retrained-vienna1', 'learna-retrained-vienna2',
        'sentrna-pretrained', 'sentrna-retrained-vienna1-rnaplot', 'sentrna-retrained-vienna2-rnaplot',
        'sentrna-retrained-vienna1-eterna', 'sentrna-retrained-vienna2-eterna',
        'eternabrain-pretrained', 'eternabrain-pretrained-flipsap', 'eternabrain-retrained-f1-sm',
        'eternabrain-retrained-f1-sm-flipsap', 'eternabrain-retrained-f2-sm', 'eternabrain-retrained-f2-sm-flipsap',
        'eternabrain-retrained-f1-ext', 'eternabrain-retrained-f1-ext-flipsap', 'eternabrain-retrained-f2-ext',
        'eternabrain-retrained-f2-ext-flipsap',
    ], required=True)
    parser.add_argument('--folder', dest='folder', choices=['vienna1', 'vienna2'], required=True)
    parser.add_argument('--structure_id', dest='structure_id', type=int, required=True)
    parser.add_argument('--trial', dest='trial', type=int, required=True)
    parser.add_argument('--timeout', dest='timeout', type=int, default=60*60*24)
    args = parser.parse_args()
    run(args.solver, args.folder, args.structure_id, args.trial, args.timeout)
