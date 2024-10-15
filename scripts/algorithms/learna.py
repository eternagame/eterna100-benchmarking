import os
import re
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired, run
from util.fold import VIENNA_VERSIONS
import tempfile

external_path = os.path.join(os.path.dirname(__file__), '../../external')

def solve(structure: str, version: VIENNA_VERSIONS, model_path: str, timeout: int):
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as fp:
            fp.write(structure)
            fp.close()

            p = Popen([
                f'{external_path}/learna-env/bin/python', '-m', 'src.learna.design_rna',
                '--mutation_threshold', '5',
                '--batch_size', '123',
                '--conv_sizes', '11', '3',
                '--conv_channels', '10', '3',
                '--embedding_size', '2',
                '--entropy_regularization', '0.00015087352506343337',
                '--fc_units', '52',
                '--learning_rate', '6.442010833400271e-05',
                '--lstm_units', '3',
                '--num_fc_layers', '1',
                '--num_lstm_layers', '0',
                '--reward_exponent', '8.932893783628236',
                '--state_radius', '29',
                '--target_structure_path', fp.name,
                '--restore_path', f'models/{model_path}',
                '--restart_timeout', '1800',
                '--vienna_version', version,
            ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=f'{external_path}/learna')
            res = p.communicate(input=structure, timeout=timeout)[0].strip()
        
        clean_res = re.sub(r'.+(Your CPU supports instructions|FutureWarning: Passing \(type, 1\)[^\n]+\n\s+ (_np_q|np_resource)|RuntimeWarning: compiletime version.+of module.+fast_tensor_util[^\n]+\n\s+return f)[^\n]+(\n|$)', '', res)
        trimmed_res = clean_res
        if len(trimmed_res) > 2500:
            trimmed_res = f'{trimmed_res[:1250]}...{trimmed_res[-1250:]}'
        print_res = trimmed_res.replace('\n', '\\n')

        print(f'Meta-Learna-Adapt(v={version}, s={structure}, m={model_path}): {print_res}')

        (elapsed_time, last_reward, last_fractional_hamming, candidate_solution) = clean_res.split('\n')[-1].split(' ')
        return {
            'Sequence': candidate_solution,
            'Last Reward': last_reward,
            'Last Fractional Hamming': last_fractional_hamming,
        }
    except TimeoutExpired:
        print(f'Meta-Learna-Adapt(v={version}, s={structure}, m={model_path}): <timeout>')
        return {
            'Sequence': '<timeout>',
            'Last Reward': '<timeout>',
            'Last Fractional Hamming': '<timeout>',
        }

def train(timeout: int, vienna_version: VIENNA_VERSIONS):
    run([
        f'{external_path}/learna-env/bin/python', '-m', 'src.learna.learn_to_design_rna',
        '--data_dir', 'data/',
        '--dataset', 'rfam_learn_train',
        '--vienna_version', vienna_version,
        '--save_path', f'models/eterna100-benchmarking/vienna-{vienna_version}',
        '--timeout', str(timeout),
        '--learning_rate', '6.442010833400271e-05',
        '--mutation_threshold', '5',
        '--reward_exponent', '8.932893783628236',
        '--state_radius', '29',
        '--conv_sizes', '11', '3',
        '--conv_channels', '10', '3',
        '--num_fc_layers', '1',
        '--fc_units', '52',
        '--batch_size', '123',
        '--entropy_regularization', '0.00015087352506343337',
        '--embedding_size', '2',
        '--lstm_units', '3',
        '--num_lstm_layers', '0'
    ], cwd=f'{external_path}/learna').check_returncode()
