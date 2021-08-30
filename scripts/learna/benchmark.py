import subprocess
import os
from tqdm import tqdm

def run(start, end): # [start, end]
    for i in tqdm(range(start, end + 1)):
        subprocess.check_output(['make', 'run-meta-learna-adapt-eterna100-%i' % i])

def get_results():
    list100 = [0] * 100
    solved = 0
    for i in range(1, 101):
        filename = os.getcwd() + '/results/newmodel/eterna/Meta-LEARNA-Adapt/run-0/%i.out' % i
        if not os.path.isfile(filename):
            # print(i)
            continue
        f = open(filename, 'r')
        lastline = f.readlines()[-1]
        f.close()
        lastline = lastline.split(' ')
        if float(lastline[1]) == 1.0:
            list100[i-1] = 1
            solved += 1
    
    return (solved, list100)


if __name__ == '__main__':
    run(1, 50)
    #x = get_results()
    #for i in x[1]:
    #    print(i)
    #print(x[0])
