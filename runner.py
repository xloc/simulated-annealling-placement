import a2
import parser
import random

random.seed(12)
chip_info = parser.parse_file('benchmarks/alu2.txt')
chip = a2.Chip(chip_info)

# chip.grid.format_print(10, a2.nets_formatter)

a2.annealing_placement(chip)
