import os
import re
from typing import Literal
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired
import tempfile

external_path = os.path.join(os.path.dirname(__file__), '../../external')


def solve(structure: str, vienna_version: Literal['1', '2'], timeout: int):
    try:
        params = [
            os.path.join(external_path, 'desirna-env/bin/python'),
            os.path.join(external_path, 'DesiRNA/DesiRNA.py'),
            '--results_number=1', '--stop_when_solved=on', '--without_timer=on', f'--timelimit={timeout}', '--replicas=1'
        ]
        if vienna_version == '1':
            params.append('--dangles=1')
        else:
            params.append('--param=2004')
        
        params.append('-f')

        with tempfile.TemporaryDirectory() as tempdir:
            with open(f'{tempdir}/in.txt', 'w') as f:
                f.write(f'>name\nf1\n>seq_restr\n{"N" * len(structure)}\n>sec_struct\n{structure}\n')
            params.append(f'{tempdir}/in.txt')

            p = Popen(params, stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=tempdir)
            res = p.communicate(timeout=timeout)[0].strip()
        
        clean_res = res.replace('\n', '\\n')
        print(f'desirna(v={vienna_version}, s={structure}): {clean_res}')
            
        match = re.search(r'(?:(?:Design not solved!)|(?:Design solved succesfully!))\n\n(?:(?:Target structure:)|(?:Best solution:))\n([AUGC]+)\nMFE Secondary Structure: \n([\(\).]+)\n', res)
        return {
            'Sequence': match.group(1),
            'Returned Structure': match.group(2),
        }
    except TimeoutExpired:
        print(
            f'desirna(v={vienna_version}, s={structure}): <timeout>')
        return {
            'Sequence': '<timeout>',
            'Returned Structure': '<timeout>',
        }
