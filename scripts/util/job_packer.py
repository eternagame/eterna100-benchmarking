from dataclasses import dataclass
from itertools import groupby

@dataclass
class Task:
    command: str
    memory: str
    timeout: int

@dataclass
class Job:
    commands: list[str]
    time_allocation: int = 0

@dataclass
class Batch:
    jobs: list[Job]
    memory: str
    timeout: int

    def to_sh(self):
        script = 'case "$SLURM_ARRAY_TASK_ID" in\n'
        for (idx, job) in enumerate(self.jobs, 1):
            script += f'\t{idx})\n'
            for cmd in job.commands:
                script += f'\t\t{cmd}\n'
            script += '\t\t;;\n'
        script += 'esac'
        return script

    
    def slurm_array_indexes(self):
        return f'1-{len(self.jobs)}'

class JobPacker:
    tasks: list[Task] = []

    def add(self, task: Task):
        self.tasks.append(task)

    def pack(self, max_timeout=60*60*24):
        batches: list[Batch] = []

        task_classes = groupby(sorted(self.tasks, key=lambda task: task.memory), lambda task: task.memory)
        for (class_mem, tasks) in task_classes:
            batch = Batch([], class_mem, max_timeout)
            batches.append(batch)

            sorted_tasks = sorted(tasks, key=lambda job: job.timeout, reverse=True)
            for task in sorted_tasks:
                job = next((job for job in batch.jobs if job.time_allocation + task.timeout <= max_timeout), None)
                if not job:
                    job = Job([])
                    batch.jobs.append(job)
                job.commands.append(task.command)
                job.time_allocation += task.timeout
        
        return batches
