import os
import re
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired, run
from util.fold import VIENNA_VERSIONS

external_path = os.path.join(os.path.dirname(__file__), '../../external')

def solve(structure: str, cnn_version: VIENNA_VERSIONS, sap_version: VIENNA_VERSIONS, model_name: str, timeout: int):
    env = os.environ.copy()
    env['VIENNA_BIN_PATH'] = f'{external_path}/ViennaRNA-{cnn_version}/build/bin'
    env['SAP_VIENNA_BIN_PATH'] = f'{external_path}/ViennaRNA-{sap_version}/build/bin'
    env['MODEL_NAME'] = model_name
    p = Popen([
        f'{external_path}/eternabrain-env/bin/python',
        'predict_pm.py',
        structure
    ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=f'{external_path}/eternabrain/rna-prediction', env=env)

    try:
        res = p.communicate(timeout=timeout)[0]

        ignore_lines = [
            r'.+The name tf\.train\.import_meta_graph is deprecated.+\n\n',
            r'.+The name tf.Session is deprecated.+\n\n',
            r'.+Could not load dynamic library ((\'\w+\.so\.10\.0\')|(\'libcudnn\.so\.7\')).+\n',
            r'.+/gpu_device\.cc:1165\]\s*\n',
            r'.+Device interconnect StreamExecutor with strength 1 edge matrix.+\n',
            r'.+service\.cc:168\] XLA service 0x[a-f0-9]+ initialized.+\n',
            r'.+cuda_gpu_executor\.cc:983\] successful NUMA node read.+\n',
            r'.+service.cc:176]   StreamExecutor device.+\n',
            r'.+cpu_utils\.cc:94\] CPU Frequency.+\n',
            r'.+Your CPU supports instructions that this TensorFlow binary was not compiled to use.+\n',
            r'.+dso_loader\.cc:44\] Successfully opened dynamic library.+\n',
        ]
        trimmed_res = re.sub('|'.join([fr'({line})' for line in ignore_lines]), '', res)
        clean_res = trimmed_res
        #clean_res = trimmed_res.replace('\n', '\\n')

        print(f'eternabrain-sap(cv={cnn_version}, sv={sap_version}, m={model_name}, s={structure}): {clean_res}')

        match = re.search('([^\n]+)\n?$', res)
        return {'Sequence': match.group(1)}
    except TimeoutExpired:
        print(f'eternabrain-sap(cv={cnn_version}, sv={sap_version}, m={model_name}, s={structure}): <timeout>')
        return {'Sequence': '<timeout>'}

def featuregen(version: VIENNA_VERSIONS):
    env = os.environ.copy()
    env['VIENNA_BIN_PATH'] = f'{external_path}/ViennaRNA-{version}/build/bin'
    if version.startswith('1'):
        env['FEATURESET_NAME'] = f'Vienna1'
    else:
        env['FEATURESET_NAME'] = f'Vienna2'

    run(
        [f'{external_path}/eternabrain-env/bin/python', 'experts.py'],
        cwd=f'{external_path}/eternabrain/rna-prediction',
        env=env
    ).check_returncode()

def train(feature_version: int, extended: bool, model: str):
    env = os.environ.copy()
    env['FEATURESET_NAME'] = f'Vienna{feature_version}'
    env['TRAIN_EXTENDED_PUZZLES'] = 'true' if extended else 'false'
    env['MODEL_NAME'] = f'eterna100-benchmarking-F{feature_version}-{"EXT" if extended else "BASE"}'

    run(
        [f'{external_path}/eternabrain-env/bin/python', f'{model}.py'],
        cwd=f'{external_path}/eternabrain/rna-prediction',
        env=env
    ).check_returncode()
