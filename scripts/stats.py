import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

puzzles = pd.read_csv(f'{DATA_DIR}/eterna100_puzzles.tsv', sep='\t')
results = pd.read_csv(f'{DATA_DIR}/results.tsv', sep='\t')

v1_structures = puzzles['Secondary Structure V1']
v2_structures = puzzles['Secondary Structure V2']

conditions = results[['Algorithm', 'Variant', 'Folder']].drop_duplicates()
for (_,condition) in conditions.iterrows():
    condition_solutions = results[
        (results['Algorithm'] == condition['Algorithm'])
        & (results['Variant'] == condition['Variant'])
        & (results['Folder'] == condition['Folder'])
        & (results['Success'] == 1)
    ]

    v1_only = condition_solutions[condition_solutions['Target Structure'].isin(puzzles['Secondary Structure V1'])]
    v2_only = condition_solutions[condition_solutions['Target Structure'].isin(puzzles['Secondary Structure V2'])]

    print(f'{condition['Algorithm']}/{condition['Variant']}/{condition['Folder']} | v1: {len(v1_only)} v2: {len(v2_only)}')
