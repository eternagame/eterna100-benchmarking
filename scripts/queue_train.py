import argparse
import os
from itertools import product
from algorithms import eternabrain, learna, sentrna

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

def run(args):
    if args.algorithm in [None, 'eternabrain']:
        if args.eternabrain_stage in [None, 'featuregen']:
            if args.eternabrain_featureset in [None, 'Vienna1']:
                eternabrain.featuregen('1.8.5')
            
            if args.eternabrain_featureset in [None, 'Vienna2']:
                eternabrain.featuregen('2.6.4')
        
        if args.eternabrain_stage in [None, 'basecnn', 'locationcnn']:
            for (stage, featureset, puzzleset) in product(
                [args.eternabrain_stage] if args.eternabrain_stage is not None else ['basecnn', 'locationcnn'],
                [args.eternabrain_featureset] if args.eternabrain_featureset is not None else ['Vienna1', 'Vienna2'],
                [args.eternabrain_puzzleset] if args.eternabrain_puzzleset is not None else ['base', 'extended']
            ):
                eternabrain.train(
                    1 if featureset == 'Vienna1' else 2,
                    True if puzzleset == 'extended' else False,
                    'baseCNN' if stage == 'basecnn' else 'locationCNN',
                )

    if args.algorithm in [None, 'learna']:
        for vienna_version in [args.learna_vienna_version] if args.learna_vienna_version else ['1.8.5', '2.6.4']:
            learna.train(args.learna_train_timeout, vienna_version)

    if args.algorithm in [None, 'sentrna']:
        for (vienna_version, renderer, trial, features) in product(
            [args.sentrna_vienna_version] if args.sentrna_vienna_version is not None else ['1.8.5', '2.6.4'],
            [args.sentrna_renderer] if args.sentrna_renderer is not None else ['eterna', 'rnaplot'],
            range(args.sentrna_trial_min, args.sentrna_trial_max + 1),
            range(args.sentrna_features_min, args.sentrna_features_max + 1),
        ):
            sentrna.train(vienna_version, features, renderer, trial)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--scheduler', dest='scheduler', type=str, choices=['naive', 'slurm'], default='naive')
    parser.add_argument('--algorithm', dest='algorithm', type=str, choices=['eternabrain', 'learna', 'sentrna'], default=None)

    parser.add_argument('--eternabrain-stage', type=str, dest='eternabrain_stage', choices=['featuregen', 'basecnn', 'locationcnn'], default=None)
    parser.add_argument('--eternabrain-featureset', type=str, dest='eternabrain_featureset', choices=['Vienna1', 'Vienna2'], default=None)
    parser.add_argument('--eternabrain-puzzleset', type=str, dest='eternabrain_puzzleset', choices=['base', 'extended'], default=None)

    parser.add_argument('--learna-vienna-version', type=str, dest='learna_vienna_version', choices=['1.8.5', '2.6.4'], default=None)
    parser.add_argument('--learna-train-timeout', type=int, dest='learna_train_timeout', default=3600)
    
    parser.add_argument('--sentrna-vienna-version', type=str, dest='sentrna_vienna_version', choices=['1.8.5', '2.6.4'], default=None)
    parser.add_argument('--sentrna-trial-min', type=int, dest='sentrna_trial_min', default=1)
    parser.add_argument('--sentrna-trial-max', type=int, dest='sentrna_trial_max', default=5)
    parser.add_argument('--sentrna-features-min', type=int, dest='sentrna_features_min', default=0)
    parser.add_argument('--sentrna-features-max', type=int, dest='sentrna_features_max', default=42)
    parser.add_argument('--sentrna-renderer', type=str, dest='sentrna_renderer', choices=['eterna', 'rnaplot'])

    args = parser.parse_args()
    run(args)