import os

for i in range(20, 30):
    os.system('python run.py --mode train --input_data ../data/train/eterna_complete_ss.pkl --results_path model%i --n_long_range_features 20' % i)
    # Test test
    os.system('python run.py --mode test --input_data ../data/test/eterna100.pkl --test_model test/model%i --results_path model_tested%i.pkl' % (i, i))
    # Refine test
    os.system('python run.py --mode refine --input_data test_results/model_tested%i.pkl --results_path model_refined%i.pkl' % (i, i))

