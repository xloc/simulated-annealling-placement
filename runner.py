import pathlib
import shutil
import os.path
import contextlib
import json

import a2
import parser
import random
import matplotlib.pyplot as plt
import time


random.seed(12)

save_path = 'saves_no_cython'


def clear_or_create_folder(dir):
    path = os.path.join(save_path, dir)
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return path


def run_benchmark(benchmark_name):
    path = clear_or_create_folder(benchmark_name)

    chip_info = parser.parse_file(f'benchmarks/{benchmark_name}.txt')
    chip = a2.Chip(chip_info)
    rec = dict(costs=[], temps=[])

    steps = a2.annealing_placement(
        chip,
        t_init=100,
        t_decrease_factor=0.5,
        t_terminate=0.01)

    print(f"{'='*10}\n{benchmark_name}")
    for chip, info in steps:
        cost = chip.cost()
        t = info['t']
        delta = info['acc_delta']
        i_iter = info['i_iter']

        print(' '.join([
            f"Cost={cost:6d}",
            f"temp={t:7.2f}",
            f"delta={delta:6d}"
        ]))

        fig = plt.figure(frameon=False, dpi=200)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor("white")
        chip.plot(ax)
        ax.axis('off')
        fig.savefig(f'{path}/{i_iter}.png')
        plt.close()

        rec['costs'].append(cost)
        rec['temps'].append(t)

    with open(f'{path}/record.json', 'w') as f:
        json.dump(rec, f)


benchmarks = [
    'cm138a',
    'cm151a',
    'cm162a',
    'cm150a',
    'alu2',
    'C880',
    'e64',
    'apex1',
    'pairb',
    'paira',
    'cps',
    'apex4',
]
for name in benchmarks:
    st = time.time()
    run_benchmark(name)
    ed = time.time()
    print(f'time = {ed-st:.2f}')
