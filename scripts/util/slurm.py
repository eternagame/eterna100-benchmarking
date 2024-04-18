import os
import re
from typing import Union
from subprocess import run

root_path = os.path.join(os.path.dirname(__file__), '../../')

def sbatch(
    commands: Union[str, list[str]],
    job_name,
    timeout: str = None,
    partition: str = None,
    cpus: int = None,
    gpus: int = None,
    memory: str = None,
    memory_per_cpu: str = None,
    ntasks: int = None,
    dependency: str = None,
    mail_type: str = None,
    constraint: str = None,
):
    args = ['sbatch']

    if job_name is not None:
        args.append(f'--job-name={job_name}')
        args.append(f'--output=data/slurm/%j-{job_name}.txt')
    
    if timeout is not None:
        args.append(f'--time={timeout}')

    if partition is not None:
        args.append(f'--partition={partition}')

    if cpus is not None:
        args.append(f'--cpus-per-task={cpus}')
    
    if gpus is not None:
        args.append(f'--gpus={gpus}')

    if memory is not None:
        args.append(f'--mem={memory}')
    
    if memory_per_cpu is not None:
        args.append(f'--mem-per-cpu={memory_per_cpu}')

    if ntasks is not None:
        args.append(f'--ntasks={ntasks}')

    if dependency is not None:
        args.append(f'--dependency={dependency}')
    
    if mail_type is not None:
        args.append(f'--mail-type={mail_type}')
    
    if constraint is not None:
        args.append(f'--constraint={constraint}')

    input = ('#!/bin/sh\n\n' + (commands if isinstance(commands, str) else '\n'.join(commands)))

    if os.environ.get('SLURM_DRY_RUN') == 'true':
        print(f'SBATCH STDIN:\n{input}\n-------')
        print(f'SBATCH COMMAND: {args}\n--------------')
        return 0
    else:
        res = run(args, input=input, text=True, cwd=root_path, capture_output=True)
        # Return job ID of queued job
        match = re.search(r'Submitted batch job (\d+)', res.stdout)
        if match is None:
            raise Exception(f'sbatch did not return job id.\nstdout\n{res.stdout}\nstderr\n{res.stderr}')
        return match.group(1)
