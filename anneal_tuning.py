import json
import matplotlib.pyplot as plt
import a2
import parser
import random


def ty(init, dec, key):
    random.seed(12)
    chip_info = parser.parse_file('benchmarks/alu2.txt')
    chip = a2.Chip(chip_info, a2.import_Net())

    steps = a2.annealing_placement(
        chip,
        t_init=init,
        t_decrease_factor=dec,
        t_terminate=0.01)

    costs = []
    temps = []
    for chip, info in (steps):
        cost = chip.cost()
        temp = info['t']
        print(' '.join([
            f"Cost={cost:6d}",
            f"temp={temp:7.2f}",
            f"delta={info['acc_delta']:6d}"
        ]))
        costs.append(cost)
        temps.append(temp)

    css[key] = dict(costs=costs, temps=temps)


ty(5, 0.9, 'i5c9')
ty(5, 0.5, 'i5c5')
ty(1, 0.9, 'i1c9')
ty(1, 0.5, 'i1c5')


def p(key):
    plt.loglog(
        css[key]['temps'][1:],
        css[key]['costs'][1:],
        label=key)


p('c=0.9')
# p('i100c9')
# p('i10c9')
p('i5c9')
p('i1c9')

# p('c=0.5')
# p('i100c5')
# p('i10c5')
# p('i5c5')
# p('i1c5')

plt.legend()
# plt.xlabel('Log of Annealing Temperature')
# plt.ylabel('Log of Half-perimeter cost')
plt.show()

with open('paras_tune.json', 'w') as f:
    json.dump(css, f, indent=2)
