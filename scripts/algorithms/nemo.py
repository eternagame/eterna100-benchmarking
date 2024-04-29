import os
import re
from typing import Literal
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired

nemo_dir = os.path.join(os.path.dirname(__file__), '../../external/nemo')

def solve(structure: str, vienna_version: Literal['1', '2'], iterations: int, timeout: int):
    params = [os.path.join(nemo_dir, 'nemo'), '-i', str(iterations)]
    if vienna_version == '1':
        params.append('-E')
    params.append(structure)
    p = Popen(params, stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8', cwd=nemo_dir)

    try:
        res = p.communicate(timeout=timeout)[0]
        clean_res = res.replace('\n', '\\n')
        print(f'nemo(v={vienna_version}, i={iterations}, s={structure}): {clean_res}')
        
        match = re.search(r'NMC: ([AUGC]+).*\nSTR: ([\(\).]+)', res)
        return {
            'Sequence': match.group(1),
            'Returned Structure': match.group(2),
        }
    except TimeoutExpired:
        print(f'nemo(v={vienna_version}, i={iterations}, s={structure}): <timeout>')
        return {
            'Sequence': '<timeout>',
            'Returned Structure': '',
        }
