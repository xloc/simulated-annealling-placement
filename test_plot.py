import pathlib
import contextlib
import parser
import a2
import random
import math
import matplotlib.pyplot as plt
import shutil


def clear_or_create_folder(path):
    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def main():
    save_path = 'saves/alu2'
    clear_or_create_folder(save_path)

    random.seed(12)
    chip_info = parser.parse_file('benchmarks/alu2.txt')
    chip = a2.Chip(chip_info)

    steps = a2.annealing_placement(
        chip,
        t_init=100,
        t_decrease_factor=0.5,
        t_terminate=0.1)

    for chip, info in steps:
        print(' '.join([
            f"Cost={chip.cost():6d}",
            f"temp={info['t']:7.2f}",
            f"delta={info['acc_delta']:6d}"
        ]))
        i_iter = info['i_iter']
        chip.plot()
        plt.savefig(f'{save_path}/{i_iter}.png')


if __name__ == "__main__":
    main()
