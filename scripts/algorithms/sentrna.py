import os
import re
import pickle
from subprocess import PIPE, Popen, STDOUT, run
from util.fold import VIENNA_VERSIONS
import tempfile

external_path = os.path.join(os.path.dirname(__file__), '../../external')

def solve(structure: str, version: VIENNA_VERSIONS, ensemble_path: str, renderer: str):
    env = os.environ.copy()
    env['PATH'] += f':{external_path}/ViennaRNA-{version}/build/bin'
    if version == '1.8.5':
        env['PATH'] += f':{external_path}/SentRNA/SentRNA/util/ViennaRNA-1.8.5/Progs/rnaplot'

    with tempfile.TemporaryDirectory() as tempdir:
        with open(f'{tempdir}/in.txt', 'w') as f:
            f.write(f'inference    {structure}')
        
        full_ensemble_path = f'{external_path}/SentRNA/models/{ensemble_path}/test'
        models = os.listdir(full_ensemble_path)
        results = []
        for model in models:
            p = Popen([
                f'{external_path}/sentrna-env/bin/python', f'{external_path}/SentRNA/SentRNA/run.py',
                '--mode', 'test',
                '--input_data', f'{tempdir}/in.txt',
                '--test_model', f'{full_ensemble_path}/{model}',
                '--results_path', 'nn.pkl',
                '--renderer', renderer
            ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=tempdir, env=env)
            res = p.communicate(input=structure)[0].strip()

            ignore_lines = [
                r'OMP: Info.+\n',
                r'WARNING:.+The name.+is deprecated.+\n\n',
                r'WARNING:.+softmax_cross_entropy_with_logits[^\n]+is deprecated(.|\n)+softmax_cross_entropy_with_logits_v2`\.\n\n',
                r'mkdir: cannot create directory ‘test_results’: File exists\n',
                r'rm: cannot remove \'input\': No such file or directory\n',
                r'.+This TensorFlow binary is optimized.+\nTo enable them.+\n',
                r'.+I tensorflow.+(CPU Frequency|XLA service|StreamExecutor device|Creating new thread pool).+\n',
                r'.+RuntimeWarning: invalid value encountered in divide\n\s+v2 = \(p3 - p2\) / np.linalg.norm\(p3 - p2\)\n'
            ]
            trimmed_res = re.sub('|'.join([fr'({line})' for line in ignore_lines]), '', res)
            clean_res = trimmed_res.replace('\n', '\\n')
            with open(f'{tempdir}/test_results/nn.pkl', 'rb') as f:
                nn_output = pickle.load(f)
            print(f'SentRNA(v={version}, s={structure}, e={ensemble_path}, m={model}, stage=NN): {clean_res} | {str(nn_output)}')

            (nn_name, nn_struct, nn_seq, nn_accuracy) = nn_output[0]

            p = Popen([
                f'{external_path}/sentrna-env/bin/python', f'{external_path}/SentRNA/SentRNA/run.py',
                '--mode', 'refine',
                '--input_data', f'{tempdir}/test_results/nn.pkl',
                '--results_path', 'refine.pkl'
            ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=tempdir, env=env)
            res = p.communicate(input=structure)[0]

            ignore_lines = [
                r'OMP: Info.+\n',
                r'rm: cannot remove \'input\': No such file or directory\n',
                r'rm: cannot remove \'rna.ps\': No such file or directory\n',
                r'mkdir: cannot create directory ‘refined’: File exists\n'
            ]
            trimmed_res = re.sub('|'.join([fr'({line})' for line in ignore_lines]), '', res)
            if len(res) > 2500:
                trimmed_res = f'{trimmed_res[:1250]}...{trimmed_res[:-1250]}'
            clean_res = trimmed_res.replace('\n', '\\n')
            with open(f'{tempdir}/refined/refine.pkl', 'rb') as f:
                refine_output = pickle.load(f)
            print(f'SentRNA(v={version}, s={structure}, e={ensemble_path}, m={model}, stage=REFINE): {clean_res} | {str(refine_output)}')

            (refine_name, refine_struct, refine_seq, refine_accuracy) = refine_output[0]
            results.append({
                'nn_seq': nn_seq,
                'nn_accuracy': nn_accuracy,
                'refine_seq': refine_seq,
                'refine_accuracy': refine_accuracy,
            })
        
    sorted_results = sorted(results, key=lambda result: float(result['refine_accuracy']))
    return {
        'Sequence': sorted_results[0]['refine_seq'],
        'Accuracy': str(sorted_results[0]['refine_accuracy']),
        'NN Accuracies': '|'.join([str(result['nn_accuracy']) for result in results]),
        'Refine Accuracies': '|'.join([str(result['refine_accuracy']) for result in results]),
        'NN Success Count': str(sum([1 if result['nn_accuracy'] == 1.0 else 0 for result in results])),
        'Refine Success Count': str(sum([1 if result['refine_accuracy'] == 1.0 else 0 for result in results])),
    }

def train(version: VIENNA_VERSIONS, features: int, renderer: str, trial: int):
    env = os.environ.copy()
    env['PATH'] += f':{external_path}/ViennaRNA-{version}/build/bin'
    if version == '1.8.5':
        env['PATH'] += f':{external_path}/SentRNA/SentRNA/util/ViennaRNA-1.8.5/Progs/rnaplot'

    run([
        f'{external_path}/sentrna-env/bin/python', f'{external_path}/SentRNA/SentRNA/run.py',
        '--mode', 'train',
        '--input_data', f'{external_path}/SentRNA/data/train/eterna_complete_ss.pkl',
        '--results_path', f'trial-{trial}_MI-{features}',
        '--n_long_range_features', str(features),
        # We could actually benefit from caching this, calculating it only once per version/renderer
        # combo and passing --long_range_input on future runs, but generating it independently
        # for each model we train simplifies things for now
        # (If we wanted to do this properly, we'd probably need to patch learna to let us run that
        # as an isolated command).
        '--long_range_output', f'long_range_features_{trial}_MI-{features}.pkl',
        '--renderer', renderer
    ], cwd=f'{external_path}/SentRNA/models/eterna100-benchmarking/vienna-{version}-{renderer}', env=env)
