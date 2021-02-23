import random
import math
import contextlib
import shutil
import pathlib

import parser
import a2
from a2 import Chip, annealing_placement


def clear_or_create_folder(path):
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


random.seed(12)
chip_info = parser.parse_file('benchmarks/alu2.txt')
chip = a2.Chip(chip_info)


steps = annealing_placement(
    chip,
    t_init=5,
    t_decrease_factor=0.5,
    t_terminate=1)

for chip, info in steps:
    print(' '.join([
        f"Cost={chip.cost():6d}",
        f"temp={info['t']:7.2f}",
        f"delta={info['acc_delta']:6d}"
    ]))
