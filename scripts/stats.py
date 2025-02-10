from os import path
import pandas as pd

res = pd.read_csv(path.join(path.dirname(__file__), '../data/results.tsv'), sep='\t')
puz = pd.read_csv(path.join(path.dirname(__file__), '../data/eterna100_puzzles.tsv'), sep='\t')

print('=========================')
print('All Puzzles')
print('=========================')
print(
    res.groupby(
        ['Algorithm', 'Variant', 'Folder']
    ).apply(
        lambda x: pd.Series({
            'v1-success': x[x['Target Structure'].isin(puz['Secondary Structure V1'])]['Success'].sum(),
            'v2-success': x[x['Target Structure'].isin(puz['Secondary Structure V2'])]['Success'].sum()
        }),
        include_groups=False
    )
)

print('=========================')
print('Unchanged Only')
print('=========================')
print(
    res.groupby(
        ['Algorithm', 'Variant', 'Folder']
    ).apply(
        lambda x: pd.Series({
            'v1-success': x[x['Target Structure'].isin(puz[puz['Secondary Structure V1'] == puz['Secondary Structure V2']]['Secondary Structure V1'])]['Success'].sum(),
            'v2-success': x[x['Target Structure'].isin(puz[puz['Secondary Structure V1'] == puz['Secondary Structure V2']]['Secondary Structure V2'])]['Success'].sum()
        }),
        include_groups=False
    )
)

print('=========================')
print('Changed Only')
print('=========================')
print(
    res.groupby(
        ['Algorithm', 'Variant', 'Folder']
    ).apply(
        lambda x: pd.Series({
            'v1-success': x[x['Target Structure'].isin(puz[puz['Secondary Structure V1'] != puz['Secondary Structure V2']]['Secondary Structure V1'])]['Success'].sum(),
            'v2-success': x[x['Target Structure'].isin(puz[puz['Secondary Structure V1'] != puz['Secondary Structure V2']]['Secondary Structure V2'])]['Success'].sum()
        }),
        include_groups=False
    )
)
