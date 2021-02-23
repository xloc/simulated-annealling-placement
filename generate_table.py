import pathlib
import shutil
import os.path
import contextlib
import json


def print_results(path):
    def sorted_path():
        a = list(pathlib.Path(path).glob("*/*.json"))
        a = {str(path).split('/')[-2]: path for path in a}
        order = ['cm138a', 'cm151a', 'cm162a', 'cm150a', 'alu2',
                 'C880', 'e64', 'apex1', 'pairb', 'paira', 'cps', 'apex4', ]
        for name in order:
            if name in a:
                yield a[name]

    names, costs = [], []
    for path in sorted_path():
        path = str(path)
        name = path.split('/')[-2]
        with open(path) as f:
            data = json.load(f)

        last_cost = data['costs'][-1] * 2
        names.append(name)
        costs.append(last_cost)

    width = 6
    print(' '.join([f"{v:>{width}s}" for v in names]))
    print(' '.join([f"{v:{width}d}" for v in costs]))


print_results('saves')
