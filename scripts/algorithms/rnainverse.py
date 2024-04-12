import os
import re
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired
from util.fold import VIENNA_VERSIONS

external_path = os.path.join(os.path.dirname(__file__), '../../external')

def solve(structure: str, version: VIENNA_VERSIONS, timeout: int):
    p = Popen([f'{external_path}/ViennaRNA-{version}/build/bin/RNAinverse', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
    try:
        res = p.communicate(input=structure, timeout=timeout)[0]
        clean_res = res.replace('\n', '\\n')
        print(f'RNAinverse(v={version}, s={structure}): {clean_res}')

        formatted = re.split('\s+| \(?\s?', res)
        return {'Sequence': formatted[0]}
    except TimeoutExpired:
        print(f'RNAinverse(v={version}, s={structure}): <timeout>')
        return {'Sequence': '<timeout>'}
