import argparse
import os
from itertools import product, zip_longest
from algorithms import eternabrain, learna, sentrna
from util.slurm import sbatch

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    # Via https://docs.python.org/3/library/itertools.html#itertools-recipes
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def run(args):
    if args.algorithm in [None, 'eternabrain']:
        featuregen_vienna1_job = None
        featuregen_vienna2_job = None
        if args.eternabrain_stage in [None, 'featuregen']:
            if args.eternabrain_featureset in [None, 'Vienna1']:
                if args.scheduler == 'slurm':
                    featuregen_vienna1_job = sbatch(
                        'python scripts/queue_train.py --algorithm eternabrain --eternabrain-stage featuregen --eternabrain-featureset Vienna1',
                        'e100-bench-train-eternabrain-featuregen-Vienna1',
                        timeout='12:00:00',
                        partition=args.slurm_partition,
                        cpus=1,
                        mail_type='END,FAIL'
                    )
                else:
                    eternabrain.featuregen('1.8.5')
            
            if args.eternabrain_featureset in [None, 'Vienna2']:
                if args.scheduler == 'slurm':
                    featuregen_vienna2_job = sbatch(
                        'python scripts/queue_train.py --algorithm eternabrain --eternabrain-stage featuregen --eternabrain-featureset Vienna2',
                        'e100-bench-train-eternabrain-featuregen-Vienna2',
                        timeout='12:00:00',
                        partition=args.slurm_partition,
                        cpus=1,
                        mail_type='END,FAIL',
                    )
                else:
                    eternabrain.featuregen('2.6.4')
        
        if args.eternabrain_stage in [None, 'basecnn', 'locationcnn']:
            for (stage, featureset, puzzleset) in product(
                [args.eternabrain_stage] if args.eternabrain_stage is not None else ['basecnn', 'locationcnn'],
                [args.eternabrain_featureset] if args.eternabrain_featureset is not None else ['Vienna1', 'Vienna2'],
                [args.eternabrain_puzzleset] if args.eternabrain_puzzleset is not None else ['base', 'extended']
            ):
                if args.scheduler == 'slurm':
                    dependency = None
                    if args.eternabrain_stage is None:
                        if args.eternabrain_featureset == 'Vienna1':
                            dependency = featuregen_vienna1_job
                        else: 
                            dependency = featuregen_vienna2_job
                    
                    sbatch(
                        f'python scripts/queue_train.py --algorithm eternabrain --eternabrain-stage {stage} --eternabrain-featureset {featureset} --eternabrain-puzzleset {puzzleset}',
                        f'e100-bench-train-eternabrain-{stage}-{featureset}-{puzzleset}',
                        timeout='6:00:00',
                        partition=args.slurm_gpu_partition,
                        cpus=1,
                        gpus=1,
                        # We need to limit ourselves to GPU generations Turning or older due to the CUDA
                        # version required by Eternabrain's version of tensorflow 
                        constraint='GPU_GEN:PSC|GPU_GEN:VLT|GPU_GEN:TUR',
                        dependency=dependency,
                        mail_type='END,FAIL',
                    )
                else:
                    eternabrain.train(
                        1 if featureset == 'Vienna1' else 2,
                        True if puzzleset == 'extended' else False,
                        'baseCNN' if stage == 'basecnn' else 'locationCNN',
                    )

    if args.algorithm in [None, 'learna']:
        for vienna_version in [args.learna_vienna_version] if args.learna_vienna_version else ['1.8.5', '2.6.4']:
            if args.scheduler == 'slurm':
                    sbatch(
                        f'python scripts/queue_train.py --algorithm learna --learna-vienna-version {vienna_version} --learna-train-timeout {args.learna_train_timeout}',
                        f'e100-bench-train-learna-{vienna_version}',
                        timeout='1:30:00',
                        partition=args.slurm_partition,
                        cpus=20,
                        mail_type='END,FAIL'
                    )
            else:
                learna.train(args.learna_train_timeout, vienna_version)

    if args.algorithm in [None, 'sentrna']:
        sentrna_configs = product(
            [args.sentrna_vienna_version] if args.sentrna_vienna_version is not None else ['1.8.5', '2.6.4'],
            [args.sentrna_renderer] if args.sentrna_renderer is not None else ['eterna', 'rnaplot'],
            [(args.sentrna_trial, args.sentrna_features)] if args.sentrna_trial is not None else (
                list(product([0], range(0, 42))) + list(list(product(range(1, 19), [0]))) + list(list(product(range(1, 19), [20]))) + list(list(product(range(1, 19), [42])))
            )
        )
        if args.scheduler == 'slurm':
            for (idx, batch) in enumerate(grouper(sentrna_configs, 20)):
                cmds = []
                for (vienna_version, renderer, (trial, features)) in [conf for conf in batch if conf != None]:
                    cmds.append(f'python scripts/queue_train.py --algorithm sentrna --sentrna-vienna-version {vienna_version} --sentrna-renderer {renderer} --sentrna-trial {trial} --sentrna-features {features}',)
                sbatch(
                    cmds,
                    f'e100-bench-train-sentrna-batch{idx + 1}',
                    timeout='2:00:00',
                    partition=args.slurm_partition,
                    cpus=1,
                    mail_type='END,FAIL'
                )
        else:
            for (vienna_version, renderer, (trial, features)) in sentrna_configs:
                sentrna.train(vienna_version, features, renderer, trial)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--scheduler', dest='scheduler', type=str, choices=['naive', 'slurm'], default='naive')
    parser.add_argument('--slurm-partition', dest='slurm_partition', type=str, default=None)
    parser.add_argument('--slurm-gpu-partition', dest='slurm_gpu_partition', type=str, default=None)

    parser.add_argument('--algorithm', dest='algorithm', type=str, choices=['eternabrain', 'learna', 'sentrna'], default=None)

    parser.add_argument('--eternabrain-stage', type=str, dest='eternabrain_stage', choices=['featuregen', 'basecnn', 'locationcnn'], default=None)
    parser.add_argument('--eternabrain-featureset', type=str, dest='eternabrain_featureset', choices=['Vienna1', 'Vienna2'], default=None)
    parser.add_argument('--eternabrain-puzzleset', type=str, dest='eternabrain_puzzleset', choices=['base', 'extended'], default=None)

    parser.add_argument('--learna-vienna-version', type=str, dest='learna_vienna_version', choices=['1.8.5', '2.6.4'], default=None)
    parser.add_argument('--learna-train-timeout', type=int, dest='learna_train_timeout', default=3600)
    
    parser.add_argument('--sentrna-vienna-version', type=str, dest='sentrna_vienna_version', choices=['1.8.5', '2.6.4'], default=None)
    parser.add_argument('--sentrna-renderer', type=str, dest='sentrna_renderer', choices=['eterna', 'rnaplot'], default=None)
    parser.add_argument('--sentrna-trial', type=int, dest='sentrna_trial', default=None)
    parser.add_argument('--sentrna-features', type=int, dest='sentrna_features', default=None)

    args = parser.parse_args()

    if (
        (args.sentrna_trial is not None and args.sentrna_features is None)
        or (args.sentrna_trial is None and args.sentrna_features is not None)
    ):
        raise Exception('If sentrna_trial or sentrna_features is provided, both need to be provided')

    run(args)