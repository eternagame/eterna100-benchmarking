import argparse
import os
import json
from math import ceil
from itertools import product
import pandas as pd
from filelock import FileLock
from benchmark import solvers, run as run_benchmark
from util.job_packer import JobPacker, Task
from util.slurm import sbatch

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def run(args):
    os.makedirs(f'{DATA_DIR}/partials', exist_ok=True)
    
    puzzles = pd.read_csv(f'{DATA_DIR}/eterna100_puzzles.tsv', sep='\t')
    structures = pd.concat([puzzles['Secondary Structure V1'], puzzles['Secondary Structure V2']]).unique()
    v2_unsolveable_structures = puzzles[puzzles['Secondary Structure V1'] != puzzles['Secondary Structure V2']]['Secondary Structure V1'].to_list()
    v1_unsolveable_structures = puzzles[puzzles['Puzzle Name'] == 'Hoglafractal']['Secondary Structure V2'].to_list()

    packer = JobPacker()
    for (solver, folder, structure, trial) in product(
        [args.solver] if args.solver is not None else solvers,
        [args.folder] if args.folder is not None else ['vienna1', 'vienna2'],
        [args.structure] if args.structure is not None else structures,
        range(args.trial_start, args.trial_end + 1)
    ):
        if folder == 'vienna2' and structure in v2_unsolveable_structures:
            continue
        if folder == 'vienna1' and structure in v1_unsolveable_structures:
            continue
        if args.minimal_solvers and solver not in [
            #'nemo-2500',
            #'learna-pretrained',
            #'learna-retrained-vienna1',
            'sentrna-pretrained-20t20f',
            'sentrna-retrained-vienna2-rnaplot-20t20f',
            #'eternabrain-pretrained',
            #'eternabrain-retrained-f1-ext',
            #'eternabrain-retrained-f2-ext',
            #'eternabrain-retrained-f2-ext-flipsap'
        ]:
            continue

        if args.scheduler == 'slurm':
            memory = '8000MB'
            timeout = 60*60*24
            if solver == 'rnainverse':
                memory = '100MB'
                if len(structure) < 120:
                    timeout = 60
                elif len(structure) < 240:
                    timeout = 60 * 30
                else:
                    timeout = 60 * 60
            if solver.startswith('nemo-'):
                memory = '100MB'
                mult = 4 if solver == 'nemo-10k' else 1
                if len(structure) < 40:
                    timeout = 60 * 10 * mult
                elif len(structure) < 120:
                    timeout = 60 * 30 * mult
                elif len(structure) < 240:
                    timeout = 60 * 60 * 2 * mult
                else:
                    timeout = 60 * 60 * 3 * mult
            if solver.startswith('sentrna-'):
                memory = '500MB'
                mult = 43 if solver.endswith('1taf') else 20
                if len(structure) < 40:
                    timeout = 60 * 4 * mult
                elif len(structure) < 120:
                    timeout = 60 * 8 * mult
                elif len(structure) < 240:
                    timeout = 60 * 20 * mult
                else:
                    timeout = 60 * 45 * mult
            if solver.startswith('learna-'):
                memory = '1250MB'
                timeout = 60 * 60 * 24
            if solver.startswith('eternabrain-'):
                memory = '4000MB'
                if len(structure) < 40:
                    timeout = 60 * 3
                elif len(structure) < 120:
                    timeout = 60 * 8
                elif len(structure) < 240:
                    timeout = 60 * 15
                else:
                    timeout = 60 * 40

            packer.add(Task(
                f'python scripts/queue_benchmarks.py --solver {solver} --folder {folder} --structure "{structure}" --trial-start {trial} --trial-end {trial} --timeout {args.timeout}',
                memory,
                timeout
            ))
        else:
            res = run_benchmark(solver, folder, structure, args.timeout)
            res['Trial'] = trial
            res['Extra'] = json.dumps(res['Extra'])
            with FileLock(f'{DATA_DIR}/results.tsv.lock'):
                if os.path.exists(f'{DATA_DIR}/results.tsv'):
                    all_results = pd.read_csv(f'{DATA_DIR}/results.tsv', sep='\t')
                    all_results = all_results[~(
                        (all_results['Algorithm'] == res['Algorithm'])
                        & (all_results['Variant'] == res['Variant'])
                        & (all_results['Folder'] == res['Folder'])
                        & (all_results['Target Structure'] == res['Target Structure'])
                        & (all_results['Trial'] == res['Trial'])
                    )]
                else:
                    # We specify these columns here to ensure they're in the order we want
                    all_results = pd.DataFrame(columns=[
                        'Algorithm',
                        'Variant',
                        'Folder',
                        'Target Structure',
                        'Trial'
                    ])
                all_results = pd.concat([all_results, pd.DataFrame([res])])
                all_results = all_results.sort_values(by=['Algorithm', 'Variant', 'Folder', 'Target Structure', 'Trial'])
                all_results.to_csv(f'{DATA_DIR}/results.tsv', sep='\t', index=False)
    
    if args.scheduler == 'slurm':
        batches = packer.pack(args.timeout)
        jobs = [job for batch in batches for job in batch.jobs]
        tasks = [task for job in jobs for task in job.commands]
        print(f'Queueing {len(batches)} batches/{len(jobs)} jobs/{len(tasks)} benchmarks')

        job_name = 'e100-bench'
        if args.solver is not None:
            job_name += f'_s-{args.solver}'
        if args.folder is not None:
            job_name += f'_f-{args.folder}'
        job_name += f'_t-{args.trial_start}-{args.trial_end}'

        for batch in batches:
            sbatch(
                batch.to_sh(),
                f'{job_name}_m-{batch.memory}',
                timeout=ceil((max([job.time_allocation for job in batch.jobs]) + 60 * 30) / 60),
                partition=args.slurm_partition,
                cpus=1,
                memory_per_cpu=batch.memory,
                mail_type='END',
                array=batch.slurm_array_indexes(),
                echo_cmd=True,
                constraint='CPU_MNF:INTEL&CPU_SKU:7502'
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--scheduler', dest='scheduler', choices=['naive', 'slurm'], default='naive')
    parser.add_argument('--slurm-partition', dest='slurm_partition', type=str, default=None)
    parser.add_argument('--timeout', dest='timeout', type=int, default=60*60*24)

    parser.add_argument('--solver', dest='solver', choices=solvers, default=None)
    parser.add_argument('--folder', dest='folder', choices=['vienna1', 'vienna2'], default=None)
    parser.add_argument('--structure', dest='structure', type=str, default=None)
    parser.add_argument('--trial-start', dest='trial_start', type=int, default=1)
    parser.add_argument('--trial-end', dest='trial_end', type=int, default=5)

    parser.add_argument('--minimal-solvers', dest='minimal_solvers', action='store_true')

    args = parser.parse_args()
    run(args)
