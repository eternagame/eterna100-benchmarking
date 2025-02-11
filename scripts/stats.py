from os import path
import re
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

res = pd.read_csv(path.join(path.dirname(__file__), '../data/results.tsv'), sep='\t')
puz = pd.read_csv(path.join(path.dirname(__file__), '../data/eterna100_puzzles.tsv'), sep='\t')

def summarize(puzzles, name):
    summary = res.groupby(
        ['Algorithm', 'Variant', 'Folder']
    ).apply(
        lambda x: pd.Series({
            'v1-success': x[x['Target Structure'].isin(puzzles['Secondary Structure V1'])]['Success'].sum(),
            'v2-success': x[x['Target Structure'].isin(puzzles['Secondary Structure V2'])]['Success'].sum()
        }),
        include_groups=False
    )
    print(summary)
    summary.to_csv(path.join(path.dirname(__file__), f'../data/{name}'), sep='\t')

print('=========================')
print('All Puzzles')
print('=========================')
summarize(puz, 'summary-all.tsv')

print('=========================')
print('Unchanged Only')
print('=========================')
summarize(puz[puz['Secondary Structure V1'] == puz['Secondary Structure V2']], 'summary-unchanged.tsv')

print('=========================')
print('Changed Only')
print('=========================')
summarize(puz[puz['Secondary Structure V1'] != puz['Secondary Structure V2']], 'summary-changed.tsv')

COLOR_FAIL = [217/255, 93/255, 39/255]
COLOR_SUCCESS = [17/255, 120/255, 60/255]

def color(x):
    x = x.to_frame().reset_index().reset_index()
    if x.sum()['Success'].iloc[0] == 0:
        return [COLOR_FAIL]
    else:
        return [COLOR_SUCCESS]

def summerize(x):
    group = x.apply(color, axis=0)
    group['Total'] = x.sum().sum()
    return group.iloc[0]

def plot(vienna_version, bench_version, ax, xticks=False, yticks=False):
    v1solves = res[
        (res['Variant'].str.contains('pretrained') | ~(res['Variant'].str.contains('retrained'))) & ~(res['Variant'].str.contains('flipsap'))
    ][
        res['Target Structure'].isin(puz[f'Secondary Structure V{bench_version}'])
    ].merge(
        puz[['Puzzle #', f'Secondary Structure V{bench_version}', 'Puzzle Name']],
        left_on='Target Structure',
        right_on=f'Secondary Structure V{bench_version}'
    ).sort_values('Puzzle #').pivot_table(
        index=['Algorithm', 'Variant', 'Folder'],
        columns=['Puzzle Name'],
        values=['Success'],
        sort=False,
        fill_value=0
    ).astype(int).reset_index()
    v1solves = v1solves[
        v1solves['Folder'] == f'vienna{vienna_version}'
    ].set_index(['Algorithm', 'Variant', 'Folder']).groupby(['Algorithm', 'Variant']).apply(summerize)
    algosolves = v1solves.groupby('Algorithm').apply(lambda x: x['Total'].mean())
    v1solves['AlgoSolves'] = v1solves.apply(lambda x: algosolves[x.name[0]], axis=1)
    v1solves = v1solves.sort_values(['AlgoSolves', 'Variant'], axis=0)
    del v1solves['Total']
    del v1solves['AlgoSolves']

    
    ax.set_title(f'Eterna100-V{bench_version} Vienna{vienna_version}')
    if xticks:
        ax.set_xticks(
            range(len(v1solves)),
            [
                f'{algo}/{variant}'.replace('-f1', '-vienna1').replace('-f2', '-vienna2').replace('-ext', '').replace('/default', '').replace('/2500', '').replace('-rnaplot', '').replace('-20t20f', '')
                for (algo, variant) in v1solves.index
            ],
            rotation=90
        )
    else:
        ax.set_xticks(range(len(v1solves)), [])
    if yticks:
        ax.set_yticks(
            range(len(v1solves.columns)),
            [name[1] for name in v1solves.columns]
        )
        for lab in ax.get_yticklabels():
            if lab.get_text() in puz[puz['Secondary Structure V1'] != puz['Secondary Structure V2']]['Puzzle Name'].values:
                lab.set_fontweight('bold')
    else:
        ax.set_yticks(range(len(v1solves.columns)), [])
    ax.imshow(v1solves.transpose().values.tolist(), aspect='auto')

fig, axs = plt.subplots(1, 4, figsize=(13, 16))
plot(1, 1, axs[0], yticks=True, xticks=True)
plot(1, 2, axs[1], xticks=True)
plot(2, 1, axs[2], xticks=True)
plot(2, 2, axs[3], xticks=True)
fig.legend(
    [
        Line2D([0], [0], color=COLOR_FAIL, lw=4),
        Line2D([0], [0], color=COLOR_SUCCESS, lw=4),
    ],
    ['Failed', 'Success'],
    loc='upper left', bbox_to_anchor=(1, 1)
)
fig.tight_layout()
fig.savefig(path.join(path.dirname(__file__), f'../data/solvechart.png'), bbox_inches='tight')
