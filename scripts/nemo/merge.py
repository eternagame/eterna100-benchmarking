'''
For batch runs where each run outputted to a separate tsv file, merge them together
'''

import glob
import pandas as pd

df = pd.DataFrame()
for file in glob.glob('nemo_results/*.tsv'):
  df = pd.concat([df, pd.read_csv(file, sep='\t', header='infer')])

df = df.reset_index(drop=True)

df.to_csv('nemo_all.tsv', index=False)

src_df = pd.read_csv('../../eterna100v1_vienna1.tsv')

for vver in range(1, 3):
  for ever in range(1, 3):
    subdf = df[
      (df['Vienna Version'] == vver) & (df['Eterna100 Version'] == ever)
    ].drop(
      columns=['Vienna Version', 'Eterna100 Version']
    ).copy(deep=True)
    subdf = subdf.set_index('Puzzle Name')
    subdf = subdf.reindex(index=src_df['Puzzle Name'])
    subdf.to_csv(f'nemo_v{ever}_vienna{vver}.tsv', sep='\t', index=False)
