import RNA
import pandas as pd
import os

if __name__ == '__main__':
    puzzle_file = pd.read_csv(os.getcwd() + '/eterna100.txt', sep=' ', delimiter='\t', header='infer')
