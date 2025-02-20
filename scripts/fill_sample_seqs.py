from os import path
import pandas as pd

res = pd.read_csv(path.join(path.dirname(__file__), '../data/results.tsv'), sep='\t')
res = res[res['Success'] == 1]
puz = pd.read_csv(path.join(path.dirname(__file__), '../data/eterna100_puzzles.tsv'), sep='\t')

merged = puz.merge(res[res['Folder'] == 'vienna1'][['Sequence', 'Target Structure']], how='left', left_on='Secondary Structure V1', right_on='Target Structure')
merged = merged.groupby(['Puzzle Name']).first().sort_values(['Puzzle #']).reset_index()
puz['Sample Sequence (V1/Vienna1)'] = merged['Sequence']

merged = puz.merge(res[res['Folder'] == 'vienna2'][['Sequence', 'Target Structure']], how='left', left_on='Secondary Structure V1', right_on='Target Structure')
merged = merged.groupby(['Puzzle Name']).first().sort_values(['Puzzle #']).reset_index()
puz['Sample Sequence (V1/Vienna2)'] = merged['Sequence']

merged = puz.merge(res[res['Folder'] == 'vienna1'][['Sequence', 'Target Structure']], how='left', left_on='Secondary Structure V2', right_on='Target Structure')
merged = merged.groupby(['Puzzle Name']).first().sort_values(['Puzzle #']).reset_index()
puz['Sample Sequence (V2/Vienna1)'] = merged['Sequence']

merged = puz.merge(res[res['Folder'] == 'vienna2'][['Sequence', 'Target Structure']], how='left', left_on='Secondary Structure V2', right_on='Target Structure')
merged = merged.groupby(['Puzzle Name']).first().sort_values(['Puzzle #']).reset_index()
puz['Sample Sequence (V2/Vienna2)'] = merged['Sequence']

puz.to_csv(path.join(path.dirname(__file__), '../data/eterna100_puzzles.tsv'), sep='\t', index=False)
