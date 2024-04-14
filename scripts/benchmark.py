import argparse
import time
from collections import OrderedDict
from algorithms import rnainverse, nemo, learna, sentrna, eternabrain
from util.fold import fold

solvers = [
    'rnainverse', 'nemo-2500', 'nemo-10k',
    'learna-pretrained', 'learna-retrained-vienna1', 'learna-retrained-vienna2',
    'sentrna-pretrained', 'sentrna-retrained-vienna1-rnaplot', 'sentrna-retrained-vienna2-rnaplot',
    'sentrna-retrained-vienna1-eterna', 'sentrna-retrained-vienna2-eterna',
    'eternabrain-pretrained', 'eternabrain-pretrained-flipsap', 'eternabrain-retrained-f1-base',
    'eternabrain-retrained-f1-base-flipsap', 'eternabrain-retrained-f2-base', 'eternabrain-retrained-f2-base-flipsap',
    'eternabrain-retrained-f1-ext', 'eternabrain-retrained-f1-ext-flipsap', 'eternabrain-retrained-f2-ext',
    'eternabrain-retrained-f2-ext-flipsap',
]

def run(solver, folder, structure, timeout):
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
    elif solver == 'eternabrain-retrained-f1-base':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F1-BASE', timeout)
    elif solver == 'eternabrain-retrained-f1-base-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F1-BASE', timeout)
    elif solver == 'eternabrain-retrained-f2-base':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F2-BASE', timeout)
    elif solver == 'eternabrain-retrained-f2-base-flipsap':
        solve = lambda: eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F2-BASE', timeout)
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

    start = time.perf_counter()
    solution = solve()
    end = time.perf_counter()
    
    sequence = solution.pop('Sequence')
    (algorithm, variant, *_) = solver.split('-', 1) + ['default']
    if sequence != '<timeout>':
        folded = fold(sequence, '1.8.5' if folder == 'vienna1' else '2.6.4')
    else:
        folded = '<timeout>'
    
    return {
        'Algorithm': algorithm,
        'Variant': variant,
        'Folder': folder,
        'Target Structure': structure,
        'Sequence': sequence,
        'Folded Structure': folded,
        'Time': str(end - start),
        'Success': '1' if structure == folded else '0',
        **solution
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', dest='solver', choices=solvers, required=True)
    parser.add_argument('--folder', dest='folder', choices=['vienna1', 'vienna2'], required=True)
    parser.add_argument('--structure', dest='structure', type=str, required=True)
    parser.add_argument('--timeout', dest='timeout', type=int, default=60*60*24)
    args = parser.parse_args()
    print(run(args.solver, args.folder, args.structure, args.timeout))
