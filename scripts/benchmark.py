import argparse
import time
from algorithms import rnainverse, nemo, learna, sentrna, eternabrain, desirna
from util.fold import fold

solvers = [
    'rnainverse', 'nemo-2500', 'nemo-10k', 'desirna',
    'learna-pretrained', 'learna-retrained-vienna1', 'learna-retrained-vienna2',
    'sentrna-pretrained-1taf', 'sentrna-pretrained-20t0f', 'sentrna-pretrained-20t20f', 'sentrna-pretrained-20t42f',
    'sentrna-retrained-vienna1-rnaplot-1taf', 'sentrna-retrained-vienna1-rnaplot-20t0f',
    'sentrna-retrained-vienna1-rnaplot-20t20f', 'sentrna-retrained-vienna1-rnaplot-20t42f',
    'sentrna-retrained-vienna1-eterna-1taf', 'sentrna-retrained-vienna1-eterna-20t0f',
    'sentrna-retrained-vienna1-eterna-20t20f', 'sentrna-retrained-vienna1-eterna-20t42f',
    'sentrna-retrained-vienna2-rnaplot-1taf', 'sentrna-retrained-vienna2-rnaplot-20t0f',
    'sentrna-retrained-vienna2-rnaplot-20t20f', 'sentrna-retrained-vienna2-rnaplot-20t42f',
    'sentrna-retrained-vienna2-eterna-1taf', 'sentrna-retrained-vienna2-eterna-20t0f',
    'sentrna-retrained-vienna2-eterna-20t20f', 'sentrna-retrained-vienna2-eterna-20t42f',
    'eternabrain-pretrained', 'eternabrain-pretrained-flipsap', 'eternabrain-retrained-f1-base',
    'eternabrain-retrained-f1-base-flipsap', 'eternabrain-retrained-f2-base', 'eternabrain-retrained-f2-base-flipsap',
    'eternabrain-retrained-f1-ext', 'eternabrain-retrained-f1-ext-flipsap', 'eternabrain-retrained-f2-ext',
    'eternabrain-retrained-f2-ext-flipsap',
]


def run(solver, folder, structure, timeout):
    if solver == 'rnainverse':
        def solve(): return rnainverse.solve(
            structure, '1.8.5' if folder == 'vienna1' else '2.6.4', timeout)
    elif solver == 'desirna':
        def solve(): return desirna.solve(
            structure, '1' if folder == 'vienna1' else '2', timeout)
    elif solver == 'nemo-2500':
        def solve(): return nemo.solve(structure, '1' if folder ==
                                       'vienna1' else '2', 2500, timeout)
    elif solver == 'nemo-10k':
        def solve(): return nemo.solve(structure, '1' if folder ==
                                       'vienna1' else '2', 10000, timeout)
    elif solver == 'learna-pretrained':
        def solve(): return learna.solve(structure, '1.8.5' if folder ==
                                         'vienna1' else '2.6.4', 'ICLR_2019/224_0_1', timeout)
    elif solver == 'learna-retrained-vienna1':
        def solve(): return learna.solve(structure, '1.8.5' if folder ==
                                         'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-1.8.5', timeout)
    elif solver == 'learna-retrained-vienna2':
        def solve(): return learna.solve(structure, '1.8.5' if folder ==
                                         'vienna1' else '2.6.4', 'eterna100-benchmarking/vienna-2.6.4', timeout)
    elif solver == 'sentrna-pretrained-1taf':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'trained_models/batch1', '1trial-allfeat', 'rnaplot', timeout)
    elif solver == 'sentrna-pretrained-20t0f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'trained_models/batch1', '20trials-nofeat', 'rnaplot', timeout)
    elif solver == 'sentrna-pretrained-20t20f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'trained_models/batch1', '20trials-20feat', 'rnaplot', timeout)
    elif solver == 'sentrna-pretrained-20t42f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'trained_models/batch1', '20trials-42feat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna1-rnaplot-1taf':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '1trial-allfeat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna1-rnaplot-20t0f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-nofeat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna1-rnaplot-20t20f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-20feat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna1-rnaplot-20t42f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-42feat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna1-eterna-1taf':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '1trial-allfeat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna1-eterna-20t0f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-nofeat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna1-eterna-20t20f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-20feat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna1-eterna-20t42f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-42feat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna2-rnaplot-1taf':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '1trial-allfeat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna2-rnaplot-20t0f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-nofeat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna2-rnaplot-20t20f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-20feat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna2-rnaplot-20t42f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-rnaplot', '20trials-42feat', 'rnaplot', timeout)
    elif solver == 'sentrna-retrained-vienna2-eterna-1taf':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '1trial-allfeat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna2-eterna-20t0f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-nofeat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna2-eterna-20t20f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-20feat', 'eterna', timeout)
    elif solver == 'sentrna-retrained-vienna2-eterna-20t42f':
        def solve(): return sentrna.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                          'eterna100-benchmarking/vienna-1.8.5-eterna', '20trials-42feat', 'eterna', timeout)
    elif solver == 'eternabrain-pretrained':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder ==
                                              'vienna1' else '2.6.4', '1.8.5' if folder == 'vienna1' else '2.6.4', 'CNN15', timeout)
    elif solver == 'eternabrain-pretrained-flipsap':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder ==
                                              'vienna1' else '2.6.4', '2.6.4' if folder == 'vienna1' else '1.8.5', 'CNN15', timeout)
    elif solver == 'eternabrain-retrained-f1-base':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F1-BASE', timeout)
    elif solver == 'eternabrain-retrained-f1-base-flipsap':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F1-BASE', timeout)
    elif solver == 'eternabrain-retrained-f2-base':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F2-BASE', timeout)
    elif solver == 'eternabrain-retrained-f2-base-flipsap':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F2-BASE', timeout)
    elif solver == 'eternabrain-retrained-f1-ext':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F1-EXT', timeout)
    elif solver == 'eternabrain-retrained-f1-ext-flipsap':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F1-EXT', timeout)
    elif solver == 'eternabrain-retrained-f2-ext':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '1.8.5' if folder == 'vienna1' else '2.6.4', 'eterna100-benchmarking-F2-EXT', timeout)
    elif solver == 'eternabrain-retrained-f2-ext-flipsap':
        def solve(): return eternabrain.solve(structure, '1.8.5' if folder == 'vienna1' else '2.6.4',
                                              '2.6.4' if folder == 'vienna1' else '1.8.5', 'eterna100-benchmarking-F2-EXT', timeout)
    else:
        raise NotImplementedError(f'Invalid solver {solver}')

    start = time.perf_counter()
    solution = solve()
    end = time.perf_counter()

    sequence = solution.pop('Sequence')
    (algorithm, variant, *_) = solver.split('-', 1) + ['default']
    if sequence != '<timeout>':
        folded = fold(sequence, '1.8.5' if folder == 'vienna1' else '2.6.4')[0]
    else:
        folded = '<timeout>'

    return {
        'Algorithm': algorithm,
        'Variant': variant,
        'Folder': folder,
        'Target Structure': structure,
        'Sequence': sequence,
        'Folded Structure': folded,
        'Time': end - start,
        'Success': '1' if structure == folded else '0',
        'Extra': solution
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', dest='solver',
                        choices=solvers, required=True)
    parser.add_argument('--folder', dest='folder',
                        choices=['vienna1', 'vienna2'], required=True)
    parser.add_argument('--structure', dest='structure',
                        type=str, required=True)
    parser.add_argument('--timeout', dest='timeout',
                        type=int, default=60*60*24)
    args = parser.parse_args()
    print(run(args.solver, args.folder, args.structure, args.timeout))
