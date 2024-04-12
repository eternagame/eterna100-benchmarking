import os
from typing import Literal
from subprocess import Popen, PIPE, STDOUT
import re

VIENNA_VERSIONS = Literal['1.8.5', '2.1.9', '2.6.4']

external_path = os.path.join(os.path.dirname(__file__), '../../external')

def fold(seq, version: VIENNA_VERSIONS):
    p = Popen([f'{external_path}/ViennaRNA-{version}/build/bin/RNAfold', '-T','37.0'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
    pair = p.communicate(seq)[0]
    formatted = re.split('\s+| \(?\s?',pair)
    return formatted[1]
