import parser
import a2
from a2 import Chip, annealing_placement
import random
import math


random.seed(12)
chip_info = parser.parse_file('benchmarks/alu2.txt')
chip = a2.Chip(chip_info)


steps = annealing_placement(
    chip,
    t_init=100,
    t_decrease_factor=0.5,
    t_terminate=1)

for chip, info in steps:
    print(' '.join([
        f"Cost={chip.cost():6d}",
        f"temp={info['t']:.2f}",
        f"delta={info['acc_delta']}"
    ]))
